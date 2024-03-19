from bcrypt import hashpw, gensalt

from Model.Email import Email
from Model.password import Password
from Model.user import User
import datetime
import re

from db_init import create_database_connection

connection = create_database_connection()

"""Module: db_functions
---------------------
Provides functions for interacting with the database to manage user registration, retrieval, and updates.

Functions:
1. create_user(connection, user)
    - Inserts a new user into the database.
    - Parameters:
        - connection: Database connection object.
        - user: User object containing user data to be inserted.
    
2. get_user_by_email(connection, email)
    - Retrieves a user from the database by their email address.
    - Parameters:
        - connection: Database connection object.
        - email: Email address of the user to retrieve.
    - Returns:
        - User object if user is found, None otherwise.

3. get_user_by_username(connection, username)
    - Retrieves a user from the database by their username.
    - Parameters:
        - connection: Database connection object.
        - username: Username of the user to retrieve.
    - Returns:
        - User object if user is found, None otherwise.

4. get_user_by_id(connection, user_id)
    - Retrieves a user from the database by their user ID.
    - Parameters:
        - connection: Database connection object.
        - user_id: User ID of the user to retrieve.
    - Returns:
        - User object if user is found, None otherwise.

5. register_user(connection, email, username, birth_date, password)
    - Registers a new user in the database.
    - Parameters:
        - connection: Database connection object.
        - email: Email address of the user.
        - username: Username of the user.
        - birth_date: Date of birth of the user.
        - password: Password of the user.
    - Returns:
        - True if registration is successful, False if user already exists.

6. validate_user_data(email, username, birth_date, password_hash, age, user_type, status)
    - Validates user data before registration.
    - Parameters:
        - email: Email address of the user.
        - username: Username of the user.
        - birth_date: Date of birth of the user.
        - password_hash: Hashed password of the user.
        - age: Age of the user.
        - user_type: Type of user ('user', 'moderator', 'administrator').
        - status: Status of the user ('active', 'inactive').
    - Raises:
        - ValueError with appropriate message if validation fails.

7. update_date_connection(connection, user)
    - Updates the connection date of a user in the database.
    - Parameters:
        - connection: Database connection object.
        - user: User object to update connection date.
"""
def create_user(connection, user):
    cursor = connection.cursor()
    query = ("INSERT INTO user (email, username, birth_date, password_hash, profile_photo, user_type, status) VALUES ("
             "%s, %s, %s, %s, %s, %s, %s)")
    values = (
        user.email.email, user.username, user.birth_date, user.password.password, user.profile_photo, user.role, user.status)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

def get_user_by_email(connection, email):
    cursor = connection.cursor()
    query = "SELECT id, email, username FROM user WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        id, email, username = user_data
        return User(email=email, username=username,user_id=id)
    return None

def get_user_by_username(connection, username):
    cursor = connection.cursor()
    query = "SELECT id, email, username,birth_date, password_hash, profile_photo, user_type, status, verified FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        id, email, username,birth_date, password_hash ,profile_photo, user_type, status, verified = user_data
        return User(email=email, username=username, user_id=id, password=password_hash, birth_date=birth_date,
                    profile_photo=profile_photo, user_type=user_type, status=status, verified=verified, mode=False)
    return None

def get_user_by_id(connection, user_id):
    cursor = connection.cursor()
    query = "SELECT id, email, username, age, profile_photo, user_type, status, verified FROM user WHERE id = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        id, email, username, profile_photo, user_type, status, verified = user_data
        return User(user_id=id, email=email, username=username, profile_photo=profile_photo, user_type=user_type, status=status, verified=verified)
    return None

def register_user(connection, email, username, birth_date, password):
    if get_user_by_username(connection, username):
        return False  # L'utilisateur existe déjà

    user = User(email=email, username=username, birth_date=birth_date, password=Password(password))

    create_user(connection, user)
    return True


def validate_user_data(email, username, birth_date, password_hash, age, user_type, status):
    if not isinstance(birth_date, datetime.date):
        raise ValueError("birth_date doit être une date")
    if not isinstance(age, int):
        raise ValueError("age doit être un entier")
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("email doit être une adresse email valide")
    if len(username) < 3:
        raise ValueError("username doit avoir au moins 3 caractères")
    if user_type not in ('user', 'moderator', 'administrator'):
        raise ValueError("user_type doit être 'user', 'moderator' ou 'administrator'")
    if status not in ('active', 'inactive'):
        raise ValueError("status doit être 'active' ou 'inactive'")

def update_date_connection(connection, user):
    cursor = connection.cursor()
    update_query = "UPDATE user SET Connected_at = NOW() WHERE username = %s"
    cursor.execute(update_query, (user.username,))
    connection.commit()
    cursor.close()
    print("date de connection mis à jour")

