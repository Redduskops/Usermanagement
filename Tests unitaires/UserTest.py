import pytest

from Factory.UserFactory import BaseUserFactory
from user_management import register_user


@pytest.fixture
def user_factory():
    return BaseUserFactory()


def test_register_user():
    # Créer un utilisateur avec la fabrique
    user = UserFactory.create(email="test@example.com", username="user")

    # Effectuer des assertions sur l'utilisateur créé
    assert user.email == "test@example.com"
    assert user.username == "user"
    assert user.id==0
    # Ajoutez d'autres assertions au besoin
