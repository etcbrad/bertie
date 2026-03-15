#!/usr/bin/env python3
import cv2
import numpy as np
import os
from PIL import Image

def precise_cut_parts(image_path, output_dir, prefix):
    """
    More precise cutting based on the actual layout visible in the annotated sheet
    """
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load {image_path}")
        return
    
    height, width = img.shape[:2]
    print(f"Processing {image_path}: {width}x{height}")
    
    # Based on the annotated sheet layout, I can see:
    # Top row: Head (1), Torso (2), Right arm segments (3,4)
    # Middle row: Left arm segments (5,6), Right leg segments (7,8)
    # Bottom row: Left leg segments (9,10) and some additional pieces
    
    # More precise region definitions based on the actual layout
    regions = {
        1: (0.02, 0.02, 0.28, 0.32),    # Head (top left)
        2: (0.32, 0.02, 0.36, 0.32),    # Torso (top center)
        3: (0.70, 0.02, 0.28, 0.18),    # Right Upper Arm (top right)
        4: (0.70, 0.22, 0.28, 0.18),    # Right Lower Arm (top right, below)
        5: (0.02, 0.36, 0.28, 0.18),    # Left Upper Arm (middle left)
        6: (0.02, 0.56, 0.28, 0.18),    # Left Lower Arm (middle left, below)
        7: (0.32, 0.36, 0.36, 0.22),    # Right Upper Leg (center)
        8: (0.32, 0.60, 0.36, 0.22),    # Right Lower Leg + Foot (center, below)
        9: (0.70, 0.42, 0.28, 0.25),    # Left Upper Leg (right side)
        10: (0.70, 0.69, 0.28, 0.25)    # Left Lower Leg + Foot (right side, below)
    }
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Cut each part with better edge detection
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
        
        # Apply edge detection to clean up the edges
        gray = cv2.cvtColor(part, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours to get better boundaries
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour (should be our main part)
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Add some padding
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(part.shape[1] - x, w + 2 * padding)
            h = min(part.shape[0] - y, h + 2 * padding)
            
            # Re-extract with better bounds
            part = part[y:y+h, x:x+w]
        
        # Save the part
        output_path = os.path.join(output_dir, f"{prefix}_part_{part_num:02d}_precise.png")
        cv2.imwrite(output_path, part)
        print(f"Saved precise part {part_num} to {output_path}")

def process_anchor_holes_advanced(image_path, output_dir, prefix):
    """
    Advanced anchor hole processing - eliminate paper but preserve ink that impedes holes
    """
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load {image_path}")
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find circular regions (anchor holes) using multiple methods
    circles = cv2.HoughCircles(
        gray, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=15,
        param1=50,
        param2=30, 
        minRadius=3,
        maxRadius=20
    )
    
    processed_img = img.copy()
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        print(f"Found {len(circles)} potential anchor holes")
        
        # Process each circle (anchor hole)
        for i, (x, y, r) in enumerate(circles):
            # Extract the region around the circle
            margin = r + 5
            x1, y1 = max(0, x - margin), max(0, y - margin)
            x2, y2 = min(gray.shape[1], x + margin), min(gray.shape[0], y + margin)
            
            region = gray[y1:y2, x1:x2]
            circle_region = processed_img[y1:y2, x1:x2]
            
            # Create mask for the hole area
            mask = np.zeros(region.shape, dtype=np.uint8)
            center_x, center_y = x - x1, y - y1
            cv2.circle(mask, (center_x, center_y), r, 255, -1)
            
            # Find edges within the hole region (ink that impedes the hole)
            edges = cv2.Canny(region, 30, 100)
            edges_in_hole = cv2.bitwise_and(edges, edges, mask=mask)
            
            # Count edge pixels in the hole
            edge_pixels = cv2.countNonZero(edges_in_hole)
            hole_area = np.pi * r * r
            edge_density = edge_pixels / hole_area if hole_area > 0 else 0
            
            # If there's significant ink in the hole, preserve it
            if edge_density > 0.1:  # Threshold for "ink impedes hole"
                # Make the hole transparent but preserve ink edges
                # Create a transparent version
                circle_region_with_alpha = cv2.cvtColor(circle_region, cv2.COLOR_BGR2BGRA)
                
                # Make the hole area transparent
                circle_region_with_alpha[mask == 255] = [0, 0, 0, 0]
                
                # Preserve ink edges
                ink_color = [0, 0, 255, 255]  # Blue for visibility
                circle_region_with_alpha[edges_in_hole == 255] = ink_color
                
                processed_img[y1:y2, x1:x2] = cv2.cvtColor(circle_region_with_alpha, cv2.COLOR_BGRA2BGR)
                
                # Mark for visualization
                cv2.circle(processed_img, (x, y), r, (255, 0, 0), 2)  # Red for ink-preserved holes
            else:
                # Clean hole - just make transparent
                cv2.circle(processed_img, (x, y), r, (0, 255, 0), 2)  # Green for clean holes
    
    # Save the processed image
    output_path = os.path.join(output_dir, f"{prefix}_anchor_holes_processed.png")
    cv2.imwrite(output_path, processed_img)
    print(f"Saved processed anchor holes to {output_path}")

if __name__ == "__main__":
    base_dir = "/Users/bradleygeiser/Documents/Bertie"
    
    # Process both images with precise cutting
    images = [
        ("TheAstonishingOfAPenAndInkPuppet_0010.png", "main"),
        ("annotated_cutout_sheet (1).png", "annotated")
    ]
    
    for image_file, prefix in images:
        image_path = os.path.join(base_dir, image_file)
        output_dir = os.path.join(base_dir, "Bertie Assets", "bones")
        
        print(f"\n=== Processing {image_file} ===")
        precise_cut_parts(image_path, output_dir, prefix)
        process_anchor_holes_advanced(image_path, output_dir, prefix)
