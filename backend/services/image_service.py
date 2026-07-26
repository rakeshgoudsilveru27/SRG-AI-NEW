"""
=========================================================
SRG AI - Image Service
=========================================================
Handles image processing using Gemini Vision.
"""

from PIL import Image

from backend.prompts import VISION_PROMPT
from backend.services.gemini_service import GeminiService
from backend.utils.logger import logger


class ImageService:

    @staticmethod
    def analyze_image(image_file):
        """
        Analyze an uploaded image using Gemini Vision.
        """

        if image_file is None:
            raise ValueError("Image file is required.")

        try:

            logger.info("Opening uploaded image...")

            image = Image.open(image_file)

            logger.info("Sending image to Gemini Vision...")

            response = GeminiService.generate_image(
                VISION_PROMPT,
                image
            )

            logger.info("Image analysis completed.")

            return {

                "status": "success",

                "reply": response

            }

        except Exception as e:

            logger.exception("Image Service Error")

            return {

                "status": "error",

                "reply": "Unable to analyze image."

            }