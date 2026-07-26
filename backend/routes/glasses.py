"""
=========================================================
SRG AI - Glasses Routes
=========================================================
Main API for SRG AI Glasses.
Supports:
- Voice
- Vision
- Future Sensor Integration
=========================================================
"""

from flask import Blueprint, jsonify, request

from backend.services.chat_service import ChatService

from backend.services.deepgram_service import DeepgramService
from backend.services.image_service import ImageService
from backend.utils.logger import logger


glasses_bp = Blueprint("glasses", __name__)


@glasses_bp.route("/glasses", methods=["GET"])
def glasses_status():
    """
    Health check endpoint.
    """

    return jsonify({
        "status": "working",
        "message": "SRG AI Glasses API is running."
    })


@glasses_bp.route("/glasses/voice", methods=["POST"])
def glasses_voice():
    """
    Voice endpoint for SRG AI Glasses.
    """

    try:

        if "audio" not in request.files:

            return jsonify({
                "status": "error",
                "reply": "No audio file received."
            }), 400

        audio = request.files["audio"]

        audio_data = audio.read()

        if not audio_data:

            return jsonify({
                "status": "error",
                "reply": "Empty audio received."
            }), 400

        logger.info("Voice received from SRG Glasses.")

        transcript = DeepgramService.transcribe_audio(audio_data)

        if not transcript:

            return jsonify({
                "status": "error",
                "reply": "No speech detected."
            }), 400

        result = ChatService.process_message(transcript)

        result["heard"] = transcript

        return jsonify(result), 200

    except Exception:

        logger.exception("Glasses Voice Route Error")

        return jsonify({
            "status": "error",
            "reply": "Voice processing failed."
        }), 500


@glasses_bp.route("/glasses/vision", methods=["POST"])
def glasses_vision():
    """
    Vision endpoint for SRG AI Glasses.
    """

    try:

        if "image" not in request.files:

            return jsonify({
                "status": "error",
                "reply": "No image received."
            }), 400

        image = request.files["image"]

        if image.filename == "":

            return jsonify({
                "status": "error",
                "reply": "No image selected."
            }), 400

        logger.info("Image received from SRG Glasses.")

        result = ImageService.analyze_image(image)

        return jsonify(result), 200

    except Exception:

        logger.exception("Glasses Vision Route Error")

        return jsonify({
            "status": "error",
            "reply": "Image processing failed."
        }), 500