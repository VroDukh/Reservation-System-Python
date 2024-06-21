# Functionalities

# SEARCH,EDIT,EXIT, MISC

import pandas as pd
import mysql.connector as ms
import random as ran

# import Airline_Login as ALL

connection = ms.connect(
    host="127.0.0.1", user="root", password="852456", database="project"
)

cursor = connection.cursor()


def menu_s_1():
    print()
    print("1. Add Reservation")
    print("2. Delete Reservation")
    print("3. Display All Reservations")
    print("4. Exit")


def exit():
    connection.close()


def ticket_available(tik, pln):
    query = f"SELECT * FROM seats WHERE Ticket_No={tik} and Bus_No={pln}"
    cursor.execute(query)
    data = cursor.fetchall()
    if data == []:
        return False
        # Seat Empty
    else:
        return True
        # Seat Taken


def print_table(data, headers=None):
    if not data:
        print("No data to display.")
        return

    # Determine the number of columns
    num_columns = len(data[0])

    # Determine the maximum width for each column by considering header and data
    column_widths = [
        max(
            len(str(headers[i])) if headers else 0,
            max(len(str(row[i])) for row in data),
        )
        for i in range(num_columns)
    ]

    # Function to print a separator line
    def print_separator():
        for width in column_widths:
            print("-" * (width + 2), end=" | ")
        print()

    # Print headers
    if headers:
        for i in range(num_columns):
            print(str(headers[i]).ljust(column_widths[i] + 2), end=" | ")
        print()
        print_separator()

    # Print data rows
    for row in data:
        for i in range(num_columns):
            print(str(row[i]).ljust(column_widths[i] + 2), end=" | ")
        print()
        print_separator()


def display_current():
    query = f"SHOW COLUMNS FROM seats;"
    cursor.execute(query)
    columns = cursor.fetchall()
    column_names = [column[0] for column in columns]
    query = f"SELECT * from seats;"
    cursor.execute(query)
    data = cursor.fetchall()

    # Call print_table with the entire dataset and column names
    print_table(data, column_names)


def destinations():
    dest = ["Jaipur", "Mumbai"]
    for i in dest:
        print(i)
        print()


def pre_reserve():
    destinations()
    destination = input("Where to ?: ")
    tickets_pl = [destination]
    query = (
        f"SELECT Bus_No,Available_Seats FROM buses WHERE Destination='{destination}';"
    )
    cursor.execute(query)
    [(Bus_No, av_seats)] = cursor.fetchall()
    if av_seats == 0:
        print("No Seats Available")
        return 0
    query = f"SELECT Ticket_No,Bus_No FROM seats WHERE Bus_No={Bus_No};"
    cursor.execute(query)
    Taken_seats = cursor.fetchall()
    for i in Taken_seats:
        tickets_pl.append(i[0])  # type: ignore
    return [tickets_pl, Bus_No, av_seats]


def reserve():
    L1temp = pre_reserve()
    if L1temp == 0:
        return
    [tickets_pl, Bus_No, av_seats] = L1temp  # type:ignore
    name = input("Enter Name: ")
    values_to_include = list(set(range(1, av_seats + 1)) - set(tickets_pl))
    ticket_no = ran.choice(values_to_include)
    query = f"INSERT INTO seats VALUES({ticket_no},'{name}',{Bus_No});"
    query2 = f"UPDATE buses set Available_Seats = {av_seats-1} WHERE Bus_No = {Bus_No};"
    cursor.execute(query)
    cursor.execute(query2)
    connection.commit()
    print(ticket_no)
    return


def delete_resrvation():
    Ticket_No = input("Enter your Ticket_No: ")
    query = f"SELECT Bus_No from seats where Ticket_No={Ticket_No}"
    cursor.execute(query)
    Bus_No = cursor.fetchall()[0][0]
    query = f"DELETE from seats where Ticket_No={Ticket_No}"
    cursor.execute(query)
    query = f"SELECT Available_Seats from buses where Bus_No={Bus_No}"
    cursor.execute(query)
    new_seats = cursor.fetchall()[0][0] + 1  # type:ignore
    query = f"UPDATE buses set Available_Seats = {new_seats} WHERE Bus_No = {Bus_No}"
    cursor.execute(query)
    connection.commit()


def menu():
    while True:
        menu_s_1()
        ch = int(input("Choose: "))
        if ch == 1:
            reserve()
        elif ch == 2:
            delete_resrvation()
        elif ch == 3:
            display_current()
        elif ch == 4:
            exit()


menu()
