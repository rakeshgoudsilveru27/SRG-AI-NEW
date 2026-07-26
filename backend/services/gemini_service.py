from google import genai

from backend.config import Config
from backend.utils.logger import logger


class GeminiService:

    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = genai.Client(
                api_key=Config.GEMINI_API_KEYS[0]
            )
        return cls._client

    @classmethod
    def generate_text(cls, prompt):

        try:

            client = cls.get_client()

            response = client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=prompt
            )

            return response.text.strip()

        except Exception as e:
            print("\n========== GEMINI ERROR ==========")
            print(type(e).__name__)
            print(str(e))
            print("==================================\n")

            logger.exception("Gemini Text Generation Failed")

            return "Sorry, I couldn't generate a response right now."

    @classmethod
    def generate_image(cls, image, prompt):

        try:

            client = cls.get_client()

            response = client.models.generate_content(
                model=Config.GEMINI_VISION_MODEL,
                contents=[
                    prompt,
                    image
                ]
            )

            return response.text.strip()

        except Exception:

            logger.exception("Gemini Vision Failed")

            return (
                "Sorry, I couldn't understand the image."
            )