"""Pydantic models for the Unit Converter application."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UnitInfo(BaseModel):
    """Detailed information about a single unit."""

    model_config = ConfigDict(frozen=True)

    key: str = Field(description="Internal key of the unit (e.g., 'm')")
    name: str = Field(description="Full name of the unit (e.g., 'Meter')")
    symbol: str = Field(description="Symbol of the unit (e.g., 'm')")


class CategoryInfo(BaseModel):
    """Detailed information about a unit category."""

    model_config = ConfigDict(frozen=True)

    key: str = Field(description="Internal key of the category (e.g., 'length')")
    name: str = Field(description="Display name of the category (e.g., 'Length')")
    icon: str = Field(description="Lucide icon name or emoji representation")
    units: list[UnitInfo] = Field(description="List of units supported in this category")


class ConversionRequest(BaseModel):
    """Payload representing a unit conversion request."""

    category: str = Field(description="Category of unit (e.g., 'length')")
    from_unit: str = Field(description="Source unit key (e.g., 'm')")
    to_unit: str = Field(description="Target unit key (e.g., 'ft')")
    value: float = Field(description="Numeric value to convert")


class ConversionResponse(BaseModel):
    """Response returned after a successful conversion."""

    category: str
    from_unit: str
    to_unit: str
    original_value: float
    converted_value: float
    formula: str = Field(description="Formula or explanation of the conversion")
