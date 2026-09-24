from src.database import initialize_database
from src.vehicle_service import VehicleService
from src.customer_service import CustomerService
from src.rental_service import RentalService
from src.reports import Reports
from src.utils import read_int, read_float, pause, print_table


def vehicle_menu(service):
    while True:
        print("\n--- Vehicle Management ---")
        print("1. Add vehicle")
        print("2. List vehicles")
        print("3. Search vehicle")
        print("4. Update vehicle")
        print("5. Delete vehicle")
        print("0. Back")
        choice = input("Choice: ").strip()

        try:
            if choice == "1":
                reg = input("Registration number: ")
                vtype = input("Vehicle type: ")
                model = input("Model: ")
                year = read_int("Year: ", 1900, 2100)
                rate = read_float("Daily rate: ", 0.5)
                service.add_vehicle(reg, vtype, model, year, rate)
                print("Vehicle added.")
            elif choice == "2":
                rows = service.list_vehicles()
                print_table(rows, ["ID", "Registration", "Type", "Model", "Year", "Rate", "Status"])
            elif choice == "3":
                term = input("Search registration/model/type: ")
                rows = service.search(term)
                print_table(rows, ["ID", "Registration", "Type", "Model", "Year", "Rate", "Status"])
            elif choice == "4":
                vid = read_int("Vehicle ID: ", 1)
                rate = read_float("New daily rate: ", 0.01)
                service.update_rate(vid, rate)
                print("Vehicle updated.")
            elif choice == "5":
                vid = read_int("Vehicle ID: ", 1)
                service.delete_vehicle(vid)
                print("Vehicle deleted.")
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except ValueError as exc:
            print(f"Error: {exc}")


def customer_menu(service):
    while True:
        print("\n--- Customer Management ------")
        print("1. Add customer")
        print("2. List customers")
        print("0. Back")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                name = input("Name: ")
                phone = input("Phone: ")
                license_no = input("License number: ")
                service.add_customer(name, phone, license_no)
                print("Customer added.")
            elif choice == "2":
                rows = service.list_customers()
                print_table(rows, ["ID", "Name", "Phone", "License"])
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except ValueError as exc:
            print(f"Error: {exc}")


def rental_menu(service):
    while True:
        print("\n--- Rental Management ---")
        print("1. Start rental")
        print("2. Return vehicle")
        print("3. Active rentals")
        print("0. Back")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                vid = read_int("Vehicle ID: ", 1)
                cid = read_int("Customer ID: ", 1)
                days = read_int("Number of days: ", 1)
                rental_id, amount = service.start_rental(vid, cid, days)
                print(f"Rental #{rental_id} created. Estimated charge: Rs. {amount:.2f}")
            elif choice == "2":
                rid = read_int("Rental ID: ", 1)
                amount = service.return_vehicle(rid)
                print(f"Vehicle returned. Final charge: Rs. {amount:.2f}")
            elif choice == "3":
                rows = service.active_rentals()
                print_table(rows, ["Rental", "Registration", "Customer", "Start", "Days", "Amount"])
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except ValueError as exc:
            print(f"Error: {exc}")


def report_menu(reports):
    while True:
        print("\n--- Reports ---")
        print("1. Fleet summary")
        print("2. Rental history")
        print("3. Revenue summary")
        print("0. Back")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                data = reports.fleet_summary()
                for key, value in data.items():
                    print(f"{key}: {value}")
            elif choice == "2":
                rows = reports.rental_history()
                print_table(rows, ["Rental", "Registration", "Customer", "Start", "Return", "Amount", "Status"])
            elif choice == "3":
                data = reports.revenue_summary()
                print(f"Completed rentals: {data['completed_rentals']}")
                print(f"Total revenue: Rs. {data['total_revenue']:.2f}")
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except ValueError as exc:
            print(f"Error: {exc}")


def main():
    conn = initialize_database()
    vehicles = VehicleService(conn)
    customers = CustomerService(conn)
    rentals = RentalService(conn)
    reports = Reports(conn)

    while True:
        print("\n========== VEHICLE MANAGEMENT SYSTEM ==========")
        print("1. Vehicle Management")
        print("2. Customer Management")
        print("3. Rental Management")
        print("4. Reports")
        print("0. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            vehicle_menu(vehicles)
        elif choice == "2":
            customer_menu(customers)
        elif choice == "3":
            rental_menu(rentals)
        elif choice == "4":
            report_menu(reports)
        elif choice == "0":
            conn.close()
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")
        pause()


if __name__ == "__main__":
    main()
