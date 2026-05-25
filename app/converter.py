"""Core unit conversion database and calculation engine."""

from __future__ import annotations

from app.models import CategoryInfo, UnitInfo, ConversionResponse

# Unit configuration database
CATEGORIES: dict[str, dict[str, str | list[dict[str, str]]]] = {
    "length": {
        "name": "Length",
        "icon": "📐",
        "units": [
            {"key": "mm", "name": "Millimeter", "symbol": "mm", "factor": 0.001},
            {"key": "cm", "name": "Centimeter", "symbol": "cm", "factor": 0.01},
            {"key": "m", "name": "Meter", "symbol": "m", "factor": 1.0},
            {"key": "km", "name": "Kilometer", "symbol": "km", "factor": 1000.0},
            {"key": "in", "name": "Inch", "symbol": "in", "factor": 0.0254},
            {"key": "ft", "name": "Foot", "symbol": "ft", "factor": 0.3048},
            {"key": "yd", "name": "Yard", "symbol": "yd", "factor": 0.9144},
            {"key": "mi", "name": "Mile", "symbol": "mi", "factor": 1609.344},
        ],
    },
    "mass": {
        "name": "Mass / Weight",
        "icon": "⚖️",
        "units": [
            {"key": "mg", "name": "Milligram", "symbol": "mg", "factor": 0.000001},
            {"key": "g", "name": "Gram", "symbol": "g", "factor": 0.001},
            {"key": "kg", "name": "Kilogram", "symbol": "kg", "factor": 1.0},
            {"key": "oz", "name": "Ounce", "symbol": "oz", "factor": 0.028349523125},
            {"key": "lb", "name": "Pound", "symbol": "lb", "factor": 0.45359237},
            {"key": "st", "name": "Stone", "symbol": "st", "factor": 6.35029318},
        ],
    },
    "temperature": {
        "name": "Temperature",
        "icon": "🌡️",
        "units": [
            {"key": "C", "name": "Celsius", "symbol": "°C"},
            {"key": "F", "name": "Fahrenheit", "symbol": "°F"},
            {"key": "K", "name": "Kelvin", "symbol": "K"},
        ],
    },
    "volume": {
        "name": "Volume",
        "icon": "🧪",
        "units": [
            {"key": "ml", "name": "Milliliter", "symbol": "ml", "factor": 0.001},
            {"key": "l", "name": "Liter", "symbol": "l", "factor": 1.0},
            {"key": "cup", "name": "Cup", "symbol": "cup", "factor": 0.2365882365},
            {"key": "pt", "name": "Pint", "symbol": "pt", "factor": 0.473176473},
            {"key": "qt", "name": "Quart", "symbol": "qt", "factor": 0.946352946},
            {"key": "gal", "name": "Gallon", "symbol": "gal", "factor": 3.785411784},
        ],
    },
    "area": {
        "name": "Area",
        "icon": "🗺️",
        "units": [
            {"key": "m2", "name": "Square Meter", "symbol": "m²", "factor": 1.0},
            {"key": "km2", "name": "Square Kilometer", "symbol": "km²", "factor": 1000000.0},
            {"key": "ft2", "name": "Square Foot", "symbol": "ft²", "factor": 0.09290304},
            {"key": "ac", "name": "Acre", "symbol": "ac", "factor": 4046.8564224},
            {"key": "ha", "name": "Hectare", "symbol": "ha", "factor": 10000.0},
        ],
    },
}


def get_categories() -> list[CategoryInfo]:
    """Retrieve all supported categories and their units."""
    result = []
    for cat_key, cat_data in CATEGORIES.items():
        units_list = []
        for u in cat_data["units"]:
            units_list.append(
                UnitInfo(key=u["key"], name=u["name"], symbol=u["symbol"])
            )
        result.append(
            CategoryInfo(
                key=cat_key,
                name=str(cat_data["name"]),
                icon=str(cat_data["icon"]),
                units=units_list,
            )
        )
    return result


def convert_units(
    category: str, from_unit: str, to_unit: str, value: float
) -> ConversionResponse:
    """Perform the conversion calculation based on unit categories and multipliers."""
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")

    cat_data = CATEGORIES[category]
    units_dict = {u["key"]: u for u in cat_data["units"]}

    if from_unit not in units_dict or to_unit not in units_dict:
        raise ValueError(
            f"Invalid unit conversion: {from_unit} to {to_unit} in category {category}"
        )

    # 1. Temperature Conversion (Non-linear offset logic)
    if category == "temperature":
        converted_val, formula = _convert_temperature(from_unit, to_unit, value)
    # 2. Linear Scaling Conversion (Multiplicative logic)
    else:
        u_from = units_dict[from_unit]
        u_to = units_dict[to_unit]
        factor_from = float(u_from["factor"])
        factor_to = float(u_to["factor"])

        # Convert to base unit, then to target unit
        base_val = value * factor_from
        converted_val = base_val / factor_to

        # Round to 6 decimal places to prevent float precision issues
        converted_val = round(converted_val, 6)

        symbol_from = u_from["symbol"]
        symbol_to = u_to["symbol"]
        # Standard formula presentation
        if factor_from == factor_to:
            formula = f"1 {symbol_from} = 1 {symbol_to}"
        else:
            rel_factor = factor_from / factor_to
            formula = f"Multiply the value by {rel_factor:g} (1 {symbol_from} ≈ {rel_factor:g} {symbol_to})"

    return ConversionResponse(
        category=category,
        from_unit=from_unit,
        to_unit=to_unit,
        original_value=value,
        converted_value=converted_val,
        formula=formula,
    )


def _convert_temperature(from_unit: str, to_unit: str, val: float) -> tuple[float, str]:
    """Helper method for temperature conversions."""
    if from_unit == to_unit:
        return val, f"1 °{from_unit} = 1 °{to_unit}"

    # Conversion logic through Celsius
    # Convert from_unit to Celsius first
    if from_unit == "C":
        celsius = val
    elif from_unit == "F":
        celsius = (val - 32) / 1.8
    elif from_unit == "K":
        celsius = val - 273.15
    else:
        raise ValueError(f"Unknown temperature unit: {from_unit}")

    # Convert Celsius to to_unit
    if to_unit == "C":
        result = celsius
    elif to_unit == "F":
        result = celsius * 1.8 + 32
    elif to_unit == "K":
        result = celsius + 273.15
    else:
        raise ValueError(f"Unknown temperature unit: {to_unit}")

    # Generate formula explanation
    formulas = {
        ("C", "F"): f"({val} * 9/5) + 32",
        ("F", "C"): f"({val} - 32) * 5/9",
        ("C", "K"): f"{val} + 273.15",
        ("K", "C"): f"{val} - 273.15",
        ("F", "K"): f"({val} - 32) * 5/9 + 273.15",
        ("K", "F"): f"({val} - 273.15) * 9/5 + 32",
    }

    formula_str = formulas.get(
        (from_unit, to_unit), f"Standard temperature conversion formula"
    )
    return round(result, 6), formula_str
