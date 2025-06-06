from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'secret_key_change_this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sae:progtr00@localhost/skills_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

users_db = {}
db = SQLAlchemy(app)

##############################
#####      DATABASE      #####
##############################

class Semestre(db.Model):
    __tablename__ = 'semestres'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    blocs = db.relationship('Bloc', backref='semestre', cascade="all, delete")

class Bloc(db.Model):
    __tablename__ = 'blocs'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    semestre_id = db.Column(db.Integer, db.ForeignKey('semestres.id'), nullable=False)
    competences = db.relationship('Competence', backref='bloc', cascade="all, delete")

class Competence(db.Model):
    __tablename__ = 'competences'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'), nullable=False)
    niveaux = db.relationship('CompetenceNiveau', backref='competence', cascade="all, delete")

class Niveau(db.Model):
    __tablename__ = 'niveaux'
    id = db.Column(db.Integer, primary_key=True)
    niveau = db.Column(db.String(50), unique=True, nullable=False)
    competences = db.relationship('CompetenceNiveau', backref='niveau')

class CompetenceNiveau(db.Model):
    __tablename__ = 'competences_niveaux'
    id = db.Column(db.Integer, primary_key=True)
    competence_id = db.Column(db.Integer, db.ForeignKey('competences.id'), nullable=False)
    niveau_id = db.Column(db.Integer, db.ForeignKey('niveaux.id'), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    if Niveau.query.count() == 0:
        niveaux_a_ajouter = ['A - Expert', 'B - C - Presque acquis', 'D - Acquisition en cours', 'E - Non acquis']
        for nom_niveau in niveaux_a_ajouter:
            niveau = Niveau(niveau=nom_niveau)
            db.session.add(niveau)
        db.session.commit()

##############################
#####       ROUTES       #####
##############################

@app.route('/get_blocs_by_semestre', methods=['POST'])
def get_blocs_by_semestre():
    semestre_id = request.form.get('semestre_id')
    blocs = Bloc.query.filter_by(semestre_id=semestre_id).all()
    bloc_data = [{"id": bloc.id, "code": bloc.code, "nom": bloc.nom} for bloc in blocs]
    return {"blocs": bloc_data}

@app.route('/about', methods=['GET', 'POST'])
def about():

    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))

    if request.method == 'POST':
        code = request.form.get('code')
        nom = request.form.get('nom')
        bloc_id = int(request.form.get('bloc_id'))
        niveau_id = int(request.form.get('niveau_id'))

        competence = Competence(code=code, nom=nom, bloc_id=bloc_id)
        db.session.add(competence)
        db.session.commit()

        competence_niveau = CompetenceNiveau(competence_id=competence.id, niveau_id=niveau_id)
        db.session.add(competence_niveau)
        db.session.commit()

        return redirect(url_for('about'))

    semestres = Semestre.query.all()
    blocs = Bloc.query.all()
    niveaux = Niveau.query.all()

    data = db.session.query(
        Competence, Bloc, Semestre, Niveau
    ).join(Bloc, Competence.bloc_id == Bloc.id) \
    .join(Semestre, Bloc.semestre_id == Semestre.id) \
    .outerjoin(CompetenceNiveau, Competence.id == CompetenceNiveau.competence_id) \
    .outerjoin(Niveau, Niveau.id == CompetenceNiveau.niveau_id) \
    .all()

    if 'username' in session:
        return render_template('about.html', data=data, semestres=semestres, blocs=blocs, niveaux=niveaux)
    else:
        return render_template('about.html', data=data, semestres=semestres, blocs=blocs, niveaux=niveaux)

@app.route('/delete-competence', methods=['POST'])
def supprimer_competence():
    competence_id = request.form.get('competence_id')
    competence = Competence.query.get_or_404(competence_id)
    db.session.delete(competence)
    db.session.commit()
    return redirect(url_for('about'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return redirect(url_for('register'))

#Sécurité mot de passe
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['username'] = user.username
            return redirect(url_for('about'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('about'))

##############################
#####      APP RUN       #####
##############################

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
