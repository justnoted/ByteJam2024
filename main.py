from flask import Flask, render_template, request, redirect, url_for
from models import *
from dotenv import load_dotenv

app = Flask(__name__, template_folder='templates')
app.secret_key = "maybe_use_env_file_lol"

session = Session()

@app.route('/', methods=['GET', 'POST'])
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
