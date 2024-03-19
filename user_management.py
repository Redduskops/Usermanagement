# user_management.py

from bcrypt import hashpw, gensalt
from Model.user import User
import datetime
import re

from db_init import create_database_connection

connection = create_database_connection()

def create_user(connection, user):
    cursor = connection.cursor()
    query = ("INSERT INTO user (email, username, birth_date, password_hash, profile_photo, user_type, status) VALUES ("
             "%s, %s, %s, %s, %s, %s, %s)")
    values = (
        user.email.value, user.username, user.birth_date, user.password.password, user.profile_photo, user.role, user.status)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def get_user_by_email(connexion, email):
    cursor = connexion.cursor()
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
    query = "SELECT id, email, username,password_hash,age, profile_photo, user_type, status, verified FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        id, email, username,password_hash, profile_photo, user_type, status, verified = user_data
        return User(email=email, username=username, user_id=id, password_hash=password_hash,
                    profile_photo=profile_photo, user_type=user_type, status=status, verified=verified)
    return None


def get_user_by_id(connection, user_id):
    cursor = connection.cursor()
    query = "SELECT id, email, username, age, profile_photo, user_type, status, verified FROM user WHERE id = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    print(user_data)  # Imprimer les données récupérées pour le débogage
    if user_data:
        id, email, username, profile_photo, user_type, status, verified = user_data
        return User(user_id=id, email=email, username=username, profile_photo=profile_photo, user_type=user_type, status=status, verified=verified)
    return None




# Autres fonctions pour récupérer, mettre à jour et supprimer des utilisateurs

def register_user(connection, email, username, birth_date, password):
    # Vérifiez si l'utilisateur existe déjà
    if get_user_by_username(connection, username):
        return False  # L'utilisateur existe déjà

    # Hash du mot de passe

    # Créer un objet User
    user = User(email = email, username=username, birth_date=birth_date, password_hash=password)

    # Ajouter l'utilisateur à la base de données
    create_user(connection, user)
    return True  # L'inscription est réussie


def verify_password(user, password):
    hashed_password = user.password_hash.encode('utf-8')
    provided_password = password.encode('utf-8')
    return hashpw(provided_password, hashed_password) == hashed_password


def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[a-zA-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
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
    if not validate_password(password_hash):
        raise ValueError("Le mot de passe ne respecte pas les critères de complexité")
    if user_type not in ('user', 'moderator', 'administrator'):
        raise ValueError("user_type doit être 'user', 'moderator' ou 'administrator'")
    if status not in ('active', 'inactive'):
        raise ValueError("status doit être 'active' ou 'inactive'")


def decode_password(password):
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def update_date_connection(connection, user):
        cursor = connection.cursor()
        update_query = "UPDATE user SET Connected_at = NOW() WHERE username = %s"
        cursor.execute(update_query, (user.username,))
        connection.commit()
        cursor.close()
        print("date de connection mis à jour")

