from flask import Flask, render_template, url_for, redirect, request
from models.models import *
import os


app = Flask(__name__, template_folder='templates')
app.secret_key = "maybe_use_env_file_lol"

os.makedirs("static", exist_ok=True)

session = Session()

username = ""
set_year = get_today_decade()


@app.route('/', methods=['GET', 'POST'])
def index():
    global username

    if request.method == 'POST':
        switch = request.form.get('switch')
        if switch:
            return render_template("login.html", signup=(switch == "register"))

        if request.form.get('submit') == "Log In":
            errors = validate_user_login(request.form.get('username'), request.form.get('password'))
            if errors:
                return render_template("login.html", errors=errors)

            username = request.form.get('username')

            return redirect(url_for('home'))

        errors = validate_user_signup(request.form.get('username'), request.form.get('email'),
                                      request.form.get('password'))
        if errors:
            return render_template("login.html", errors=errors, signup=True)

        new_user = User(request.form.get('username'), request.form.get('email'), request.form.get('password'))

        session.add(new_user)
        session.commit()

        username = new_user.username

        return redirect(url_for("home"))

    return render_template("login.html")


@app.route('/home')
def home():
    return f"{username} | {set_year}"
    # return render_template(f"{session['year']}/index.html")     # TODO: Hook up the API JSON here


@app.route('/article')
def article():
    return render_template(f"{session['year']}/article.html")   # TODO: Add article query to display content


if __name__ == '__main__':
    app.run()
