
import os
import subprocess
import platform
from utils import get_os, get_linux_distro
from dependencies import dependency_manager

def install(version=None):
    os_type = get_os()
    
    # Install dependencies first
    print("🔧 Installing Docker dependencies...")
    if not dependency_manager.install_dependencies('docker'):
        print("❌ Failed to install Docker dependencies. Aborting installation.")
        return False
    
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower() or 'debian' in distro.lower():
            return _install_docker_ubuntu(distro, version)
        elif 'centos' in distro.lower() or 'rhel' in distro.lower() or 'fedora' in distro.lower():
            return _install_docker_centos(distro, version)
        else:
            print(f'Unsupported Linux distribution: {distro}')
            return False
    elif os_type == 'Darwin':
        return _install_docker_macos(version)
    elif os_type == 'Windows':
        return _install_docker_windows(version)
    else:
        print(f'Unsupported OS: {os_type}')
        return False

def _install_docker_ubuntu(distro, version=None):
    """Install Docker on Ubuntu/Debian with proper repository setup"""
    print(f'Installing Docker on {distro}...')
    
    try:
        # Step 1: Update package index
        print("🔄 Updating package index...")
        subprocess.run(['sudo', 'apt', 'update'], check=True, timeout=60)
        
        # Step 2: Install required packages
        print("📦 Installing required packages...")
        required_packages = ['apt-transport-https', 'ca-certificates', 'curl', 'gnupg', 'lsb-release']
        subprocess.run(['sudo', 'apt', 'install', '-y'] + required_packages, check=True, timeout=120)
        
        # Step 3: Add Docker's official GPG key
        print("🔑 Adding Docker's official GPG key...")
        subprocess.run([
            'sudo', 'mkdir', '-p', '/etc/apt/keyrings'
        ], check=True, timeout=30)
        
        subprocess.run([
            'curl', '-fsSL', 'https://download.docker.com/linux/ubuntu/gpg'
        ], stdout=subprocess.PIPE, check=True, timeout=30)
        
        # Step 4: Add Docker repository
        print("📥 Adding Docker repository...")
        docker_repo = 'deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable'
        with open('/etc/apt/sources.list.d/docker.list', 'w') as f:
            f.write(docker_repo + '\n')
        
        # Step 5: Update package index again
        print("🔄 Updating package index with Docker repository...")
        subprocess.run(['sudo', 'apt', 'update'], check=True, timeout=60)
        
        # Step 6: Install Docker
        print("🐳 Installing Docker...")
        if version and version != "latest":
            subprocess.run(['sudo', 'apt', 'install', '-y', f'docker-ce={version}', 'docker-ce-cli', 'containerd.io'], check=True, timeout=300)
        else:
            subprocess.run(['sudo', 'apt', 'install', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io'], check=True, timeout=300)
        
        # Step 7: Start and enable Docker service
        print("🚀 Starting Docker service...")
        subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True, timeout=30)
        subprocess.run(['sudo', 'systemctl', 'enable', 'docker'], check=True, timeout=30)
        
        # Step 8: Add current user to docker group
        print("👤 Adding current user to docker group...")
        current_user = os.getenv('USER')
        if current_user:
            subprocess.run(['sudo', 'usermod', '-aG', 'docker', current_user], check=True, timeout=30)
        
        # Step 9: Verify installation
        print("✅ Verifying Docker installation...")
        result = subprocess.run(['sudo', 'docker', '--version'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Docker installed successfully: {result.stdout.strip()}")
            print("🔧 Important: You may need to log out and log back in for group changes to take effect")
            print("🧪 Test Docker: docker run hello-world")
            return True
        else:
            print("❌ Docker installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Docker: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Docker installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Docker installation: {e}")
        return False

def _install_docker_centos(distro, version=None):
    """Install Docker on CentOS/RHEL/Fedora with proper repository setup"""
    print(f'Installing Docker on {distro}...')
    
    try:
        # Step 1: Install required packages
        print("📦 Installing required packages...")
        if 'fedora' in distro.lower():
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'dnf-plugins-core'], check=True, timeout=120)
        else:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'yum-utils'], check=True, timeout=120)
        
        # Step 2: Add Docker repository
        print("📥 Adding Docker repository...")
        if 'fedora' in distro.lower():
            subprocess.run([
                'sudo', 'dnf', 'config-manager', '--add-repo',
                'https://download.docker.com/linux/fedora/docker-ce.repo'
            ], check=True, timeout=60)
        else:
            subprocess.run([
                'sudo', 'yum-config-manager', '--add-repo',
                'https://download.docker.com/linux/centos/docker-ce.repo'
            ], check=True, timeout=60)
        
        # Step 3: Install Docker
        print("🐳 Installing Docker...")
        if 'fedora' in distro.lower():
            if version and version != "latest":
                subprocess.run(['sudo', 'dnf', 'install', '-y', f'docker-ce-{version}', 'docker-ce-cli', 'containerd.io'], check=True, timeout=300)
            else:
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io'], check=True, timeout=300)
        else:
            if version and version != "latest":
                subprocess.run(['sudo', 'yum', 'install', '-y', f'docker-ce-{version}', 'docker-ce-cli', 'containerd.io'], check=True, timeout=300)
            else:
                subprocess.run(['sudo', 'yum', 'install', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io'], check=True, timeout=300)
        
        # Step 4: Start and enable Docker service
        print("🚀 Starting Docker service...")
        subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True, timeout=30)
        subprocess.run(['sudo', 'systemctl', 'enable', 'docker'], check=True, timeout=30)
        
        # Step 5: Add current user to docker group
        print("👤 Adding current user to docker group...")
        current_user = os.getenv('USER')
        if current_user:
            subprocess.run(['sudo', 'usermod', '-aG', 'docker', current_user], check=True, timeout=30)
        
        # Step 6: Verify installation
        print("✅ Verifying Docker installation...")
        result = subprocess.run(['sudo', 'docker', '--version'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Docker installed successfully: {result.stdout.strip()}")
            print("🔧 Important: You may need to log out and log back in for group changes to take effect")
            print("🧪 Test Docker: docker run hello-world")
            return True
        else:
            print("❌ Docker installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Docker: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Docker installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Docker installation: {e}")
        return False

def _install_docker_macos(version=None):
    """Install Docker on macOS"""
    print('Installing Docker on macOS...')
    
    try:
        if version and version != "latest":
            print(f'Installing Docker Desktop version {version} on macOS...')
            subprocess.run(['brew', 'install', '--cask', f'docker@{version}'], check=True, timeout=300)
        else:
            print('Installing latest Docker Desktop on macOS...')
            subprocess.run(['brew', 'install', '--cask', 'docker'], check=True, timeout=300)
        
        print("✅ Docker Desktop installed successfully!")
        print("🚀 Start Docker Desktop from Applications or run: open -a Docker")
        print("🧪 Test Docker: docker run hello-world")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Docker: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Docker installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Docker installation: {e}")
        return False

def _install_docker_windows(version=None):
    """Install Docker on Windows"""
    print('Installing Docker on Windows...')
    
    try:
        # For Windows, we'll use winget or chocolatey
        print("📥 Installing Docker Desktop via package manager...")
        
        # Try winget first
        try:
            if version and version != "latest":
                subprocess.run(['winget', 'install', 'Docker.DockerDesktop', '--version', version], check=True, timeout=600)
            else:
                subprocess.run(['winget', 'install', 'Docker.DockerDesktop'], check=True, timeout=600)
            
            print("✅ Docker Desktop installed successfully!")
            print("🚀 Start Docker Desktop from Start Menu")
            print("🧪 Test Docker: docker run hello-world")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to chocolatey
            try:
                if version and version != "latest":
                    subprocess.run(['choco', 'install', 'docker-desktop', '--version', version, '-y'], check=True, timeout=600)
                else:
                    subprocess.run(['choco', 'install', 'docker-desktop', '-y'], check=True, timeout=600)
                
                print("✅ Docker Desktop installed successfully!")
                print("🚀 Start Docker Desktop from Start Menu")
                print("🧪 Test Docker: docker run hello-world")
                return True
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("❌ Neither winget nor chocolatey found. Please install Docker Desktop manually:")
                print("1. Download from: https://www.docker.com/products/docker-desktop")
                print("2. Run the installer as administrator")
                return False
                
    except Exception as e:
        print(f"❌ Error during Docker installation: {e}")
        return False

def uninstall():
    """Uninstall Docker with proper cleanup"""
    os_type = get_os()
    
    try:
        if os_type == 'Linux':
            distro = get_linux_distro()
            if 'ubuntu' in distro.lower() or 'debian' in distro.lower():
                print('Uninstalling Docker from Ubuntu/Debian...')
                subprocess.run(['sudo', 'apt', 'remove', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io'], check=True, timeout=120)
                subprocess.run(['sudo', 'apt', 'autoremove', '-y'], check=True, timeout=60)
                subprocess.run(['sudo', 'rm', '-rf', '/var/lib/docker'], check=True, timeout=30)
                subprocess.run(['sudo', 'rm', '-rf', '/etc/docker'], check=True, timeout=30)
            elif 'centos' in distro.lower() or 'rhel' in distro.lower() or 'fedora' in distro.lower():
                print('Uninstalling Docker from CentOS/RHEL/Fedora...')
                subprocess.run(['sudo', 'systemctl', 'stop', 'docker'], check=True, timeout=30)
                if 'fedora' in distro.lower():
                    subprocess.run(['sudo', 'dnf', 'remove', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io'], check=True, timeout=120)
                else:
                    subprocess.run(['sudo', 'yum', 'remove', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io'], check=True, timeout=120)
                subprocess.run(['sudo', 'rm', '-rf', '/var/lib/docker'], check=True, timeout=30)
                subprocess.run(['sudo', 'rm', '-rf', '/etc/docker'], check=True, timeout=30)
            else:
                print(f'Unsupported Linux distribution: {distro}')
                return False
                
        elif os_type == 'Darwin':
            print('Uninstalling Docker from macOS...')
            subprocess.run(['brew', 'uninstall', '--cask', 'docker'], check=True, timeout=120)
            
        elif os_type == 'Windows':
            print('Uninstalling Docker from Windows...')
            try:
                subprocess.run(['winget', 'uninstall', 'Docker.DockerDesktop'], check=True, timeout=300)
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    subprocess.run(['choco', 'uninstall', 'docker-desktop', '-y'], check=True, timeout=300)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("Please uninstall Docker Desktop manually from Control Panel")
                    return False
        else:
            print(f'Unsupported OS: {os_type}')
            return False
            
        print("✅ Docker uninstalled successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to uninstall Docker: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Uninstall timed out")
        return False
    except Exception as e:
        print(f"❌ Error during Docker uninstallation: {e}")
        return False

def update(version=None):
    """Update Docker to the specified version or latest"""
    print("🔄 Updating Docker...")
    
    # For updates, we can use the same install process
    # as it will upgrade existing installations
    return install(version)
