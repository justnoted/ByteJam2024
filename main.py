import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, )
app.secret_key = "secret"

app = Flask(__name__, template_folder='templates')
app.secret_key = "maybe_use_env_file_lol"
os.makedirs("static", exist_ok=True)

session = Session()

# @app.route('/')
# def index():
#     if request.method == "POST":
#         session['username'] = request.form['username']
#         session['email'] = request.form['email']
#         session['password'] = request.form['password']  # TODO: Add to Users
#
#
#         return redirect(url_for('home'))
#     return render_template("login.html")


@app.route('/home', methods=['GET', 'POST'])

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def index():

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
            return render_template('create_account')



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