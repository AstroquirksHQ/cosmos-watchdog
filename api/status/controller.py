from flask import Blueprint, make_response, jsonify


class StatusController:

    status_routes = Blueprint("status", __name__)

    @staticmethod
    @status_routes.route("/_health", methods=["GET"])
    def get_health():
        return make_response(jsonify({"success": "True"}))
