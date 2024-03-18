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
        self._password_hash = None
        self._niveau = None
        self._valide = False
        self._encrypted = False  # Par défaut, le mot de passe n'est pas encore encrypté
        self._save_to_database = save_to_database  # Mode d'utilisation : True pour enregistrer dans la base de données, False pour juste charger les données
        if password is not None:
            self.set_password(password)
        else:
            self.generate_password(niveau)

    @property
    def password_hash(self):
        return self._password_hash

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

    @password_hash.setter
    def password_hash(self, value):
        if not isinstance(value, str):
            raise ValueError("Le mot de passe doit être une chaîne de caractères")
        self._validate_password(value)
        self._password = value

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
        if self.password_hash:
            return f"Mot de passe chiffré : {self.password_hash}"
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
                return password, niveau, length  # Retourne le mot de passe dès qu'il satisfait tous les critères

    def _validate_password(self, password):
        # Vérification de la présence de caractères majuscules, minuscules, chiffres et spéciaux
        if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) \
                and re.search(r'\d', password) and re.search(r'[!@#$%^&*()-=_+]', password):
            # Vérification de la longueur du mot de passe
            if 8 <= len(password) <= 14:
                self._niveau = NiveauMotDePasse.ACCEPTABLE
                self._valide = True
                return True

            if len(password) > 14:
                # Vérification de la présence de caractères consécutifs répétés
                has_repeated_chars = any(password[i] == password[i + 1] for i in range(len(password) - 1))
                if not has_repeated_chars:
                    self._niveau = NiveauMotDePasse.EXCELLENT
                    self._valide = True
                    return True
                else:
                    self._niveau = NiveauMotDePasse.ACCEPTABLE
                    self._valide = True
                    return True
        return False

    def set_password(self, new_password):
        # Vérification de la validité du nouveau mot de passe
        self._validate_password(new_password)

        # Si le nouveau mot de passe est valide
        if self._valide:
            if self._save_to_database:
                self._password_hash = self.hash_password(new_password)
                self._encrypted = True
            else:
                self._password_hash = new_password
                self._encrypted = False
        else:
            raise PasswordError("Le nouveau mot de passe n'est pas valide")

    def check_password_strength(self, password):
        self._validate_password(password)
        return self._niveau, self._valide, password
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_passwordo = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_passwordo

    @staticmethod
    def has_similar_characters(password):
        for i in range(len(password) - 1):
            if password[i] == password[i + 1]:
                return True
        return False

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

