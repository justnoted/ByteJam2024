import os
from datetime import datetime

import requests
from flask import Flask, render_template, request, redirect, url_for, json, session
from models import*

app = Flask(__name__, )
app.secret_key = "secret"

os.makedirs("static", exist_ok=True)

@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    ss = Session()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = User(username=name, email=email, password=password)

        ss.add(new_user)



def get_news_data():
    conn = "https://api.nytimes.com/svc/archive/v1/2024/11.json?api-key=Uk0DAHWEzvDcpsjumb5ZoGp2GmgtfcSq"
    response = requests.get(conn)
    json_response = response.json()
    # parse_data(json_response)
    print(json_response)

def parse_data(json_response):
    articles = []
    for article in json_response:
        # pub_date = datetime.strptime(article['pub_date'])
        parsed_article = {
            'abstract': article['abstract'],
            'web_url': article['web_url'],
            'headline': article['headline'],
            'pub_date': article['pub_date'],
            'section_name': article['section_name'],
            'subsection_name': article['subsection_name'],
            'keywords': article['keywords']
        }
        articles.append(parsed_article)
        print(parsed_article)
    return articles

get_news_data()
if __name__ == '__main__':
    app.run()