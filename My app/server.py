from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DB_FILE = 'database.json'

def read_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/data/<year_month>', methods=['GET'])
def get_data(year_month):
    data = read_data()
    return jsonify(data.get(year_month, {}))

@app.route('/data/<year_month>', methods=['POST'])
def update_data(year_month):
    all_data = read_data()
    if year_month not in all_data:
        all_data[year_month] = {}

    update = request.json
    all_data[year_month].update(update)

    write_data(all_data)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5000))