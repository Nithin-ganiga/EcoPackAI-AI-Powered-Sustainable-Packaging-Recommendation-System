"""This file loads pretrained ML artifacts and performs safe batch inference for candidate materials so each recommendation includes predicted cost, CO2 impact, and sustainability tier signals."""

from pathlib import Path
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd


MODELS_DIR = Path(__file__).resolve().parent / "models"

ML_FEATURES = [
    "Weight_Capacity_kg",
    "Biodegradability_Score",
    "Recyclability_Percent",
    "Strength_Encoded",
    "Industry_LE",
    "Material_Type_LE",
    "Packaging_Material_LE",
    "Packaged_Item_LE",
]


rf_cost = None
xgb_co2 = None
rf_tier = None
le_dict = {}
tier_label_encoder = None
ml_features_from_file = ML_FEATURES
MODELS_LOADED = False


def _safe_load(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return joblib.load(path)
    except Exception:
        return None


def load_models() -> bool:
    global rf_cost, xgb_co2, rf_tier, le_dict, tier_label_encoder, ml_features_from_file, MODELS_LOADED

    rf_cost = _safe_load(MODELS_DIR / "model_cost_rf.pkl")
    xgb_co2 = _safe_load(MODELS_DIR / "model_co2_xgb.pkl")
    rf_tier = _safe_load(MODELS_DIR / "model_tier_clf.pkl")
    le_dict = _safe_load(MODELS_DIR / "label_encoders.pkl") or {}
    tier_label_encoder = _safe_load(MODELS_DIR / "tier_label_encoder.pkl")
    ml_features_from_file = _safe_load(MODELS_DIR / "ml_features.pkl") or ML_FEATURES

    MODELS_LOADED = all([rf_cost is not None, xgb_co2 is not None, rf_tier is not None, tier_label_encoder is not None])
    return MODELS_LOADED


def encode_label(col: str, value: str) -> int:
    encoder = le_dict.get(col)
    if encoder is None:
        return 0

    normalized = str(value or "").strip()
    classes = list(getattr(encoder, "classes_", []))
    if normalized not in classes:
        return 0

    return int(encoder.transform([normalized])[0])


def build_feature_row(material: Dict[str, Any]) -> Dict[str, Any]:
    strength_map = {"Low": 1, "Medium": 2, "High": 3}
    strength = (material.get("strength") or "Low").strip().capitalize()

    return {
        "Weight_Capacity_kg": float(material.get("weight_capacity_kg", 0) or 0),
        "Biodegradability_Score": float(material.get("biodegradability_score", 0) or 0),
        "Recyclability_Percent": float(material.get("recyclability_percent", 0) or 0),
        "Strength_Encoded": strength_map.get(strength, 1),
        "Industry_LE": encode_label("industry", material.get("industry", "")),
        "Material_Type_LE": encode_label("material_type", material.get("material_type", "")),
        "Packaging_Material_LE": encode_label("packaging_material", material.get("packaging_material", "")),
        "Packaged_Item_LE": encode_label("packaged_item", material.get("packaged_item", material.get("packaging_material", ""))),
    }


def predict_for_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not candidates:
        return []

    if not MODELS_LOADED:
        load_models()

    feature_rows = [build_feature_row(c) for c in candidates]
    X = pd.DataFrame(feature_rows, columns=ML_FEATURES)

    X["Weight_Capacity_kg"] = X["Weight_Capacity_kg"].clip(lower=0, upper=500)
    X["Biodegradability_Score"] = X["Biodegradability_Score"].clip(lower=0, upper=100)
    X["Recyclability_Percent"] = X["Recyclability_Percent"].clip(lower=0, upper=100)
    X["Strength_Encoded"] = X["Strength_Encoded"].clip(lower=1, upper=3)

    if MODELS_LOADED:
        try:
            pred_cost = np.clip(rf_cost.predict(X), 0.5, 179)
            pred_co2 = np.clip(xgb_co2.predict(X), 5, 78)
            pred_tier_raw = rf_tier.predict(X)

            if hasattr(tier_label_encoder, "inverse_transform") and np.issubdtype(np.array(pred_tier_raw).dtype, np.number):
                pred_tiers = tier_label_encoder.inverse_transform(pred_tier_raw)
            else:
                pred_tiers = np.array([str(item) for item in pred_tier_raw])
        except Exception as exc:
            print(f"[recommender] prediction fallback due to error: {exc}")
            pred_cost = np.clip(X["Weight_Capacity_kg"].values * 2.8, 0.5, 179)
            pred_co2 = np.clip(80 - (X["Biodegradability_Score"].values * 0.5), 5, 78)
            pred_tiers = np.array(["Good" for _ in range(len(candidates))])
    else:
        pred_cost = np.clip(X["Weight_Capacity_kg"].values * 2.8, 0.5, 179)
        pred_co2 = np.clip(80 - (X["Biodegradability_Score"].values * 0.5), 5, 78)
        pred_tiers = np.array(["Good" for _ in range(len(candidates))])

    enriched = []
    for idx, material in enumerate(candidates):
        updated = dict(material)
        updated["predicted_cost"] = float(round(pred_cost[idx], 2))
        updated["predicted_co2"] = float(round(pred_co2[idx], 2))
        updated["predicted_tier"] = str(pred_tiers[idx])
        enriched.append(updated)

    return enriched
