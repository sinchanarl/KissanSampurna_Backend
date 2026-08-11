#!/usr/bin/env python3
"""
Package creation script for Kisaan Sampurna distribution.
This script creates a clean, distributable ZIP package.
"""

import os
import shutil
import zipfile
from pathlib import Path
import datetime

def print_header():
    print("=" * 60)
    print("📦 Kisaan Sampurna - Package Creation Tool")
    print("=" * 60)
    print()

def clean_directory(directory):
    """Remove unnecessary files and directories."""
    print(f"🧹 Cleaning {directory}...")
    
    # Files and directories to remove
    cleanup_patterns = [
        "__pycache__",
        ".pytest_cache",
        ".DS_Store",
        "*.pyc",
        "*.pyo",
        "*.log",
        ".git",
        ".gitignore",
        "venv",
        ".venv",
        "node_modules",
        ".env",
        "backend.log",
        "frontend.log"
    ]
    
    removed_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Remove directories
        for pattern in cleanup_patterns:
            if pattern in dirs:
                dir_path = os.path.join(root, pattern)
                shutil.rmtree(dir_path, ignore_errors=True)
                dirs.remove(pattern)
                removed_count += 1
                print(f"  ❌ Removed directory: {dir_path}")
        
        # Remove files
        for file in files:
            for pattern in cleanup_patterns:
                if pattern.startswith("*.") and file.endswith(pattern[1:]):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    removed_count += 1
                    print(f"  ❌ Removed file: {file_path}")
                elif pattern == file:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    removed_count += 1
                    print(f"  ❌ Removed file: {file_path}")
    
    print(f"✅ Cleanup complete: {removed_count} items removed")
    return removed_count

def verify_essential_files(directory):
    """Verify that all essential files are present."""
    print("🔍 Verifying essential files...")
    
    essential_files = [
        "README.md",
        "requirements.txt",
        "setup.py",
        "frontend.html",
        "test_qa_models.py",
        "check_models.py",
        "start_system.bat",
        "start_system.sh",
        "DEPLOYMENT_GUIDE.md",
        "app/app.py",
        "app/services/modelService.py",
        "app/routers/v1/analyze.py"
    ]
    
    missing_files = []
    
    for file_path in essential_files:
        full_path = os.path.join(directory, file_path)
        if os.path.exists(full_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} essential files!")
        return False
    
    print("✅ All essential files present")
    return True

def count_model_files(directory):
    """Count model files in the assets directory."""
    print("🤖 Counting model files...")
    
    assets_path = os.path.join(directory, "app", "assets")
    if not os.path.exists(assets_path):
        print("  ❌ Assets directory not found")
        return 0
    
    model_count = 0
    model_dirs = [
        "crop_models/crop_qa_models",
        "crop_models/crop_obt_models",
        "fruit_models/fruit_qa_models",
        "fruit_models/fruits_obt_models",
        "vegetable_models/vegetable_qa_models",
        "vegetable_models/vegetables_obt_models"
    ]
    
    for model_dir in model_dirs:
        dir_path = os.path.join(assets_path, model_dir)
        if os.path.exists(dir_path):
            pt_files = [f for f in os.listdir(dir_path) if f.endswith('.pt')]
            model_count += len(pt_files)
            print(f"  📁 {model_dir}: {len(pt_files)} models")
        else:
            print(f"  ⚠️  {model_dir}: Directory not found")
    
    print(f"📊 Total models: {model_count}")
    return model_count

def calculate_directory_size(directory):
    """Calculate total size of directory."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def format_size(size_bytes):
    """Format size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def create_zip_package(source_dir, output_path):
    """Create ZIP package."""
    print(f"📦 Creating ZIP package: {output_path}")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, os.path.dirname(source_dir))
                zipf.write(file_path, arc_path)
                print(f"  📄 Added: {arc_path}")
    
    # Get ZIP file size
    zip_size = os.path.getsize(output_path)
    print(f"✅ ZIP package created: {format_size(zip_size)}")
    
    return zip_size

def create_package_info(output_dir, model_count, package_size):
    """Create package information file."""
    info_content = f"""# 📦 Kisaan Sampurna Distribution Package

**Package Created**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version**: 1.0.0
**Package Size**: {format_size(package_size)}
**Model Files**: {model_count} total models

## 🚀 Quick Start

1. **Extract Package**:
   ```bash
   unzip kisaan-sampurna-system.zip
   cd kisaansampurna-backend
   ```

2. **Run Setup**:
   ```bash
   python setup.py
   ```

3. **Start System**:
   ```bash
   # Windows:
   start_system.bat
   
   # macOS/Linux:
   ./start_system.sh
   ```

4. **Access Application**:
   - Main App: http://localhost:3000/frontend.html
   - API Docs: http://localhost:8000/docs

## 📋 System Requirements

- Python 3.11+ (3.12 recommended)
- 8GB RAM minimum (16GB recommended)
- 5GB free disk space
- Windows 10+, macOS 10.15+, or Ubuntu 18.04+

## 📞 Support

- Check README.md for detailed instructions
- See DEPLOYMENT_GUIDE.md for troubleshooting
- Run `python check_models.py` to verify installation

---
**Happy Disease Detection! 🌾🔬**
"""
    
    info_path = os.path.join(output_dir, "PACKAGE_INFO.md")
    with open(info_path, 'w') as f:
        f.write(info_content)
    
    print(f"📄 Created package info: {info_path}")

def main():
    """Main packaging function."""
    print_header()
    
    # Get current directory
    current_dir = os.getcwd()
    project_name = "kisaansampurna-backend"
    
    # Create distribution directory
    dist_dir = os.path.join(os.path.dirname(current_dir), "kisaan-sampurna-distribution")
    package_dir = os.path.join(dist_dir, project_name)
    
    print(f"📁 Source directory: {current_dir}")
    print(f"📁 Distribution directory: {dist_dir}")
    print()
    
    # Create distribution directory
    if os.path.exists(dist_dir):
        print("🗑️  Removing existing distribution directory...")
        shutil.rmtree(dist_dir)
    
    os.makedirs(dist_dir, exist_ok=True)
    print(f"✅ Created distribution directory: {dist_dir}")
    
    # Copy project files
    print("📋 Copying project files...")
    shutil.copytree(current_dir, package_dir)
    print(f"✅ Copied to: {package_dir}")
    
    # Clean the copied directory
    clean_directory(package_dir)
    
    # Verify essential files
    if not verify_essential_files(package_dir):
        print("❌ Package verification failed!")
        return False
    
    # Count models
    model_count = count_model_files(package_dir)
    
    # Calculate size
    package_size = calculate_directory_size(package_dir)
    print(f"📊 Package size: {format_size(package_size)}")
    
    # Create ZIP package
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"kisaan-sampurna-system_{timestamp}.zip"
    zip_path = os.path.join(dist_dir, zip_filename)
    
    zip_size = create_zip_package(package_dir, zip_path)
    
    # Create package info
    create_package_info(dist_dir, model_count, zip_size)
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 Package Creation Complete!")
    print("=" * 60)
    print(f"📦 Package: {zip_path}")
    print(f"📊 Size: {format_size(zip_size)}")
    print(f"🤖 Models: {model_count} total")
    print(f"📁 Distribution folder: {dist_dir}")
    print()
    print("📧 Ready for distribution!")
    print("📋 Share the ZIP file and PACKAGE_INFO.md with recipients")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Packaging completed successfully!")
        else:
            print("\n❌ Packaging failed!")
    except KeyboardInterrupt:
        print("\n\n⚠️  Packaging interrupted by user")
    except Exception as e:
        print(f"\n❌ Packaging failed with error: {e}")
        import traceback
        traceback.print_exc()