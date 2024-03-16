import os
import mysql.connector
from dotenv import load_dotenv
import random
from faker import Faker
from mysql.connector import Error

load_dotenv()
# Récupérez les informations de connexion depuis les variables d'environnement
host = os.environ.get('DB_HOST')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
database = os.environ.get('DB_NAME')


def create_database_connection():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

#function up
def up():
    try:
        # Connectez-vous à la base de données MySQL
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        cursor = connection.cursor()

        # Créez la base de données si elle n'existe pas déjà
        cursor.execute("CREATE DATABASE IF NOT EXISTS {} ".format(database))

        # Utilisez la base de données
        cursor.execute("USE {}".format(database))

        # Créez la table "user" si elle n'existe pas déjà
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(255) UNIQUE NOT NULL,
                birth_date DATE NOT NULL,
                age INT UNSIGNED,
                password_hash VARCHAR(255) NOT NULL,
                profile_photo VARCHAR(255),
                user_type ENUM('user', 'moderator', 'administrator') NOT NULL,
                status ENUM('active', 'inactive') NOT NULL,
                verified BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                verified_at TIMESTAMP,
                connected_at TIMESTAMP
            )
        """)
        # Créez le déclencheur BEFORE INSERT pour calculer l'âge lors de l'insertion
        cursor.execute("""
                   CREATE TRIGGER calculate_age_before_insert
                   BEFORE INSERT ON user
                   FOR EACH ROW
                   BEGIN
                       SET NEW.age = TIMESTAMPDIFF(YEAR, NEW.birth_date, CURDATE());
                   END
               """)

        # Créez le déclencheur BEFORE UPDATE pour empêcher la modification de la colonne "birth_date"
        cursor.execute("""
                   CREATE TRIGGER prevent_birth_date_update
                   BEFORE UPDATE ON user
                   FOR EACH ROW
                   BEGIN
                       IF OLD.birth_date <> NEW.birth_date THEN
                           SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La colonne "birth_date" ne peut pas être modifiée.';
                       END IF;
                   END
               """)

        # Insérez des données fictives dans la table "user"
        Seed(30)  # Vous pouvez appeler votre fonction de seeding ici

        print("La base de données et la table 'user' ont été créées avec succès.")

    except Error as e:
        print("Erreur lors de la création de la base de données et de la table:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def down():
    try:
        # Connectez-vous à la base de données MySQL
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        # Utilisez la base de données
        cursor.execute("USE {}".format(database))

        # Supprimez la table "user" si elle existe
        cursor.execute("DROP TABLE IF EXISTS user")

        print("La table 'user' a été supprimée avec succès.")

        cursor.execute("DROP DATABASE IF EXISTS {}".format(database))

        print("La base de données a été supprimée")

    except Error as e:
        print("Erreur lors de la suppression de la table 'user':", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Créez une base de données
def create_database(database_name):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS  {}".format(database))
    cursor.close()
    print("Base de données {} crée avec succès!".format(database))

# Créez les tables nécessaires
def create_tables():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = connection.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    birth_date DATE NOT NULL,
    age INT  INVISIBLE,
    password_hash VARCHAR(255) NOT NULL,
    profile_photo VARCHAR(255),
    user_type ENUM('user', 'moderator', 'administrator') NOT NULL,
    status ENUM('active', 'inactive') NOT NULL,
    verified BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP null INVISIBLE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP null INVISIBLE ON UPDATE CURRENT_TIMESTAMP ,
    verified_at TIMESTAMP null INVISIBLE,
    connected_at TIMESTAMP null INVISIBLE
);
      """)

    print("Table Users Created Successfully")
    cursor.close()


def Seed(nbre):
    # Connectez-vous à la base de données MySQL
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    # Créez une instance de Faker pour générer des données fictives
    faker = Faker()

    # Définissez les types d'utilisateurs possibles
    user_types = ['user', 'moderator', 'administrator']

    # Générez et insérez des données fictives pour la table "user"
    for _ in range(nbre):  # Créez 10 utilisateurs fictifs
        email = faker.email()
        username = faker.user_name()
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=90)
        age = 0
        password_hash = faker.password()
        profile_photo = faker.image_url()
        user_type = random.choice(user_types)
        status = random.choice(['active', 'inactive'])
        verified = faker.boolean()

        # Insérez l'utilisateur dans la table "user"
        query = """
        INSERT INTO user (email, username, birth_date, age, password_hash, profile_photo, user_type, status, verified)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (email, username, birth_date, age, password_hash, profile_photo, user_type, status, verified)
        cursor.execute(query, values)

    # Validez les changements et fermez la connexion
    connection.commit()
    cursor.close()
    connection.close()
    print("Les données fictives pour la table 'user' ont été insérées avec succès.")


def refresh():
    down()  # Supprimez la table "user"
    up()    # Recréez la base de données, la table "user" et insérez des données fictives


def delete_all_users():
    # Connectez-vous à la base de données MySQL
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    # Exécutez la commande pour supprimer toutes les données de la table "user"
    cursor.execute("DELETE FROM user")

    # Validez les changements et fermez la connexion
    connection.commit()
    cursor.close()
    connection.close()

    print("Toutes les données de la table 'user' ont été supprimées avec succès.")


def drop_database(database_name):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {}".format(database_name))
    cursor.close()
    connection.close()
    print("Base de données {} supprimée avec succès!".format(database_name))


if __name__ == "__main__":
    refresh()
