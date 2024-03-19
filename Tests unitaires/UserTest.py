import unittest
from Model.user import User, NiveauMotDePasse, PasswordError

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("test@example.com", "testuser")

    def test_generate_and_set_password(self):
        # Définir le nombre de fois que vous souhaitez exécuter le test
        iterations = 100

        # Stocker les résultats de chaque itération pour vérification
        results = []

        for i in range(iterations):
            # Génération et assignation d'un mot de passe avec un niveau excellent
            self.user.generate_and_set_password(niveau=NiveauMotDePasse.EXCELLENT)
            expected = (NiveauMotDePasse.EXCELLENT, True)
            result = (i, NiveauMotDePasse.EXCELLENT, self.user.password.valide)
            if result[1:] != expected:
                results.append((result, self.user.password.password))

            # Génération et assignation d'un mot de passe avec un niveau acceptable
            self.user.generate_and_set_password(niveau=NiveauMotDePasse.ACCEPTABLE)
            expected = (NiveauMotDePasse.ACCEPTABLE, True)
            result = (i, NiveauMotDePasse.ACCEPTABLE, self.user.password.valide)
            if result[1:] != expected:
                results.append((result, self.user.password.password))

            # Tentative de génération et assignation d'un mot de passe avec un niveau basique
            try:
                self.user.generate_and_set_password(niveau=NiveauMotDePasse.BASIQUE)
                expected = (NiveauMotDePasse.BASIQUE, False)
                result = (i, NiveauMotDePasse.BASIQUE, self.user.password.valide)
                if result[1:] != expected:
                    results.append((result, self.user.password.password))
            except PasswordError:
                expected = (NiveauMotDePasse.BASIQUE, False)
                result = (i, NiveauMotDePasse.BASIQUE, False)
                results.append((result, "PasswordError"))

        # Vérifier que les résultats sont constants pour chaque itération
        for result, _ in results:
            self.assertEqual(result[1:], expected)

if __name__ == '__main__':
    unittest.main()
