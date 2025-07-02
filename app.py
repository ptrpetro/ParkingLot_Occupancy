from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

parking_data = {
    "occupied": 0,
    "available": 0,
    "last_updated": None
}

@app.route('/')
def index():
    return render_template("index.html", data=parking_data)

@app.route('/api/update-parking', methods=['POST'])
def update_parking():
    global parking_data
    data = request.get_json()
    if "occupied" in data and "available" in data:
        parking_data["occupied"] = data["occupied"]
        parking_data["available"] = data["available"]
        parking_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({"status": "success", "data": parking_data})
    else:
        return jsonify({"status": "error", "message": "Missing data fields"}), 400

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(parking_data)

if __name__ == "__main__":
    app.run(debug=True)
