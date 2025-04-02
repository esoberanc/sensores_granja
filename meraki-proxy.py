from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Habilita CORS

MERAKI_API_KEY = "9290a4d061c3c77a15978928b4eb8ff119b4aec2"
ORGANIZATION_ID = "1654515"
SENSOR_SERIAL = "Q3CA-AT85-YJMB"

@app.route("/sensor-data")
def get_sensor_data():
    url = f"https://api.meraki.com/api/v1/organizations/{ORGANIZATION_ID}/sensor/readings/latest"
    headers = {
        "X-Cisco-Meraki-API-Key": MERAKI_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for sensor in data:
            if sensor["serial"] == SENSOR_SERIAL:
                for reading in sensor["readings"]:
                    if reading["metric"] == "temperature":
                        temp = reading["temperature"]["celsius"]
                        return jsonify({"temperature": temp})
        return jsonify({"error": "Temperatura no encontrada"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
