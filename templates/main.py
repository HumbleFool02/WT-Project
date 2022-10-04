from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/ManagerLogin")
def ManagerLogin():
    return render_template('ManagerLogin.html')


@app.route("/SecurityLogin")
def SecurityLogin():
    return render_template('SecurityLogin.html')

@app.route("/Registration")
def registration():
    return render_template('registration.html')

app.run(debug=True)

