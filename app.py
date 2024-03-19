import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from Model.user import User
from user_management import get_user_by_id, register_user, verify_password, get_user_by_username, create_user
from datetime import datetime

from db_init import create_database_connection

connection = create_database_connection()
load_dotenv()
database = os.environ.get('DB_NAME')
app = Flask(__name__)
app.secret_key = 'ZROMqZPkvExSOKnWO19pEA'

app.config.update(
    DATABASE_URL=database,
    DEBUG=True)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(get_user_by_id)


@app.route('/')
def hello_world():
    return 'Hello World!'


def register_u(connection, email, username, password, confirm_password, birth_date):
    # Vérifiez si le mot de passe et sa confirmation correspondent
    if password != confirm_password:
        flash('Les mots de passe ne correspondent pas.', 'danger')
        return redirect(url_for('register'))

    # Effectuez la validation et l'inscription de l'utilisateur
   # if register_user(connection, email, username, password, birth_date):
       # flash('Inscription réussie. Veuillez vous connecter.', 'success')
       # return redirect(url_for('login'))
    #else:
       # flash('Nom d\'utilisateur ou adresse e-mail déjà pris. Veuillez en choisir un autre.', 'danger'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        birth_date = datetime.strptime(request.form.get('birth_date'), "%Y-%m-%d").date()

        # Vérifiez si le mot de passe et sa confirmation correspondent
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return render_template('register.html', email=email, username=username, birth_date=birth_date), 422

        # Validez les données du formulaire
        try:
            user_test = User(email=email, username=username, birth_date=birth_date, password=password)
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('register.html', email=email, username=username, birth_date=birth_date), 422

        # Vérifiez si l'utilisateur existe déjà dans la base de données
        connection = create_database_connection()
        if User.user_exists(connection, user_test.username, user_test.email.value):
            flash('Nom d\'utilisateur ou adresse e-mail déjà pris. Veuillez en choisir un autre.', 'danger')
            return render_template('register.html', email=email, username=username, birth_date=birth_date), 422

        # Créez une instance de la classe User
        if user_test.user_valide:
            # Enregistrez l'utilisateur dans la base de données
            if user_test.save_to_database():
                flash('Inscription réussie. Veuillez vous connecter.', 'success')
                return redirect(url_for('login')), 200
            else:
                flash('Erreur lors de l\'enregistrement de l\'utilisateur.', 'danger')
                return render_template('register.html', email=email, username=username, birth_date=birth_date), 500
        else:
            flash('Veuillez fournir des informations utilisateur valides.', 'danger')
            return render_template('register.html', email=email, username=username, birth_date=birth_date), 422

    # Si la méthode n'est pas POST, renvoyer une erreur 405 (Method Not Allowed)
    return make_response(render_template('register.html'), 405, [("Error", "pas une requete POST")])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(connection, username)
        if user and verify_password(user, password):
            login_user(user)
            flash('Connexion réussie.')
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


def config():
    return {'TESTING': True}

def test_client():
    return None