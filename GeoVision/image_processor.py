import os
import uuid
from PIL import Image
import numpy as np
from app import app

def process_uploaded_image(file, original_filename):
    """Process uploaded image: resize, optimize, and save"""
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        processed_filename = f"{file_id}.jpg"  # Always save as JPEG
        
        # Full path for saving
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        
        # Open and process image
        image = Image.open(file.stream)
        
        # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to 800x600 while maintaining aspect ratio
        image.thumbnail((800, 600), Image.Resampling.LANCZOS)
        
        # Create a new 800x600 image with black background
        new_image = Image.new('RGB', (800, 600), (0, 0, 0))
        
        # Center the resized image
        x = (800 - image.width) // 2
        y = (600 - image.height) // 2
        new_image.paste(image, (x, y))
        
        # Save with JPEG compression at 85% quality
        new_image.save(upload_path, 'JPEG', quality=85, optimize=True)
        
        # Get file size
        file_size = os.path.getsize(upload_path)
        
        return processed_filename, file_size, 'image/jpeg'
        
    except Exception as e:
        app.logger.error(f"Image processing error: {str(e)}")
        raise Exception(f"Failed to process image: {str(e)}")

def generate_feature_vector():
    """Generate a mock 512-dimensional feature vector for similarity matching"""
    # In production, this would use a real AI model like ResNet50 or Vision Transformer
    return np.random.rand(512).tolist()
