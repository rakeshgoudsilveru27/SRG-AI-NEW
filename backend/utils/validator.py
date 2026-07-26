"""
=========================================================
SRG AI - Validators
=========================================================
"""

from pathlib import Path

from backend.config import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_AUDIO_EXTENSIONS
)


class Validator:

    @staticmethod
    def allowed_image(filename):

        return (
            "." in filename
            and
            filename.rsplit(".",1)[1].lower()
            in ALLOWED_IMAGE_EXTENSIONS
        )

    @staticmethod
    def allowed_audio(filename):

        return (
            "." in filename
            and
            filename.rsplit(".",1)[1].lower()
            in ALLOWED_AUDIO_EXTENSIONS
        )

    @staticmethod
    def file_exists(path):

        return Path(path).exists()
    