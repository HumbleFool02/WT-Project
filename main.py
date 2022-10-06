from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
from flask import request


app = Flask(__name__)
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

@app.route("/ManagerLogin")
def ManagerLogin():
    return render_template('ManagerLogin.html')

@app.route("/SecurityLogin")
def SecurityLogin():
    return render_template('SecurityLogin.html')

@app.route("/registration", methods = ['GET', 'POST'])
def registration():
    if(request.method=='POST'):
        '''Add entry to the database'''
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
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        entry = Contact(name=name, email = email ,phone = phone, msg = message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')    

app.run(debug=True)

