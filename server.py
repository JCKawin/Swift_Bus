from flask import Flask, request, jsonify
app = Flask(__name__)

buses = {}  # bus_id: {lat, lon, route}
broadcast = ""

@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.get_json()
    buses[data["bus_id"]] = {"lat": data["lat"], "lon": data["lon"], "route": data["route"]}
    return "ok"

@app.route("/buses", methods=["GET"])
def get_buses():
    return jsonify({"buses": list(buses.values()), "broadcast": broadcast})

@app.route("/broadcast", methods=["POST"])
def update_broadcast():
    global broadcast
    broadcast = request.get_json()["message"]
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
