import json
from datetime import datetime

import requests
from flask import Flask, render_template, url_for, redirect, request
from models.models import *

app = Flask(__name__, )
app.secret_key = "secret"
import os

from flask import Flask, render_template
app = Flask(__name__, template_folder='templates')
app.secret_key = "maybe_use_env_file_lol"
os.makedirs("static", exist_ok=True)

session = Session()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        switch = request.form.get('switch')
        if switch:
            return render_template("login.html", signup=(switch == "register"))

        if request.form.get('submit') == "Log In":
            errors = validate_user_login(request.form.get('username'), request.form.get('password'))
            if errors:
                return render_template("login.html", errors=errors)
            session['year'] = get_today_decade()
            return redirect(url_for('home'))

        if validate_user_signup(name, email, password):
            new_user = User(username=name, email=email, password=password)
            session.add(new_user)
            session.commit()
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    return render_template('welcome.html')
        errors = validate_user_signup(request.form.get('username'), request.form.get('email'), request.form.get('password'))
        if errors:
            return render_template("login.html", errors=errors, signup=True)

        new_user = User(request.form.get('username'), request.form.get('email'), request.form.get('password'))
        session.add(new_user)
        session.commit()

@app.route("/welcome")
def welcome():
    return render_template('welcome.html')
        session['username'] = new_user.username
        session['year'] = get_today_decade()

        return redirect(url_for("home"))

    return render_template("login.html")


@app.route('/home')
def home():
    return render_template(f"{session['year']}/index.html")     # TODO: Hook up the API JSON here

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
