from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'secret_key_change_this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:progtr00@localhost/skills_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

##############################
#####       ROUTES       #####
##############################

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/skills')
def skills():
    data = db.session.query(Competence, Bloc, Semestre, Niveau).\
        join(Bloc).join(Semestre).\
        outerjoin(CompetenceNiveau).outerjoin(Niveau).all()
    return render_template('skills.html', data=data)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    blocs = Bloc.query.all()
    niveaux = Niveau.query.all()

    if request.method == 'POST':
        code = request.form['code']
        nom = request.form['nom']
        bloc_id = request.form['bloc_id']
        niveau_id = request.form['niveau_id']

        comp = Competence(code=code, nom=nom, bloc_id=bloc_id)
        db.session.add(comp)
        db.session.commit()

        comp_niv = CompetenceNiveau(competence_id=comp.id, niveau_id=niveau_id)
        db.session.add(comp_niv)
        db.session.commit()

        return redirect(url_for('skills'))

    return render_template('form.html', blocs=blocs, niveaux=niveaux)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

##############################
#####      APP RUN       #####
##############################

if __name__ == '__main__':
    app.run(port=5000, debug=True)
