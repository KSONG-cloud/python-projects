import os
import sqlite3


# Constants
COMMA               = ","
LEFT_BRACKET        = "("
RIGHT_BRACKET       = ")"
SPACE               = " "


# Creates database and return it
def create_or_connect_database(name):

    if name[-3:] != ".db":
        print("The database name does not end with \'.db\', so it is not valid.")


    # Database is already created
    if os.path.exists(name):
        print(f"Database {name} was already created.")

        database = sqlite3.connect(name)
        cur = database.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

        table_list = res.fetchall()



        print("Would you like to delete and create a new database?")

        
        valid = False

        while not valid:
            response = input("Enter \"Yes\" or \"No\". \n")

            if response == "Yes":
                os.remove(name)
                valid = True
            elif response == "No":
                valid = True
            else:
                print("Response is not valid. Please enter \"Yes\" or \"No\".")

    database = sqlite3.connect(name)

    return database




def create_table(database,  name, columns):

    # Create cursor to interact with database
    cur = database.cursor()

    sql_command = "CREATE TABLE" + SPACE + name + SPACE + LEFT_BRACKET

    for i in range(len(columns)):
        sql_command += columns[i] 
        if i != len(columns) - 1:
            sql_command += COMMA

    sql_command += RIGHT_BRACKET

    cur.execute(sql_command)
    return



if __name__ == "__main__":
    database = create_or_connect_database("./ppab6.db")


    # create_table(database, "users", ["username VARCHAR", "password_hash VARCHAR"])
    # create_table(database, "apple", ["username VARCHAR", "password_hash VARCHAR"])
    # create_table(database, "pear", ["username VARCHAR", "password_hash VARCHAR"])

    cur = database.cursor()


    # res = cur.execute("SELECT * FROM sqlite_master.COLUMNS")
    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(res)
    # print(res.fetchone())
    print(res.fetchall())