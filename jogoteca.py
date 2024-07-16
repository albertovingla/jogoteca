from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "@cd001*BA@"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "{SGDB}://{usuario}:{senha}@{servidor}/{database}".format(
        SGDB="mysql+mysqlconnector",
        usuario="root",
        senha="root",
        servidor="localhost",
        database="jogoteca",
    )
)
db = SQLAlchemy(app)


class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.name


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.name


@app.route("/index")
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


app.run(debug=True)
