
from flask import Flask
from app.routes.user_routes import user_blueprint
from app.routes.product_routes import product_blueprint
from app.metrics import get_metrics

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(user_blueprint)
    app.register_blueprint(product_blueprint)
    
    # Add metrics endpoint
    @app.route('/metrics')
    def metrics():
        return get_metrics()
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {"status": "healthy"}, 200

    return app
