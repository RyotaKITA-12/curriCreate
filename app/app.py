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


def calculate_total_credits():
    total = credits_required
    for s_id in session['select_id']:
        df_credit = pd.read_sql(
            sql='SELECT credit_required, credit_elective FROM curriculums WHERE curriculum_id = 3',
            con=connection
        )
        total += [sum(elem) for elem in df_credit.values.tolist()][0]
    return total


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
app.secret_key = 'select_id'


df_credit_required = pd.read_sql(
    sql=f"SELECT credit_required FROM curriculums WHERE credit_elective=0 AND entrance_year={ENTRANCE_YEAR}",
    con=connection
)
credits_required = sum([elem[0] for elem in df_credit_required.values.tolist()])


@app.route("/")
@app.route("/index")
def index():
    session['select_id'] = []
    select_list = session['select_id']
    credits_total = calculate_total_credits()
    df_category = pd.read_sql(
        sql='SELECT course_keyword FROM keywords;',
        con=connection
    )
    record_category = set([elem[0] for elem in df_category.values.tolist()])
    return render_template("index.html",
                           categorys=record_category,
                           total=credits_total,
                           select_list=select_list)


@app.route("/", methods=["POST"])
@app.route("/index", methods=["POST"])
def post_index():
    select_id = request.form.getlist("elem")
    if 'select_id' not in session:
        session['select_id'] = []
    select_list = session['select_id']
    for i in select_id:
        select_list.append(i)
    session['select_id'] = select_list
    credits_total = calculate_total_credits()
    df_category = pd.read_sql(
        sql='SELECT course_keyword FROM keywords;',
        con=connection
    )
    record_category = set([elem[0] for elem in df_category.values.tolist()])
    return render_template("index.html",
                           categorys=record_category,
                           total=credits_total,
                           select_list=select_list)


@app.route("/selects", methods=["POST"])
def selects():
    select_categorys = request.form.getlist("elem")
    if 'select_id' not in session:
        session['select_id'] = []
    select_list = session['select_id']
    credits_total = calculate_total_credits()
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
                           record=record,
                           total=credits_total,
                           select_list=select_list)


if __name__ == "__main__":
    app.run(debug=True)
