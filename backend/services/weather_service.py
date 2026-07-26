"""
=========================================================
SRG AI - Weather Service
=========================================================
Handles current and tomorrow weather using OpenWeather API.
"""

import requests

from backend.config import Config
from backend.utils.logger import logger


class WeatherService:

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    @staticmethod
    def get_weather(city):
        """
        Get current weather for a city.
        """

        if not Config.WEATHER_API_KEY:
            raise RuntimeError("OpenWeather API key is not configured.")

        try:

            logger.info(f"Getting current weather for {city}")

            url = (
                f"{WeatherService.BASE_URL}/weather"
                f"?q={city}"
                f"&appid={Config.WEATHER_API_KEY}"
                f"&units=metric"
            )

            response = requests.get(
                url,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            weather = data["weather"][0]["description"].title()

            temperature = data["main"]["temp"]

            feels_like = data["main"]["feels_like"]

            humidity = data["main"]["humidity"]

            wind_speed = data["wind"]["speed"]

            return (
                f"Current weather in {city.title()}:\n\n"
                f"🌤 Weather: {weather}\n"
                f"🌡 Temperature: {temperature}°C\n"
                f"🤗 Feels Like: {feels_like}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬 Wind Speed: {wind_speed} m/s"
            )

        except requests.exceptions.HTTPError:

            logger.error(f"City not found: {city}")

            return "Sorry, I couldn't find that city."

        except requests.exceptions.Timeout:

            logger.error("Weather request timed out.")

            return "Weather service timed out."

        except requests.exceptions.RequestException as e:

            logger.error(str(e))

            return "Unable to connect to the weather service."

        except Exception as e:

            logger.error(str(e))

            return "Unable to retrieve weather information."

    @staticmethod
    def get_tomorrow_weather(city):
        """
        Get tomorrow's weather forecast.
        """

        if not Config.WEATHER_API_KEY:
            raise RuntimeError("OpenWeather API key is not configured.")

        try:

            logger.info(f"Getting tomorrow forecast for {city}")

            url = (
                f"{WeatherService.BASE_URL}/forecast"
                f"?q={city}"
                f"&appid={Config.WEATHER_API_KEY}"
                f"&units=metric"
            )

            response = requests.get(
                url,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            if len(data["list"]) < 8:

                return "Tomorrow's forecast is unavailable."

            forecast = data["list"][7]

            weather = forecast["weather"][0]["description"].title()

            temperature = forecast["main"]["temp"]

            humidity = forecast["main"]["humidity"]

            wind_speed = forecast["wind"]["speed"]

            return (
                f"Tomorrow's weather in {city.title()}:\n\n"
                f"🌤 Weather: {weather}\n"
                f"🌡 Temperature: {temperature}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬 Wind Speed: {wind_speed} m/s"
            )

        except requests.exceptions.HTTPError:

            logger.error(f"City not found: {city}")

            return "Sorry, I couldn't find that city."

        except requests.exceptions.Timeout:

            logger.error("Forecast request timed out.")

            return "Weather service timed out."

        except requests.exceptions.RequestException as e:

            logger.error(str(e))

            return "Unable to connect to the weather service."

        except Exception as e:

            logger.error(str(e))

            return "Unable to retrieve tomorrow's weather."