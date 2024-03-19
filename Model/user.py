import datetime
import re
from flask_login import UserMixin
from Model.Email import Email, EmailError
from Model.password import Password, NiveauMotDePasse, PasswordError
from db_init import create_database_connection

"""Classe User
------------

La classe User représente un utilisateur dans le système. Elle hérite de la classe UserMixin de Flask-Login.

Attributs:
- _id: Identifiant de l'utilisateur (entier).
- _email: Adresse email de l'utilisateur (objet Email).
- _username: Nom d'utilisateur de l'utilisateur (chaîne de caractères).
- _birth_date: Date de naissance de l'utilisateur (objet datetime.date).
- _password: Mot de passe de l'utilisateur (objet Password).
- _profile_photo: Chemin vers la photo de profil de l'utilisateur (chaîne de caractères).
- _user_type: Type d'utilisateur (chaîne de caractères: 'user', 'admin', 'moderator').
- _status: Statut de l'utilisateur (chaîne de caractères: 'active', 'inactive', 'suspended').
- _verified: Indique si l'utilisateur est vérifié (booléen).

Méthodes:
1. __init__(self, email=None, username=None, user_id=0, birth_date=None, password=None, profile_photo="default.jpg",
            user_type="user", status="inactive", verified=False, mode=True)
    - Constructeur de la classe User.
    - Paramètres:
        - email: Adresse email de l'utilisateur (par défaut None).
        - username: Nom d'utilisateur de l'utilisateur (par défaut None).
        - user_id: Identifiant de l'utilisateur (par défaut 0).
        - birth_date: Date de naissance de l'utilisateur (par défaut None).
        - password: Mot de passe de l'utilisateur (par défaut None).
        - profile_photo: Chemin vers la photo de profil de l'utilisateur (par défaut "default.jpg").
        - user_type: Type d'utilisateur (par défaut "user").
        - status: Statut de l'utilisateur (par défaut "inactive").
        - verified: Indique si l'utilisateur est vérifié (par défaut False).
        - mode: Mode de sauvegarde du mot de passe dans la base de données (par défaut True).

2. __str__(self)
    - Retourne une représentation sous forme de chaîne de caractères des informations de l'utilisateur.

3. create(cls, email, username)
    - Méthode de classe pour créer un utilisateur.
    - Paramètres:
        - email: Adresse email de l'utilisateur.
        - username: Nom d'utilisateur de l'utilisateur.
    - Retourne une instance de la classe User.

4. save_to_database(self)
    - Enregistre l'utilisateur dans la base de données.

5. generate_and_set_password(self, niveau=NiveauMotDePasse.ACCEPTABLE)
    - Génère et définit un nouveau mot de passe pour l'utilisateur.

6. is_admin(self)
    - Vérifie si l'utilisateur est un administrateur.

7. is_moderator(self)
    - Vérifie si l'utilisateur est un modérateur.

8. can_edit_post(self)
    - Vérifie si l'utilisateur peut éditer un message.

9. is_active(self)
    - Vérifie si l'utilisateur est actif.

10. validate_data(self)
    - Valide les données de l'utilisateur.

11. __repr__(self)
    - Retourne une représentation sous forme de chaîne de caractères de l'utilisateur.

12. Les autres méthodes sont des getters et des setters pour les attributs de la classe User.
"""


class User(UserMixin):
    def __init__(self, email=None, username=None, user_id=0, birth_date=None, password=None, profile_photo="default.jpg",
                 user_type="user", status="inactive", verified=False, mode=True, user_valide=False):
        assert isinstance(email, (str, type(None))), "Email must be an instance of Email class or None"
        assert isinstance(username, (str, type(None))), "Username must be a string or None"
        assert isinstance(user_id, int), "User ID must be an integer"
        assert isinstance(birth_date, (datetime.date, type(None))), "Birth date must be a datetime.date object or None"

        self._id = user_id
        self._username = username
        self._email = Email(email) if isinstance(email, str) else email
        self._birth_date = birth_date
        self._password = Password(password, save_to_database=False if mode is False else True) if password is not None else None
        self._profile_photo = profile_photo
        self._user_type = user_type
        self._status = status
        self._verified = verified
        self._user_valide = self.validate_save_to_database()


    def __str__(self):
        return (f"User Information:\n"
                f"ID: {self.id}\n"
                f"Email: {self.email.value if self.email is not None else None }\n"
                f"Username: {self.username}\n"
                f"Age: {self.age if self.birth_date is not None else None}\n"
                f"Birth Date: {self.birth_date.strftime('%Y-%m-%d') if self.birth_date is not None else None}\n" # Conversion en str
                f"Password: {self.password if self.password is not None else None}\n"
                f"Profile Photo: {self.profile_photo}\n"
                f"User Type: {self.role}\n"
                f"Status: {self.status}\n"
               f"Verified: {True if self.verified else False}\n")

    @classmethod
    def create(cls, email, username):
        return cls(email, username)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer")
        self._id = value

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if value is None:
            self.password = None
        elif isinstance(value, Password):
            self.password = value
        elif isinstance(value, str):
            new_password = Password(value)
            self.password = new_password
        else:
            raise ValueError("Le mot de passe doit être une instance de la classe Password ou une chaîne de caractères")

    @email.setter
    def email(self, value):
        if isinstance(value, Email):
            self._email = value
        elif isinstance(value, str):
            try:
                self._email = Email(value)
            except EmailError as e:
                print(f"Error setting email: {e}")
        else:
            raise ValueError("Email must be an instance of Email class or a string")

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = self._validate_username(value)

    @property
    def role(self):
        return self._user_type

    @role.setter
    def role(self, value):
        if not isinstance(value, str):
            raise ValueError("user_type must be a string")
        if value not in ("user", "admin", "moderator"):
            raise ValueError("Invalid user_type. Must be one of: user, admin, moderator")
        self._user_type = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, str):
            raise ValueError("user_type must be a string")
        if value not in ("active", "inactive", "suspended"):
            raise ValueError("Invalid status. Must be one of: active, inactive, suspended")
        self._status = value

    @property
    def age(self):
        # Calculer l'âge à partir de la date de naissance
        today = datetime.date.today()
        age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = self.validate_date(value)

    @property
    def profile_photo(self):
        return self._profile_photo

    @profile_photo.setter
    def profile_photo(self, value):
        if not isinstance(value, str):
            raise ValueError("Profile photo must be a string")
        self._profile_photo = value

    @property
    def verified(self):
        return self._verified

    @verified.setter
    def verified(self, value):
        if isinstance(value, bool):
            self._verified = int(value)
        elif value in (0, 1):
            self._verified = value
        else:
            raise ValueError("Invalid value for verified. Must be a boolean or 0 or 1.")


    @property
    def user_valide(self):
        return self._user_valide

    @user_valide.setter
    def user_valide(self, value):
        self._user_valide = value

    @staticmethod
    def _validate_username(username):
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', username):
            raise ValueError("Invalid username format")
        return username

    @staticmethod
    def validate_date(date_string):
        if date_string is not None:
            if isinstance(date_string, datetime.date):
                # Pas besoin de conversion, date_string est déjà un objet date
                return date_string
            try:
                # Convertir la chaîne en objet date
                date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
                return date_obj
            except ValueError:
                raise ValueError("La date n'est pas valide.")
        else:
            return None

    def is_admin(self):
        return self.role == 'admin'  # Utilisation de _user_type

    def is_moderator(self):
        return self.role == 'moderator'  # Utilisation de _user_type

    def can_edit_post(self):
        return self.is_admin() or self.is_moderator()  # Utilisation de is_admin() et is_moderator()

    def is_active(self):
        return self.status == 'active'

    def generate_and_set_password(self, niveau=NiveauMotDePasse.ACCEPTABLE):

        # Vérification si le niveau est basique
        if niveau == NiveauMotDePasse.BASIQUE:
            raise PasswordError("Le niveau de sécurité 'Basique' n'est pas autorisé pour cette opération.")
        else:
            # Utilisation de la classe Password pour générer un mot de passe
            new_password = Password().generate_password(niveau)
            print(new_password)
            # Assignation du nouveau mot de passe à l'attribut password
            self.password = Password(new_password)

    def _validate_email(self, email):
        m1= Email(email)
        if not m1.valide:
         raise EmailError("fInvalid email: {e}")
        return m1

    def save_to_database(self):
        if not self.validate_save_to_database():
            return False

        existing_user = self.user_exists(create_database_connection(), username=self.username, email=self.email.value)
        if existing_user:
            return False

        connection = create_database_connection()
        cursor = connection.cursor()
        query = (
            "INSERT INTO user (email, username, birth_date, password_hash, profile_photo, user_type, status, verified)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        values = (
            self.email.value, self.username,
            datetime.date.today() if self.birth_date is None else self.birth_date,
            self.password.password, self.profile_photo,
            self.role, self.status, self.verified
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return True


    @staticmethod
    def get_user_by_username(connection, username):
        cursor = connection.cursor()
        query = "SELECT id, email, username, birth_date, password_hash, profile_photo, user_type, status, verified FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            id, email, username, birth_date, password_hash, profile_photo, user_type, status, verified = user_data
            return User(email=email, username=username, user_id=id, password=password_hash, birth_date=birth_date,
                        profile_photo=profile_photo, user_type=user_type, status=status, verified=verified, mode=False)
        return user_data

    @staticmethod
    def get_user_by_email(connection, email):
        cursor = connection.cursor()
        query = "SELECT id, email, username FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            id, email, username = user_data
            return User(email=email, username=username, user_id=id)
        return None

    @staticmethod
    def get_user_by_id(connection, user_id):
        cursor = connection.cursor()
        query = "SELECT id, email, username, age, profile_photo, user_type, status, verified FROM user WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            id, email, username, profile_photo, user_type, status, verified = user_data
            return User(user_id=id, email=email, username=username, profile_photo=profile_photo, user_type=user_type,
                        status=status, verified=verified)
        return None

    @staticmethod
    def update_date_connection(connection, user):
        cursor = connection.cursor()
        update_query = "UPDATE user SET Connected_at = NOW() WHERE username = %s"
        cursor.execute(update_query, (user.username,))
        connection.commit()
        cursor.close()
        print("date de connection mis à jour")

    def validate_save_to_database(self):
        # Vérifier si l'email est valide
        if self.email is None:
            raise ValueError("Email is required")
        if not isinstance(self.email, Email):
            raise ValueError("Email must be an instance of Email class")
        if not self.email.valide:
            raise ValueError("email is not an correct email")

        # Vérifier si le nom d'utilisateur est valide
        if not self.username:
            raise ValueError("Username is required")
        if len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long")

        # Vérifier si le mot de passe est valide
        if not self.password:
            raise ValueError("Password is required")
        if not isinstance(self.password, Password):
            raise ValueError("Password must be an instance of password class")
        if not self.password.valide:
            raise ValueError("Password is not strong enough")

        # Vérifier si la date de naissance est valide
        if not self.birth_date:
            raise ValueError("Birth date is required")
        if not isinstance(self.birth_date, datetime.date):
            raise ValueError("Birth date must be a datetime.date object")

        # Vérifier si le chemin de la photo de profil est valide
        if not isinstance(self.profile_photo, str) or self.profile_photo is None:
            raise ValueError("Profile photo must be a string")

        # Vérifier si le statut est valide
        if self.status not in ("active", "inactive", "suspended"):
            raise ValueError("Invalid status. Must be one of: active, inactive, suspended")

        # Vérifier si le type d'utilisateur est valide
        if self.role not in ("user", "admin", "moderator"):
            raise ValueError("Invalid user_type. Must be one of: user, admin, moderator")

        return True

    @staticmethod
    def user_exists(connection, username, email):
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM user WHERE username = %s OR email = %s"
        cursor.execute(query, (username, email))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0

    def __repr__(self):
        return f"<User id={self.id}, email='{self.email}', username='{self.username}'>"

