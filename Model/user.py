import datetime
import re
from flask_login import UserMixin
from bcrypt import hashpw

from Model.password import Password, NiveauMotDePasse


class EmailError(Exception):
    pass


class User(UserMixin):
    def __init__(self, email, username, user_id=0, birth_date=None, password=None, profile_photo="default.jpg",
                 user_type="user", status="inactive", verified=0, ):
        self.password_hash = None
        self._id = user_id
        self._email = email
        self._username = username
        self._birth_date = birth_date
        self._password = password if password is None else Password(password, NiveauMotDePasse.EXCELLENT)
        self._profile_photo = profile_photo
        self._user_type = user_type
        self._status = status
        self._verified = verified

    def __str__(self):
        return (f"User Information:\n"
                f"ID: {self.id}\n"
                f"Email: {self.email}\n"
                f"Username: {self.username}\n"
                f"Age: {self.age}\n"
                f"Birth Date: {self.birth_date.strftime('%Y-%m-%d')}\n"  # Conversion en str
                f"Password Hash: {self.password_hash}\n"
                f"Profile Photo: {self.profile_photo}\n"
                f"User Type: {self._user_type}\n"  
                f"Status: {self.status}\n"        
                f"Verified: {self.verified}")

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

    @email.setter
    def email(self, value):
        try:
            self._validate_email(value)
        except EmailError as e:
            print(f"Erreur de validation de l'email : {e}")
            return
        self._email = value
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = self._validate_username(value)

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if not isinstance(value, str):
            raise ValueError("user_type must be a string")
        if value not in ("user", "admin", "moderator"):
            raise ValueError("Invalid user_type. Must be one of: user, admin, moderator")
        self._role = value

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
    def _validate_email(email):
        if not isinstance(email, str):
            raise EmailError("Email must be a string")
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
            raise EmailError("Invalid email format")
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

    def verify_password(self, password):
        return hashpw(password.encode('utf-8'), self.password_hash.encode('utf-8')) == self.password_hash.encode(
            'utf-8')

    def is_admin(self):
        return self._user_type == 'admin'  # Utilisation de _user_type

    def is_moderator(self):
        return self._user_type == 'moderator'  # Utilisation de _user_type

    def can_edit_post(self):
        return self.is_admin() or self.is_moderator()  # Utilisation de is_admin() et is_moderator()


    def is_active(self):
        return self._status == 'active'

    def __repr__(self):
        return f"<User id={self.id}, email='{self.email}', username='{self.username}'>"
