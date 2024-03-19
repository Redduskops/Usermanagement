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
                 user_type="user", status="inactive", verified=False, mode=True):
        self._id = user_id
        self._email = self._validate_email(email)
        self._username = username
        self._birth_date = birth_date
        self.password = Password(password, save_to_database=False if mode is False else True) if password is not None else None
        self._profile_photo = profile_photo
        self._user_type = user_type
        self._status = status
        self._verified = verified

    def __str__(self):
        return (f"User Information:\n"
                f"ID: {self.id}\n"
                f"Email: {self.email.value}\n"
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
            self._password = None
        elif isinstance(value, Password):
            self._password = value
        elif isinstance(value, str):
            new_password = Password(value)
            if new_password.niveau == NiveauMotDePasse.BASIQUE:
                raise ValueError("Le niveau de sécurité du mot de passe est trop bas.")
            self._password = new_password
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
        return self._user_type == 'admin'  # Utilisation de _user_type

    def is_moderator(self):
        return self._user_type == 'moderator'  # Utilisation de _user_type

    def can_edit_post(self):
        return self.is_admin() or self.is_moderator()  # Utilisation de is_admin() et is_moderator()

    def is_active(self):
        return self._status == 'active'

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
        if self.email is None or self.username is None:
            raise ValueError("User must have an email and a username to be saved to the database")

        # Valider les données avant l'insertion dans la base de données
        if not self.validate_data:
            return False  # La validation a échoué, retourner False

        # Vérifier si un utilisateur avec le même nom d'utilisateur existe déjà
        existing_user = User.get_user_by_username(create_database_connection(), self.username)
        if existing_user:
            return False

        # Vérifier si un utilisateur avec le même email existe déjà
        existing_user = User.get_user_by_email(create_database_connection(), self.email.value)
        if existing_user:
            return False

        # Générer un mot de passe aléatoire si aucun n'a été fourni
        if self.password is None:
            password = Password().generate_password()
        else:
            password = self.password

        # Insertion des données dans la base de données
        connection = create_database_connection()
        cursor = connection.cursor()
        query = (
            "INSERT INTO user (email, username, birth_date, password_hash, profile_photo, user_type, status, verified)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        values = (
            self.email.value, self.username,
            datetime.date.today() if self.birth_date is None else self.birth_date,
            password.password, self.profile_photo,
            self.role, self.status, self.verified
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return True  # Succès de l'insertion

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

    @property
    def validate_data(self):
        if not self.email :
            return False
        if not self.username:
            return False
        if not self.password:
            return False
        if not self.birth_date:
            return False
        if not isinstance(self.email, Email):
            return False

        if len(self.username) < 3:
            return False

        if not isinstance(self.birth_date, datetime.date):
            return False

        if self.password and not isinstance(self.password, Password):
            return False
        if not isinstance(self.profile_photo, str) or self.profile_photo is None:
            return False
        if not isinstance(self.verified, bool):
            return False
        if self.role not in ("user", "admin", "moderator"):
            return False
        if self.status not in ("active", "inactive", "suspended"):
            return False

        # Si toutes les validations réussissent, retournez True
        return True
    def __repr__(self):
        return f"<User id={self.id}, email='{self.email}', username='{self.username}'>"
