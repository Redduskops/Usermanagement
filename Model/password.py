import re
import random
import string
import bcrypt
from enum import Enum


class NiveauMotDePasse(Enum):
    BASIQUE = "Basique"
    ACCEPTABLE = "Acceptable"
    EXCELLENT = "Excellent"


class PasswordError(Exception):
    pass


class Password:
    def __init__(self, password=None, niveau=NiveauMotDePasse.ACCEPTABLE, save_to_database=True):
        self._password = None
        self._niveau = None
        self._valide = False
        self._erreur = ""
        self._encrypted = False  # Par défaut, le mot de passe n'est pas encore encrypté
        self._save_to_database = save_to_database  # Mode d'utilisation : True pour enregistrer dans la base de
        # données, False pour juste charger les données
        if password is not None:
            if isinstance(password, str):
                self.set_password(password)
            else:
                raise ValueError("Le mot de passe doit être une chaîne de caractères ou une valeur cryptée")
        else:
            self.generate_password(niveau)

    @property
    def password(self):
        return self._password

    @property
    def niveau(self):
        return self._niveau

    @property
    def valide(self):
        return self._valide

    @property
    def encrypted(self):
        return self._encrypted

    @property
    def save_to_database(self):
        return self._save_to_database

    @password.setter
    def password(self, value):
        if value is None:
            self._password = None
        elif isinstance(value, str):
            self._password = value
        else:
            raise ValueError("Le mot de passe doit être une instance de la classe str")

    @niveau.setter
    def niveau(self, value):
        if not isinstance(value, NiveauMotDePasse):
            raise ValueError("La valeur de niveau doit être une instance de NiveauMotDePasse")
        self._niveau = value

    @valide.setter
    def valide(self, value):
        if value not in [True, False]:
            raise ValueError("La valeur de l'attribut valide doit être True ou False")
        self._valide = value

    @encrypted.setter
    def encrypted(self, value):
        if value not in [True, False]:
            raise ValueError("La valeur de l'attribut encrypted doit être True ou False")
        self._encrypted = value

    @save_to_database.setter
    def save_to_database(self, value):
        if value not in [True, False]:
            raise ValueError("La valeur de l'attribut save_to_database doit être True ou False")
        self._save_to_database = value

    def __str__(self):
        if self.password:
            return f"{self.password}"
        else:
            return "Mot de passe non défini"

    # Autres méthodes de la classe Password...
    def generate_password(self, niveau=NiveauMotDePasse.ACCEPTABLE):
        # Caractères possibles pour le mot de passe
        characters = string.ascii_letters + string.digits + string.punctuation

        if niveau == NiveauMotDePasse.EXCELLENT:
            length = random.randint(14, 35)  # Longueur du mot de passe entre 14 et 35 caractères
        elif niveau == NiveauMotDePasse.ACCEPTABLE:
            length = random.randint(8, 14)  # Longueur du mot de passe entre 8 et 14 caractères
        else:
            length = random.randint(6, 7)  # Longueur du mot de passe entre 6 et 7 caractères pour le niveau Basique

        # Génération du mot de passe aléatoire
        while True:
            password = ''.join(random.choice(characters) for _ in range(length))
            # Vérification des critères du mot de passe
            if all(c in string.ascii_letters + string.digits + string.punctuation for c in password) \
                    and any(c in string.ascii_lowercase for c in password) \
                    and any(c in string.ascii_uppercase for c in password) \
                    and any(c in string.digits for c in password) \
                    and any(c in string.punctuation for c in password):
                if niveau == NiveauMotDePasse.EXCELLENT:
                    if self.has_similar_characters(password):
                        continue  # Re-générer le mot de passe s'il contient des caractères similaires consécutifs
                return password  # Retourne le mot de passe dès qu'il satisfait tous les critères

    def _validate_password(self, passw):
        self.niveau = NiveauMotDePasse.BASIQUE
        self.valide = False
        # Vérification de la présence de caractères majuscules, minuscules, chiffres et spéciaux
        if re.search(r'[A-Z]', passw) and re.search(r'[a-z]', passw) \
                and re.search(r'\d', passw) and re.search(r'[!@#$%^&*()-=_+]', passw):
            # Vérification de la longueur du mot de passe
            if 8 <= len(passw) <= 14:
                self.niveau = NiveauMotDePasse.ACCEPTABLE
                self.valide = True
                return True

            if len(passw) > 14:
                # Vérification de la présence de caractères consécutifs répétés
                has_repeated_chars = any(passw[i] == passw[i + 1] for i in range(len(passw) - 1))
                if not has_repeated_chars:
                    self.niveau = NiveauMotDePasse.EXCELLENT
                    self.valide = True
                    return True
                else:
                    self.niveau = NiveauMotDePasse.ACCEPTABLE
                    self.valide = True
                    return True
        return False



    def set_password(self, new_password):
        if isinstance(new_password, str):
            a= False
            self._validate_password(new_password)
            if self.valide:
                a=True
                if self.save_to_database:
                    self.password = self.hash_password(new_password)
                    self.encrypted = True
                else:
                    self.password = new_password
                    self.encrypted = True
            else:
                self.password = new_password
                self.encrypted = False
        else:
            raise ValueError("Le mot de passe doit être une chaîne de caractères ou une valeur cryptée")
        return a

    def check_password_strength(self, password):
        self._validate_password(password)
        return self.niveau, self.valide, password

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_passwordo = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        return hashed_passwordo

    @staticmethod
    def has_similar_characters(password):
        for i in range(len(password) - 1):
            if password[i] == password[i + 1]:
                return True
        return False

    @staticmethod
    def verify_password(plain_password, self):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password.encode('utf-8'))

    # Ajout d'une méthode pour vérifier si un mot de passe est basique
    def is_basic_password(self):
        return self._niveau == NiveauMotDePasse.BASIQUE

    @staticmethod
    def is_encrypted_password(password):
        return isinstance(password, bytes)
