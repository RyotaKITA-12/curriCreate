import argparse
import os
from os.path import join, dirname

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine


def main():
    PATH = get_path_db()
    engine = create_engine(PATH)

    args = get_args()
    df = pd.read_csv(args.path_csv)

    df.to_sql(args.table, con=engine, if_exists='replace', index=False)


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


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("table")
    parser.add_argument("path_csv")
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
