import mysql.connector as ms
import random as ran
from tabulate import tabulate
import os

connection = ms.connect(
    host="127.0.1.1", user="root", password="852456", database="project"
)

cursor = connection.cursor()


def cls(x=None):
    os.system("cls")
    if x == None:
        print("****************************************")


def menu_1():
    print(
        """
    ****************************************
        Bus E-Ticket Reservation System
    ****************************************
    1. Add Reservation
    2. Delete Reservation
    3. Update Reservation Details
    4. Display Reservations
    5. Print Ticket
    6. Exit
    """
    )


def exit_program():
    connection.close()
    print("Goodbye!")
    exit()


def destinations():
    cursor.execute("SELECT Bus_No, Destination FROM buses")
    data = cursor.fetchall()
    headers = ["Bus_No", "Destination"]
    print(tabulate(data, headers, tablefmt="grid"))


def print_ticket(ticket_no, x=None):
    if x == None:
        cls()
    query = f"SELECT * FROM seats WHERE Ticket_No={ticket_no};"
    cursor.execute(query)
    reservation_seat = cursor.fetchone()
    if reservation_seat:
        Bus_No = reservation_seat[2]
        query = f"SELECT * FROM buses WHERE Bus_No={Bus_No}"
        cursor.execute(query)
        reservation_bus = cursor.fetchone()
        if reservation_bus:
            ticket_data = [
                ["Ticket No:", ticket_no],
                ["Name:", reservation_seat[1]],
                ["Departure Time:", reservation_bus[1]],
                ["Bus No:", reservation_seat[2]],
                ["Seat Type:", reservation_seat[3]],
                [
                    "Bill:",
                    reservation_bus[4]
                    if reservation_seat[3] == "Regular"
                    else reservation_bus[5],
                ],
            ]

            table = tabulate(ticket_data, tablefmt="grid")

            print("*" * 15, " Ticket ", "*" * 16)
            print(table)
            print("*" * 41)
    else:
        print("Invalid reservation details or ticket number not found")


def pre_reserve(destination):
    query = f"SELECT Bus_No, Available_Seats FROM buses WHERE Destination = '{destination}';"
    cursor.execute(query)
    result = cursor.fetchone()

    if result and result[1]:
        bus_no, available_seats_str = result[0], result[1]
        available_seats_regular, available_seats_premium = map(
            int, available_seats_str.split(",")  # type:ignore
        )
        return {
            "bus_no": bus_no,
            "available_seats_regular": available_seats_regular,
            "available_seats_premium": available_seats_premium,
        }
    else:
        return None


def generate_unique_ticket_number():
    while True:
        ticket_number = ran.randint(10, 999)
        query = f"SELECT Ticket_No FROM seats WHERE Ticket_No = {ticket_number};"
        cursor.execute(query)
        existing_ticket = cursor.fetchone()

        if not existing_ticket:
            return ticket_number


def reserve():
    destinations()
    destination = input("Where to?: ")
    data = pre_reserve(destination)
    if not data:
        cls()
        print("No Seats Available")
        return
    name = input("Enter Name: ")
    print("Available Seat Types:")
    print(f"1. Regular ({data['available_seats_regular']} available)")
    print(f"2. Premium ({data['available_seats_premium']} available)")
    choice = int(input("Choose Seat Type (1 for Regular, 2 for Premium): "))
    if choice in [1, 2]:
        seat_type = "Regular" if choice == 1 else "Premium"
        available_seats_key = (
            "available_seats_regular"
            if seat_type == "Regular"
            else "available_seats_premium"
        )
        available_seats = data[available_seats_key]
        if available_seats > 0:
            ticket_number = generate_unique_ticket_number()
            query = (
                f"SELECT Available_Seats FROM buses WHERE Bus_No = {data['bus_no']};"
            )
            cursor.execute(query)
            current_available_seats = cursor.fetchone()[0].split(",")  # type:ignore
            available_regular_seats, available_premium_seats = map(
                int, current_available_seats
            )
            if seat_type == "Regular":
                available_regular_seats -= 1
            else:
                available_premium_seats -= 1
            new_available_seats = f"{available_regular_seats},{available_premium_seats}"
            values = f"{ticket_number}, '{name}', {data['bus_no']}, '{seat_type}'"
            query = f"INSERT INTO seats (Ticket_No, Name, Bus_No, Seat_Type) VALUES ({values});"
            cursor.execute(query)
            query = f"UPDATE buses SET Available_Seats = '{new_available_seats}' WHERE Bus_No = {data['bus_no']};"
            cursor.execute(query)
            connection.commit()
            cls()
            print(
                f"Reservation successful! You have reserved a {seat_type} seat with Ticket No: {ticket_number}"
            )
            print("The Following are the Details of the Reservation")
            print_ticket(ticket_number, 0)
        else:
            print("No Seats Available for the selected type.")
    else:
        print("Invalid choice. Reservation canceled.")


def delete_reservation():
    ticket_no = input("Enter your Ticket_No: ")
    query = f"SELECT Bus_No, Seat_Type FROM seats WHERE Ticket_No = {ticket_no}"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        bus_no, seat_type = result[0], result[1]
        query = f"DELETE FROM seats WHERE Ticket_No = {ticket_no};"
        cursor.execute(query)
        query = f"SELECT Available_Seats FROM buses WHERE Bus_No = {bus_no};"
        cursor.execute(query)
        current_available_seats = cursor.fetchone()[0].split(",")  # type:ignore
        available_regular_seats, available_premium_seats = map(
            int, current_available_seats
        )

        if seat_type == "Regular":
            available_regular_seats += 1
        else:
            available_premium_seats += 1
        new_available_seats = f"{available_regular_seats},{available_premium_seats}"
        query = f"UPDATE buses SET Available_Seats = '{new_available_seats} '"
        query += f"WHERE Bus_No = {bus_no};"
        cursor.execute(query)
        connection.commit()

        cls()
        print(
            f"Reservation with Ticket No {ticket_no} deleted successfully. +1 {seat_type} seat is now available."
        )
    else:
        cls()
        print("Invalid Ticket No.")


def display_reservations():
    destinations()
    Bus_No = int(input("Choose Bus No. (0 for all): "))
    if Bus_No == 0:
        query = "SELECT * FROM seats;"
    else:
        query = f"SELECT * FROM seats WHERE Bus_No={Bus_No};"
    cursor.execute(query)
    data = cursor.fetchall()
    if data:
        column_names = [i[0] for i in cursor.description]  # type:ignore
        table = tabulate(data, headers=column_names, tablefmt="grid")
        print(table)
    else:
        print("No reservations found.")


def change_reservation_details(ticket_no):
    cls()
    query = f"SELECT Name, Bus_No, Seat_Type FROM seats WHERE Ticket_No = {ticket_no};"
    cursor.execute(query)
    reservation = cursor.fetchone()

    if reservation:
        current_name, bus_no, current_seat_type = (
            reservation[0],
            reservation[1],
            reservation[2],
        )
        print("Current Details:")
        print_ticket(ticket_no)
        new_name = input("Enter new name (press Enter to keep the current name): ")
        new_seat_type = input(
            "Enter new seat type (Regular/Premium, press Enter to keep the current type): "
        )

        if not new_name:
            new_name = current_name
        if new_seat_type.lower() not in ["regular", "premium"]:
            new_seat_type = current_seat_type

        cost_difference = 0
        if new_seat_type != current_seat_type:
            query = f"SELECT Reg_Cost, Prem_Cost FROM buses WHERE Bus_No = {bus_no};"
            cursor.execute(query)
            cost_data = cursor.fetchone()

            if cost_data:
                reg_cost, prem_cost = cost_data[0], cost_data[1]
                new_cost = reg_cost if new_seat_type == "Regular" else prem_cost

                query = f"SELECT Seat_Type FROM seats WHERE Ticket_No = {ticket_no};"
                cursor.execute(query)
                current_seat_type = cursor.fetchone()
                current_cost = reg_cost if current_seat_type == "Regular" else prem_cost
                cost_difference = new_cost - current_cost  # type:ignore

                print(f"Seat type changed. Cost difference: ₹{cost_difference}")

        query = (
            f"UPDATE seats SET Name = '{new_name}', Seat_Type = '{new_seat_type}' "
            f"WHERE Ticket_No = {ticket_no};"
        )
        cursor.execute(query)
        connection.commit()

        if cost_difference != 0:
            query = f"SELECT Available_Seats FROM buses WHERE Bus_No = {bus_no};"
            cursor.execute(query)
            current_available_seats = cursor.fetchone()[0].split(",")  # type:ignore
            available_regular_seats, available_premium_seats = map(
                int, current_available_seats
            )

            if current_seat_type == "Regular":
                available_regular_seats += 1
                available_premium_seats -= 1
            else:
                available_regular_seats -= 1
                available_premium_seats += 1

            new_available_seats = f"{available_regular_seats},{available_premium_seats}"

            query = f"UPDATE buses SET Available_Seats = '{new_available_seats}' WHERE Bus_No = {bus_no};"
            cursor.execute(query)
            connection.commit()

        print(ticket_no)
        print("Reservation details updated successfully.")
    else:
        print("Invalid ticket number or reservation not found.")


# Menu Choices
MENU_ADD_RESERVATION = 1
MENU_DELETE_RESERVATION = 2
MENU_UPDATE_RESERVATION = 3
MENU_DISPLAY_RESERVATIONS = 4
MENU_PRINT_TICKET = 5
MENU_EXIT = 6


def main_menu():
    while True:
        menu_1()
        choice = int(input("Choose: "))

        if choice == MENU_ADD_RESERVATION:
            reserve()
        elif choice == MENU_DELETE_RESERVATION:
            delete_reservation()
        elif choice == MENU_UPDATE_RESERVATION:
            ticket_no = input("Enter Ticket No to Update: ")
            change_reservation_details(ticket_no)
        elif choice == MENU_DISPLAY_RESERVATIONS:
            cls()
            display_reservations()
        elif choice == MENU_PRINT_TICKET:
            ticket_no = input("Enter Ticket No to print a ticket: ")
            print_ticket(ticket_no)
        elif choice == MENU_EXIT:
            exit_program()
        else:
            cls(0)
            print("Invalid choice. Please select a valid option.")


main_menu()
