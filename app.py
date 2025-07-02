from flask import Flask, request, jsonify, render_template
from db import mongo
from models import format_event
from datetime import datetime

app = Flask(__name__)
app.config.from_object("config.Config")
mongo.init_app(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    record = format_event(event_type, data)
    if record:
        mongo.db.events.insert_one(record)
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "ignored"}), 204

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/events', methods=['GET'])
def get_events():
    events = list(mongo.db.events.find().sort("timestamp", -1).limit(10))
    for e in events:
        e['_id'] = str(e['_id'])
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)