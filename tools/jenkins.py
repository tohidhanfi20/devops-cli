
import os
import subprocess
from utils import get_os, get_linux_distro
from versioning import get_download_url
from dependencies import dependency_manager

def install(version=None):
    os_type = get_os()
    
    # Install dependencies first
    print("🔧 Installing Jenkins dependencies...")
    if not dependency_manager.install_dependencies('jenkins'):
        print("❌ Failed to install Jenkins dependencies. Aborting installation.")
        return False
    
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower() or 'debian' in distro.lower():
            print(f'Installing Jenkins on {distro}...')
            
            # Modern Jenkins installation method (2024+)
            try:
                # Download and add Jenkins key using modern method
                print("📥 Adding Jenkins repository key...")
                subprocess.run([
                    'sudo', 'wget', '-O', '/etc/apt/keyrings/jenkins-keyring.asc',
                    'https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key'
                ], check=True, timeout=30)
                
                # Add Jenkins repository
                print("📦 Adding Jenkins repository...")
                jenkins_repo = 'deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/'
                with open('/etc/apt/sources.list.d/jenkins.list', 'w') as f:
                    f.write(jenkins_repo + '\n')
                
                # Update package list
                print("🔄 Updating package list...")
                subprocess.run(['sudo', 'apt', 'update'], check=True, timeout=60)
                
                # Install Jenkins
                if version and version != "latest":
                    print(f'Installing Jenkins version {version} on Ubuntu...')
                    subprocess.run(['sudo', 'apt', 'install', '-y', f'jenkins={version}'], check=True, timeout=300)
                else:
                    print('Installing latest Jenkins on Ubuntu...')
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'jenkins'], check=True, timeout=300)
                
                print("✅ Jenkins installed successfully!")
                print("🚀 To start Jenkins: sudo systemctl start jenkins")
                print("🔧 To enable auto-start: sudo systemctl enable jenkins")
                print("🌐 Access Jenkins at: http://localhost:8080")
                print("🔑 Get initial admin password: sudo cat /var/lib/jenkins/secrets/initialAdminPassword")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install Jenkins: {e}")
                return False
            except subprocess.TimeoutExpired:
                print("⏰ Installation timed out")
                return False
        elif 'centos' in distro.lower() or 'rhel' in distro.lower() or 'fedora' in distro.lower():
            print(f'Installing Jenkins on {distro}...')
            
            try:
                # Add Jenkins repository for RHEL/CentOS/Fedora
                print("📥 Adding Jenkins repository...")
                subprocess.run([
                    'sudo', 'wget', '-O', '/etc/yum.repos.d/jenkins.repo',
                    'https://pkg.jenkins.io/redhat-stable/jenkins.repo'
                ], check=True, timeout=30)
                
                # Import Jenkins key
                print("🔑 Importing Jenkins key...")
                subprocess.run([
                    'sudo', 'rpm', '--import', 
                    'https://pkg.jenkins.io/redhat-stable/jenkins.io.key'
                ], check=True, timeout=30)
                
                # Install Jenkins
                if version and version != "latest":
                    print(f'Installing Jenkins version {version} on {distro}...')
                    subprocess.run(['sudo', 'yum', 'install', '-y', f'jenkins-{version}'], check=True, timeout=300)
                else:
                    print(f'Installing latest Jenkins on {distro}...')
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'jenkins'], check=True, timeout=300)
                
                print("✅ Jenkins installed successfully!")
                print("🚀 To start Jenkins: sudo systemctl start jenkins")
                print("🔧 To enable auto-start: sudo systemctl enable jenkins")
                print("🌐 Access Jenkins at: http://localhost:8080")
                print("🔑 Get initial admin password: sudo cat /var/lib/jenkins/secrets/initialAdminPassword")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install Jenkins: {e}")
                return False
            except subprocess.TimeoutExpired:
                print("⏰ Installation timed out")
                return False
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing Jenkins on macOS...')
        try:
            if version and version != "latest":
                print(f'Installing Jenkins version {version} on macOS...')
                subprocess.run(['brew', 'install', f'jenkins-lts@{version}'], check=True, timeout=300)
            else:
                print('Installing latest Jenkins on macOS...')
                subprocess.run(['brew', 'install', 'jenkins-lts'], check=True, timeout=300)
            
            print("✅ Jenkins installed successfully!")
            print("🚀 To start Jenkins: brew services start jenkins-lts")
            print("🌐 Access Jenkins at: http://localhost:8080")
            print("🔑 Get initial admin password: cat ~/.jenkins/secrets/initialAdminPassword")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Jenkins: {e}")
            return False
        except subprocess.TimeoutExpired:
            print("⏰ Installation timed out")
            return False
            
    elif os_type == 'Windows':
        print('Installing Jenkins on Windows...')
        try:
            # For Windows, we'll download the Jenkins WAR file
            jenkins_version = version if version and version != "latest" else "2.401.3"
            download_url = f"https://get.jenkins.io/war-stable/{jenkins_version}/jenkins.war"
            
            print(f"📥 Downloading Jenkins {jenkins_version}...")
            subprocess.run([
                'powershell', '-Command',
                f'Invoke-WebRequest -Uri {download_url} -OutFile .\\jenkins.war'
            ], check=True, timeout=300)
            
            print("✅ Jenkins downloaded successfully!")
            print("🚀 To start Jenkins: java -jar jenkins.war")
            print("🌐 Access Jenkins at: http://localhost:8080")
            print("🔑 Get initial admin password from the console output when starting Jenkins")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to download Jenkins: {e}")
            return False
        except subprocess.TimeoutExpired:
            print("⏰ Download timed out")
            return False
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    os_type = get_os()
    
    try:
        if os_type == 'Linux':
            distro = get_linux_distro()
            if 'ubuntu' in distro.lower() or 'debian' in distro.lower():
                print(f'Uninstalling Jenkins from {distro}...')
                subprocess.run(['sudo', 'apt', 'remove', '-y', 'jenkins'], check=True, timeout=60)
                subprocess.run(['sudo', 'apt', 'autoremove', '-y'], check=True, timeout=60)
            elif 'centos' in distro.lower() or 'rhel' in distro.lower() or 'fedora' in distro.lower():
                print(f'Uninstalling Jenkins from {distro}...')
                subprocess.run(['sudo', 'yum', 'remove', '-y', 'jenkins'], check=True, timeout=60)
            else:
                print(f'Unsupported Linux distribution: {distro}')
                return False
                
        elif os_type == 'Darwin':
            print('Uninstalling Jenkins from macOS...')
            if version and version != "latest":
                subprocess.run(['brew', 'uninstall', f'jenkins-lts@{version}'], check=True, timeout=60)
            else:
                subprocess.run(['brew', 'uninstall', 'jenkins-lts'], check=True, timeout=60)
                
        elif os_type == 'Windows':
            print('Uninstalling Jenkins from Windows...')
            print('Please delete the jenkins.war file manually.')
            if version and version != "latest":
                print(f'You may need to look for version {version} in the current directory.')
                
        print("✅ Jenkins uninstalled successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to uninstall Jenkins: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Uninstall timed out")
        return False

def update(version=None):
    """Update Jenkins to the specified version or latest"""
    print("🔄 Updating Jenkins...")
    
    # First uninstall the current version
    if not uninstall():
        print("❌ Failed to uninstall current Jenkins version")
        return False
    
    # Then install the new version
    return install(version)
