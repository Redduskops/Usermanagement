import factory
from faker import Faker
from Model.user import User

fake = Faker()

class BaseUserFactory(factory.Factory):
    class Meta:
        model = User

    user_id = factory.Sequence(lambda n: n % 2001)  # Utilisation d'une séquence avec une fonction lambda
    email = factory.LazyAttribute(lambda x: fake.email())
    username = factory.LazyAttribute(lambda x: fake.user_name())
    birth_date = factory.LazyAttribute(lambda x: fake.date_of_birth(minimum_age=18, maximum_age=100))
    password_hash = factory.LazyAttribute(lambda x: fake.password())
    profile_photo = factory.LazyAttribute(lambda x: fake.image_url())
    user_type = factory.LazyAttribute(lambda x: fake.random_element(elements=("user", "admin", "moderator")))
    status = factory.LazyAttribute(lambda x: fake.random_element(elements=("active", "inactive", "suspended")))
    verified = factory.LazyAttribute(lambda x: fake.boolean())

class SimpleUserFactory(BaseUserFactory):
    pass

class AdminUserFactory(BaseUserFactory):
    user_type = "admin"

class ModeratorUserFactory(BaseUserFactory):
    user_type = "moderator"

# Exemple d'utilisation
simple_user = SimpleUserFactory.create()
admin_user = AdminUserFactory.create()
moderator_user = ModeratorUserFactory.create()



if __name__ == "__main__":
    new_user = ModeratorUserFactory.create()
    print(new_user)