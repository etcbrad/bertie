#!/usr/bin/env python3
import cv2
import numpy as np
import os
from PIL import Image
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "Bertie Assets" / "bones"

# Image processing constants
DEFAULT_REGIONS = {
    1: (0.05, 0.05, 0.25, 0.35),    # Head
    2: (0.35, 0.05, 0.30, 0.35),    # Torso  
    3: (0.70, 0.05, 0.25, 0.25),    # Right Upper Arm
    4: (0.70, 0.35, 0.25, 0.25),    # Right Lower Arm
    5: (0.05, 0.45, 0.25, 0.25),    # Left Upper Arm
    6: (0.05, 0.75, 0.25, 0.20),    # Left Lower Arm
    7: (0.35, 0.45, 0.30, 0.25),    # Right Upper Leg
    8: (0.35, 0.75, 0.30, 0.20),    # Right Lower Leg + Foot
    9: (0.70, 0.65, 0.25, 0.30),    # Left Upper Leg
    10: (0.70, 0.95, 0.25, 0.05)    # Left Lower Leg + Foot
}

def validate_image_path(image_path):
    """Validate that the image file exists and is readable"""
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not read image file: {image_path}")
        return img
    except Exception as e:
        raise ValueError(f"Error loading image {image_path}: {str(e)}")
def analyze_and_cut_parts(image_path, prefix, regions=None):
    """
    Analyze the image and cut it into 10 parts based on the annotated sheet
    
    Args:
        image_path: Path to input image
        prefix: Prefix for output files
        regions: Custom region definitions (optional)
    """
    # Validate and load image
    img = validate_image_path(image_path)
    height, width = img.shape[:2]
    print(f"Image size: {width}x{height}")
    
    # Use default or custom regions
    regions = regions or DEFAULT_REGIONS
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Cut each part
    for part_num, (x_pct, y_pct, w_pct, h_pct) in regions.items():
        x = int(x_pct * width)
        y = int(y_pct * height)
        w = int(w_pct * width)
        h = int(h_pct * height)
        
        # Ensure we don't go out of bounds
        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))
        w = max(1, min(w, width - x))
        h = max(1, min(h, height - y))
        
        # Extract the part
        part = img[y:y+h, x:x+w]
        
        # Save the part
        output_path = OUTPUT_DIR / f"{prefix}_part_{part_num:02d}.png"
        cv2.imwrite(str(output_path), part)
        print(f"Saved part {part_num} to {output_path}")

def process_anchor_holes(image_path, prefix, min_radius=5, max_radius=15):
    """
    Process anchor holes - eliminate paper but preserve ink that impedes holes
    
    Args:
        image_path: Path to input image
        prefix: Prefix for output files
        min_radius: Minimum anchor hole radius
        max_radius: Maximum anchor hole radius
    """
    # Validate and load image
    img = validate_image_path(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find circular regions (anchor holes) using Hough Circle Transform
    circles = cv2.HoughCircles(
        gray, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=20,
        param1=50,
        param2=30, 
        minRadius=5,
        maxRadius=15
    )
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # Process each circle (anchor hole)
        for (x, y, r) in circles:
            # Create a mask for the circle
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)
            
            # Find edges within the circle region
            edges = cv2.Canny(gray, 50, 150)
            edges_in_circle = cv2.bitwise_and(edges, edges, mask=mask)
            
            # Create a transparent hole but preserve ink edges
            # This is a simplified approach - we'd need more sophisticated processing
            # to preserve only the ink that impedes the hole
            
            # For now, let's just mark these regions
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)  # Green circles for debugging
    
    # Save the processed image with marked anchor holes
    output_path = OUTPUT_DIR / f"{prefix}_anchor_holes_marked.png"
    cv2.imwrite(str(output_path), img)
    print(f"Saved anchor hole analysis to {output_path}")

if __name__ == "__main__":
    # Define images to process
    images = [
        ("TheAstonishingOfAPenAndInkPuppet_0010.png", "main"),
        ("annotated_cutout_sheet (1).png", "annotated")
    ]
    
    for image_file, prefix in images:
        image_path = PROJECT_ROOT / image_file
        
        if not image_path.exists():
            print(f"Warning: Image file not found: {image_path}")
            continue
            
        print(f"Processing {image_file}...")
        try:
            analyze_and_cut_parts(image_path, prefix)
            process_anchor_holes(image_path, prefix)
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
            continue
