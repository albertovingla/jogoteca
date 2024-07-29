from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
    send_from_directory,
)
from jogoteca import app, db
from models import Jogos, Usuarios


@app.route("/")
def index():
    listGames = Jogos.query.order_by(Jogos.id)
    return render_template("list.html", titulo="Jogos", jogos=listGames)


@app.route("/newGame")
def newGame():
    if "user_logged" not in session or session["user_logged"] is None:
        flash("Voce deve estar logado para realizar esta ação.")
        return redirect(url_for("login", next=url_for("newGame")))
    return render_template("newGame.html", titulo="Novo Jogo")


@app.route(
    "/create",
    methods=[
        "POST",
    ],
)
def create():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash("Este jogo já está incluído na sua lista!")
        return redirect(url_for("index"))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    file = request.files["file"]
    upload_path = app.config["UPLOAD_PATH"]
    file.save(f"upload_path/image{novo_jogo.id}.jpg")

    return redirect(url_for("index"))


@app.route("/editGame/<int:id>")
def editGame(id):
    if "user_logged" not in session or session["user_logged"] is None:
        flash("Voce deve estar logado para realizar esta ação.")
        return redirect(url_for("login", next=url_for("editGame", id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    return render_template("editGame.html", titulo="Editar Jogo", jogo=jogo)


@app.route(
    "/alter",
    methods=[
        "POST",
    ],
)
def alter():
    jogo = Jogos.query.filter_by(id=request.form["id"]).first()
    jogo.nome = request.form["nome"]
    jogo.categoria = request.form["categoria"]
    jogo.console = request.form["console"]

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete(id):
    if "user_logged" not in session or session["user_logged"] is None:
        return redirect(url_for("login"))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Jogo deletado com sucesso!")

    return redirect(url_for("index"))


@app.route("/login")
def login():
    next = request.args.get("next")
    return render_template("login.html", next=next)


@app.route(
    "/autenticate",
    methods=[
        "POST",
    ],
)
def autenticate():
    user = Usuarios.query.filter_by(nickname=request.form["user"]).first()
    if user:
        if request.form["password"] == user.senha:
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


@app.route("/uploads/<file_name>")
def image(file_name):
    return send_from_directory("uploads", file_name)
