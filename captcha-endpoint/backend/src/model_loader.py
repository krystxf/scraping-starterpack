"""Model loading and initialization logic"""
import torch
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
from src.config import logger, MODEL_NAME


class ModelManager:
    """Manages the model, processor, and device state"""
    
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = None
    
    def get_device(self):
        """Determine the best available device"""
        if torch.backends.mps.is_available():
            device = torch.device("mps")
            logger.info("Using MPS (Metal Performance Shaders) for M4 Mac optimization")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
            logger.info("Using CUDA")
        else:
            device = torch.device("cpu")
            logger.info("Using CPU")
        return device
    
    def initialize(self):
        """Initialize the model locally"""
        self.device = self.get_device()
        
        try:
            # Load processor
            logger.info("Loading processor...")
            self.processor = AutoProcessor.from_pretrained(
                MODEL_NAME,
                trust_remote_code=True,
                local_files_only=False
            )
            logger.info("Processor loaded successfully!")
            
            # Load model
            logger.info("Loading model weights (this may take a few minutes on first run)...")
            if self.device.type == "mps":
                # For MPS, use float16 for better performance
                self.model = Qwen3VLForConditionalGeneration.from_pretrained(
                    MODEL_NAME,
                    dtype=torch.float16,
                    device_map=None,  # We'll move manually for MPS
                    trust_remote_code=True,
                    local_files_only=False
                )
                logger.info("Moving model to MPS device...")
                self.model = self.model.to(self.device)
            else:
                # For CPU/CUDA, use auto device_map
                self.model = Qwen3VLForConditionalGeneration.from_pretrained(
                    MODEL_NAME,
                    dtype="auto",
                    device_map="auto",
                    trust_remote_code=True,
                    local_files_only=False
                )
            
            self.model.eval()
            logger.info(f"Model loaded successfully and running locally on {self.device}")
            logger.info("Model is ready for inference!")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            import traceback
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            raise
    
    def is_loaded(self):
        """Check if model and processor are loaded"""
        return self.model is not None and self.processor is not None


# Global model manager instance
model_manager = ModelManager()

