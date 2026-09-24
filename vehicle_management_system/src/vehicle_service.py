from .validators import require_text, validate_year, validate_rate


class VehicleService:
    def __init__(self, conn):
        self.conn = conn

    def add_vehicle(self, registration_no, vehicle_type, model, year, daily_rate):
        registration_no = require_text(registration_no, "Registration number").upper()
        vehicle_type = require_text(vehicle_type, "Vehicle type")
        model = require_text(model, "Model")
        validate_year(year)
        validate_rate(daily_rate)
        try:
            self.conn.execute(
                """INSERT INTO vehicles
                   (registration_no, vehicle_type, model, year, daily_rate)
                   VALUES (?, ?, ?, ?, ?)""",
                (registration_no, vehicle_type, model, year, daily_rate),
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            raise ValueError(f"Could not add vehicle: {exc}") from exc

    def list_vehicles(self):
        return self.conn.execute(
            """SELECT vehicle_id, registration_no, vehicle_type, model,
                      year, daily_rate, status
               FROM vehicles ORDER BY vehicle_id"""
        ).fetchall()

    def search(self, term):
        term = f"%{term.strip()}%"
        return self.conn.execute(
            """SELECT vehicle_id, registration_no, vehicle_type, model,
                      year, daily_rate, status
               FROM vehicles
               WHERE registration_no LIKE ?
                  OR vehicle_type LIKE ?
                  OR model LIKE ?
               ORDER BY vehicle_id""",
            (term, term, term),
        ).fetchall()

    def update_rate(self, vehicle_id, daily_rate):
        validate_rate(daily_rate)
        cur = self.conn.execute(
            "UPDATE vehicles SET daily_rate = ? WHERE vehicle_id = ?",
            (daily_rate, vehicle_id),
        )
        if cur.rowcount == 0:
            raise ValueError("Vehicle not found.")
        self.conn.commit()

    def delete_vehicle(self, vehicle_id):
        row = self.conn.execute(
            "SELECT status FROM vehicles WHERE vehicle_id = ?", (vehicle_id,)
        ).fetchone()
        if row is None:
            raise ValueError("Vehicle not found.")
        if row[0] == "RENTED":
            raise ValueError("A rented vehicle cannot be deleted.")
        try:
            self.conn.execute("DELETE FROM vehicles WHERE vehicle_id = ?", (vehicle_id,))
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            raise ValueError("Vehicle cannot be deleted because it has related rental records.") from exc
