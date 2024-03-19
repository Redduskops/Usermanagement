import pytest

from Model.user import User
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_successful_registration(client):
    # Simuler une requête POST avec des données valides
    response = client.post('/register', data={
        'email': 'test@6354example.com',
        'username': 'test_user1234',
        'password': 'StrongPassword_123',
        'confirm_password': 'StrongPassword_123',
        'birth_date': '1990-01-01'
    })

    # Assurez-vous que la réponse est une redirection vers la page de connexion
    assert response.status_code == 302
    assert response.location == 'http://localhost/login'

    # Vérifiez que l'utilisateur est maintenant enregistré dans la base de données
    assert User.query.filter_by(email='test@example.com').first() is not None
    assert User.query.filter_by(username='test_user').first() is not None
