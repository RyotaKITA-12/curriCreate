from flask import Flask, render_template, request

app = Flask(__name__)


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
