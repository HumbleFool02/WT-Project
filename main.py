from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
from flask import request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/securitysystem'
db = SQLAlchemy()

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    msg = db.Column(db.String(120), unique=False, nullable=False)


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

@app.route("/registration")
def registration():
    return render_template('registration.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('msg')
        entry = Contacts(name=name, email = email , msg = message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')    

app.run(debug=True)

