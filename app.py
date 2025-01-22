from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import subprocess
import certifi
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://admin:RtnPUAi3LSI7n7rx@twitter-scrapping.cpib0.mongodb.net/?retryWrites=true&w=majority&appName=Twitter-Scrapping"
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
db = client["trending_db"]
collection = db["trends"]

def fetch_latest_document():
    latest_doc = collection.find_one(sort=[("_id", -1)])
    return latest_doc or {"trends": "No data available", "date": "N/A", "IP": "N/A"}

@app.route('/')
def index():
    latest_doc = fetch_latest_document()
    return render_template('index.html', trend=latest_doc["trends"], date=latest_doc["timestamp"], ip=latest_doc["ip_address"])

@app.route('/run-script')
def run_script():
    subprocess.run(["python3", "scrapping with proxy.py"], check=True)
    latest_doc = fetch_latest_document()
    return jsonify(latest_doc)

@app.route('/refresh')
def refresh_data():
    latest_doc = fetch_latest_document()
    return jsonify(latest_doc)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
