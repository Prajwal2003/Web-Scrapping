from flask import Flask, render_template, send_file
from flask_socketio import SocketIO
from pymongo import MongoClient
import subprocess
import time
import certifi
from pymongo.server_api import ServerApi

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

uri = "mongodb+srv://admin:RtnPUAi3LSI7n7rx@twitter-scrapping.cpib0.mongodb.net/?retryWrites=true&w=majority&appName=Twitter-Scrapping"
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
db = client["trending_db"]
collection = db["trends"]

def fetch_latest_document():
    return collection.find_one(sort=[("_id", -1)])

@app.route('/')
def index():
    subprocess.Popen(["python3", "scrapping with proxy.py"])
    return send_file('/Users/starkz/PycharmProjects/Web Scrapping/templetes/index.html')

@socketio.on('get_latest_trend')
def send_latest_trend():
    latest_doc = fetch_latest_document()
    if latest_doc:
        socketio.emit('update_trend', latest_doc)

def watch_database():
    last_id = None
    while True:
        latest_doc = fetch_latest_document()
        if latest_doc and latest_doc['_id'] != last_id:
            last_id = latest_doc['_id']
            socketio.emit('update_trend', latest_doc)
        time.sleep(5)

if __name__ == '__main__':
    socketio.start_background_task(watch_database)
    socketio.run(app, debug=False)
