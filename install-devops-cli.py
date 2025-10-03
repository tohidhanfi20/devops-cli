#!/usr/bin/env python3
"""
DevOps CLI - Single File Installer
==================================
A universal installer for DevOps tools across Windows, macOS, and Linux.
Automatically fetches latest versions and installs tools with proper dependencies.

Usage:
    python3 install-devops-cli.py
    # or
    curl -sSL https://raw.githubusercontent.com/tohidhanfi20/devops-cli/main/install-devops-cli.py | python3
"""

import os
import sys
import subprocess
import platform
import tempfile
import shutil
import zipfile
import urllib.request
import json
from pathlib import Path

# Version and repository info
CLI_VERSION = "1.0.1"
REPO_URL = "https://github.com/tohidhanfi20/devops-cli"
DOWNLOAD_URL = f"{REPO_URL}/archive/refs/heads/main.zip"

def print_banner():
    """Print installation banner"""
    print("""
🚀 DevOps CLI Installer v1.0.1
===============================
A universal installer for DevOps tools across Windows, macOS, and Linux.
Automatically fetches latest versions and installs tools with proper dependencies.

Supported Tools:
• 🐳 Docker - Container platform
• ☸️ kubectl - Kubernetes CLI  
• ☁️ AWS CLI - Amazon Web Services CLI
• 🌩️ gcloud - Google Cloud SDK
• 🔵 Azure CLI - Microsoft Azure CLI
• 🔧 Jenkins - CI/CD automation server
• ⛵ Helm - Kubernetes package manager
• 📊 Prometheus - Monitoring system
• 🏗️ Terraform - Infrastructure as Code
""")

def get_os_info():
    """Get operating system information"""
    system = platform.system().lower()
    if system == "windows":
        return "Windows"
    elif system == "darwin":
        return "macOS"
    elif system == "linux":
        return "Linux"
    else:
        return "Unknown"

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    return True

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_pip():
    """Try to install pip if not available"""
    print("🔧 Installing pip...")
    try:
        subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
        print("✅ pip installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install pip")
        return False

def download_cli():
    """Download the CLI from GitHub"""
    print("📥 Downloading DevOps CLI...")
    
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="devops-cli-")
        zip_path = os.path.join(temp_dir, "devops-cli.zip")
        
        # Download the repository
        print(f"   Downloading from: {DOWNLOAD_URL}")
        urllib.request.urlretrieve(DOWNLOAD_URL, zip_path)
        
        # Extract the zip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extracted directory
        extracted_dir = None
        for item in os.listdir(temp_dir):
            if item.startswith("devops-cli"):
                extracted_dir = os.path.join(temp_dir, item)
                break
        
        if not extracted_dir:
            raise Exception("Could not find extracted directory")
        
        print(f"✅ Downloaded to: {extracted_dir}")
        return extracted_dir
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

def install_cli_globally(cli_dir):
    """Install the CLI globally using pip"""
    print("🔧 Installing DevOps CLI globally...")
    
    try:
        # Install in development mode for global access
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], cwd=cli_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ DevOps CLI installed successfully!")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def create_standalone_script(cli_dir):
    """Create a standalone script for systems without pip"""
    print("📝 Creating standalone script...")
    
    try:
        # Create a standalone script that can run without pip
        standalone_script = f"""#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '{cli_dir}')
from main import main
if __name__ == '__main__':
    main()
"""
        
        script_path = os.path.join(cli_dir, "devops-cli-standalone.py")
        with open(script_path, 'w') as f:
            f.write(standalone_script)
        
        # Make it executable on Unix systems
        if os.name != 'nt':
            os.chmod(script_path, 0o755)
        
        print(f"✅ Standalone script created: {script_path}")
        return script_path
        
    except Exception as e:
        print(f"❌ Failed to create standalone script: {e}")
        return None

def verify_installation():
    """Verify the installation"""
    print("\n🔍 Verifying installation...")
    
    try:
        # Try to run the CLI
        result = subprocess.run(["devops-cli", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ DevOps CLI is working!")
            print(f"   Version: {result.stdout.strip()}")
            return True
        else:
            print("❌ CLI command not found in PATH")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ CLI command not found")
        return False
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions"""
    print("""
🎉 Installation Complete!
========================

You can now use the DevOps CLI:

📋 Basic Commands:
   devops-cli --help              # Show all available commands
   devops-cli init                # Start interactive installation (recommended)
   devops-cli list                # List all available tools
   devops-cli install <tool>      # Install a specific tool
   devops-cli status              # Check installation status

🚀 Quick Start:
   devops-cli init                # This will guide you through installing tools

💡 Troubleshooting:
   If 'devops-cli' command is not found:
   1. Restart your terminal
   2. Run: source ~/.bashrc (Linux/macOS)
   3. Check PATH: echo $PATH
   4. Try: python3 -m main (from CLI directory)

🔗 Documentation: https://github.com/tohidhanfi20/devops-cli
""")

def main():
    """Main installation process"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check pip availability
    pip_available = check_pip()
    if not pip_available:
        print("⚠️  pip not found, attempting to install...")
        pip_available = install_pip()
    
    # Download CLI
    cli_dir = download_cli()
    if not cli_dir:
        print("❌ Installation failed!")
        sys.exit(1)
    
    # Try to install globally if pip is available
    if pip_available:
        success = install_cli_globally(cli_dir)
        if success:
            # Verify installation
            if verify_installation():
                show_usage_instructions()
                return
            else:
                print("⚠️  Installation completed but CLI not in PATH")
                print("   You may need to restart your terminal")
    
    # Fallback: Create standalone script
    print("\n🔄 Creating standalone installation...")
    script_path = create_standalone_script(cli_dir)
    if script_path:
        print(f"""
✅ Standalone installation complete!

📁 CLI Location: {cli_dir}
🚀 To use the CLI, run:
   python3 {script_path} init

💡 Or add to PATH:
   export PATH="{cli_dir}:$PATH"
   devops-cli init
""")
    else:
        print("❌ Installation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
