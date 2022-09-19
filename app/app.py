import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import psycopg2


def get_path_db():
    load_dotenv(verbose=True)
    path_env = join(dirname(__file__), '.env')
    load_dotenv(path_env)

    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_USER")
    host = os.environ.get("POSTGRES_SERVER")
    port = os.environ.get("POSTGRES_PORT")
    database = os.environ.get("POSTGRES_DB")
    config = {
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'database': database
    }
    path = f'postgresql://{user}:{password}@{host}:{port}/{database}'

    return path, config


app = Flask(__name__)
path, config = get_path_db()
app.config['SQLALCHEMY_DATABASE_URL'] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

connection = psycopg2.connect(**config)

df = pd.read_sql(sql='SELECT * FROM curriculums;', con=connection)
header = ["entrance_year", "course_id", "course_category", "course_name",
          "course_year", "credit_required", "credit_elective",
          "course_summary", "course_keyword"]
record = df.values.tolist()


class Keywords(db.Model):
    __tablename__ = 'keywords'
    curriculum_id = db.Column(db.Integer, primary_key=True)
    course_keyword = db.Column(db.String)


class Curriculums(db.Model):
    __tablename__ = 'curriculums'
    curriculum_id = db.Column(db.Integer, primary_key=True)
    entrance_year = db.Column(db.Integer)
    course_id = db.Column(db.Integer)
    course_category = db.Column(db.String)
    course_name = db.Column(db.String)
    course_year = db.Column(db.String)
    credit_required = db.Column(db.Integer)
    credit_elective = db.Column(db.Integer)
    course_summary = db.Column(db.String)
    course_keyword = db.Column(db.String)


@app.route("/")
@app.route("/index")
def index():
    categorys = ["データサイエンス", "機械学習", "ゲーム", "IoT",
                 "Web", "深層学習", "強化学習", "数学", "スクレイピング",
                 "倫理", "データベース", "音声認識", "画像認識", "自然言語処理"]
    return render_template("index.html", categorys=categorys, test=record)


@app.route("/selects", methods=["POST"])
def selects():
    select_categorys = request.form.getlist("elem")
    return render_template("select.html", selects=select_categorys)


if __name__ == "__main__":
    app.run(debug=True)
