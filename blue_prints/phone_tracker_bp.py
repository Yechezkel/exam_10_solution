from flask import Blueprint, request, jsonify

phone_tracker_bp = Blueprint('phone_tracker_bp', __name__)

@phone_tracker_bp.route("/phone_tracker",  methods=['POST'])
def get_interaction():
   print(request.json)
   return jsonify({ }), 200