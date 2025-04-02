from flask_cors import CORS

import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)
CORS(app)  
API_KEY = "9290a4d061c3c77a15978928b4eb8ff119b4aec2"
ORG_ID = "1654515"
TARGET_SERIAL = "Q3CA-AT85-YJMB"  # Reemplaza si quieres otro

@app.route("/sensor-data")
def get_sensor_data():
    url = f"https://api.meraki.com/api/v1/organizations/{ORG_ID}/sensor/readings/latest"
    headers = {
        "X-Cisco-Meraki-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    for device in data:
        if device["serial"] == TARGET_SERIAL:
            for reading in device["readings"]:
                if reading["metric"] == "temperature":
                    return jsonify({
                        "celsius": reading["temperature"]["celsius"]
                    })

    return jsonify({"error": "No temperature data found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
