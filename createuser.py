"""Script for creating a new user account.

The script can be executed by typing in: `python createuser.py` (assuming your
current directory is `USC_Timeline`).

Upon executing the script, you will be prompted to enter a username, email and
password. Using this information a new User will be instantiated and stored in
the database.
"""

import sys
import json
from getpass import getpass
from usctimeline import create_app, db, bcrypt
from usctimeline.models import User

def create_user(username, email, password):
    new_user = User(
        username=username,
        email=email,
        password=bcrypt.generate_password_hash(password).decode('utf-8')
    )
    db.session.add(new_user)
    db.session.commit()

def main():
    username = input("Username: ")
    email = input("Email: ")
    password = getpass("Password: ")
    password_verification = getpass("Confirm Password: ")
    if password == password_verification:
        create_user(username, email, password)
    else:
        print("Error: Passwords did not match. Please try again.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()
