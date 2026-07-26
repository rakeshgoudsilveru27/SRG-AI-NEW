"""
=========================================================
SRG AI - Health Routes
=========================================================
System health monitoring.
=========================================================
"""

from flask import Blueprint, jsonify

from backend.config import Config


health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    """

    return jsonify({

        "status": "healthy",

        "application": "SRG AI",

        "version": Config.APP_VERSION,

        "services": {

            "gemini": bool(Config.GEMINI_API_KEYS),

            "deepgram": bool(Config.DEEPGRAM_API_KEY),

            "weather": bool(Config.WEATHER_API_KEY)

        }

    }), 200