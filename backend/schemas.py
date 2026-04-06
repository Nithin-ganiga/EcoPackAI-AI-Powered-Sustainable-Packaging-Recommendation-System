"""This file defines request and response schemas for the API so validation and response shape stay consistent, predictable, and easy for the frontend to consume."""

from typing import List
from pydantic import BaseModel, Field, field_validator


class RecommendRequest(BaseModel):
    product_name: str = Field(..., min_length=1, description="Name of product to package")
    product_weight_grams: float = Field(..., gt=0, description="Product weight in grams")

    @field_validator("product_name")
    @classmethod
    def product_name_not_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Product name must not be empty")
        return cleaned


class MaterialRecommendation(BaseModel):
    rank: int = Field(..., ge=1, le=5)
    material_name: str
    material_type: str
    industry: str
    strength: str
    weight_capacity: str
    cost_inr: float
    cost_level: str
    eco_friendly: bool
    sustainability_tier: str
    biodegradability_score: int
    recyclability_percent: int
    co2_emission_score: int
    fragility_support: str
    suitability_score: float
    rank_score: float
    why_recommended: str


class RecommendResponse(BaseModel):
    status: str
    product_name: str
    product_weight_grams: float
    fragility: str
    total_candidates: int
    recommendations: List[MaterialRecommendation] = Field(default_factory=list, max_length=5)
    message: str


class ReportRequest(BaseModel):
    product_name: str = Field(..., description="Name of product that was searched")
    product_weight_grams: float = Field(..., gt=0, description="Weight of product in grams")
    fragility: str = Field(..., description="Fragility level: low, medium, or high")
    generated_at: str = Field(..., description="ISO format datetime string when report was generated")
    recommendations: List[MaterialRecommendation] = Field(..., max_length=5, description="List of 5 recommendations")
