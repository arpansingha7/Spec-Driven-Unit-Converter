# unit-conversion Specification

## Purpose
TBD - created by archiving change unit-converter. Update Purpose after archive.
## Requirements
### Requirement: List Categories
The system SHALL return the complete set of supported unit categories (Length, Mass, Temperature, Volume, Area) and their constituent unit definitions (key, name, symbol) via a HTTP GET request.

#### Scenario: Retrieve Categories Successfully
- **WHEN** the user sends a HTTP GET request to `/api/categories`
- **THEN** the system returns a 200 OK status code with a JSON list of categories and units

### Requirement: Linear Unit Conversion
The system SHALL calculate and return accurate, rounded, and validated conversions between linear units of the same category via a HTTP POST request.

#### Scenario: Convert Meters to Feet
- **WHEN** the user requests a POST conversion of 100 meters to feet
- **THEN** the system returns a 200 OK status code with a converted value of 328.08399 and a conversion explanation formula

### Requirement: Non-Linear Temperature Conversion
The system SHALL apply custom offset calculations to convert between Celsius, Fahrenheit, and Kelvin temperature units via a HTTP POST request.

#### Scenario: Convert Celsius to Fahrenheit
- **WHEN** the user requests a POST conversion of 100 Celsius to Fahrenheit
- **THEN** the system returns a 200 OK status code with a converted value of 212.0 and the math formula "(100.0 * 9/5) + 32"

