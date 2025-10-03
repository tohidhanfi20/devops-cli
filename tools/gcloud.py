
import os
import subprocess
from utils import get_os, get_linux_distro
from dependencies import dependency_manager

def install(version=None):
    os_type = get_os()
    
    # Install dependencies first
    print("🔧 Installing Google Cloud SDK dependencies...")
    if not dependency_manager.install_dependencies('gcloud'):
        print("❌ Failed to install Google Cloud SDK dependencies. Aborting installation.")
        return False
    
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower() or 'debian' in distro.lower() or 'centos' in distro.lower() or 'rhel' in distro.lower() or 'fedora' in distro.lower():
            return _install_gcloud_linux(distro, version)
        else:
            print(f'Unsupported Linux distribution: {distro}')
            return False
    elif os_type == 'Darwin':
        return _install_gcloud_macos(version)
    elif os_type == 'Windows':
        return _install_gcloud_windows(version)
    else:
        print(f'Unsupported OS: {os_type}')
        return False

def _install_gcloud_linux(distro, version=None):
    """Install Google Cloud SDK on Linux with proper error handling"""
    print(f'Installing Google Cloud SDK on {distro}...')
    
    try:
        # Step 1: Download and run the installer
        print("📥 Downloading Google Cloud SDK installer...")
        if version and version != "latest":
            print(f'Installing Google Cloud SDK version {version}...')
            subprocess.run([
                'curl', 'https://sdk.cloud.google.com', '|', 'bash', '-s', '--', f'--version={version}'
            ], shell=True, check=True, timeout=600)
        else:
            print('Installing latest Google Cloud SDK...')
            subprocess.run([
                'curl', 'https://sdk.cloud.google.com', '|', 'bash'
            ], shell=True, check=True, timeout=600)
        
        # Step 2: Add to PATH
        print("🔧 Adding Google Cloud SDK to PATH...")
        gcloud_path = os.path.expanduser('~/google-cloud-sdk/bin')
        if gcloud_path not in os.environ.get('PATH', ''):
            # Add to .bashrc
            bashrc_path = os.path.expanduser('~/.bashrc')
            with open(bashrc_path, 'a') as f:
                f.write(f'\nexport PATH="{gcloud_path}:$PATH"\n')
        
        # Step 3: Initialize gcloud
        print("🚀 Initializing Google Cloud SDK...")
        subprocess.run([f'{gcloud_path}/gcloud', 'init', '--quiet'], check=True, timeout=300)
        
        # Step 4: Verify installation
        print("✅ Verifying Google Cloud SDK installation...")
        result = subprocess.run([f'{gcloud_path}/gcloud', 'version'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Google Cloud SDK installed successfully: {result.stdout.strip()}")
            print("🧪 Test gcloud: gcloud version")
            print("🔧 Note: You may need to restart your terminal or run: source ~/.bashrc")
            return True
        else:
            print("❌ Google Cloud SDK installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Google Cloud SDK: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Google Cloud SDK installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Google Cloud SDK installation: {e}")
        return False

def _install_gcloud_macos(version=None):
    """Install Google Cloud SDK on macOS"""
    print('Installing Google Cloud SDK on macOS...')
    
    try:
        # Step 1: Download and run the installer
        print("📥 Downloading Google Cloud SDK installer...")
        if version and version != "latest":
            print(f'Installing Google Cloud SDK version {version}...')
            subprocess.run([
                'curl', 'https://sdk.cloud.google.com', '|', 'bash', '-s', '--', f'--version={version}'
            ], shell=True, check=True, timeout=600)
        else:
            print('Installing latest Google Cloud SDK...')
            subprocess.run([
                'curl', 'https://sdk.cloud.google.com', '|', 'bash'
            ], shell=True, check=True, timeout=600)
        
        # Step 2: Add to PATH
        print("🔧 Adding Google Cloud SDK to PATH...")
        gcloud_path = os.path.expanduser('~/google-cloud-sdk/bin')
        if gcloud_path not in os.environ.get('PATH', ''):
            # Add to .zshrc or .bash_profile
            shell_config = os.path.expanduser('~/.zshrc') if os.path.exists(os.path.expanduser('~/.zshrc')) else os.path.expanduser('~/.bash_profile')
            with open(shell_config, 'a') as f:
                f.write(f'\nexport PATH="{gcloud_path}:$PATH"\n')
        
        # Step 3: Initialize gcloud
        print("🚀 Initializing Google Cloud SDK...")
        subprocess.run([f'{gcloud_path}/gcloud', 'init', '--quiet'], check=True, timeout=300)
        
        # Step 4: Verify installation
        print("✅ Verifying Google Cloud SDK installation...")
        result = subprocess.run([f'{gcloud_path}/gcloud', 'version'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Google Cloud SDK installed successfully: {result.stdout.strip()}")
            print("🧪 Test gcloud: gcloud version")
            print("🔧 Note: You may need to restart your terminal or run: source ~/.zshrc")
            return True
        else:
            print("❌ Google Cloud SDK installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Google Cloud SDK: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Google Cloud SDK installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Google Cloud SDK installation: {e}")
        return False

def _install_gcloud_windows(version=None):
    """Install Google Cloud SDK on Windows"""
    print('Installing Google Cloud SDK on Windows...')
    
    try:
        # Step 1: Download the installer
        print("📥 Downloading Google Cloud SDK installer...")
        installer_url = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
        subprocess.run([
            'powershell', '-Command',
            f'Invoke-WebRequest -Uri {installer_url} -OutFile .\\GoogleCloudSDKInstaller.exe'
        ], check=True, timeout=300)
        
        # Step 2: Run the installer
        print("🔧 Installing Google Cloud SDK...")
        if version and version != "latest":
            print(f'Installing Google Cloud SDK version {version}...')
            subprocess.run([
                '.\\GoogleCloudSDKInstaller.exe', '/S', f'/D=C:\\google-cloud-sdk'
            ], check=True, timeout=600)
        else:
            print('Installing latest Google Cloud SDK...')
            subprocess.run([
                '.\\GoogleCloudSDKInstaller.exe', '/S', '/D=C:\\google-cloud-sdk'
            ], check=True, timeout=600)
        
        # Step 3: Clean up
        subprocess.run(['del', 'GoogleCloudSDKInstaller.exe'], check=True, timeout=30)
        
        print("✅ Google Cloud SDK installed successfully!")
        print("🧪 Test gcloud: gcloud version")
        print("🔧 Note: You may need to restart your terminal for PATH changes to take effect")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Google Cloud SDK: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Google Cloud SDK installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Google Cloud SDK installation: {e}")
        return False

def uninstall(version=None):
    """Uninstall Google Cloud SDK with proper cleanup"""
    os_type = get_os()
    
    try:
        if os_type == 'Linux' or os_type == 'Darwin':
            print('Uninstalling Google Cloud SDK...')
            gcloud_path = os.path.expanduser('~/google-cloud-sdk')
            if os.path.exists(gcloud_path):
                subprocess.run(['rm', '-rf', gcloud_path], check=True, timeout=60)
            
            # Remove from PATH
            shell_configs = ['.bashrc', '.zshrc', '.bash_profile']
            for config in shell_configs:
                config_path = os.path.expanduser(f'~/{config}')
                if os.path.exists(config_path):
                    # Remove gcloud PATH entries
                    with open(config_path, 'r') as f:
                        lines = f.readlines()
                    with open(config_path, 'w') as f:
                        for line in lines:
                            if 'google-cloud-sdk' not in line:
                                f.write(line)
            
            print("✅ Google Cloud SDK uninstalled successfully!")
            return True
        elif os_type == 'Windows':
            print('Uninstalling Google Cloud SDK from Windows...')
            try:
                subprocess.run(['winget', 'uninstall', 'Google.CloudSDK'], check=True, timeout=300)
                print("✅ Google Cloud SDK uninstalled successfully!")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Please uninstall Google Cloud SDK manually from Control Panel")
                return False
        else:
            print(f'Unsupported OS: {os_type}')
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to uninstall Google Cloud SDK: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Uninstall timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Google Cloud SDK uninstallation: {e}")
        return False

def update(version=None):
    """Update Google Cloud SDK to the specified version or latest"""
    print("🔄 Updating Google Cloud SDK...")
    
    try:
        gcloud_path = os.path.expanduser('~/google-cloud-sdk/bin/gcloud')
        if os.path.exists(gcloud_path):
            if version and version != "latest":
                print(f'Updating Google Cloud SDK components to version {version}...')
                subprocess.run([gcloud_path, 'components', 'update', f'--version={version}'], check=True, timeout=300)
            else:
                print('Updating Google Cloud SDK components to latest...')
                subprocess.run([gcloud_path, 'components', 'update'], check=True, timeout=300)
            
            print("✅ Google Cloud SDK updated successfully!")
            return True
        else:
            print("❌ Google Cloud SDK not found. Please install it first.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update Google Cloud SDK: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Update timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Google Cloud SDK update: {e}")
        return False
