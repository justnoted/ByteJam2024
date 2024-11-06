import os

import requests
from flask import Flask, render_template, request, redirect, url_for
from models import *
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, )
app.secret_key = "secret"

app = Flask(__name__, template_folder='templates')
app.secret_key = "maybe_use_env_file_lol"
os.makedirs("static", exist_ok=True)

session = Session()
engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)

@app.route('/', methods=['GET', 'POST'])
conn = "https://api.nytimes.com/svc/archive/v1/2024/11.json?api-key=Uk0DAHWEzvDcpsjumb5ZoGp2GmgtfcSq"

response = requests.get(conn)
print(response.json())

@app.route('/')
def index():
    if request.method == "POST":
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        session['password'] = request.form['password']  # TODO: Add to Users

        return redirect(url_for('home'))
    return render_template("login.html")


@app.route('/home', methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run()

@app.route('/home')
def home():
    return render_template('home.html')