import mysql.connector as ms
import random as ran

# Database connection setup
connection = ms.connect(
    host="127.0.0.1", user="root", password="852456", database="project"
)

cursor = connection.cursor()

# Constants for menu choices
MENU_ADD_RESERVATION = 1
MENU_DELETE_RESERVATION = 2
MENU_DISPLAY_RESERVATIONS = 3
MENU_EXIT = 4


def menu_s_1():
    print()
    print("1. Add Reservation")
    print("2. Delete Reservation")
    print("3. Display All Reservations")
    print("4. Exit")


def exit_program():
    connection.close()
    print("Goodbye!")
    exit()


def pre_reserve(destination):
    # Check seat availability and retrieve data
    query = f"SELECT Bus_No, Available_Seats FROM buses WHERE Destination = '{destination}';"
    cursor.execute(query)
    result = cursor.fetchone()
    print(result)

    if result and result[1] > 0:  # type:ignore
        bus_no = result[0]

        # Retrieve taken seat numbers
        query = f"SELECT Ticket_No FROM seats WHERE Bus_No = {bus_no};"
        cursor.execute(query)
        taken_seats = set(ticket_no for (ticket_no,) in cursor.fetchall())

        # Generate available seat numbers
        available_seats = list(
            set(range(1, result[1] + 1)) - taken_seats  # type:ignore
        )

        return {
            "bus_no": bus_no,
            "available_seats": available_seats,
        }
    else:
        return None


def reserve():
    destination = input("Where to?: ")
    data = pre_reserve(destination)

    if not data:
        print("No Seats Available")
        return

    name = input("Enter Name: ")
    available_seats = data["available_seats"]

    if not available_seats:
        print("No Seats Available")
        return

    # Randomly choose a seat
    ticket_no = ran.choice(available_seats)

    # Insert the reservation into the database
    query = f"INSERT INTO seats (Ticket_No, Name, Bus_No) VALUES ({ticket_no}, '{name}', {data['bus_no']});"
    cursor.execute(query)

    # Update available seats
    query = f"UPDATE buses SET Available_Seats = Available_Seats - 1 WHERE Bus_No = {data['bus_no']};"
    cursor.execute(query)
    connection.commit()

    print(f"Reservation successful! Your ticket number is {ticket_no}")


def delete_reservation():
    ticket_no = input("Enter your Ticket_No: ")
    query = f"SELECT Bus_No FROM seats WHERE Ticket_No = {ticket_no}"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        bus_no = result[0]

        # Delete the reservation from the database
        query = f"DELETE FROM seats WHERE Ticket_No = {ticket_no};"
        cursor.execute(query)

        # Update available seats
        query = f"UPDATE buses SET Available_Seats = Available_Seats + 1 WHERE Bus_No = {bus_no};"
        cursor.execute(query)
        connection.commit()

        print(f"Reservation with Ticket No {ticket_no} deleted successfully.")
    else:
        print("Invalid Ticket No.")


def display_reservations():
    query = "SELECT * FROM seats;"
    cursor.execute(query)
    data = cursor.fetchall()

    if data:
        column_names = [i[0] for i in cursor.description]  # type:ignore
        print_table(data, column_names)
    else:
        print("No reservations found.")


def print_table(data, headers):
    # Function to print a separator line
    def print_separator(widths):
        for width in widths:
            print("-" * (width + 2), end=" | ")
        print()

    # Determine the number of columns
    num_columns = len(headers)

    # Determine the maximum width for each column
    column_widths = [
        max(
            len(str(headers[i])) if headers else 0,
            max(len(str(row[i])) for row in data),
        )
        for i in range(num_columns)
    ]

    # Print headers
    for i in range(num_columns):
        print(str(headers[i]).ljust(column_widths[i] + 2), end=" | ")
    print()
    print_separator(column_widths)

    # Print data rows
    for row in data:
        for i in range(num_columns):
            print(str(row[i]).ljust(column_widths[i] + 2), end=" | ")
        print()
        print_separator(column_widths)


def main_menu():
    while True:
        menu_s_1()
        choice = int(input("Choose: "))

        if choice == MENU_ADD_RESERVATION:
            reserve()
        elif choice == MENU_DELETE_RESERVATION:
            delete_reservation()
        elif choice == MENU_DISPLAY_RESERVATIONS:
            display_reservations()
        elif choice == MENU_EXIT:
            exit_program()
        else:
            print("Invalid choice. Please select a valid option.")
