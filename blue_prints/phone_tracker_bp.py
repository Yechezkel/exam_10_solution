from flask import Blueprint, request, jsonify
from repositories.neo4j_repo import *
from connections.neo4j_connection import neo4j_driver
from services.validation_service import validate_interaction_data

phone_tracker_bp = Blueprint('phone_tracker_bp', __name__)

@phone_tracker_bp.route("/phone_tracker",  methods=['POST'])
def record_interaction_route():
   interaction_data = request.get_json()
   print(f"received {interaction_data}") # todo: remove this
   if not validate_interaction_data(interaction_data):
      return jsonify({"error": "invalid input"}), 400
   if interaction_data["devices"][0]['id'] == interaction_data["devices"][1]['id']:
      return jsonify({"error": "a device cannot interact itself"}), 400
   try:
      interaction_id = record_interaction(neo4j_driver, interaction_data)
      return jsonify({ "interaction_id": interaction_id}), 200
   except Exception as e:
      print(f"error in POST /api/phone_tracker  {e}")
      return jsonify({"error": "internal server error"}), 500


@phone_tracker_bp.route("/phone_tracker/signal_strength_stronger_than_-60", methods=['GET'])
def get_by_signal_strength_route():
   try:
      result = get_by_signal_strength(neo4j_driver)
      return {"result": result}, 200
   except Exception as e:
      print(f"error in GET /api/phone_tracker/signal_strength_stronger_than_-60  {e}")
      return jsonify({"error": "internal server error"}), 500


@phone_tracker_bp.route("/phone_tracker/count_connected_devices", methods=['GET'])
def count_connected_devices_route():
   data = request.get_json()
   if not data.get('source_id'):
      return jsonify({"error": "no source_id provided"}), 400
   try:
      neighbors_count = count_connected_devices(neo4j_driver, data['source_id'])
      return jsonify({"neighbors_count": neighbors_count}), 200
   except Exception as e:
      print(f"error in GET /api/phone_tracker/count_connected_devices   {e}")
      return jsonify({"error": "internal server error"}), 500






