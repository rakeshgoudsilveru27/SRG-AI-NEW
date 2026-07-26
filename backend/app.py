from pathlib import Path

from flask import Flask, jsonify, render_template

from backend.config import Config

# =========================
# Blueprints
# =========================
from backend.routes.chat import chat_bp
from backend.routes.voice import voice_bp
from backend.routes.vision import vision_bp
from backend.routes.weather import weather_bp
from backend.routes.health import health_bp
from backend.routes.glasses import glasses_bp

# =========================
# Logger
# =========================
from backend.utils.logger import logger


def create_app():
    """
    Create and configure the SRG.ai Flask application.
    """

    # =====================================================
    # Base Directory
    # =====================================================
    BASE_DIR = Path(__file__).resolve().parent.parent

    # =====================================================
    # Flask Application
    # =====================================================
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "frontend" / "templates"),
        static_folder=str(BASE_DIR / "frontend" / "static")
    )

    # =====================================================
    # Configuration
    # =====================================================
    app.config.from_object(Config)

    # =====================================================
    # Home
    # =====================================================
    @app.route("/", methods=["GET"])
    def home():
        return render_template("login.html")

    # =====================================================
    # Chat Page
    # =====================================================
    @app.route("/chat", methods=["GET"])
    def chat():
        return render_template("index.html")

    # =====================================================
    # Ping
    # =====================================================
    @app.route("/ping", methods=["GET"])
    def ping():
        return jsonify({
            "success": True,
            "status": "online",
            "name": "SRG.ai",
            "device": "SRG AI Server",
            "version": Config.APP_VERSION
        })

    # =====================================================
    # Health Check
    # =====================================================
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "success": True,
            "status": "healthy"
        })

    # =====================================================
    # Register API Blueprints
    # =====================================================
    blueprints = [
        chat_bp,
        voice_bp,
        vision_bp,
        weather_bp,
        health_bp,
        glasses_bp
    ]

    for blueprint in blueprints:
        app.register_blueprint(
            blueprint,
            url_prefix="/api"
        )

    # =====================================================
    # Error Handlers
    # =====================================================
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint not found."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": "Method not allowed."
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.exception(error)

        return jsonify({
            "success": False,
            "error": "Internal Server Error"
        }), 500

    # =====================================================
    # Startup Logs
    # =====================================================
    logger.info("=" * 60)
    logger.info("SRG.ai Backend Started")
    logger.info("=" * 60)
    logger.info(f"Version   : {Config.APP_VERSION}")
    logger.info(f"Host      : {Config.HOST}")
    logger.info(f"Port      : {Config.PORT}")
    logger.info(f"Debug     : {Config.DEBUG}")
    logger.info(f"Templates : {app.template_folder}")
    logger.info(f"Static    : {app.static_folder}")
    logger.info("=" * 60)

    return app


# =====================================================
# Application Instance
# =====================================================
app = create_app()


# =====================================================
# Run Server
# =====================================================
if __name__ == "__main__":

    logger.info("Starting SRG.ai Server...")

    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        threaded=True
    )