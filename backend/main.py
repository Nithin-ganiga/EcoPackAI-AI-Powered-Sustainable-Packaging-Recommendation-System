"""This file starts and configures the FastAPI server, exposes health and recommendation endpoints, and coordinates database loading, ML prediction, and rule-based ranking so the API can return clean packaging recommendations to the frontend."""

from typing import List
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from database import (
    create_search_logs_table,
    get_all_unique_materials,
    get_autocomplete_suggestions,
    get_materials_by_product,
    save_search_log,
    test_connection,
)
from dashboard import router as dashboard_router
import recommender
from rule_engine import apply_rules
from schemas import MaterialRecommendation, RecommendRequest, RecommendResponse, ReportRequest
import report_generator


app = FastAPI(title="EcoPackAI API", version="3.0.0")

app.include_router(dashboard_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_why_recommended(material: dict, rank: int, fragility: str) -> str:
    parts: List[str] = []

    if rank == 1:
        parts.append("Best Match:")

    strength = (material.get("strength") or "").capitalize()
    tier = (material.get("sustainability_tier") or "").capitalize()
    recyclability = int(material.get("recyclability_percent", 0) or 0)
    biodegradability = int(material.get("biodegradability_score", 0) or 0)
    cost = float(material.get("predicted_cost", material.get("packaging_cost_inr", 0)) or 0)

    if fragility == "high" and strength == "High":
        parts.append("High strength provides excellent fragility protection for your product.")
    elif fragility == "medium" and strength in {"Medium", "High"}:
        parts.append("Strength profile is well suited for moderate fragility handling.")
    else:
        parts.append("Material handling profile matches your product requirements.")

    if tier == "Excellent":
        parts.append("Highest sustainability rating.")
    elif tier == "Good":
        parts.append("Good eco-friendly sustainability rating.")

    if cost < 10:
        parts.append("Budget friendly option.")

    if recyclability > 90:
        parts.append(f"Highly recyclable at {recyclability} percent.")

    if biodegradability > 80:
        parts.append("Strong biodegradability profile.")

    return " ".join(parts).strip()


def infer_fragility_from_weight(product_weight_grams: float) -> str:
    if product_weight_grams > 0:
        return "low"
    return "low"


@app.on_event("startup")
def startup_event() -> None:
    models_ok = recommender.load_models()
    db_ok = test_connection()
    _ = create_search_logs_table()

    print(f"[startup] models_loaded={models_ok}")
    print(f"[startup] db_connected={db_ok}")


@app.get("/")
def root() -> dict:
    return {
        "message": "Welcome to EcoPackAI Packaging Material Recommendation API",
        "status": "ok",
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "db_connected": test_connection(),
        "models_loaded": recommender.MODELS_LOADED,
    }


@app.post("/api/recommend", response_model=RecommendResponse)
def recommend(payload: RecommendRequest) -> RecommendResponse:
    product_name = payload.product_name.strip()
    product_weight_grams = payload.product_weight_grams
    fragility = infer_fragility_from_weight(product_weight_grams)

    if not product_name:
        raise HTTPException(status_code=400, detail="product_name must not be empty")
    if product_weight_grams <= 0:
        raise HTTPException(status_code=400, detail="product_weight_grams must be greater than 0")

    candidates = get_materials_by_product(product_name)
    if not candidates:
        candidates = get_all_unique_materials()

    if not candidates:
        raise HTTPException(status_code=404, detail="No packaging materials found in database")

    enriched = recommender.predict_for_candidates(candidates)
    top_materials = apply_rules(enriched, product_weight_grams, fragility)

    recommendations: List[MaterialRecommendation] = []
    for index, material in enumerate(top_materials, start=1):
        why = build_why_recommended(material, index, fragility)
        recommendation = MaterialRecommendation(
            rank=index,
            material_name=str(material.get("packaging_material", "Unknown")),
            material_type=str(material.get("material_type", "Unknown")),
            industry=str(material.get("industry", "General")),
            strength=str(material.get("strength", "Low")),
            weight_capacity=str(material.get("weight_capacity", "Up to 0.0 kg")),
            cost_inr=float(material.get("predicted_cost", material.get("packaging_cost_inr", 0)) or 0),
            cost_level=str(material.get("cost_level", "Mid-range")),
            eco_friendly=bool(material.get("eco_friendly", False)),
            sustainability_tier=str(material.get("sustainability_tier", "Average")),
            biodegradability_score=int(material.get("biodegradability_score", 0) or 0),
            recyclability_percent=int(material.get("recyclability_percent", 0) or 0),
            co2_emission_score=int(round(float(material.get("predicted_co2", material.get("co2_emission_score", 0)) or 0))),
            fragility_support=str(material.get("fragility_support", "Low")),
            suitability_score=float(round(float(material.get("material_suitability_score", 0) or 0), 2)),
            rank_score=float(round(float(material.get("final_score", 0) or 0), 2)),
            why_recommended=why,
        )
        recommendations.append(recommendation)

    if recommendations:
        save_search_log(
            product_name=product_name,
            weight_grams=product_weight_grams,
            fragility=fragility,
            top_result=recommendations[0].material_name,
        )

    return RecommendResponse(
        status="success",
        product_name=product_name,
        product_weight_grams=product_weight_grams,
        fragility=fragility,
        total_candidates=len(candidates),
        recommendations=recommendations,
        message=f"Found {len(recommendations)} recommendations for {product_name}",
    )


@app.get("/api/autocomplete")
def autocomplete(q: str = Query("", min_length=0, max_length=120)) -> dict:
    query = q.strip()
    if not query:
        return {"suggestions": []}

    suggestions = get_autocomplete_suggestions(query)
    return {"suggestions": suggestions}


@app.post("/api/report/pdf")
def generate_pdf_report(report_data: ReportRequest):
    """Generate and return a PDF report with recommendation details."""
    try:
        pdf_bytes = report_generator.generate_pdf_report(report_data)

        # Create filename with product name and date
        product_name_clean = (
            report_data.product_name.lower()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )
        filename = f"EcoPackAI_{product_name_clean}_{datetime.now().strftime('%Y-%m-%d')}.pdf"

        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF report: {str(e)}")


@app.post("/api/report/excel")
def generate_excel_report(report_data: ReportRequest):
    """Generate and return an Excel report with recommendation details."""
    try:
        excel_bytes = report_generator.generate_excel_report(report_data)

        # Create filename with product name and date
        product_name_clean = (
            report_data.product_name.lower()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )
        filename = f"EcoPackAI_{product_name_clean}_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

        return StreamingResponse(
            iter([excel_bytes]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Excel report: {str(e)}")
