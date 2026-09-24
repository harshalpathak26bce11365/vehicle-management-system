from .validators import require_text, validate_phone


class CustomerService:
    def __init__(self, conn):
        self.conn = conn

    def add_customer(self, name, phone, license_no):
        name = require_text(name, "Name")
        phone = validate_phone(phone)
        license_no = require_text(license_no, "License number").upper()
        try:
            self.conn.execute(
                "INSERT INTO customers (name, phone, license_no) VALUES (?, ?, ?)",
                (name, phone, license_no),
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            raise ValueError(f"Could not add customer: {exc}") from exc

    def list_customers(self):
        return self.conn.execute(
            "SELECT customer_id, name, phone, license_no FROM customers ORDER BY customer_id"
        ).fetchall()
