from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from . import db


db = db.DB()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@cross_origin()
@app.route('/get_all')
def get_all():
    authors = db.get_authors_and_books()
    return jsonify(authors)


@cross_origin()
@app.route('/save_all', methods=['POST'])
def save_all():
    data = request.json
    print(data)
    db.save_authors_and_books(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
