import hashlib
import json

# USERNAMES_AND_PASSWORDS = {"robert":"ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f", 
#                            "james":"b0c13ca9c1f061dbfb4f816197822d8725438049c557a54cbdb5709512af0113"}

# credentials_file = open("User Logins/usernames_passwords.json", 'r')

# credentials = json.load(credentials_file)

def load_credentials(file_path):
    credentials_file = open(file_path, 'r')

    credentials_list = json.load(credentials_file)

    credentials = {}

    for user in credentials_list:
        credentials[user["username"]] = user["password_hash"]

    return credentials


def is_valid_credentials(username, password, credentials):
    hash_password_sha256 = hashlib.sha256()
    hash_password_sha256.update(password.encode("utf-8"))
    if username in credentials.keys() and credentials[username] == hash_password_sha256.hexdigest():
        print("Darkest secret!")
    else:
        print("You shall NOT know!!! Get lost!")
    pass



if __name__ == "__main__":

    # username = input("Please enter your username: ")
    # password = input("Please enter your password: ")
    print(load_credentials("User Logins/usernames_passwords.json"))

    # is_valid_credentials(username,password)