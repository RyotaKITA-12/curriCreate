import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


def get_path_db():
    load_dotenv(verbose=True)
    path_env = join(dirname(__file__), '.env')
    load_dotenv(path_env)

    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_USER")
    server = os.environ.get("POSTGRES_SERVER")
    port = os.environ.get("POSTGRES_PORT")
    db = os.environ.get("POSTGRES_DB")
    PATH = f'postgresql://{user}:{password}@{server}:{port}/{db}'

    return PATH


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = get_path_db()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Curriculums(db.Model):
    __tablename__ = 'Shohin'


@app.route("/")
@app.route("/index")
def index():
    categorys = ["データサイエンス", "機械学習", "ゲーム", "IoT",
                 "Web", "深層学習", "強化学習", "数学", "スクレイピング",
                 "倫理", "データベース", "音声認識", "画像認識", "自然言語処理"]
    return render_template("index.html", categorys=categorys)


@app.route("/selects", methods=["POST"])
def selects():
    select_categorys = request.form.getlist("elem")
    print(select_categorys)
    return render_template("select.html", selects=select_categorys)


if __name__ == "__main__":
    app.run(debug=True)
