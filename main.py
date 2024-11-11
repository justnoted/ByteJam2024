import json
from datetime import datetime

import requests
from flask import Flask, request, redirect, url_for

from models import*

app = Flask(__name__, )
app.secret_key = "secret"
import os

from flask import Flask, render_template
app = Flask(__name__, template_folder='templates')
app.secret_key = "maybe_use_env_file_lol"
os.makedirs("static", exist_ok=True)

session = Session()

app = Flask(__name__, )
app.secret_key = "secret"

os.makedirs("static", exist_ok=True)

@app.route('/')
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if validate_user_signup(name, email, password):
            new_user = User(username=name, email=email, password=password)
            session.add(new_user)
            session.commit()
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    return render_template('welcome.html')

@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

def get_news_data():
    try:
        conn = "https://api.nytimes.com/svc/archive/v1/2024/11.json?api-key=Uk0DAHWEzvDcpsjumb5ZoGp2GmgtfcSq"
        response = requests.get(conn)
        json_response = response.json()
    except Exception as e:
        print(e)


    parse_data(json_response)


def parse_data(json_response):
    try:
        articles = []
        docs = json_response["response"]["docs"]

        for article in docs:
            authors = []
            if 'byline' in article and 'person' in article['byline']:
                for person in article['byline']['person']:
                    author = {
                        'firstname': person.get('firstname', ''),
                        'middlename': person.get('middlename', ''),
                        'lastname': person.get('lastname', ''),
                        'role': person.get('role', '')
                    }
                    authors.append(author)

            # pub_date = datetime.strptime(article['pub_date'], "%Y-%m-%dT%H:%M:%S%z")
            # formatted_date = pub_date.strftime("%B %d, %Y")

            parsed_article = {
                'abstract': article.get('abstract', ''),
                'web_url': article.get('web_url', ''),
                'headline': article['headline'].get('main', ''),
                # 'pub_date': formatted_date,
                'section_name': article.get('section_name', ''),
                'lead_paragraph': article.get('lead_paragraph', ''),
                'keywords': [kw.get('value', '') for kw in article.get('keywords', [])],
                'authors': authors
            }
            articles.append(parsed_article)

        return articles
    except KeyError as e:
        print(f"Error parsing data: {e}")
        return None
get_news_data()
if __name__ == '__main__':
    app.run()
