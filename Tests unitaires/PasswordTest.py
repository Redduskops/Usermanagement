import string
import unittest
import bcrypt

from Model.password import Password, PasswordError, NiveauMotDePasse


class TestPassword(unittest.TestCase):
    def setUp(self):
        self.password = Password()

    def test_generate_password(self):
        # Test that generate_password returns a tuple with password, niveau, and length
        generated_password = self.password.generate_password()
        self.assertIsInstance(generated_password, tuple)
        self.assertEqual(len(generated_password), 3)

        # Test that the generated password has the correct length based on the default niveau (ACCEPTABLE)
        password, niveau, length = generated_password
        self.assertTrue(8 <= len(password) <= 14)
        self.assertEqual(niveau, NiveauMotDePasse.ACCEPTABLE)

        # Test that the generated password meets the criteria for the default niveau (ACCEPTABLE)
        self.assertTrue(self.password._validate_password(password))

    def test_check_password_strength(self):
        # Test that check_password_strength returns a tuple with niveau, valide, and the password
        result = self.password.check_password_strength("TestPassword123!")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)

        # Test that the default password is generated with the correct niveau and is valid
        niveau, valide, password = result
        self.assertEqual(niveau, NiveauMotDePasse.ACCEPTABLE)
        self.assertTrue(valide)
        self.assertEqual(password, "TestPassword123!")


    def test_verify_password(self):
        # Test verifying a correct password
        valid_password = "TestPassword123!"
        self.password.set_password(valid_password)
        hashed_password = self.password.password_hash
        self.assertTrue(Password.verify_password(valid_password, hashed_password))

        # Test verifying an incorrect password
        invalid_password = "IncorrectPassword"
        self.assertFalse(Password.verify_password(invalid_password, hashed_password))


class TestPasswordGeneration(unittest.TestCase):
    def test_generate_password_acceptable(self):
        password_object = Password()
        password, niveau, length = password_object.generate_password(NiveauMotDePasse.ACCEPTABLE)
        self.assertEqual(niveau, NiveauMotDePasse.ACCEPTABLE)
        self.assertTrue(8 <= length <= 14)
        self.assertTrue(self.check_password_criteria(password))

    def test_generate_password_excellent(self):
        password_object = Password()
        password, niveau, length = password_object.generate_password(NiveauMotDePasse.EXCELLENT)
        self.assertEqual(niveau, NiveauMotDePasse.EXCELLENT)
        self.assertTrue(14 <= length <= 35)
        self.assertTrue(self.check_password_criteria(password))

    def test_generate_password_basique(self):
        password_object = Password()
        password, niveau, length = password_object.generate_password(NiveauMotDePasse.BASIQUE)
        self.assertEqual(niveau, NiveauMotDePasse.BASIQUE)
        self.assertTrue(6 <= length <= 7)
        self.assertTrue(self.check_password_criteria(password))

    def check_password_criteria(self, password):
        # Vérifie si le mot de passe satisfait les critères
        has_lowercase = any(c.islower() for c in password)
        has_uppercase = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        return has_lowercase and has_uppercase and has_digit and has_special

class TestPasswordGeneration(unittest.TestCase):
    def setUp(self):
        self.password = Password()

    def test_generate_passwords(self):
        # Niveau de mot de passe à tester
        niveau = NiveauMotDePasse.ACCEPTABLE

        # Générer 100 mots de passe pour le niveau spécifié
        for _ in range(100):
            generated_password, generated_niveau, _ = self.password.generate_password(niveau)

            # Vérifier si le mot de passe est valide et du niveau attendu
            is_valid = self.password.check_password_strength(generated_password)

            # Vérifier si le niveau généré correspond au niveau spécifié
            self.assertEqual(generated_niveau, niveau)

            # Vérifier si le mot de passe est valide
            self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()
