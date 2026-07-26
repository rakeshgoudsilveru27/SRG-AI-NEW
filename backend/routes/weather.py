"""
=========================================================
SRG AI - Weather Routes
=========================================================
Handles weather requests.
"""

from flask import Blueprint, jsonify, request

from backend.services.weather_service import WeatherService
from backend.utils.logger import logger


weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather", methods=["GET"])
def weather_status():
    """
    Health check endpoint.
    """

    return jsonify({
        "status": "working",
        "message": "SRG Weather API is running."
    })


@weather_bp.route("/weather/current", methods=["GET"])
def current_weather():
    """
    Get current weather for a city.
    Example:
    /weather/current?city=Hyderabad
    """

    try:

        city = request.args.get("city", "").strip()

        if not city:

            return jsonify({
                "status": "error",
                "reply": "City is required."
            }), 400

        logger.info(f"Current weather request: {city}")

        reply = WeatherService.get_weather(city)

        return jsonify({
            "status": "success",
            "city": city,
            "reply": reply
        }), 200

    except Exception:

        logger.exception("Current Weather Route Error")

        return jsonify({
            "status": "error",
            "reply": "Unable to fetch current weather."
        }), 500


@weather_bp.route("/weather/tomorrow", methods=["GET"])
def tomorrow_weather():
    """
    Get tomorrow's weather forecast.
    Example:
    /weather/tomorrow?city=Hyderabad
    """

    try:

        city = request.args.get("city", "").strip()

        if not city:

            return jsonify({
                "status": "error",
                "reply": "City is required."
            }), 400

        logger.info(f"Tomorrow weather request: {city}")

        reply = WeatherService.get_tomorrow_weather(city)

        return jsonify({
            "status": "success",
            "city": city,
            "reply": reply
        }), 200

    except Exception:

        logger.exception("Tomorrow Weather Route Error")

        return jsonify({
            "status": "error",
            "reply": "Unable to fetch tomorrow's weather."
        }), 500
    