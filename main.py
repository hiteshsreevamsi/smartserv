import flask
import pandas as pd

app = flask.Flask(__name__)
PRODUCTS_JSON_URL = "https://s3.amazonaws.com/open-to-cors/assignment.json"
GLOBAL_FRAME = None


@app.before_request
def before_request():
    if flask.request.endpoint in ['get_headers', 'display'] and GLOBAL_FRAME is None:
        return flask.jsonify(response="Before using other end points Call '/parse' to set the JSON/CSV file")


@app.route("/parse", methods=["POST"])
def parse_json():
    global GLOBAL_FRAME
    if flask.request.form["ftype"].lower() == "csv":
        df = pd.read_csv(flask.request.files["file"])
    elif flask.request.form["ftype"].lower() == "json":
        df = pd.read_json(flask.request.files["file"])
    else:
        return flask.jsonify(response="Improper request. File type not correct")
    GLOBAL_FRAME = pd.read_json(df.products.to_json()).T
    GLOBAL_FRAME.popularity = GLOBAL_FRAME.popularity.astype(int)
    GLOBAL_FRAME.sort_values("popularity", inplace=True)
    return flask.render_template("choose.html", table_headers=GLOBAL_FRAME.columns.tolist())


@app.route("/display", methods=["POST"])
def display():
    return flask.render_template('display.html', html=GLOBAL_FRAME[
        flask.request.form.getlist("FeatureCodes[]")].to_html())


@app.route("/get_headers", methods=["GET"])
def get_headers():
    return flask.jsonify(table_headers=GLOBAL_FRAME.columns.tolist())


@app.route("/")
def home():
    return flask.render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True, port=8083)
