"""This file applies deterministic business rules after ML prediction, including weight checks, fragility support scoring, deduplication, and final ranking so recommendations are practical and unique."""

from typing import Dict, List


FRAGILITY_STRENGTH_MAP = {
    "low": ["Low", "Medium", "High"],
    "medium": ["Medium", "High"],
    "high": ["High"],
}


def get_fragility_support(strength: str) -> str:
    normalized = (strength or "").strip().capitalize()
    if normalized == "High":
        return "High"
    if normalized == "Medium":
        return "Medium"
    return "Low"


def get_cost_level(cost_inr: float) -> str:
    if cost_inr < 10:
        return "Budget"
    if cost_inr < 50:
        return "Mid-range"
    return "Premium"


def filter_by_weight(materials: List[Dict], product_weight_grams: float) -> List[Dict]:
    product_weight_kg = product_weight_grams / 1000.0
    filtered = [m for m in materials if float(m.get("weight_capacity_kg", 0) or 0) >= product_weight_kg]

    if filtered:
        return filtered

    return sorted(materials, key=lambda x: float(x.get("weight_capacity_kg", 0) or 0), reverse=True)


def filter_by_fragility(materials: List[Dict], fragility: str) -> List[Dict]:
    fragility_key = (fragility or "low").lower()
    required_strengths = FRAGILITY_STRENGTH_MAP.get(fragility_key, FRAGILITY_STRENGTH_MAP["low"])

    filtered = [m for m in materials if (m.get("strength") or "").strip().capitalize() in required_strengths]
    return filtered if filtered else materials


def compute_rule_score(material: Dict, product_weight_grams: float, fragility: str) -> float:
    score = 0.0
    product_weight_kg = product_weight_grams / 1000.0
    capacity = float(material.get("weight_capacity_kg", 0) or 0)
    strength = (material.get("strength") or "").strip().capitalize()
    tier = (material.get("sustainability_tier") or "").strip().capitalize()

    if capacity >= product_weight_kg * 2:
        score += 10
    elif capacity >= product_weight_kg:
        score += 5

    fragility_key = (fragility or "low").lower()
    if fragility_key == "high" and strength == "High":
        score += 20
    elif fragility_key == "medium" and strength in ("Medium", "High"):
        score += 15
    elif fragility_key == "low":
        score += 10

    if tier == "Excellent":
        score += 10
    elif tier == "Good":
        score += 5

    recyclability = int(material.get("recyclability_percent", 0) or 0)
    biodegradability = int(material.get("biodegradability_score", 0) or 0)

    if recyclability > 90:
        score += 5
    if biodegradability > 80:
        score += 5

    return score


def apply_rules(materials: List[Dict], product_weight_grams: float, fragility: str) -> List[Dict]:
    weighted = filter_by_weight(materials, product_weight_grams)
    fragility_filtered = filter_by_fragility(weighted, fragility)

    ranked = []
    for material in fragility_filtered:
        rule_score = compute_rule_score(material, product_weight_grams, fragility)
        suitability_score = float(material.get("material_suitability_score", 0) or 0)
        final_score = suitability_score * 0.6 + rule_score * 0.4

        strength = (material.get("strength") or "Low").strip().capitalize()
        cost = float(material.get("predicted_cost", material.get("packaging_cost_inr", 0)) or 0)
        tier = (material.get("predicted_tier", material.get("sustainability_tier", "Average")) or "Average").strip().capitalize()

        enriched = {
            **material,
            "rule_score": round(rule_score, 2),
            "final_score": round(final_score, 2),
            "fragility_support": get_fragility_support(strength),
            "cost_level": get_cost_level(cost),
            "eco_friendly": tier in {"Excellent", "Good"},
            "weight_capacity": f"Up to {float(material.get('weight_capacity_kg', 0) or 0):.1f} kg",
            "strength": strength,
            "sustainability_tier": tier,
        }
        ranked.append(enriched)

    ranked.sort(key=lambda x: x.get("final_score", 0), reverse=True)

    deduped: List[Dict] = []
    seen = set()
    for material in ranked:
        key = str(material.get("packaging_material", "")).strip().lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(material)

    return deduped[:5]
