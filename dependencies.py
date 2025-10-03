"""
Dependency Management System for DevOps CLI
Handles automatic installation of dependencies for each tool
"""

import os
import subprocess
import platform
from utils import get_os, get_linux_distro

class DependencyManager:
    """Manages dependencies for DevOps tools"""
    
    def __init__(self):
        self.os_type = get_os()
        self.distro = get_linux_distro() if self.os_type == 'Linux' else None
        
        # Define dependencies for each tool
        self.dependencies = {
            'jenkins': {
                'Linux': {
                    'ubuntu': ['openjdk-21-jre', 'fontconfig'],
                    'debian': ['openjdk-21-jre', 'fontconfig'],
                    'centos': ['java-21-openjdk', 'fontconfig'],
                    'rhel': ['java-21-openjdk', 'fontconfig'],
                    'fedora': ['java-21-openjdk', 'fontconfig']
                },
                'Darwin': ['openjdk@21'],
                'Windows': ['openjdk-21-jre']
            },
            'docker': {
                'Linux': {
                    'ubuntu': ['apt-transport-https', 'ca-certificates', 'curl', 'gnupg', 'lsb-release'],
                    'debian': ['apt-transport-https', 'ca-certificates', 'curl', 'gnupg', 'lsb-release'],
                    'centos': ['yum-utils', 'device-mapper-persistent-data', 'lvm2'],
                    'rhel': ['yum-utils', 'device-mapper-persistent-data', 'lvm2'],
                    'fedora': ['dnf-plugins-core', 'device-mapper-persistent-data', 'lvm2']
                },
                'Darwin': [],
                'Windows': []
            },
            'kubectl': {
                'Linux': {
                    'ubuntu': ['curl'],
                    'debian': ['curl'],
                    'centos': ['curl'],
                    'rhel': ['curl'],
                    'fedora': ['curl']
                },
                'Darwin': [],
                'Windows': []
            },
            'awscli': {
                'Linux': {
                    'ubuntu': ['unzip'],
                    'debian': ['unzip'],
                    'centos': ['unzip'],
                    'rhel': ['unzip'],
                    'fedora': ['unzip']
                },
                'Darwin': [],
                'Windows': []
            },
            'gcloud': {
                'Linux': {
                    'ubuntu': ['curl', 'python3', 'python3-pip'],
                    'debian': ['curl', 'python3', 'python3-pip'],
                    'centos': ['curl', 'python3', 'python3-pip'],
                    'rhel': ['curl', 'python3', 'python3-pip'],
                    'fedora': ['curl', 'python3', 'python3-pip']
                },
                'Darwin': [],
                'Windows': []
            },
            'az': {
                'Linux': {
                    'ubuntu': ['curl', 'lsb-release', 'gnupg'],
                    'debian': ['curl', 'lsb-release', 'gnupg'],
                    'centos': ['curl'],
                    'rhel': ['curl'],
                    'fedora': ['curl']
                },
                'Darwin': [],
                'Windows': []
            },
            'helm': {
                'Linux': {
                    'ubuntu': ['curl'],
                    'debian': ['curl'],
                    'centos': ['curl'],
                    'rhel': ['curl'],
                    'fedora': ['curl']
                },
                'Darwin': [],
                'Windows': []
            },
            'prometheus': {
                'Linux': {
                    'ubuntu': ['curl'],
                    'debian': ['curl'],
                    'centos': ['curl'],
                    'rhel': ['curl'],
                    'fedora': ['curl']
                },
                'Darwin': [],
                'Windows': []
            },
            'terraform': {
                'Linux': {
                    'ubuntu': ['curl', 'unzip'],
                    'debian': ['curl', 'unzip'],
                    'centos': ['curl', 'unzip'],
                    'rhel': ['curl', 'unzip'],
                    'fedora': ['curl', 'unzip']
                },
                'Darwin': [],
                'Windows': []
            }
        }
    
    def get_dependencies(self, tool_name):
        """Get dependencies for a specific tool"""
        if tool_name not in self.dependencies:
            return []
        
        tool_deps = self.dependencies[tool_name]
        
        if self.os_type not in tool_deps:
            return []
        
        if self.os_type == 'Linux' and self.distro:
            # Get distro-specific dependencies
            distro_lower = self.distro.lower()
            for distro_key in tool_deps[self.os_type]:
                if distro_key in distro_lower:
                    return tool_deps[self.os_type][distro_key]
            # Fallback to ubuntu if no specific distro match
            return tool_deps[self.os_type].get('ubuntu', [])
        else:
            return tool_deps[self.os_type]
    
    def check_dependency_installed(self, package_name):
        """Check if a dependency is already installed"""
        try:
            if self.os_type == 'Linux':
                if self.distro and 'ubuntu' in self.distro.lower() or 'debian' in self.distro.lower():
                    result = subprocess.run(['dpkg', '-l', package_name], 
                                          capture_output=True, text=True, timeout=10)
                    return result.returncode == 0 and 'ii' in result.stdout
                elif self.distro and ('centos' in self.distro.lower() or 'rhel' in self.distro.lower() or 'fedora' in self.distro.lower()):
                    result = subprocess.run(['rpm', '-q', package_name], 
                                          capture_output=True, text=True, timeout=10)
                    return result.returncode == 0
            elif self.os_type == 'Darwin':
                result = subprocess.run(['brew', 'list', package_name], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            elif self.os_type == 'Windows':
                # For Windows, we'll assume dependencies are available or will be installed
                return True
        except Exception:
            return False
        return False
    
    def install_dependency(self, package_name):
        """Install a single dependency"""
        print(f"Installing dependency: {package_name}")
        
        try:
            if self.os_type == 'Linux':
                if self.distro and ('ubuntu' in self.distro.lower() or 'debian' in self.distro.lower()):
                    subprocess.run(['sudo', 'apt', 'update'], check=True, timeout=60)
                    subprocess.run(['sudo', 'apt', 'install', '-y', package_name], check=True, timeout=300)
                elif self.distro and ('centos' in self.distro.lower() or 'rhel' in self.distro.lower()):
                    subprocess.run(['sudo', 'yum', 'install', '-y', package_name], check=True, timeout=300)
                elif self.distro and 'fedora' in self.distro.lower():
                    subprocess.run(['sudo', 'dnf', 'install', '-y', package_name], check=True, timeout=300)
            elif self.os_type == 'Darwin':
                subprocess.run(['brew', 'install', package_name], check=True, timeout=300)
            elif self.os_type == 'Windows':
                # For Windows, we'll use chocolatey or winget
                try:
                    subprocess.run(['choco', 'install', package_name, '-y'], check=True, timeout=300)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    try:
                        subprocess.run(['winget', 'install', package_name], check=True, timeout=300)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        print(f"Warning: Could not install {package_name} on Windows. Please install manually.")
                        return False
            
            print(f"✅ Successfully installed {package_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package_name}: {e}")
            return False
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout installing {package_name}")
            return False
        except Exception as e:
            print(f"❌ Error installing {package_name}: {e}")
            return False
    
    def install_dependencies(self, tool_name):
        """Install all dependencies for a tool"""
        dependencies = self.get_dependencies(tool_name)
        
        if not dependencies:
            print(f"No dependencies required for {tool_name}")
            return True
        
        print(f"Installing dependencies for {tool_name}: {', '.join(dependencies)}")
        
        failed_deps = []
        
        for dep in dependencies:
            if not self.check_dependency_installed(dep):
                if not self.install_dependency(dep):
                    failed_deps.append(dep)
            else:
                print(f"✅ {dep} is already installed")
        
        if failed_deps:
            print(f"❌ Failed to install dependencies: {', '.join(failed_deps)}")
            return False
        
        print(f"✅ All dependencies for {tool_name} installed successfully")
        return True
    
    def validate_dependencies(self, tool_name):
        """Validate that all dependencies are installed"""
        dependencies = self.get_dependencies(tool_name)
        
        if not dependencies:
            return True
        
        missing_deps = []
        for dep in dependencies:
            if not self.check_dependency_installed(dep):
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"❌ Missing dependencies for {tool_name}: {', '.join(missing_deps)}")
            return False
        
        return True

# Global dependency manager instance
dependency_manager = DependencyManager()
