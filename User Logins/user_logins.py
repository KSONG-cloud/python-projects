
USERNAMES_AND_PASSWORDS = {"robert":"password123", "james":"donotusethispassword"}

def is_valid_credentials(username, password):

    if username in USERNAMES_AND_PASSWORDS.keys() and USERNAMES_AND_PASSWORDS[username] == password:
        print("Darkest secret!")
    else:
        print("You shall NOT know!!! Get lost!")
    pass



if __name__ == "__main__":

    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    is_valid_credentials(username,password)