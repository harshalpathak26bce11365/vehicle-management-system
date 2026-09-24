CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_no TEXT NOT NULL UNIQUE,
    vehicle_type TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    daily_rate REAL NOT NULL CHECK(daily_rate > 0),
    status TEXT NOT NULL DEFAULT 'AVAILABLE'
        CHECK(status IN ('AVAILABLE', 'RENTED', 'MAINTENANCE'))
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    license_no TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS rentals (
    rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    expected_days INTEGER NOT NULL CHECK(expected_days > 0),
    return_date TEXT,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE'
        CHECK(status IN ('ACTIVE', 'COMPLETED')),
    FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
