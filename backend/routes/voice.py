"""
=========================================================
SRG AI - Voice Routes
=========================================================
Handles Speech-to-Text requests for SRG AI.
"""

import time

from flask import Blueprint, jsonify, request

from backend.services.chat_service import ChatService
from backend.services.deepgram_service import DeepgramService
from backend.utils.logger import logger


voice_bp = Blueprint("voice", __name__)


# =========================================================
# Health Check
# =========================================================

@voice_bp.route("/glasses_voice", methods=["GET"])
def voice_status():

    return jsonify({
        "status": "online",
        "service": "SRG AI Voice API",
        "message": "Voice API is running."
    }), 200


# =========================================================
# Voice Processing
# =========================================================

@voice_bp.route("/glasses_voice", methods=["POST"])
def glasses_voice():

    start_time = time.time()

    try:

        # ---------------------------------------------
        # Validate Request
        # ---------------------------------------------

        if "audio" not in request.files:

            return jsonify({
                "status": "error",
                "reply": "No audio file uploaded. Use form-data with key 'audio'."
            }), 400

        audio = request.files["audio"]

        if audio.filename == "":

            return jsonify({
                "status": "error",
                "reply": "No audio file selected."
            }), 400

        # ---------------------------------------------
        # Validate Extension
        # ---------------------------------------------

        allowed_extensions = (
            ".wav",
            ".mp3",
            ".m4a",
            ".ogg",
            ".webm",
            ".aac",
            ".flac"
        )

        filename = audio.filename.lower()

        if not filename.endswith(allowed_extensions):

            return jsonify({
                "status": "error",
                "reply": "Unsupported audio format."
            }), 400

        audio_data = audio.read()

        if len(audio_data) == 0:

            return jsonify({
                "status": "error",
                "reply": "Uploaded audio is empty."
            }), 400

        logger.info(f"Voice Request: {audio.filename}")

        # ---------------------------------------------
        # Speech To Text
        # ---------------------------------------------

        transcript = DeepgramService.transcribe_audio(audio_data)

        if transcript is None:

            return jsonify({
                "status": "error",
                "reply": "Speech recognition failed."
            }), 500

        transcript = transcript.strip()

        if transcript == "":

            return jsonify({
                "status": "error",
                "reply": "No speech detected."
            }), 400

        logger.info(f"Transcript: {transcript}")

        # ---------------------------------------------
        # AI Response
        # ---------------------------------------------

        result = ChatService.process_message(transcript)

        if not isinstance(result, dict):

            result = {
                "status": "success",
                "reply": str(result)
            }

        result["heard"] = transcript
        result["processing_time"] = round(time.time() - start_time, 2)

        logger.info("Voice request completed successfully.")

        return jsonify(result), 200

    except Exception as e:

        logger.exception("Voice Route Error")

        return jsonify({
            "status": "error",
            "reply": "Voice processing failed.",
            "details": str(e)
        }), 500