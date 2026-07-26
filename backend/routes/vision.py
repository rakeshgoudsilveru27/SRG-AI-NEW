"""
=========================================================
SRG AI - Vision Routes
=========================================================
Handles image analysis requests.
"""

from flask import Blueprint, jsonify, request

from backend.services.image_service import ImageService
from backend.utils.logger import logger


vision_bp = Blueprint("vision", __name__)


@vision_bp.route("/vision", methods=["GET"])
def vision_status():
    """
    Health check endpoint.
    """

    return jsonify({
        "status": "working",
        "message": "SRG Vision API is running."
    })


@vision_bp.route("/vision", methods=["POST"])
def analyze_image():
    """
    Analyze an uploaded image using Gemini Vision.
    """

    try:

        # ----------------------------------------
        # Validate Image
        # ----------------------------------------

        if "image" not in request.files:

            return jsonify({
                "status": "error",
                "reply": "No image file received."
            }), 400

        image = request.files["image"]

        if image.filename == "":

            return jsonify({
                "status": "error",
                "reply": "No image selected."
            }), 400

        logger.info(f"Image received: {image.filename}")

        # ----------------------------------------
        # Analyze Image
        # ----------------------------------------

        result = ImageService.analyze_image(image)

        logger.info("Image analyzed successfully.")

        return jsonify(result), 200

    except Exception:

        logger.exception("Vision Route Error")

        return jsonify({
            "status": "error",
            "reply": "Image processing failed."
        }), 500