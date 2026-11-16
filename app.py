"""
Vehicle Service API
A RESTful API for managing a registry of vehicles.
"""

import os
from flask import Flask, jsonify, request, abort
from functools import wraps

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory store
# ---------------------------------------------------------------------------
_vehicles: dict[int, dict] = {}
_next_id: int = 1


def _next_vehicle_id() -> int:
    global _next_id
    vid = _next_id
    _next_id += 1
    return vid


# ---------------------------------------------------------------------------
# API Key auth middleware
# ---------------------------------------------------------------------------
API_KEY = os.environ.get("API_KEY", "dev-api-key")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key or key != API_KEY:
            return jsonify({"message": "Unauthorized. A valid X-API-Key header is required."}), 401
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
REQUIRED_FIELDS = {"vin", "make", "model", "year", "miles"}


def _vehicle_response(v: dict) -> dict:
    return {
        "id": v["id"],
        "nickName": v.get("nickName", ""),
        "vin": v["vin"],
        "make": v["make"],
        "model": v["model"],
        "year": v["year"],
        "miles": v["miles"],
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

# GET /vehicles — list all vehicles
@app.route("/vehicles", methods=["GET"])
@require_api_key
def get_all_vehicles():
    try:
        return jsonify([_vehicle_response(v) for v in _vehicles.values()]), 200
    except Exception:
        return jsonify({"message": "An unexpected error occurred."}), 500


# POST /vehicles — create a vehicle
@app.route("/vehicles", methods=["POST"])
@require_api_key
def create_vehicle():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"message": "Request body is required."}), 400

        for field in REQUIRED_FIELDS:
            if field not in data:
                return jsonify({"message": f"Request body missing required attribute: {field}"}), 400

        # VIN uniqueness check
        vin = data["vin"]
        for v in _vehicles.values():
            if v["vin"] == vin:
                return jsonify({
                    "message": f"Vehicle with VIN {vin} already exists. Existing vehicle ID: {v['id']}"
                }), 409

        vid = _next_vehicle_id()
        vehicle = {
            "id": vid,
            "nickName": data.get("nickName", ""),
            "vin": vin,
            "make": data["make"],
            "model": data["model"],
            "year": str(data["year"]),
            "miles": data["miles"],
        }
        _vehicles[vid] = vehicle
        return jsonify(_vehicle_response(vehicle)), 201

    except Exception:
        return jsonify({"message": "An unexpected error occurred."}), 500


# GET /vehicles/<id> — retrieve a single vehicle
@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
@require_api_key
def get_vehicle(vehicle_id: int):
    try:
        vehicle = _vehicles.get(vehicle_id)
        if not vehicle:
            return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404
        return jsonify(_vehicle_response(vehicle)), 200
    except Exception:
        return jsonify({"message": "An unexpected error occurred."}), 500


# PATCH /vehicles/<id> — update a vehicle
@app.route("/vehicles/<int:vehicle_id>", methods=["PATCH"])
@require_api_key
def update_vehicle(vehicle_id: int):
    try:
        vehicle = _vehicles.get(vehicle_id)
        if not vehicle:
            return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"message": "Bad request body."}), 400

        updatable = {"nickName", "vin", "make", "model", "year", "miles"}
        for key, value in data.items():
            if key in updatable:
                vehicle[key] = value

        return jsonify(_vehicle_response(vehicle)), 200

    except Exception:
        return jsonify({"message": "An unexpected error occurred."}), 500


# DELETE /vehicles/<id> — delete a vehicle
@app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
@require_api_key
def delete_vehicle(vehicle_id: int):
    try:
        if vehicle_id not in _vehicles:
            return jsonify({"message": f"Vehicle with id: {vehicle_id} not found."}), 404
        del _vehicles[vehicle_id]
        return "", 204
    except Exception:
        return jsonify({"message": "An unexpected error occurred."}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
