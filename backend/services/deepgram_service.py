"""
=========================================================
SRG AI - Deepgram Service
=========================================================
Handles Speech-to-Text using Deepgram.
"""

import requests

from backend.config import Config
from backend.utils.logger import logger


class DeepgramService:

    @staticmethod
    def transcribe(audio_data):
        """
        Convert WAV audio into text using Deepgram.
        """

        if not Config.DEEPGRAM_API_KEY:
            raise RuntimeError("Deepgram API key is not configured.")

        if not audio_data:
            raise ValueError("Audio data is empty.")

        headers = {
            "Authorization": f"Token {Config.DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav"
        }

        url = (
            "https://api.deepgram.com/v1/listen"
            f"?model={Config.DEEPGRAM_MODEL}"
            "&smart_format=true"
        )

        try:

            logger.info("Sending audio to Deepgram...")

            response = requests.post(
                url=url,
                headers=headers,
                data=audio_data,
                timeout=60
            )

            logger.info(
                f"Deepgram Status: {response.status_code}"
            )

            if response.status_code != 200:

                logger.error(response.text)

                raise RuntimeError(
                    f"Deepgram request failed ({response.status_code})"
                )

            data = response.json()

            transcript = (
                data.get("results", {})
                    .get("channels", [{}])[0]
                    .get("alternatives", [{}])[0]
                    .get("transcript", "")
                    .strip()
            )

            if not transcript:

                logger.warning("No speech detected.")

                return ""

            logger.info(f"Transcript: {transcript}")

            return transcript

        except requests.exceptions.Timeout:

            logger.error("Deepgram request timed out.")

            raise RuntimeError(
                "Deepgram request timed out."
            )

        except requests.exceptions.RequestException as e:

            logger.error(str(e))

            raise RuntimeError(
                "Unable to connect to Deepgram."
            )

        except Exception as e:

            logger.error(str(e))

            raise