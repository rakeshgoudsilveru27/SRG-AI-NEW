"""
=========================================================
SRG AI - Chat Service
=========================================================
Processes all chat requests.
"""

from backend.prompts import SYSTEM_PROMPT
from backend.services.gemini_service import GeminiService
from backend.services.weather_service import WeatherService
from backend.services.wikipedia_service import WikipediaService
from backend.utils.logger import logger


class ChatService:

    @staticmethod
    def process(user_message, history=""):
        """
        Process incoming user messages and return a response.
        """

        # -------------------------------------------------
        # Validate Input
        # -------------------------------------------------

        message = (user_message or "").strip()

        if not message:
            return {
                "status": "error",
                "reply": "Please enter a message.",
                "title": "New Chat"
            }

        logger.info(f"User Message: {message}")

        lower = message.lower()

        # -------------------------------------------------
        # Weather Intent
        # -------------------------------------------------

        weather_keywords = [
            "weather",
            "temperature",
            "forecast",
            "humidity",
            "rain",
            "hot",
            "cold"
        ]

        if any(word in lower for word in weather_keywords):

            city = ChatService.extract_city(lower)

            if city:

                try:

                    if "tomorrow" in lower:

                        reply = WeatherService.get_tomorrow_weather(city)

                    else:

                        reply = WeatherService.get_weather(city)

                    return {
                        "status": "success",
                        "reply": reply,
                        "title": f"Weather - {city.title()}"
                    }

                except Exception as e:

                    logger.error(str(e))

                    return {
                        "status": "error",
                        "reply": "Unable to fetch weather information.",
                        "title": "Weather"
                    }

        # -------------------------------------------------
        # Wikipedia Intent
        # -------------------------------------------------

        wiki_keywords = [
            "who is",
            "what is",
            "tell me about",
            "history of",
            "information about",
            "wikipedia"
        ]

        if any(keyword in lower for keyword in wiki_keywords):

            try:

                wiki = WikipediaService.get_summary(message)

                if wiki:

                    return {
                        "status": "success",
                        "reply": wiki,
                        "title": " ".join(message.split()[:5])
                    }

            except Exception as e:

                logger.error(str(e))

        # -------------------------------------------------
        # Gemini AI
        # -------------------------------------------------

        prompt = f"""
{SYSTEM_PROMPT}

Conversation:

{history}

User:

{message}

Assistant:
"""

        try:

            reply = GeminiService.generate_text(prompt)
            
            logger.info("Gemini response generated successfully.")

            return {
                "status": "success",
                "reply": reply,
                "title": " ".join(message.split()[:5])
            }

        except Exception as e:

            logger.error(str(e))

            return {
                "status": "error",
                "reply": "Sorry, I couldn't process your request right now.",
                "title": "Error"
            }

    @staticmethod
    def extract_city(message):
        """
        Extract supported city names from the message.
        """

        cities = [
            "hyderabad",
            "mumbai",
            "delhi",
            "bangalore",
            "bengaluru",
            "chennai",
            "kolkata",
            "pune",
            "ahmedabad",
            "surat",
            "jaipur",
            "lucknow",
            "kanpur",
            "nagpur",
            "visakhapatnam",
            "vijayawada",
            "warangal",
            "tirupati",
            "mysore",
            "coimbatore",
            "kochi"
        ]

        for city in cities:

            if city in message:

                return city

        return None