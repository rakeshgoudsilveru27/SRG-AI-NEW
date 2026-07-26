"""
=========================================================
SRG AI - Chat Route
=========================================================
Handles all chat requests.
"""

from flask import Blueprint, request, jsonify

from backend.services.chat_service import ChatService
from backend.utils.logger import logger


chat_bp = Blueprint("chat", __name__)


# ---------------------------------------------------------
# Chat API Health Check
# ---------------------------------------------------------
@chat_bp.route("/chat", methods=["GET"])
def chat_info():
    return jsonify({
        "status": "online",
        "service": "SRG AI Chat API",
        "method": "POST",
        "endpoint": "/api/chat",
        "message": "Send a POST request with JSON."
    }), 200


# ---------------------------------------------------------
# Chat API
# ---------------------------------------------------------
@chat_bp.route("/chat", methods=["POST"])
def chat():

    try:

        if not request.is_json:

            return jsonify({
                "status": "error",
                "reply": "Request must be JSON."
            }), 400

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "status": "error",
                "reply": "Invalid JSON data."
            }), 400

        message = str(data.get("message", "")).strip()

        if message == "":

            return jsonify({
                "status": "error",
                "reply": "Message is required."
            }), 400

        logger.info(f"User: {message}")

        result = ChatService.process(message)

        if not isinstance(result, dict):

            result = {
                "status": "success",
                "reply": str(result)
            }

        logger.info("Chat response generated successfully.")

        return jsonify(result), 200

    except Exception as e:

        logger.exception("Chat Route Error")

        return jsonify({
            "status": "error",
            "reply": "Internal Server Error",
            "details": str(e)
        }), 500