# Vehicle Management System

A command-line Vehicle Management System built with Python and SQLite. It manages vehicles, customers, rentals, returns, and summary reports without requiring a GUI.

## Features

1. **Vehicle Management**
   - Add, view, search, update and delete vehicles.
   - Track registration number, type, model, year, daily rate and status.

2. **Customer Management**
   - Add and view customers.
   - Validate phone numbers and basic customer details.

3. **Rental Management**
   - Rent an available vehicle to a customer.
   - Calculate rental charges from the daily rate and rental duration.
   - Return vehicles and record final charges.

4. **Reports**
   - Show fleet statistics.
   - Show active rentals.
   - Show rental history and revenue summary.

## Technologies

- Python 3.10+
- SQLite3
- Python standard library only
- unittest for tests

## Project Structure

```text
vehicle_management_system/
├── README.md
├── statement.md
├── requirements.txt
├── schema.sql
├── main.py
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── validators.py
│   ├── vehicle_service.py
│   ├── customer_service.py
│   ├── rental_service.py
│   ├── reports.py
│   └── utils.py
├── data/
│   └── .gitkeep
└── tests/
    ├── __init__.py
    └── test_system.py
```

## Setup

1. Install Python 3.10 or later.
2. Clone/download this repository.
3. Open a terminal in the repository root.
4. No third-party packages are required.

## Run

```bash
python main.py
```

The SQLite database is created automatically in `data/vehicle_management.db`.

## Test

```bash
python -m unittest discover -s tests -v
```

## Typical Workflow

1. Add a vehicle.
2. Add a customer.
3. Start a rental using the vehicle registration number and customer ID.
4. Return the vehicle.
5. Open reports to view fleet status, active rentals and revenue.

## Notes

This is a command-line academic project. The database file is generated locally and should normally not be committed to GitHub.

## Academic Requirements Covered

- Three major functional modules: vehicle, customer and rental management.
- CRUD/data processing and reporting.
- Input validation and error handling.
- Modular implementation with multiple Python files.
- SQLite storage.
- Unit tests.
- Documentation and design artifacts are provided in the accompanying project report.
