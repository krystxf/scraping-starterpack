"""Main Flask application entry point"""
import socket
from flask import Flask
from src.config import logger, DEFAULT_HOST, DEFAULT_PORT
from src.model_loader import model_manager
from src.routes import register_routes

app = Flask(__name__)

# Register all routes
register_routes(app)


def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to a remote address to determine local IP
        # This doesn't actually send data, just determines the route
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # Connect to a non-routable address
            s.connect(('10.254.254.254', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    except Exception:
        return '127.0.0.1'


if __name__ == '__main__':
    logger.info("Starting Qwen3-VL-2B-Instruct text extraction API...")
    logger.info("This will download the model on first run (~8GB)")
    logger.info("")
    
    # Initialize model on startup
    try:
        model_manager.initialize()
    except Exception as e:
        logger.error(f"Failed to initialize model: {str(e)}")
        logger.warning("Server will start but /extract-text endpoint will not work")
    
    local_ip = get_local_ip()
    logger.info(f"Starting Flask server on http://{DEFAULT_HOST}:{DEFAULT_PORT}")
    logger.info(f"Server is accessible on your local network at: http://{local_ip}:{DEFAULT_PORT}")
    logger.info(f"Also accessible locally at: http://localhost:{DEFAULT_PORT}")
    logger.info("")
    logger.info("If you cannot connect from other devices, check macOS Firewall settings:")
    logger.info("  System Settings > Network > Firewall > Options")
    logger.info("  Make sure Python is allowed to accept incoming connections")
    logger.info("")
    
    app.run(debug=True, host=DEFAULT_HOST, port=DEFAULT_PORT, use_reloader=False)
