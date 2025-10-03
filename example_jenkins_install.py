#!/usr/bin/env python3
"""
Example script demonstrating the improved Jenkins installation
with automatic dependency management and modern installation methods
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dependencies import dependency_manager
from tools.jenkins import install as install_jenkins
from enhanced_versioning import version_manager

def demonstrate_jenkins_installation():
    """Demonstrate the improved Jenkins installation process"""
    
    print("🚀 DevOps CLI - Enhanced Jenkins Installation Demo")
    print("=" * 60)
    
    # Step 1: Check dependencies
    print("\n📋 Step 1: Checking Jenkins dependencies...")
    jenkins_deps = dependency_manager.get_dependencies('jenkins')
    print(f"Dependencies required: {', '.join(jenkins_deps)}")
    
    # Step 2: Validate dependencies
    print("\n🔍 Step 2: Validating dependencies...")
    if dependency_manager.validate_dependencies('jenkins'):
        print("✅ All dependencies are installed")
    else:
        print("❌ Missing dependencies detected")
        print("📦 Installing missing dependencies...")
        if dependency_manager.install_dependencies('jenkins'):
            print("✅ Dependencies installed successfully")
        else:
            print("❌ Failed to install dependencies")
            return False
    
    # Step 3: Get available versions
    print("\n📦 Step 3: Fetching available Jenkins versions...")
    try:
        versions = version_manager.get_versions('jenkins', 'Linux')
        print(f"Available versions: {', '.join(versions[:5])}")
    except Exception as e:
        print(f"Error fetching versions: {e}")
        versions = ["latest"]
    
    # Step 4: Install Jenkins
    print("\n🔧 Step 4: Installing Jenkins...")
    try:
        # Install latest version
        success = install_jenkins(version="latest")
        if success:
            print("✅ Jenkins installation completed successfully!")
            print("\n📝 Next steps:")
            print("1. Start Jenkins: sudo systemctl start jenkins")
            print("2. Enable auto-start: sudo systemctl enable jenkins")
            print("3. Access Jenkins: http://localhost:8080")
            print("4. Get admin password: sudo cat /var/lib/jenkins/secrets/initialAdminPassword")
        else:
            print("❌ Jenkins installation failed")
            return False
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False
    
    return True

def show_improvements():
    """Show the improvements made to the DevOps CLI"""
    
    print("\n🎯 Key Improvements Made:")
    print("=" * 40)
    
    improvements = [
        "✅ Automatic dependency management (Java, fontconfig, etc.)",
        "✅ Modern installation methods (no deprecated apt-key)",
        "✅ Enhanced error handling and retry logic",
        "✅ Better version fetching with fallbacks",
        "✅ Comprehensive logging and status reporting",
        "✅ Cross-platform dependency support",
        "✅ Timeout handling for long-running operations",
        "✅ Dependency validation before installation",
        "✅ Clean uninstallation with proper cleanup"
    ]
    
    for improvement in improvements:
        print(f"  {improvement}")
    
    print("\n🔧 Technical Enhancements:")
    print("  • Replaced os.system() with subprocess.run() for better control")
    print("  • Added proper timeout handling for all operations")
    print("  • Implemented retry logic for network operations")
    print("  • Added comprehensive error handling and logging")
    print("  • Created dependency management system")
    print("  • Enhanced version fetching with multiple fallbacks")
    print("  • Added validation for all dependencies")

if __name__ == "__main__":
    print("DevOps CLI - Enhanced Installation Demo")
    print("This script demonstrates the improved dependency management")
    print("and modern installation methods for Jenkins.\n")
    
    # Show improvements
    show_improvements()
    
    # Ask user if they want to proceed with demo
    response = input("\nDo you want to run the Jenkins installation demo? (y/N): ")
    if response.lower() in ['y', 'yes']:
        demonstrate_jenkins_installation()
    else:
        print("Demo cancelled. The improvements are ready to use!")
        print("Run: python main.py install jenkins")
