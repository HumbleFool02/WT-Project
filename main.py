from flask import Flask, render_template , redirect,url_for, session, logging, request
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false



app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/onlinesystem'
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=False, nullable=False)
    msg = db.Column(db.String(120), unique=False, nullable=False)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), unique=False, nullable=False)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    pword = db.Column(db.String(120), unique=False, nullable=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/ManagerLogin", methods = ['GET', 'POST'])
def managerLogin():
    if request.method == 'GET':
        return render_template('ManagerLogin.html')
    else:
        username = request.form.get('username')
        pword = request.form.get('pword')
        try:
            data = Registration.query.filter_by(username=username, pword=pword).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('managerdashoard'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"

@app.route("/managerdashboard", methods = ['GET', 'POST'])
def dashboard():
    return render_template('managerdash.html')

@app.route("/SecurityLogin", methods = ['GET', 'POST'])
def securityLogin():

    return render_template('SecurityLogin.html')

@app.route("/registration", methods = ['GET', 'POST'])
def registration():
    if(request.method=='POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        domain = request.form.get('domain')
        idno = request.form.get('idno')
        pword = request.form.get('pword')
        entry = Registration(name=name, username = username , domain = domain ,idno = idno, pword = pword)
        db.session.add(entry)
        db.session.commit()
    return render_template('registration.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        entry = Contact(name=name, email = email ,phone = phone, msg = message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')    

app.run(debug=True)

