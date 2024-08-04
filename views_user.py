from jogoteca import app
from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import UserForm
from flask_bcrypt import check_password_hash


@app.route("/login")
def login():
    next = request.args.get("next")
    form = UserForm()
    return render_template("login.html", next=next, form=form)


@app.route(
    "/autenticate",
    methods=[
        "POST",
    ],
)
def autenticate():
    form = UserForm(request.form)
    user = Usuarios.query.filter_by(nickname=form.user.data).first()
    password = check_password_hash(user.senha, form.password.data)

    if user and password:
        session["user_logged"] = user.nickname
        flash(user.nickname + " logado com sucesso!")
        next_page = request.form["next"]
        return redirect(next_page)
    else:
        flash("Login ou senha inválidos. Verifique suas credenciais.")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session["user_logged"] = None
    flash("Logout realizado!")
    return redirect(url_for("index"))
