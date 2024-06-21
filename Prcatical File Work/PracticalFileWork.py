# S.No 1
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def print_factorial_series(n, m):
    for i in range(n, m + 1):
        print(f"{i}! = {factorial(i)}")


print_factorial_series(1, 5)


# S.No 2
def login(passwd, user="Admin"):
    if user == "Admin" and passwd == 123:
        print("Login Successful.")
        return True
    else:
        print("Incorrect Login Info")
        return False


if login(user=input("Enter User: "), passwd=int(input("Enter Passwd: "))) != True:
    login(passwd=int(input("Enter Passwd for Default User: ")))


# S.No 3
def product(*args):
    result = 1
    for arg in args:
        result *= arg
    return result


def power(*args):
    result = []
    for arg in args:
        result.append(arg**2)
    return result


numbers = range(1, 11)
print(f"Product of the first 10 numbers: {product(*numbers)}")
print(f"Power of the first 10 numbers: {power(*numbers)}")

# S.No 4
with open("intro.txt", "w") as f:
    text = input("Please enter a line of text: ")
    f.write(text + "\n")

# S.No 5
total_lines = 0
abc_lines = 0

with open("MyFile.txt", "r") as f:
    for line in f:
        total_lines += 1
        if line[0] in ["A", "B", "C"]:
            abc_lines += 1

print(f"Total number of lines: {total_lines}")
print(f"Number of lines starting with A, B, or C: {abc_lines}")

# S.No 6
with open("intro.txt", "r") as f:
    text = f.read()
text = text.replace(" ", "-")
with open("intro.txt", "w") as f:
    f.write(text)
    print("Done!")

# S.No 7
with open("MyFile.txt", "r") as f:
    # Print the initial position
    initial_position = f.tell()
    print(f"Initial position: {initial_position}")
    # Move the cursor to 4th position
    f.seek(4)
    # Display next 5 characters
    print(f"Next 5 characters: {f.read(5)}")
    # Move the cursor to the next 10 characters
    f.seek(10)
    # Print the current cursor position
    current_position = f.tell()
    print(f"Current position: {current_position}")
    # Print next 10 characters from the current cursor position
    print(f"Next 10 characters: {f.read(10)}")

# S.No 8
import pickle

# Customer data
customers = {
    1: {"name": "Alice", "city": "New York"},
    2: {"name": "Bob", "city": "Los Angeles"},
    3: {"name": "Charlie", "city": "Chicago"},
}
# Write customer data to binary file
with open("cust.dat", "wb") as f:
    pickle.dump(customers, f)
# Read customer data from binary file
with open("cust.dat", "rb") as f:
    customers = pickle.load(f)
# Print customer data
for id, data in customers.items():
    print(f"ID: {id}, Name: {data['name']}, City: {data['city']}")


##To Make Data##
import pickle

students = {}
for i in range(5):
    students[i] = {
        "name": input("Enter Name: "),
        "age": int(input("Enter Age")),
        "marks": int(input("Enter Marks: ")),
    }
print(students)
with open("student.dat", "wb") as f:
    pickle.dump(students, f)


# S.No 9
import pickle


# Function to update a student record by roll number
def update_student(rollno, name, age, marks):
    # Load student data from file
    with open("student.dat", "rb") as f:
        students = pickle.load(f)
    # Update student record
    if rollno in students:
        students[rollno] = {"name": name, "age": age, "marks": marks}
        # Save updated student data to file
        with open("student.dat", "wb") as f:
            pickle.dump(students, f)
        # Display updated record
        print(
            f"Updated record: Roll No: {rollno}, Name: {name}, Age: {age}, Marks: {marks}"
        )
    else:
        print(f"No record found for roll number {rollno}")


# Example: Update the record for roll number 1
update_student(1, "Alice", 20, 95)

# S.No 10
import pickle

# Student data
students = [
    {"name": "Alice", "marks": 90},
    {"name": "Bob", "marks": 95},
    {"name": "Charlie", "marks": 100},
]
# Write student data to binary file
with open("marks.dat", "wb") as f:
    pickle.dump(students, f)
# Read student data from binary file
with open("marks.dat", "rb") as f:
    students = pickle.load(f)
# Display records of students who scored more than 95 marks
for student in students:
    if student["marks"] > 95:
        print(f"Name: {student['name']}, Marks: {student['marks']}")

# S.No 11
import csv

with open("top5.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(", ".join(row))

# S.No 12
import csv

with open("top5.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the first row (header)
    for row in reader:
        print("\t".join(row))

# S.No 13
import csv

with open("students.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the first row (header)
    for row in reader:
        print("\t".join(row))


# S.No 14
class EmployeeStack:
    def __init__(self):
        self.stack = []

    def push(self, empno, name):
        self.stack.append((empno, name))

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            print("Stack is empty")

    def is_empty(self):
        return len(self.stack) == 0

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            print("Stack is empty")

    def display(self):
        for emp in self.stack:
            print(f"EmpNo: {emp[0]}, Name: {emp[1]}")


# Example usage
emp_stack = EmployeeStack()
print("PUSH")
emp_stack.push(1, "Alice")
emp_stack.push(2, "Bob")
emp_stack.display()
print("POP")
emp_stack.pop()
emp_stack.display()


# S.No 15
def is_palindrome(s):
    stack = []
    for char in s:
        stack.append(char)
    for char in s:
        if char != stack.pop():
            return False
    return True


# Example usage
print(is_palindrome("racecar"))  # True
print(is_palindrome("hello"))  # False


# S.No 21
import mysql.connector

conn = mysql.connector.connect(user="root", password="852456", host="127.0.0.1")
cursor = conn.cursor()
cursor.execute("CREATE DATABASE school")
cursor.execute("USE school")
cursor.execute(
    """
    CREATE TABLE students (
        ROLLNO INT,
        NAME VARCHAR(10),
        MARKS FLOAT,
        GRADE VARCHAR(10)
    )
"""
)
cursor.execute("INSERT INTO students VALUES (1, 'Alice', 99, 'A+')")
cursor.execute("INSERT INTO students VALUES (2, 'Bob', 82, 'B+')")
conn.commit()
cursor.execute("SELECT * FROM students")
for row in cursor:
    print(row)
cursor.close()
conn.close()

# S.No 22
# NO CLUE

# S.No 23
import mysql.connector

conn = mysql.connector.connect(
    user="root", password="852456", host="127.0.0.1", database="shop"
)
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS customer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255)
    )
"""
)


def display_menu1():
    print(
        """
        Menu:
        1. Add customer details
        2. Update customer details
        3. Delete customer details
        4. Display all customer details
        5. Exit
    """
    )


def add_customer1():
    name = input("Enter customer name: ")
    address = input("Enter customer address: ")
    cursor.execute(
        "INSERT INTO customer (name, address) VALUES (%s, %s)", (name, address)
    )
    conn.commit()
    print("Customer added successfully!")


def update_customer1():
    id = int(input("Enter customer ID: "))
    name = input("Enter new customer name: ")
    address = input("Enter new customer address: ")
    cursor.execute(
        "UPDATE customer SET name=%s, address=%s WHERE id=%s", (name, address, id)
    )
    conn.commit()
    print("Customer updated successfully!")


def delete_customer1():
    id = int(input("Enter customer ID: "))
    cursor.execute("DELETE FROM customer WHERE id=%s", (id,))
    conn.commit()
    print("Customer deleted successfully!")


def display_customers1():
    cursor.execute("SELECT * FROM customer")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Address: {row[2]}")


while True:
    display_menu1()
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add_customer1()
    elif choice == 2:
        update_customer1()
    elif choice == 3:
        delete_customer1()
    elif choice == 4:
        display_customers1()
    elif choice == 5:
        break

cursor.close()
conn.close()

# S.No 24
import mysql.connector

conn = mysql.connector.connect(
    user="root", password="852456", host="127.0.0.1", database="shop_2"
)
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS customer2 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        city VARCHAR(255),
        bill INT,
        category VARCHAR(255)
    )"""
)


def display_menu():
    print(
        """
        Menu:
        1. Add customer details
        2. Update customer details
        3. Delete customer details
        4. Display all customer details
        5. Exit
    """
    )


def display_sub_menu():
    print(
        """
        Display Menu:
        1.  Display customers
        2.  Display customer details by city
        3.  Display customer details by bill amount
        4.  Display customer details by name
        5.  Display customer details by category
        6.  Exit
        """
    )


def add_customer():
    name = input("Enter customer name: ")
    city = input("Enter customer city: ")
    bill = int(input("Enter custromer bill: "))
    category = input("Enter customer category: ")
    cursor.execute(
        f"INSERT INTO customer2 (name, city, bill, category) VALUES ('{name}','{city}',{bill},'{category}')"
    )
    conn.commit()
    print("Customer added successfully!")


def update_customer():
    id = int(input("Enter customer ID: "))
    name = input("Enter new customer name: ")
    city = input("Enter customer city: ")
    bill = int(input("Enter custromer bill: "))
    category = input("Enter customer category: ")
    cursor.execute(
        f"UPDATE customer2 SET name='{name}', city='{city}', bill={bill}, category='{category}' WHERE id={id}"
    )
    conn.commit()
    print("Customer updated successfully!")


def delete_customer():
    id = int(input("Enter customer ID: "))
    cursor.execute("DELETE FROM customer2 WHERE id=%s", (id,))
    conn.commit()
    print("Customer deleted successfully!")


def display_customers(order):
    cursor.execute(f"SELECT * FROM customer2 order by id {order}")
    rows = cursor.fetchall()
    for row in rows:
        print(
            f"ID: {row[0]}, Name: {row[1]}, City: {row[2]}, Bill: {row[3]}, Category: {row[4]}"
        )


def display_customer_city(order):
    cursor.execute(f"SELECT * FROM customer2 order by city {order}")
    rows = cursor.fetchall()
    for row in rows:
        print(
            f"ID: {row[0]}, Name: {row[1]}, City: {row[2]}, Bill: {row[3]}, Category: {row[4]}"
        )


def display_customer_name(order):
    cursor.execute(f"SELECT * FROM customer2 order by name {order}")
    rows = cursor.fetchall()
    for row in rows:
        print(
            f"ID: {row[0]}, Name: {row[1]}, City: {row[2]}, Bill: {row[3]}, Category: {row[4]}"
        )


def display_customer_bill(order):
    cursor.execute(f"SELECT * FROM customer2 order by bill {order}")
    rows = cursor.fetchall()
    for row in rows:
        print(
            f"ID: {row[0]}, Name: {row[1]}, City: {row[2]}, Bill: {row[3]}, Category: {row[4]}"
        )


def display_customer_category(order):
    cursor.execute(f"SELECT * FROM customer2 order by category {order}")
    rows = cursor.fetchall()
    for row in rows:
        print(
            f"ID: {row[0]}, Name: {row[1]}, City: {row[2]}, Bill: {row[3]}, Category: {row[4]}"
        )


while True:
    display_menu()
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add_customer()
    elif choice == 2:
        update_customer()
    elif choice == 3:
        delete_customer()
    elif choice == 4:
        while True:
            display_sub_menu()
            choice = int(input("Enter your choice: "))
            order_1 = int(input("1.Aesc \n2.Desc \nChoose: "))
            if order_1 == 1:
                order = "Asc"
            elif order_1 == 2:
                order = "Desc"
            else:
                print("Invalid Input")
            if choice == 1:
                display_customers(order)
            elif choice == 2:
                display_customer_city(order)
            elif choice == 3:
                display_customer_bill(order)
            elif choice == 4:
                display_customer_name(order)
            elif choice == 5:
                display_customer_category(order)
            elif choice == 6:
                break
    elif choice == 5:
        break

cursor.close()
conn.close()


# Sno 22
import mysql.connector as ms

cn = ms.connect(host="localhost", user="root", passwd="852456", database="school")
cr = cn.cursor()


def insert_rec():
    try:
        while True:
            rn = int(input("Enter roll number:"))
            sname = input("Enter name:")
            marks = float(input("Enter marks:"))
            gr = input("Enter grade:")
            cr.execute(
                "insert into students values({},'{}',{},'{}')".format(
                    rn, sname, marks, gr
                )
            )
            cn.commit()
            ch = input("Want more records? Press (N/n) to stop entry:")
            if ch in "Nn":
                break
    except Exception as e:
        print("Error", e)


def update_rec():
    try:
        rn = int(input("Enter rollno to update:"))
        marks = float(input("Enter new marks:"))
        gr = input("Enter Grade:")
        cr.execute(
            "update students set marks={},grade='{}' where rollno={}".format(
                marks, gr, rn
            )
        )
        cn.commit()
    except Exception as e:
        print("Error", e)


def delete_rec():
    try:
        rn = int(input("Enter rollno to delete:"))
        cr.execute("delete from students where rollno={}".format(rn))
        cn.commit()
    except Exception as e:
        print("Error", e)


def view_rec():
    try:
        cr.execute("select * from students")
        data = cr.fetchall()
        for i in data:
            print(i)
    except Exception as e:
        print("Error", e)


while True:
    print(
        """
        MENU:
        1. Insert Record
        2. Update Record 
        3. Delete Record
        4. Display Record 
        5. Exit
        """
    )
    ch = int(input("Enter your choice<1-4>="))
    if ch == 1:
        insert_rec()
    elif ch == 2:
        update_rec()
    elif ch == 3:
        delete_rec()
    elif ch == 4:
        view_rec()
    elif ch == 5:
        break
    else:
        print("Wrong option selected")
