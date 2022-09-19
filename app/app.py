from datetime import timedelta
import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask, render_template, request, session
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
app.permanent_session_lifetime = timedelta(minutes=10)

path, config = get_path_db()
app.config['SQLALCHEMY_DATABASE_URL'] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connection = psycopg2.connect(**config)
HEADER_CURRICULUM = ["entrance_year", "course_id", "course_category",
                     "course_name", "course_year", "credit_required",
                     "credit_elective", "course_summary", "course_keyword"]

ENTRANCE_YEAR = "2020"
app.secret_key = 'selects'


@app.route("/")
@app.route("/index")
def index():
    df_category = pd.read_sql(
        sql='SELECT course_keyword FROM keywords;',
        con=connection
    )
    record_category = set([elem[0] for elem in df_category.values.tolist()])
    return render_template("index.html",
                           categorys=record_category)


@app.route("/", methods=["POST"])
@app.route("/index", methods=["POST"])
def post_index():
    select_id = request.form.getlist("elem")
    df_category = pd.read_sql(
        sql='SELECT course_keyword FROM keywords;',
        con=connection
    )
    record_category = set([elem[0] for elem in df_category.values.tolist()])
    return render_template("index.html",
                           categorys=record_category)


@app.route("/selects", methods=["POST"])
def selects():
    select_categorys = request.form.getlist("elem")
    sql = "SELECT * FROM curriculums"
    sql += " INNER JOIN keywords"
    sql += " ON curriculums.curriculum_id = keywords.course_id"
    sql += f" WHERE curriculums.entrance_year = '{ENTRANCE_YEAR}' AND"
    for elem in select_categorys:
        sql += f" keywords.course_keyword = '{elem}' OR"
    sql = sql[:-3]
    df_curriculum = pd.read_sql(
        sql=sql,
        con=connection
    )
    record = df_curriculum.values.tolist()
    return render_template("select.html",
                           selects=select_categorys,
                           record=record)


if __name__ == "__main__":
    app.run(debug=True)
