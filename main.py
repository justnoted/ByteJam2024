from flask import Flask, render_template, url_for, redirect, request
from models.models import *

app = Flask(__name__, template_folder='templates')
app.secret_key = "maybe_use_env_file_lol"

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

        errors = validate_user_signup(request.form.get('username'), request.form.get('email'), request.form.get('password'))
        if errors:
            return render_template("login.html", errors=errors, signup=True)

        new_user = User(request.form.get('username'), request.form.get('email'), request.form.get('password'))
        session.add(new_user)
        session.commit()

        session['username'] = new_user.username
        session['year'] = get_today_decade()

        return redirect(url_for("home"))

    return render_template("login.html")


@app.route('/home')
def home():
    return render_template(f"{session['year']}/index.html")     # TODO: Hook up the API JSON here


if __name__ == '__main__':
    app.run()
