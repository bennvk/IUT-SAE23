from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ton_user:ton_mdp@localhost:3306/nom_de_ta_base'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    if 'username' in session:
        return f'Bonjour, {session["username"]}! <a href="/logout">Se déconnecter</a>'
    return render_template('~/Documents/IUT-SAE23/code/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['username'] = user.username
            return redirect(url_for('index'))
        return 'Identifiants invalides'
    return render_template('~/Documents/IUT-SAE23/code/login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('~/Documents/IUT-SAE23/code/index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        new_user = User(username=request.form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('~/Documents/IUT-SAE23/code/register.html')

def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
