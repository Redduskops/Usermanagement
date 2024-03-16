from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from Model.user import User
from user_management import get_user_by_id, register_user, verify_password, get_user_by_username,update_date_connection
from datetime import datetime

from db_init import create_database_connection

connection = create_database_connection()

app = Flask(__name__)
app.secret_key = 'ZROMqZPkvExSOKnWO19pEA'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(get_user_by_id)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(connection, user_id)

@app.route('/')
def hello_world():
    return 'Hello World!'


def register_u(connection, email, username, password, confirm_password, birth_date):
    # Vérifiez si le mot de passe et sa confirmation correspondent
    if password != confirm_password:
        flash('Les mots de passe ne correspondent pas.', 'danger')
        return redirect(url_for('register'))

    # Effectuez la validation et l'inscription de l'utilisateur
    if register_user(connection, email, username,birth_date, password):
        flash('Inscription réussie. Veuillez vous connecter.', 'success')
        return redirect(url_for('login'))
    else:
       flash('Nom d\'utilisateur ou adresse e-mail déjà pris. Veuillez en choisir un autre.', 'danger')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        birth_date =datetime.strptime(request.form.get('birth_date'), "%Y-%m-%d").date()
        print(email, username, password, confirm_password, birth_date)
        register_u(connection, email, username, password, confirm_password, birth_date)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(connection, username)
        if user and verify_password(user, password):
            login_user(user)
            flash('Connexion réussie.')
            update_date_connection(connection, user)
            return redirect(url_for('profile'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté avec succès.')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
