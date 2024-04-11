from cryptography.fernet import Fernet
import os.path
import cryptography  # Import the cryptography module

# Function to generate and write a new key to a file
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Check if the key file exists, if not, generate a new key
if not os.path.isfile("key.key"):
    write_key()

# Load the key
def load_key():
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key

# Get the master password from user input
master_pwd = input("Enter the master password: ")

# Combine master password with some input (seems like you wanted to concatenate two inputs?)
master_pwd += input("Enter master password again: ")

# Encode the master password
master_pwd = master_pwd.encode()

# Load the key
key = load_key()

# Combine key and master password
key += master_pwd

# Create a Fernet instance with the combined key
fer = Fernet(key)

# Function to view passwords
def view():
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                decrypted_password = fer.decrypt(passw.encode()).decode()
                print("User:", user, "| Password:", decrypted_password)
    except cryptography.fernet.InvalidToken:
        print("Error: Unable to decrypt password. The data may be corrupted or was encrypted with a different key.")

# Function to add passwords
def add():
    name = input('Enter account name: ')
    pwd = input("Enter password: ")
    # Encrypt password and write to file
    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + str(fer.encrypt(pwd.encode())).decode() + "\n")

# Main loop
while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
    if mode == "q":
        break
    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue
