import re


"""Class: Email
-----------------
Represents an email address.

Attributes:
- value: str
    The email address value.
- valide: bool
    Indicates whether the email address is valid or not.

Methods:
- __init__(self, email: str)
    Initializes an Email object with the specified email address.
    
- _validate_email(self, email: str)
    Validates the format of the email address and updates the 'valide' attribute accordingly.

- __str__(self) -> str
    Returns a string representation of the Email object.

Properties:
- value: str
    Getter and setter for the email address value. Automatically validates the format of the email when setting the value.

- valide: bool
    Getter and setter for the validity status of the email address.

Example Usage:
---------------
# Create an Email object
email = Email("example@example.com")

# Access and print email address value and validity status
print(email.value)    # Output: example@example.com
print(email.valide)   # Output: True
print(email)          # Output: Email: example@example.com, Valide: True
"""
class EmailError(Exception):
    pass

class Email:
    def __init__(self, email):
        self._value = None
        self._valide = False
        self.value = email

    @property
    def value(self):
        return self._email

    @value.setter
    def value(self, value):
        self._validate_email(value)
        self._email = value

    @property
    def valide(self):
        return self._valide

    @valide.setter
    def valide(self, value):
        if not isinstance(value, bool):
            raise ValueError("Valide must be a boolean")
        self._valide = value

    def _validate_email(self, email)  :
        if not isinstance(email, str) or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            self.valide = False
        else:
            self.valide = True

    def _validateemail(self):
        if not isinstance(self.value, str) or not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.value):
           return  False
        else:
            return True

    def __str__(self):
        return f"Email: {self.value}, Valide: {self.valide}"
