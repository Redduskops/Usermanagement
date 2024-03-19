import unittest
from datetime import datetime
from Model.user import User, EmailError, NiveauMotDePasse, PasswordError

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(email="test@example.com", username="testuser", birth_date=datetime(1990, 1, 1))

    def test_user_creation(self):
        self.assertEqual(self.user.email.value, "test@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.birth_date, datetime(1990, 1, 1))
        self.assertIsNone(self.user.password)

    def test_user_creation_with_invalid_email(self):
        with self.assertRaises(EmailError):
            User(email="invalid_email", username="testuser", birth_date=datetime(1990, 1, 1))

    def test_set_email(self):
        self.user.email.email = "new_email@example.com"
        self.assertEqual(self.user.email.email, "new_email@example.com")

    def test_set_invalid_email(self):
        self.user.email = "invalid_email"
        self.assertEqual(self.user.email.valide, False)

    def test_set_password_with_basic_level(self):
        # Assurez-vous que l'assignation d'un mot de passe basique lève une erreur
        with self.assertRaises(PasswordError):
            self.user.password = "new_password"

    def test_set_password_with_strong_level(self):
        # Assurez-vous que l'assignation d'un mot de passe fort réussit sans erreur
        self.user.password = "Very_Strong_Password123!"
        # Ajoutez d'autres assertions si nécessaire pour vérifier les propriétés du mot de passe

    def test_set_password_with_excellent_level(self):
        # Assurez-vous que l'assignation d'un mot de passe excellent réussit sans erreur
        self.user.password = "Extremely_Strong_Password_with_more_than_14_characters!"

    def test_generate_and_set_password_with_excellent_level(self):
        self.user.generate_and_set_password(niveau=NiveauMotDePasse.EXCELLENT)
        self.assertIsNotNone(self.user.password)
        self.assertEqual(self.user.password.niveau, NiveauMotDePasse.EXCELLENT)

    def test_generate_and_set_password_with_acceptable_level(self):
        self.user.generate_and_set_password(niveau=NiveauMotDePasse.ACCEPTABLE)
        self.assertIsNotNone(self.user.password)
        self.assertEqual(self.user.password.niveau, NiveauMotDePasse.ACCEPTABLE)

    def test_generate_and_set_password_with_basic_level(self):
        with self.assertRaises(PasswordError):
            self.user.generate_and_set_password(niveau=NiveauMotDePasse.BASIQUE)

if __name__ == '__main__':
    unittest.main()
