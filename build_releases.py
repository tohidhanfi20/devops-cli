#!/usr/bin/env python3
"""
DevOps CLI - Build Platform-Specific Releases
Creates platform-specific packages like kubectx
"""

import os
import sys
import shutil
import zipfile
import tarfile
import subprocess
from pathlib import Path
import platform

def create_directory_structure():
    """Create the release directory structure"""
    release_dir = Path("releases")
    release_dir.mkdir(exist_ok=True)
    
    # Clean previous releases
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    return release_dir

def create_platform_package(platform_name, arch, ext):
    """Create platform-specific package"""
    release_dir = Path("releases")
    package_name = f"devops-cli_v1.0.0_{platform_name}_{arch}"
    package_path = release_dir / f"{package_name}.{ext}"
    
    print(f"📦 Creating {platform_name} {arch} package...")
    
    # Create temporary directory
    temp_dir = Path("temp_build")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # Copy all necessary files
    files_to_copy = [
        "main.py", "versioning.py", "utils.py", "interactive.py",
        "setup.py", "requirements.txt", "README.md", "install"
    ]
    
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, temp_dir)
    
    # Copy tools directory
    if Path("tools").exists():
        shutil.copytree("tools", temp_dir / "tools")
    
    # Create platform-specific install script
    if platform_name == "windows":
        install_script = temp_dir / "install.bat"
        install_content = f'''@echo off
echo Installing DevOps CLI for Windows {arch}...
python setup.py install
echo.
echo [SUCCESS] DevOps CLI installed successfully!
echo.
echo Usage:
echo   devops-cli --help
echo   devops-cli init
echo   devops-cli install docker
'''
    else:
        install_script = temp_dir / "install.sh"
        install_content = f'''#!/bin/bash
echo "Installing DevOps CLI for {platform_name} {arch}..."
python3 setup.py install
echo
echo "[SUCCESS] DevOps CLI installed successfully!"
echo
echo "Usage:"
echo "  devops-cli --help"
echo "  devops-cli init"
echo "  devops-cli install docker"
'''
    
    with open(install_script, 'w', encoding='utf-8') as f:
        f.write(install_content)
    
    if platform_name != "windows":
        os.chmod(install_script, 0o755)
    
    # Create package
    if ext == "zip":
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arc_path)
    else:  # tar.gz
        with tarfile.open(package_path, 'w:gz') as tar:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(temp_dir)
                    tar.add(file_path, arc_path)
    
    # Clean up
    shutil.rmtree(temp_dir)
    
    file_size = package_path.stat().st_size
    size_mb = file_size / (1024 * 1024)
    print(f"✅ Created {package_name}.{ext} ({size_mb:.2f} MB)")
    
    return package_path

def create_checksums():
    """Create checksums.txt file"""
    release_dir = Path("releases")
    checksums_file = release_dir / "checksums.txt"
    
    print("🔐 Creating checksums...")
    
    with open(checksums_file, 'w', encoding='utf-8') as f:
        for file_path in sorted(release_dir.glob("*.zip")) + sorted(release_dir.glob("*.tar.gz")):
            if file_path.name != "checksums.txt":
                # Calculate SHA256 checksum
                import hashlib
                with open(file_path, 'rb') as file:
                    sha256_hash = hashlib.sha256()
                    for chunk in iter(lambda: file.read(4096), b""):
                        sha256_hash.update(chunk)
                    checksum = sha256_hash.hexdigest()
                
                f.write(f"{checksum}  {file_path.name}\n")
    
    print(f"✅ Created checksums.txt")

def main():
    """Main build function"""
    print("🚀 DevOps CLI - Building Platform-Specific Releases")
    print("=" * 60)
    
    # Create release directory
    release_dir = create_directory_structure()
    
    # Platform configurations
    platforms = [
        # Linux
        ("linux", "x86_64", "tar.gz"),
        ("linux", "arm64", "tar.gz"),
        ("linux", "armhf", "tar.gz"),
        ("linux", "armv7", "tar.gz"),
        ("linux", "ppc64le", "tar.gz"),
        ("linux", "s390x", "tar.gz"),
        
        # macOS
        ("darwin", "x86_64", "tar.gz"),
        ("darwin", "arm64", "tar.gz"),
        
        # Windows
        ("windows", "x86_64", "zip"),
        ("windows", "arm64", "zip"),
        ("windows", "armhf", "zip"),
        ("windows", "armv7", "zip"),
    ]
    
    # Build packages for each platform
    for platform_name, arch, ext in platforms:
        try:
            create_platform_package(platform_name, arch, ext)
        except Exception as e:
            print(f"❌ Failed to create {platform_name} {arch}: {e}")
    
    # Create checksums
    create_checksums()
    
    print("\n🎉 Build complete!")
    print(f"📁 Release files created in: {release_dir.absolute()}")
    print("\n📋 Files created:")
    
    for file_path in sorted(release_dir.glob("*")):
        if file_path.is_file():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"  {file_path.name} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()