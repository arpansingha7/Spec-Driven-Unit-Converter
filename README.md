# Spec-Driven Unit Converter

A modern, high-fidelity Unit Converter application built as part of the Spec-Driven Development Workshop. The project compares two distinct AI-assisted engineering methodologies: **Vibe Coding** and **Spec-Driven Development (SDD)**.

## Project Structure & Branch Conventions

To satisfy the workshop submission requirements, this repository contains three core branches:

1. **`main`**: The base structure of the repository, containing packaging configuration (`pyproject.toml`) and standard base settings.
2. **`vibe_coded_submission`**: The complete implementation of the Unit Converter developed purely using direct visual development ("Vibe Coding"). It features a premium, responsive glassmorphism web interface served by FastAPI.
3. **`sdd_submission`**: The complete implementation of the Unit Converter developed systematically following the **OpenSpec** methodology. All requirements, designs, and tasks are defined in formal OpenSpec changes and implemented step-by-step.

## Features

- **Multi-Category Conversion**: Seamless conversions for **Length**, **Mass/Weight**, **Temperature**, **Volume**, and **Area**.
- **FastAPI HTTP REST API**: Clean RESTful API serving categories, units, and precise conversion operations.
- **Premium Glassmorphic UI**: Sleek, modern front-end served directly by FastAPI static files. It includes HSL-tailored colors, smooth animations, a light/dark mode toggle, value swapping, and clipboard-copying utilities.
- **Accurate Calculation**: Deterministic precision logic including floating-point correction and non-multiplicative conversions (e.g. Fahrenheit/Kelvin).

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn
- **Frontend**: HTML5, Vanilla CSS3 (custom CSS variables, glassmorphism design system), Vanilla ES6 JavaScript

---

## Local Setup

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/arpansingha7/Spec-Driven-Unit-Converter.git
cd Spec-Driven-Unit-Converter

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# Install package in editable mode
pip install -e .
```

### 3. Run the Server
```bash
uvicorn app.main:app --reload --port 8000
```
Then visit `http://localhost:8000` in your web browser.
