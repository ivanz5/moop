from flask import Flask
from flask import jsonify
from flask import request
from . import db


app = Flask(__name__)
db = db.DB()


@app.route('/get_all')
def get_all():
    authors = db.get_authors_and_books()
    return jsonify(authors)


@app.route('/save_all', methods=['POST'])
def save_all():
    data = request.json
    db.save_authors_and_books(data)
    return jsonify(data)
