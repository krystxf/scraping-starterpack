"""Flask route handlers"""
from flask import jsonify, request
from PIL import Image
import io
from src.config import logger, DEFAULT_EXTRACTION_PROMPT
from src.model_loader import model_manager
from src.text_extractor import extract_text_from_image


def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/', methods=['GET'])
    def hello():
        return jsonify({
            "message": "Text extraction API is running. Use POST /extract-text to extract text from images."
        })
    
    @app.route('/health', methods=['GET'])
    def health():
        model_status = "loaded" if model_manager.is_loaded() else "not_loaded"
        return jsonify({
            "status": "healthy",
            "model": model_status,
            "device": str(model_manager.device) if model_manager.device else "unknown"
        })
    
    @app.route('/extract-text', methods=['POST'])
    def extract_text():
        """Extract text from an uploaded image"""
        if not model_manager.is_loaded():
            return jsonify({"error": "Model not initialized"}), 500
        
        try:
            # Check if image is in request
            if 'image' not in request.files:
                return jsonify({
                    "error": "No image file provided. Please upload an image using the 'image' field."
                }), 400
            
            image_file = request.files['image']
            if image_file.filename == '':
                return jsonify({"error": "Empty image file"}), 400
            
            # Read and process image
            image_bytes = image_file.read()
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            # Get optional custom prompt from request
            custom_prompt = request.form.get('prompt', None)
            
            # Extract text
            logger.info(f"Processing image: {image_file.filename} (size: {image.size})")
            extracted_text = extract_text_from_image(image, prompt=custom_prompt)
            
            return jsonify({
                "success": True,
                "text": extracted_text,
                "prompt": custom_prompt if custom_prompt else DEFAULT_EXTRACTION_PROMPT
            })
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({"error": f"Error processing image: {str(e)}"}), 500

