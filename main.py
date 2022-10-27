from hashlib import sha256
from tkinter import SE
from flask import Flask, render_template , redirect,url_for, session, logging, request, flash
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import pymysql
pymysql.install_as_MySQLdb()


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

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), unique=False, nullable=False)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    pword = db.Column(db.String(500), unique=False, nullable=False)

class Security(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), unique=False, nullable=False)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    pword = db.Column(db.String(120), unique=False, nullable=False)

class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    sdate = db.Column(db.String, unique=False, nullable=False)
    edate = db.Column(db.String, unique=False, nullable=False)
    reason = db.Column(db.String(120), unique=False, nullable=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/index")
def index():
    print(url_for('managerdashboard'))
    return render_template('index.html')
    

@app.route("/ManagerLogin", methods = ['GET', 'POST'])
def managerLogin():
    if request.method == 'GET':
        return render_template('ManagerLogin.html')
    else:
        username = request.form.get('username')
        pword = (request.form.get('pword'))
        try:
            print("in try")
            data = Manager.query.filter_by(username=username,pword=pword).first()
            if data is not None:
                print("logged in")
                session['logged_in'] = True
                return redirect(url_for('managerdashboard'))
            else:
                print("dont login 1")
                return 'Dont Login'
        except:
            print("dont login 2")
            return "Dont Login"

@app.route("/SecurityLogin", methods = ['GET', 'POST'])
def securityLogin():
    if request.method == 'GET':
        return render_template('SecurityLogin.html')
    else:
        username = request.form.get('username')
        pword = request.form.get('pword')
        try:
            data1 = Security.query.filter_by(username=username, pword=pword).first()
            if (data1 is not None):
                print("logged in")
                session['logged_in'] = True
                return redirect(url_for('securitydashboard'))
            else:
                print("dont login 1")
                return 'Dont Login else'
        except:
            print("dont login 2")
            return "Dont Login except"

@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route("/managerdashboard", methods = ['GET', 'POST'])
def managerdashboard():
    print("Print Print")
    # try:
    #     print("try")
    #     security = Security.query.filter_by(domain = 'Security').all()
    #     security_text = '<ul>'
    #     for secu in security:
    #         security_text += '<li>' + secu.name + ',' + secu.username + '</li>'
    #         print(security_text)
    #     security_text += '</ul>'
    #     return security_text
    # except Exception as e:
    #     # e holds description of the error
    #     print("except")
    #     error_text = "<p>The error:<br>" + str(e) + "</p>"
    #     hed = '<h1>Something is broken.</h1>'
    #     return hed + error_text
    try:
        security = Security.query.filter_by(domain='Security').order_by(Security.name).all()
        return render_template('managerdash.html', security=security)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route("/securitydashboard", methods = ['GET', 'POST'])
def securitydashboard():
    if(request.method=='POST'):
        idno = request.form.get('idno')
        sdate = request.form.get('sdate')
        edate = request.form.get('edate')
        reason = request.form.get('reason')
        print(reason)
        print(edate)
        abs = Absence(idno=idno , sdate= sdate,edate=edate,reason=reason)
        db.session.add(abs)
        db.session.commit()
        
    return render_template('securitydash.html')

@app.route("/registration", methods = ['GET', 'POST'])
def registration():
    if(request.method=='POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        domain = request.form.get('domain')
        idno = request.form.get('idno')
        pword = request.form.get('pword')
        cpword = request.form.get('cpword') 
        if pword == cpword :
            if domain == "Manager": 
                entry = Manager(name=name, username = username , domain = domain ,idno = idno, pword = pword)
                db.session.add(entry)
                db.session.commit()
            else:
                entry = Security(name=name, username = username , domain = domain ,idno = idno, pword = pword)
                db.session.add(entry)
                db.session.commit()
        else :
            return "Password does not match" 

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

