def validate_save_to_database(self):
    if not self.email:
        return "Email is required"
    if self.email.valide is not True:
        return "Password is not enough"
    if not self.username:
        return "Username is required"
    if not self.password:
        return "Password is required"
    if not self.birth_date:
        return "Birth date is required"
    if not isinstance(self.email, Email):
        return "Email has a bad  Type"

    if len(self.username) < 3:
        return "Email need to be >= 3 characters"

    if not isinstance(self.birth_date, datetime.date):
        return "birth_date has a bad  Type"

    if self.password and not isinstance(self.password, Password):
        return "Password has a bad  Type"
    if self.password.valide is not True:
        return "Password is not enough"
    if not isinstance(self.profile_photo, str) or self.profile_photo is None:
        return "profile_photo has a bad  Type"
    if not isinstance(self.verified, bool):
        return "verified has a bad  Type"
    if self.role not in ("user", "admin", "moderator"):
        return "role has a bad  Type"
    if self.status not in ("active", "inactive", "suspended"):
        return "status has a bad  Type"
    # Si toutes les validations réussissent, retournez True
    return True