from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from functools import wraps
from flask import request, Response
import logging

# Initialize Prometheus metrics
exception_counter_by_endpoint = Counter(
    'api_exceptions_total',
    'Total number of exceptions raised by API endpoint',
    ['endpoint', 'method', 'exception_type']
)

total_exceptions_counter = Counter(
    'api_exceptions_sum_total',
    'Total sum of all exceptions raised across all endpoints'
)

def track_exceptions(f):
    """Decorator to track exceptions per endpoint"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            endpoint = request.endpoint or 'unknown'
            method = request.method
            exception_type = type(e).__name__
            
            # Log the exception
            logging.error(f"Exception in {endpoint} ({method}): {exception_type} - {str(e)}")
            
            # Increment metrics
            exception_counter_by_endpoint.labels(
                endpoint=endpoint,
                method=method,
                exception_type=exception_type
            ).inc()
            
            total_exceptions_counter.inc()
            
            raise
    return decorated_function

def get_metrics():
    """Generate Prometheus metrics"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)