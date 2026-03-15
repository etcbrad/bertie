#!/usr/bin/env python3
import cv2
import numpy as np
import os
import json
from pathlib import Path

# Get project root directory (where this script is located)
PROJECT_ROOT = Path(__file__).parent
BASE_DIR = PROJECT_ROOT / "Bertie Assets"

def create_joint_references():
    """
    Create joint reference files based on the bone structure
    """
    joints_dir = BASE_DIR / "joints"
    bones_dir = BASE_DIR / "bones"
    
    # Ensure directories exist
    joints_dir.mkdir(parents=True, exist_ok=True)
    bones_dir.mkdir(parents=True, exist_ok=True)
    
    # Joint definitions based on the HTML puppet structure
    joints = {
        "neck": {
            "connects": ["head", "torso"],
            "type": "ball",
            "rotation_limits": {"x": [-45, 45], "y": [-30, 30], "z": [-30, 30]},
            "anchor_hole": True
        },
        "left_shoulder": {
            "connects": ["torso", "left_upper_arm"],
            "type": "ball",
            "rotation_limits": {"x": [-180, 180], "y": [-90, 90], "z": [-180, 180]},
            "anchor_hole": True
        },
        "left_elbow": {
            "connects": ["left_upper_arm", "left_lower_arm"],
            "type": "hinge",
            "rotation_limits": {"x": [0, 150], "y": [0, 0], "z": [0, 0]},
            "anchor_hole": True
        },
        "right_shoulder": {
            "connects": ["torso", "right_upper_arm"],
            "type": "ball",
            "rotation_limits": {"x": [-180, 180], "y": [-90, 90], "z": [-180, 180]},
            "anchor_hole": True
        },
        "right_elbow": {
            "connects": ["right_upper_arm", "right_lower_arm"],
            "type": "hinge",
            "rotation_limits": {"x": [0, 150], "y": [0, 0], "z": [0, 0]},
            "anchor_hole": True
        },
        "left_hip": {
            "connects": ["torso", "left_upper_leg"],
            "type": "ball",
            "rotation_limits": {"x": [-120, 45], "y": [-30, 30], "z": [-45, 45]},
            "anchor_hole": True
        },
        "left_knee": {
            "connects": ["left_upper_leg", "left_lower_leg"],
            "type": "hinge",
            "rotation_limits": {"x": [0, 150], "y": [0, 0], "z": [0, 0]},
            "anchor_hole": True
        },
        "right_hip": {
            "connects": ["torso", "right_upper_leg"],
            "type": "ball",
            "rotation_limits": {"x": [-120, 45], "y": [-30, 30], "z": [-45, 45]},
            "anchor_hole": True
        },
        "right_knee": {
            "connects": ["right_upper_leg", "right_lower_leg"],
            "type": "hinge",
            "rotation_limits": {"x": [0, 150], "y": [0, 0], "z": [0, 0]},
            "anchor_hole": True
        }
    }
    
    # Save joint definitions as JSON
    joints_file = joints_dir / "joint_definitions.json"
    with open(joints_file, 'w') as f:
        json.dump(joints, f, indent=2)
    
    print(f"Created joint definitions: {joints_file}")
    
    # Create bone mapping
    bone_mapping = {
        "part_01": {"name": "head", "type": "body_part"},
        "part_02": {"name": "torso", "type": "body_part"},
        "part_03": {"name": "right_upper_arm", "type": "arm_segment"},
        "part_04": {"name": "right_lower_arm", "type": "arm_segment"},
        "part_05": {"name": "left_upper_arm", "type": "arm_segment"},
        "part_06": {"name": "left_lower_arm", "type": "arm_segment"},
        "part_07": {"name": "right_upper_leg", "type": "leg_segment"},
        "part_08": {"name": "right_lower_leg_with_foot", "type": "leg_segment"},
        "part_09": {"name": "left_upper_leg", "type": "leg_segment"},
        "part_10": {"name": "left_lower_leg_with_foot", "type": "leg_segment"}
    }
    
    # Save bone mapping
    mapping_file = joints_dir / "bone_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(bone_mapping, f, indent=2)
    
    print(f"Created bone mapping: {mapping_file}")
    
    # Create assembly instructions
    assembly_instructions = {
        "title": "Bertie Puppet Assembly",
        "description": "10-part puppet with feet attached to legs, no hands",
        "parts": [
            {"id": 1, "name": "Head", "file": "part_01", "connections": ["neck"]},
            {"id": 2, "name": "Torso", "file": "part_02", "connections": ["neck", "left_shoulder", "right_shoulder", "left_hip", "right_hip"]},
            {"id": 3, "name": "Right Upper Arm", "file": "part_03", "connections": ["right_shoulder", "right_elbow"]},
            {"id": 4, "name": "Right Lower Arm", "file": "part_04", "connections": ["right_elbow"]},
            {"id": 5, "name": "Left Upper Arm", "file": "part_05", "connections": ["left_shoulder", "left_elbow"]},
            {"id": 6, "name": "Left Lower Arm", "file": "part_06", "connections": ["left_elbow"]},
            {"id": 7, "name": "Right Upper Leg", "file": "part_07", "connections": ["right_hip", "right_knee"]},
            {"id": 8, "name": "Right Lower Leg + Foot", "file": "part_08", "connections": ["right_knee"]},
            {"id": 9, "name": "Left Upper Leg", "file": "part_09", "connections": ["left_hip", "left_knee"]},
            {"id": 10, "name": "Left Lower Leg + Foot", "file": "part_10", "connections": ["left_knee"]}
        ],
        "notes": [
            "Feet are attached to lower leg segments (parts 8 and 10)",
            "No hand segments - arms end at lower arm (parts 4 and 6)",
            "Anchor holes should be cleared of paper material",
            "Preserve any ink that impedes anchor holes for structural integrity"
        ]
    }
    
    # Save assembly instructions
    assembly_file = joints_dir / "assembly_instructions.json"
    with open(assembly_file, 'w') as f:
        json.dump(assembly_instructions, f, indent=2)
    
    print(f"Created assembly instructions: {assembly_file}")
    
    return joints, bone_mapping, assembly_instructions

def create_asset_manifest():
    """
    Create a manifest of all assets
    """
    manifest = {
        "project": "Bertie Assets",
        "description": "10-part puppet rigging assets with bone and joint definitions",
        "created": "2025-06-17",
        "structure": {
            "bones": {
                "description": "Cut puppet parts with anchor hole processing",
                "files": []
            },
            "joints": {
                "description": "Joint definitions and assembly instructions",
                "files": []
            }
        }
    }
    
    # List bone files
    bones_dir = BASE_DIR / "bones"
    if bones_dir.exists():
        for file in bones_dir.glob("*.png"):
            manifest["structure"]["bones"]["files"].append(file.name)
    
    # List joint files
    joints_dir = BASE_DIR / "joints"
    if joints_dir.exists():
        for file in joints_dir.iterdir():
            if file.is_file():
                manifest["structure"]["joints"]["files"].append(file.name)
    
    # Save manifest
    manifest_file = BASE_DIR / "manifest.json"
    import json
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Created asset manifest: {manifest_file}")
    return manifest

if __name__ == "__main__":
    print("=== Creating Bertie Assets Joint System ===")
    create_joint_references()
    create_asset_manifest()
    print("\n=== Bertie Assets System Complete ===")
