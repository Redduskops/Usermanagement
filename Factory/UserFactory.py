from faker import Faker
import factory
import datetime

from Model.user import User

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User

    user_id = factory.Sequence(lambda n: n % 2001)
    email = factory.LazyAttribute(lambda x: fake.email())
    username = factory.LazyAttribute(lambda x: fake.user_name())
    birth_date = factory.LazyAttribute(lambda x: fake.date_of_birth(minimum_age=18, maximum_age=100))
    password = factory.LazyAttribute(lambda x: fake.password())
    profile_photo = "default.jpg"
    user_type = "user"
    status = "inactive"
    verified = False
    user_valide = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create classmethod to set password_hash instead of password.
        """
        password = kwargs.pop('password', None)  # Pop the 'password' argument if provided
        if password is None:
            password = fake.password()  # Generate a random password if not provided
        kwargs['password'] = password  # Set the password argument for the instance creation
        user = model_class(*args, **kwargs)
        return user

# Création de 10 utilisateurs
users = [UserFactory.create() for _ in range(10)]

# Affichage des utilisateurs créés
for user in users:
    print(user.save_to_database())
