"""
=========================================================
SRG AI - Configuration File
=========================================================
Loads all environment variables and project settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------------
# Base Directory
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# Load .env
# -------------------------------------------------------

load_dotenv(BASE_DIR / ".env")

# -------------------------------------------------------
# Flask Settings
# -------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")

DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

HOST = os.getenv("HOST", "0.0.0.0")

PORT = int(os.getenv("PORT", 5000))

# -------------------------------------------------------
# Upload & Storage Settings
# -------------------------------------------------------

UPLOAD_FOLDER = BASE_DIR / "uploads"

TEMP_FOLDER = BASE_DIR / "temp"

LOG_FOLDER = BASE_DIR / "logs"

MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

ALLOWED_IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
}

ALLOWED_AUDIO_EXTENSIONS = {
    "wav",
}

# -------------------------------------------------------
# API Keys
# -------------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# -------------------------------------------------------
# Gemini API Keys
# -------------------------------------------------------

GEMINI_API_KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY1"),
    os.getenv("GEMINI_API_KEY2"),
    os.getenv("GEMINI_API_KEY3"),
]

# Remove empty keys
GEMINI_API_KEYS = [
    key.strip()
    for key in GEMINI_API_KEYS
    if key and key.strip()
]
# -------------------------------------------------------
# Gemini Models
# -------------------------------------------------------

GEMINI_MODEL = "gemini-2.5-flash"

GEMINI_VISION_MODEL = "gemini-2.5-flash"

# -------------------------------------------------------
# Deepgram
# -------------------------------------------------------

DEEPGRAM_MODEL = "nova-3"

# -------------------------------------------------------
# Groq Models
# -------------------------------------------------------

GROQ_SMALL_MODEL = "llama-3.1-8b-instant"

GROQ_LARGE_MODEL = "llama-3.3-70b-versatile"

# -------------------------------------------------------
# Conversation
# -------------------------------------------------------

MAX_HISTORY = 20

# -------------------------------------------------------
# Logging
# -------------------------------------------------------

LOG_LEVEL = "INFO"

LOG_FILE = LOG_FOLDER / "server.log"

# -------------------------------------------------------
# App Information
# -------------------------------------------------------

APP_NAME = "SRG AI"

APP_VERSION = "2.0"

DEVICE_NAME = "SRG AI Glasses"

# -------------------------------------------------------
# Create Required Directories
# -------------------------------------------------------

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

TEMP_FOLDER.mkdir(parents=True, exist_ok=True)

LOG_FOLDER.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# Flask Config Class
# -------------------------------------------------------

class Config:
    # Flask
    SECRET_KEY = SECRET_KEY
    DEBUG = DEBUG
    HOST = HOST
    PORT = PORT

    # App Info
    APP_NAME = APP_NAME
    APP_VERSION = APP_VERSION
    DEVICE_NAME = DEVICE_NAME

    # Directories
    BASE_DIR = str(BASE_DIR)
    UPLOAD_FOLDER = str(UPLOAD_FOLDER)
    TEMP_FOLDER = str(TEMP_FOLDER)
    LOG_FOLDER = str(LOG_FOLDER)

    # Upload Limits
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
    ALLOWED_IMAGE_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS
    ALLOWED_AUDIO_EXTENSIONS = ALLOWED_AUDIO_EXTENSIONS

    # Gemini
    GEMINI_API_KEYS = GEMINI_API_KEYS
    GEMINI_MODEL = GEMINI_MODEL
    GEMINI_VISION_MODEL = GEMINI_VISION_MODEL

    # Groq
    GROQ_API_KEY = GROQ_API_KEY
    GROQ_SMALL_MODEL = GROQ_SMALL_MODEL
    GROQ_LARGE_MODEL = GROQ_LARGE_MODEL

    # Deepgram
    DEEPGRAM_API_KEY = DEEPGRAM_API_KEY
    DEEPGRAM_MODEL = DEEPGRAM_MODEL

    # Weather
    WEATHER_API_KEY = OPENWEATHER_API_KEY

    # Conversation
    MAX_HISTORY = MAX_HISTORY

    # Logging
    LOG_LEVEL = LOG_LEVEL
    LOG_FILE = str(LOG_FILE)