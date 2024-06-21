import mysql.connector as ms
import random as ran

connection = ms.connect(
    host="127.0.0.1", user="root", password="srlab123", database="project"
)

cursor = connection.cursor()


def user_create():
    while True:
        user = input("Enter Username: ")
        psswd = input("Enter New Password: ")
        psswd1 = input("Confirm Password: ")
        if psswd1 == psswd:
            print("New User Created Successfully")
            return [user, psswd]
        else:
            print("Password Doesn't Match")
            print("Please Try Again")


def user_ids():
    query = f"SELECT UserId from users;"
    cursor.execute(query)
    taken = cursor.fetchall()
    while True:
        user_id = ran.randint(1, 1000)
        reset = True
        for i in taken:
            if user_id != i:
                reset = True
            else:
                reset = False
        if reset == True:
            break
    return user_id


def user_save():
    user, psswd = user_create()
    user_id = user_ids()
    query = f"INSERT INTO users VALUES({user_id},'{user}','{psswd}');"
    cursor.execute(query)
    connection.commit()


user_save()
