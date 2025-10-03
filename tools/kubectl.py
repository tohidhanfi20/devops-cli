import os
import subprocess
from utils import get_os, get_linux_distro
from versioning import get_download_url
from dependencies import dependency_manager

def install(version=None):
    os_type = get_os()
    
    # Install dependencies first
    print("🔧 Installing kubectl dependencies...")
    if not dependency_manager.install_dependencies('kubectl'):
        print("❌ Failed to install kubectl dependencies. Aborting installation.")
        return False
    
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower() or 'debian' in distro.lower():
            return _install_kubectl_ubuntu(distro, version)
        elif 'centos' in distro.lower() or 'rhel' in distro.lower() or 'fedora' in distro.lower():
            return _install_kubectl_centos(distro, version)
        else:
            print(f'Unsupported Linux distribution: {distro}')
            return False
    elif os_type == 'Darwin':
        return _install_kubectl_macos(version)
    elif os_type == 'Windows':
        return _install_kubectl_windows(version)
    else:
        print(f'Unsupported OS: {os_type}')
        return False

def _install_kubectl_ubuntu(distro, version=None):
    """Install kubectl on Ubuntu/Debian with modern methods"""
    print(f'Installing kubectl on {distro}...')
    
    try:
        # Step 1: Update package index
        print("🔄 Updating package index...")
        subprocess.run(['sudo', 'apt', 'update'], check=True, timeout=60)
        
        # Step 2: Install required packages
        print("📦 Installing required packages...")
        required_packages = ['apt-transport-https', 'ca-certificates', 'curl', 'gnupg']
        subprocess.run(['sudo', 'apt', 'install', '-y'] + required_packages, check=True, timeout=120)
        
        # Step 3: Add Kubernetes GPG key (modern method)
        print("🔑 Adding Kubernetes GPG key...")
        subprocess.run([
            'curl', '-fsSL', 'https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key'
        ], stdout=subprocess.PIPE, check=True, timeout=30)
        
        # Step 4: Add Kubernetes repository (modern method)
        print("📥 Adding Kubernetes repository...")
        k8s_repo = 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /'
        with open('/etc/apt/sources.list.d/kubernetes.list', 'w') as f:
            f.write(k8s_repo + '\n')
        
        # Step 5: Update package index
        print("🔄 Updating package index with Kubernetes repository...")
        subprocess.run(['sudo', 'apt', 'update'], check=True, timeout=60)
        
        # Step 6: Install kubectl
        print("☸️ Installing kubectl...")
        if version and version != "latest":
            subprocess.run(['sudo', 'apt', 'install', '-y', f'kubectl={version}'], check=True, timeout=300)
        else:
            subprocess.run(['sudo', 'apt', 'install', '-y', 'kubectl'], check=True, timeout=300)
        
        # Step 7: Verify installation
        print("✅ Verifying kubectl installation...")
        result = subprocess.run(['kubectl', 'version', '--client'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ kubectl installed successfully: {result.stdout.strip()}")
            print("🧪 Test kubectl: kubectl version --client")
            return True
        else:
            print("❌ kubectl installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install kubectl: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ kubectl installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during kubectl installation: {e}")
        return False

def _install_kubectl_centos(distro, version=None):
    """Install kubectl on CentOS/RHEL/Fedora"""
    print(f'Installing kubectl on {distro}...')
    
    try:
        # Step 1: Install required packages
        print("📦 Installing required packages...")
        if 'fedora' in distro.lower():
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'curl'], check=True, timeout=120)
        else:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'curl'], check=True, timeout=120)
        
        # Step 2: Add Kubernetes repository
        print("📥 Adding Kubernetes repository...")
        if 'fedora' in distro.lower():
            subprocess.run([
                'sudo', 'dnf', 'config-manager', '--add-repo',
                'https://pkgs.k8s.io/core:/stable:/v1.28/rpm/'
            ], check=True, timeout=60)
        else:
            subprocess.run([
                'sudo', 'yum-config-manager', '--add-repo',
                'https://pkgs.k8s.io/core:/stable:/v1.28/rpm/'
            ], check=True, timeout=60)
        
        # Step 3: Install kubectl
        print("☸️ Installing kubectl...")
        if 'fedora' in distro.lower():
            if version and version != "latest":
                subprocess.run(['sudo', 'dnf', 'install', '-y', f'kubectl-{version}'], check=True, timeout=300)
            else:
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'kubectl'], check=True, timeout=300)
        else:
            if version and version != "latest":
                subprocess.run(['sudo', 'yum', 'install', '-y', f'kubectl-{version}'], check=True, timeout=300)
            else:
                subprocess.run(['sudo', 'yum', 'install', '-y', 'kubectl'], check=True, timeout=300)
        
        # Step 4: Verify installation
        print("✅ Verifying kubectl installation...")
        result = subprocess.run(['kubectl', 'version', '--client'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ kubectl installed successfully: {result.stdout.strip()}")
            print("🧪 Test kubectl: kubectl version --client")
            return True
        else:
            print("❌ kubectl installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install kubectl: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ kubectl installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during kubectl installation: {e}")
        return False

def _install_kubectl_macos(version=None):
    """Install kubectl on macOS"""
    print('Installing kubectl on macOS...')
    
    try:
        if version and version != "latest":
            print(f'Installing kubectl version {version} on macOS...')
            subprocess.run(['brew', 'install', f'kubectl@{version}'], check=True, timeout=300)
        else:
            print('Installing latest kubectl on macOS...')
            subprocess.run(['brew', 'install', 'kubectl'], check=True, timeout=300)
        
        # Verify installation
        print("✅ Verifying kubectl installation...")
        result = subprocess.run(['kubectl', 'version', '--client'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ kubectl installed successfully: {result.stdout.strip()}")
            print("🧪 Test kubectl: kubectl version --client")
            return True
        else:
            print("❌ kubectl installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install kubectl: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ kubectl installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during kubectl installation: {e}")
        return False

def _install_kubectl_windows(version=None):
    """Install kubectl on Windows"""
    print('Installing kubectl on Windows...')
    
    try:
        if version and version != "latest":
            print(f'Installing kubectl version {version} on Windows...')
            subprocess.run(['winget', 'install', 'Kubernetes.kubectl', '--version', version], check=True, timeout=300)
        else:
            print('Installing latest kubectl on Windows...')
            subprocess.run(['winget', 'install', 'Kubernetes.kubectl'], check=True, timeout=300)
        
        print("✅ kubectl installed successfully!")
        print("🧪 Test kubectl: kubectl version --client")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install kubectl: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ kubectl installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during kubectl installation: {e}")
        return False

def uninstall(version=None):
    """Uninstall kubectl with proper cleanup"""
    os_type = get_os()
    
    try:
        if os_type == 'Linux':
            distro = get_linux_distro()
            if 'ubuntu' in distro.lower() or 'debian' in distro.lower():
                print(f'Uninstalling kubectl from {distro}...')
                subprocess.run(['sudo', 'apt', 'remove', '-y', 'kubectl'], check=True, timeout=60)
                subprocess.run(['sudo', 'rm', '-f', '/usr/local/bin/kubectl'], check=True, timeout=30)
            elif 'centos' in distro.lower() or 'rhel' in distro.lower() or 'fedora' in distro.lower():
                print(f'Uninstalling kubectl from {distro}...')
                if 'fedora' in distro.lower():
                    subprocess.run(['sudo', 'dnf', 'remove', '-y', 'kubectl'], check=True, timeout=60)
                else:
                    subprocess.run(['sudo', 'yum', 'remove', '-y', 'kubectl'], check=True, timeout=60)
                subprocess.run(['sudo', 'rm', '-f', '/usr/local/bin/kubectl'], check=True, timeout=30)
            else:
                print(f'Unsupported Linux distribution: {distro}')
                return False
                
        elif os_type == 'Darwin':
            print('Uninstalling kubectl from macOS...')
            if version and version != "latest":
                subprocess.run(['brew', 'uninstall', f'kubectl@{version}'], check=True, timeout=60)
            else:
                subprocess.run(['brew', 'uninstall', 'kubectl'], check=True, timeout=60)
            subprocess.run(['sudo', 'rm', '-f', '/usr/local/bin/kubectl'], check=True, timeout=30)
            
        elif os_type == 'Windows':
            print('Uninstalling kubectl from Windows...')
            if version and version != "latest":
                subprocess.run(['winget', 'uninstall', 'Kubernetes.kubectl', '--version', version], check=True, timeout=300)
            else:
                subprocess.run(['winget', 'uninstall', 'Kubernetes.kubectl'], check=True, timeout=300)
        else:
            print(f'Unsupported OS: {os_type}')
            return False
            
        print("✅ kubectl uninstalled successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to uninstall kubectl: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Uninstall timed out")
        return False
    except Exception as e:
        print(f"❌ Error during kubectl uninstallation: {e}")
        return False

def update(version=None):
    """Update kubectl to the specified version or latest"""
    print("🔄 Updating kubectl...")
    
    # For updates, we can use the same install process
    # as it will upgrade existing installations
    return install(version)