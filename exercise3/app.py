import asyncio
import os
from functools import wraps

from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    logging,
)

from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import User
from posts.handler import PostHandler
from forms import PostForm, RegisterForm

app = Flask(__name__)
app.secret_key = os.environ.get("DATABASE_URL", "KSADkasjhfj43932jk2kajhdkj3KJH")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
post_handler = PostHandler()


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        user = User(username=username, password=password, name=name, email=email)
        db.session.add(user)
        db.session.commit()
        flash("You are now registered and can log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get Form Fields
        username = request.form["username"]
        password_candidate = request.form["password"]

        # Get user by username
        user = User.query.filter_by(username=username).first()

        if user:
            # Get stored hash
            password = user.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session["logged_in"] = True
                session["username"] = username

                flash("You are now logged in", "success")
                return redirect(url_for("members_only"))
            else:
                error = "Invalid login"
                return render_template("login.html", error=error)
        else:
            error = "Username not found"
            return render_template("login.html", error=error)

    return render_template("login.html")


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", "danger")
            return redirect(url_for("login"))

    return wrap


@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for("login"))


@app.route("/members_only", methods=["GET", "POST"])
@is_logged_in
def members_only():
    form = PostForm(request.form)
    response = ""
    if request.method == "POST" and form.validate():
        id_post = form.id_post.data
        response = asyncio.run(post_handler.get_post(id_post))
    return render_template("posts.html", post=response, form=form)

