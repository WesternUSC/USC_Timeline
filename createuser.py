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
    """Creates a new user account.

    Takes in a given username, email and password. Password is hashed. Creates
    a new instance of User and stores in database.

    Args:
        username: Username
        email: Email
        password: Password

    Returns:
        None
    """
    new_user = User(
        username=username,
        email=email,
        password=bcrypt.generate_password_hash(password).decode('utf-8')
    )
    db.session.add(new_user)
    db.session.commit()


def main():
    """Prompts user for username, email, password, then calls create_user().

    Returns:
        None
    """
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
