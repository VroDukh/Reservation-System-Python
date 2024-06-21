import random
import mysql.connector

# Define the list of possible Bus_No values
bus_nos = [3344, 5563, 6645, 7725, 8869]

# Create lists of first names and surnames separately
original_first_names = [
    "Amit",
    "Sneha",
    "Rajesh",
    "Sangeeta",
    "Manoj",
    "Priya",
    "Rahul",
    "Pooja",
    "Vikram",
    "Neha",
    "Anita",
    "Deepak",
    "Sunita",
    "Alok",
    "Nidhi",
    "Sanjay",
    "Rita",
    "Suresh",
    "Mita",
    "Raj",
    # Add more first names as needed
]

original_surnames = [
    "Sharma",
    "Verma",
    "Patel",
    "Singh",
    "Kumar",
    "Gupta",
    "Mishra",
    "Joshi",
    "Pandey",
    "Chauhan",
    "Agarwal",
    "Verma",
    "Yadav",
    "Gandhi",
    "Mehra",
    "Verma",
    "Kaur",
    "Malhotra",
    "Choudhary",
    "Mehta",
    # Add more surnames as needed
]

# Create copies of the original lists to avoid modifying them
first_names = list(original_first_names)
surnames = list(original_surnames)

# Create a list to store used name combinations
used_name_combinations = set()


# Define a function to generate a random Indian name
def generate_name():
    if not first_names:
        first_names.extend(original_first_names)  # Reset the first names list
        random.shuffle(first_names)
    if not surnames:
        surnames.extend(original_surnames)  # Reset the surnames list
        random.shuffle(surnames)

    while True:
        # Randomly pick a first name and a surname
        first_name = first_names.pop()
        surname = surnames.pop()
        name = f"{first_name} {surname}"

        # Check if the name combination has been used before
        if name not in used_name_combinations:
            used_name_combinations.add(name)
            return name


# Establish a connection to your MySQL database
connection = mysql.connector.connect(
    host="127.0.1.1", user="root", password="852456", database="project"
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Generate and insert random data into the table
generated_ticket_numbers = set()  # Keep track of generated ticket numbers
for _ in range(50):  # You can change the number of rows you want to insert
    while True:
        ticket_no = random.randint(100, 999)  # Generate a 3-digit random ticket number
        if ticket_no not in generated_ticket_numbers:
            generated_ticket_numbers.add(ticket_no)
            break
    name = generate_name()
    bus_no = random.choice(bus_nos)
    seat_type = random.choice(["Regular", "Premium"])

    # Insert the data into the table
    insert_query = f"INSERT INTO seats (Ticket_No, Name, Bus_No, Seat_Type) VALUES ({ticket_no}, '{name}', {bus_no}, '{seat_type}')"
    cursor.execute(insert_query)
    connection.commit()

# Close the database connection
connection.close()
