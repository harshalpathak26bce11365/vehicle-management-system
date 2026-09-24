class Reports:
    def __init__(self, conn):
        self.conn = conn

    def fleet_summary(self):
        rows = self.conn.execute(
            "SELECT status, COUNT(*) FROM vehicles GROUP BY status"
        ).fetchall()
        data = {"Total vehicles": 0, "AVAILABLE": 0, "RENTED": 0, "MAINTENANCE": 0}
        for status, count in rows:
            data[status] = count
            data["Total vehicles"] += count
        return data

    def rental_history(self):
        return self.conn.execute(
            """SELECT r.rental_id, v.registration_no, c.name,
                      r.start_date, r.return_date, r.total_amount, r.status
               FROM rentals r
               JOIN vehicles v ON v.vehicle_id = r.vehicle_id
               JOIN customers c ON c.customer_id = r.customer_id
               ORDER BY r.rental_id DESC"""
        ).fetchall()

    def revenue_summary(self):
        row = self.conn.execute(
            """SELECT COUNT(*), COALESCE(SUM(total_amount), 0)
               FROM rentals WHERE status = 'COMPLETED'"""
        ).fetchone()
        return {"completed_rentals": row[0], "total_revenue": row[1]}
