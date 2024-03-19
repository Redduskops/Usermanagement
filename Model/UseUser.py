import datetime

from Model.password import Password
from Model.user import User

from db_init import create_database_connection


connection = create_database_connection()
user = User(email="kdnkdk@ndk.dkd", username="kdnkdkdkdkd", password="kjwwjK@45kdjdjw", birth_date= datetime.date(2004, 12,
                                                                                                                       0o6))



print(user.save_to_database())