from datetime import date
from .validators import validate_days


class RentalService:
    def __init__(self, conn):
        self.conn = conn

    def start_rental(self, vehicle_id, customer_id, days):
        validate_days(days)
        vehicle = self.conn.execute(
            "SELECT daily_rate, status FROM vehicles WHERE vehicle_id = ?",
            (vehicle_id,),
        ).fetchone()
        if vehicle is None:
            raise ValueError("Vehicle not found.")
        if vehicle[1] != "AVAILABLE":
            raise ValueError("Vehicle is not available.")

        customer = self.conn.execute(
            "SELECT customer_id FROM customers WHERE customer_id = ?",
            (customer_id,),
        ).fetchone()
        if customer is None:
            raise ValueError("Customer not found.")

        amount = vehicle[0] * days
        try:
            cur = self.conn.execute(
                """INSERT INTO rentals
                   (vehicle_id, customer_id, start_date, expected_days, total_amount)
                   VALUES (?, ?, ?, ?, ?)""",
                (vehicle_id, customer_id, date.today().isoformat(), days, amount),
            )
            self.conn.execute(
                "UPDATE vehicles SET status = 'RENTED' WHERE vehicle_id = ?",
                (vehicle_id,),
            )
            self.conn.commit()
            return cur.lastrowid, amount
        except Exception as exc:
            self.conn.rollback()
            raise ValueError(f"Could not start rental: {exc}") from exc

    def return_vehicle(self, rental_id):
        rental = self.conn.execute(
            """SELECT vehicle_id, total_amount, status
               FROM rentals WHERE rental_id = ?""",
            (rental_id,),
        ).fetchone()
        if rental is None:
            raise ValueError("Rental not found.")
        if rental[2] == "COMPLETED":
            raise ValueError("Rental is already completed.")

        try:
            self.conn.execute(
                """UPDATE rentals
                   SET return_date = ?, status = 'COMPLETED'
                   WHERE rental_id = ?""",
                (date.today().isoformat(), rental_id),
            )
            self.conn.execute(
                "UPDATE vehicles SET status = 'AVAILABLE' WHERE vehicle_id = ?",
                (rental[0],),
            )
            self.conn.commit()
            return rental[1]
        except Exception as exc:
            self.conn.rollback()
            raise ValueError(f"Could not return vehicle: {exc}") from exc

    def active_rentals(self):
        return self.conn.execute(
            """SELECT r.rental_id, v.registration_no, c.name,
                      r.start_date, r.expected_days, r.total_amount
               FROM rentals r
               JOIN vehicles v ON v.vehicle_id = r.vehicle_id
               JOIN customers c ON c.customer_id = r.customer_id
               WHERE r.status = 'ACTIVE'
               ORDER BY r.rental_id"""
        ).fetchall()
