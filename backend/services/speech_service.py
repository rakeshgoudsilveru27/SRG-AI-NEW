"""
=========================================================
SRG AI - Speech Service
=========================================================
Converts text to speech using Deepgram TTS.
"""

import requests

from backend.config import Config
from backend.utils.logger import logger


class SpeechService:

    BASE_URL = "https://api.deepgram.com/v1/speak"

    @staticmethod
    def text_to_speech(text):
        """
        Convert text into speech using Deepgram TTS.

        Returns:
            bytes: Audio data
            None: If conversion fails
        """

        if not text or not text.strip():
            return None

        if not Config.DEEPGRAM_API_KEY:
            raise RuntimeError("Deepgram API Key is not configured.")

        try:

            logger.info("Generating speech using Deepgram...")

            headers = {
                "Authorization": f"Token {Config.DEEPGRAM_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "text": text
            }

            params = {
                "model": "aura-2-thalia-en"
            }

            response = requests.post(
                SpeechService.BASE_URL,
                headers=headers,
                params=params,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            logger.info("Speech generated successfully.")

            return response.content

        except requests.exceptions.Timeout:

            logger.error("Speech generation timed out.")

            return None

        except requests.exceptions.RequestException as e:

            logger.error(str(e))

            return None

        except Exception:

            logger.exception("Speech Service Error")

            return None