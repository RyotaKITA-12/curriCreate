from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("name")
    animals = ["dog", "cat"]
    return render_template("index.html", name=name, animals=animals)


@app.route("/index", methods=["post"])
def post():
    name = request.form["name"]
    animals = ["dog", "cat"]
    return render_template("index.html", name=name, animals=animals)


if __name__ == "__main__":
    app.run(debug=True)
