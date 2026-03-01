# pyright: reportUnusedFunction=false

from __future__ import annotations

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from web.routes.observations import bp as observations_bp
from web.routes.targets import bp as targets_bp


def create_app() -> Flask:
    """Create and configure the Flask app with registered blueprints."""
    app = Flask(__name__)

    # --- Middleware ---
    # Tells Flask it is behind a proxy (Coolify/Traefik).
    # This ensures url_for() and redirects use https:// automatically.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # --- Blueprints ---
    app.register_blueprint(targets_bp)
    app.register_blueprint(observations_bp)

    # --- Root route ---
    @app.route("/")
    def index():
        """Render the dashboard/home page using the base layout."""
        return render_template("base.html")

    return app
