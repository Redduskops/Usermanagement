from datetime import datetime

from flask_login import UserMixin
from bcrypt import hashpw


class User(UserMixin):
    def __init__(self, email, username, birth_date, password_hash, age, profile_photo, user_type, status):
        if not isinstance(age, int):
            raise ValueError("age doit être un entier")

        self.email = email
        self.username = username
        self.birth_date = birth_date
        self.age = age
        self.password_hash = password_hash
        self.profile_photo = profile_photo
        self.role = user_type
        self.status = status

    def verify_password(self, password):
        return hashpw(password.encode('utf-8'), self.password_hash.encode('utf-8')) == self.password_hash.encode(
            'utf-8')

    def is_admin(self):
        return self.role == 'administrator'

    def is_moderator(self):
        return self.role == 'moderator'

    def is_active(self):
        return self.role == 'active'

    def can_edit_post(self):
        return self.is_admin() or self.is_moderator()

    def update_role(self, new_role):
        self.role = new_role

    def update_status(self, new_status):
        self.status = new_status

    def __repr__(self):
        return f"<User {self.username}>"
