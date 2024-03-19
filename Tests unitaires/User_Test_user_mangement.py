import unittest
import datetime
from unittest.mock import MagicMock, patch

from db_init import create_database_connection
from user_management import create_user, get_user_by_email, get_user_by_username, register_user, validate_user_data, update_date_connection
from Model.Email import Email
from Model.password import Password
from Model.user import User

class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.connection = create_database_connection()

    def tearDown(self):
        # Nettoyer les données de test après chaque test si nécessaire
        pass

    def test_create_user(self):
        # Créer un utilisateur de test
        email = "test@example.com"
        username = "testuser"
        birth_date = datetime.date(1990, 1, 1)
        password = "password123T@4"
        user = User(email=email, username=username, birth_date=birth_date,password=password)

        # Ajouter l'utilisateur à la base de données
        create_user(self.connection, user)

        # Vérifier si l'utilisateur a été ajouté avec succès en récupérant son email
        retrieved_user = get_user_by_email(self.connection, "test@example.com")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")

    class TestUserManagement(unittest.TestCase):
        @patch('user_management.conn')
        def test_get_user_by_email(self, mock_create_connection):
            # Mock de la méthode cursor de l'objet connexion
            mock_cursor = mock_create_connection.return_value.cursor.return_value
            # Définir le comportement attendu pour la méthode execute du curseur
            mock_cursor.execute.return_value = [(1, 'test@example.com', 'testuser')]

            # Appeler la fonction get_user_by_email
            user = get_user_by_email(mock_create_connection(), 'test@example.com')

            # Vérifier si la fonction a renvoyé un utilisateur avec les bonnes informations
            self.assertIsInstance(user, User)
            self.assertEqual(user.email, Email('test@example.com'))
            self.assertEqual(user.username, 'testuser')
        # Créez d'autres tests pour les autres fonctions de gestion des litterateurs

if __name__ == "__main__":
    unittest.main()
