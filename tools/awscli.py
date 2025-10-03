
import os
import subprocess
from utils import get_os, get_linux_distro
from versioning import get_download_url
from dependencies import dependency_manager

def install(version=None):
    os_type = get_os()
    
    # Install dependencies first
    print("🔧 Installing AWS CLI dependencies...")
    if not dependency_manager.install_dependencies('awscli'):
        print("❌ Failed to install AWS CLI dependencies. Aborting installation.")
        return False
    
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower() or 'debian' in distro.lower() or 'centos' in distro.lower() or 'rhel' in distro.lower() or 'fedora' in distro.lower():
            return _install_awscli_linux(distro, version)
        else:
            print(f'Unsupported Linux distribution: {distro}')
            return False
    elif os_type == 'Darwin':
        return _install_awscli_macos(version)
    elif os_type == 'Windows':
        return _install_awscli_windows(version)
    else:
        print(f'Unsupported OS: {os_type}')
        return False

def _install_awscli_linux(distro, version=None):
    """Install AWS CLI on Linux with proper error handling"""
    print(f'Installing AWS CLI on {distro}...')
    
    try:
        # Step 1: Download AWS CLI
        print("📥 Downloading AWS CLI...")
        if version and version != "latest":
            download_url = f"https://awscli.amazonaws.com/awscli-exe-linux-x86_64-{version}.zip"
        else:
            download_url = "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
        
        subprocess.run(['curl', download_url, '-o', 'awscliv2.zip'], check=True, timeout=300)
        
        # Step 2: Install unzip if not available
        print("📦 Installing unzip...")
        if 'fedora' in distro.lower():
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'unzip'], check=True, timeout=120)
        elif 'centos' in distro.lower() or 'rhel' in distro.lower():
            subprocess.run(['sudo', 'yum', 'install', '-y', 'unzip'], check=True, timeout=120)
        else:
            subprocess.run(['sudo', 'apt', 'install', '-y', 'unzip'], check=True, timeout=120)
        
        # Step 3: Extract and install
        print("📦 Extracting AWS CLI...")
        subprocess.run(['unzip', 'awscliv2.zip'], check=True, timeout=60)
        
        print("🔧 Installing AWS CLI...")
        subprocess.run(['sudo', './aws/install'], check=True, timeout=300)
        
        # Step 4: Clean up
        print("🧹 Cleaning up...")
        subprocess.run(['rm', '-rf', 'awscliv2.zip', 'aws'], check=True, timeout=30)
        
        # Step 5: Verify installation
        print("✅ Verifying AWS CLI installation...")
        result = subprocess.run(['aws', '--version'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ AWS CLI installed successfully: {result.stdout.strip()}")
            print("🧪 Test AWS CLI: aws --version")
            return True
        else:
            print("❌ AWS CLI installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install AWS CLI: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ AWS CLI installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during AWS CLI installation: {e}")
        return False

def _install_awscli_macos(version=None):
    """Install AWS CLI on macOS"""
    print('Installing AWS CLI on macOS...')
    
    try:
        if version and version != "latest":
            print(f'Installing AWS CLI version {version} on macOS...')
            download_url = f"https://awscli.amazonaws.com/AWSCLIV2-{version}.pkg"
        else:
            print('Installing latest AWS CLI on macOS...')
            download_url = "https://awscli.amazonaws.com/AWSCLIV2.pkg"
        
        # Download and install
        print("📥 Downloading AWS CLI...")
        subprocess.run(['curl', download_url, '-o', 'AWSCLIV2.pkg'], check=True, timeout=300)
        
        print("🔧 Installing AWS CLI...")
        subprocess.run(['sudo', 'installer', '-pkg', 'AWSCLIV2.pkg', '-target', '/'], check=True, timeout=300)
        
        # Clean up
        subprocess.run(['rm', 'AWSCLIV2.pkg'], check=True, timeout=30)
        
        # Verify installation
        print("✅ Verifying AWS CLI installation...")
        result = subprocess.run(['aws', '--version'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ AWS CLI installed successfully: {result.stdout.strip()}")
            print("🧪 Test AWS CLI: aws --version")
            return True
        else:
            print("❌ AWS CLI installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install AWS CLI: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ AWS CLI installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during AWS CLI installation: {e}")
        return False

def _install_awscli_windows(version=None):
    """Install AWS CLI on Windows"""
    print('Installing AWS CLI on Windows...')
    
    try:
        if version and version != "latest":
            print(f'Installing AWS CLI version {version} on Windows...')
            download_url = f"https://awscli.amazonaws.com/AWSCLIV2-{version}.msi"
        else:
            print('Installing latest AWS CLI on Windows...')
            download_url = "https://awscli.amazonaws.com/AWSCLIV2.msi"
        
        # Download and install
        print("📥 Downloading AWS CLI...")
        subprocess.run([
            'powershell', '-Command',
            f'Invoke-WebRequest -Uri {download_url} -OutFile .\\AWSCLIV2.msi'
        ], check=True, timeout=300)
        
        print("🔧 Installing AWS CLI...")
        subprocess.run(['msiexec.exe', '/i', 'AWSCLIV2.msi', '/quiet'], check=True, timeout=300)
        
        # Clean up
        subprocess.run(['del', 'AWSCLIV2.msi'], check=True, timeout=30)
        
        print("✅ AWS CLI installed successfully!")
        print("🧪 Test AWS CLI: aws --version")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install AWS CLI: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ AWS CLI installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during AWS CLI installation: {e}")
        return False

def uninstall(version=None):
    """Uninstall AWS CLI with proper cleanup"""
    os_type = get_os()
    
    try:
        if os_type == 'Linux':
            print('Uninstalling AWS CLI from Linux...')
            subprocess.run(['sudo', 'rm', '-rf', '/usr/local/aws-cli'], check=True, timeout=30)
            subprocess.run(['sudo', 'rm', '/usr/local/bin/aws'], check=True, timeout=30)
            subprocess.run(['sudo', 'rm', '/usr/local/bin/aws_completer'], check=True, timeout=30)
        elif os_type == 'Darwin':
            print('Uninstalling AWS CLI from macOS...')
            subprocess.run(['sudo', 'rm', '-rf', '/usr/local/aws-cli'], check=True, timeout=30)
            subprocess.run(['sudo', 'rm', '/usr/local/bin/aws'], check=True, timeout=30)
            subprocess.run(['sudo', 'rm', '/usr/local/bin/aws_completer'], check=True, timeout=30)
        elif os_type == 'Windows':
            print('Uninstalling AWS CLI from Windows...')
            try:
                subprocess.run(['winget', 'uninstall', 'Amazon.AWSCLI'], check=True, timeout=300)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print('Please uninstall AWS CLI manually through "Add or remove programs"')
                if version and version != "latest":
                    print(f'You may need to search for AWS CLI version {version} in "Add or remove programs"')
        else:
            print(f'Unsupported OS: {os_type}')
            return False
            
        print("✅ AWS CLI uninstalled successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to uninstall AWS CLI: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Uninstall timed out")
        return False
    except Exception as e:
        print(f"❌ Error during AWS CLI uninstallation: {e}")
        return False

def update(version=None):
    """Update AWS CLI to the specified version or latest"""
    print("🔄 Updating AWS CLI...")
    
    # For updates, we can use the same install process
    # as it will upgrade existing installations
    return install(version)
