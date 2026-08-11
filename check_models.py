#!/usr/bin/env python3
"""
Check what QA model files are available in the assets directory.
"""

from pathlib import Path
import os

def check_models():
    """Check and display available model files."""
    
    # Model paths
    base_path = Path(__file__).parent / "app" / "assets"
    
    model_dirs = {
        "Crop QA Models": base_path / "crop_models" / "crop_qa_models",
        "Crop OBT Models": base_path / "crop_models" / "crop_obt_models", 
        "Fruit QA Models": base_path / "fruit_models" / "fruit_qa_models",
        "Fruit OBT Models": base_path / "fruit_models" / "fruits_obt_models",
        "Vegetable QA Models": base_path / "vegetable_models" / "vegetable_qa_models",
        "Vegetable OBT Models": base_path / "vegetable_models" / "vegetables_obt_models",
    }
    
    print("🌾 Kisaan Sampurna - Model Files Check")
    print("=" * 50)
    
    total_models = 0
    
    for category, path in model_dirs.items():
        print(f"\n📁 {category}")
        print(f"   Path: {path}")
        
        if not path.exists():
            print("   ❌ Directory does not exist")
            continue
            
        # Get .pt files
        pt_files = list(path.glob("*.pt"))
        
        if not pt_files:
            print("   ⚠️  No .pt model files found")
        else:
            print(f"   ✅ Found {len(pt_files)} model files:")
            for pt_file in sorted(pt_files):
                size_mb = pt_file.stat().st_size / (1024 * 1024)
                print(f"      • {pt_file.name} ({size_mb:.1f} MB)")
            total_models += len(pt_files)
    
    print(f"\n📊 Summary: {total_models} total model files found")
    
    if total_models == 0:
        print("\n💡 To add models:")
        print("   1. Create the directory structure:")
        for path in model_dirs.values():
            print(f"      mkdir -p {path}")
        print("   2. Copy your .pt model files to the appropriate directories")
        print("   3. Run this script again to verify")

if __name__ == "__main__":
    check_models()