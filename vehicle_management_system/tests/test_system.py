import sqlite3
import unittest

from src.database import SCHEMA_PATH
from src.vehicle_service import VehicleService
from src.customer_service import CustomerService
from src.rental_service import RentalService


class VehicleManagementTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())
        self.vehicles = VehicleService(self.conn)
        self.customers = CustomerService(self.conn)
        self.rentals = RentalService(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_vehicle_and_customer_creation(self):
        self.vehicles.add_vehicle("MP20AB1234", "Car", "Sedan", 2024, 1500)
        self.customers.add_customer("Test User", "9876543210", "LIC123")
        self.assertEqual(len(self.vehicles.list_vehicles()), 1)
        self.assertEqual(len(self.customers.list_customers()), 1)

    def test_rental_changes_vehicle_status_and_return_restores_it(self):
        self.vehicles.add_vehicle("MP20XY5678", "Car", "Hatchback", 2023, 1000)
        self.customers.add_customer("Test User", "9876543210", "LIC456")
        rental_id, amount = self.rentals.start_rental(1, 1, 3)
        self.assertEqual(amount, 3000)
        self.assertEqual(
            self.conn.execute("SELECT status FROM vehicles WHERE vehicle_id=1").fetchone()[0],
            "RENTED",
        )
        final_amount = self.rentals.return_vehicle(rental_id)
        self.assertEqual(final_amount, 3000)
        self.assertEqual(
            self.conn.execute("SELECT status FROM vehicles WHERE vehicle_id=1").fetchone()[0],
            "AVAILABLE",
        )

    def test_invalid_phone(self):
        with self.assertRaises(ValueError):
            self.customers.add_customer("Test", "123", "LIC999")


if __name__ == "__main__":
    unittest.main()
