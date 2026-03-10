"""Text extraction logic using the loaded model"""
import torch
from src.config import DEFAULT_EXTRACTION_PROMPT, MAX_NEW_TOKENS
from src.model_loader import model_manager


def extract_text_from_image(image, prompt=None):
    """Extract text from an image using the loaded model"""
    if not model_manager.is_loaded():
        raise RuntimeError("Model not initialized")
    
    # Use custom prompt or default text extraction prompt
    if prompt is None:
        prompt = DEFAULT_EXTRACTION_PROMPT
    
    # Prepare messages for text extraction
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt}
            ]
        }
    ]
    
    # Process inputs
    inputs = model_manager.processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    )
    
    # Move inputs to the same device as the model
    inputs = inputs.to(model_manager.model.device)
    
    # Generate response
    with torch.no_grad():
        generated_ids = model_manager.model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = model_manager.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )
    
    return output_text[0] if output_text else ""

