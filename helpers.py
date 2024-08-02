import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class GameForm(FlaskForm):
    nome = StringField(
        "Nome do Jogo", [validators.DataRequired(), validators.Length(min=1, max=50)]
    )
    categoria = StringField(
        "Categoria", [validators.DataRequired(), validators.Length(min=1, max=40)]
    )
    console = StringField(
        "Console", [validators.DataRequired(), validators.Length(min=1, max=20)]
    )
    save = SubmitField("Salvar")


class UserForm(FlaskForm):
    user = StringField(
        "Usuário", [validators.DataRequired(), validators.Length(min=1, max=8)]
    )
    password = PasswordField(
        "Senha", [validators.DataRequired(), validators.Length(min=1, max=100)]
    )
    login = SubmitField("Login")


def recover_image(id):
    for file_name in os.listdir(app.config["UPLOAD_PATH"]):
        if f"image{id}" in file_name:
            return file_name

    return "default_image.jpg"


def delete_file_modified(id):
    file = recover_image(id)
    if file != "default_image.jpg":
        os.remove(os.path.join(app.config["UPLOAD_PATH"], file))
