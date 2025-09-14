from flask import Blueprint, jsonify
from app.services.product_service import ProductService
from app.metrics import track_exceptions

product_blueprint = Blueprint('product_blueprint', __name__)
product_service = ProductService()

@product_blueprint.route('/products', methods=['GET'])
@track_exceptions
def get_products():
    products = product_service.get_products()
    return jsonify(products), 200

@product_blueprint.route('/products/<int:product_id>', methods=['GET'])
@track_exceptions
def get_product(product_id):
    product = product_service.get_product_by_id(product_id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"message": "Product not found"}), 404

@product_blueprint.route('/products/<int:product_id>/error', methods=['GET'])
@track_exceptions
def simulate_product_error(product_id):
    """Endpoint that demonstrates exception handling"""
    if product_id == 999:
        raise ConnectionError("Database connection failed")
    elif error_type == "key":
        raise KeyError("Product not found in catalog")
    else:
        return jsonify({"message": f"Product {product_id} processed successfully"}), 200
