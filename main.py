import os

import requests
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, )
app.secret_key = "secret"

os.makedirs("static", exist_ok=True)

engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)

conn = "https://api.nytimes.com/svc/archive/v1/2024/11.json?api-key=Uk0DAHWEzvDcpsjumb5ZoGp2GmgtfcSq"

response = requests.get(conn)
print(response.json())

@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run()

@app.route('/home')
def home():
    return render_template('home.html')