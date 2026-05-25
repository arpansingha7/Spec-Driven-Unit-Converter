## Context

The Unit Converter is built as a lightweight FastAPI microservice. The system executes calculations in memory using highly verified conversion coefficients and handles custom temperature equation logic. The frontend is served directly by mounting static directories from the FastAPI application.

## Goals / Non-Goals

**Goals:**
- Provide precise unit conversions across Length, Mass, Temperature, Volume, and Area.
- Expose standardized REST endpoints for metadata and calculation.
- Support strict validation of requests through Pydantic v2.
- Build a fast, gorgeous glassmorphism web dashboard in pure HTML/CSS/JS.

**Non-Goals:**
- External dynamic conversions requiring API synchronization (e.g., Currency conversion).
- Persistent storage or historical database of conversion records.

## Decisions

- **FastAPI / Pydantic Framework**: Chosen for rapid endpoint development, automatic OpenAPI documentation, and built-in type validation.
- **Base Unit Multiplier Design**: Instead of managing a large, complex matrix of $N^2$ conversion rates, each unit defines a multiplier factor relative to a base unit (e.g., Meter for length). All conversions transform to the base unit first, then scale to the target unit.
- **Non-Linear Custom Functions**: Temperature conversions do not follow standard linear scaling. Custom conditional functions manage conversions to/from Celsius as a bridge to other units (Kelvin, Fahrenheit).
- **Vanilla Static Front-end**: The UI is served entirely via `fastapi.staticfiles.StaticFiles`. This keeps deployment completely stateless and simple.

## Risks / Trade-offs

- **Risk**: Floating point division precision issues.
  - **Mitigation**: Outputs are rounded to 6 decimal places inside the backend layer, and formatted cleanly on the client-side.
- **Risk**: High volume conversion spikes slowing down the server.
  - **Mitigation**: Keep all lookup data static and in-memory, avoiding any remote API calls or blocking database IO.
