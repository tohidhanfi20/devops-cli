
import os
from utils import get_os, get_linux_distro

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print('Installing Docker on Ubuntu...')
            os.system('sudo apt-get update')
            os.system('sudo apt-get install -y docker-ce docker-ce-cli containerd.io')
        elif 'centos' in distro.lower():
            print('Installing Docker on CentOS...')
            os.system('sudo yum install -y -q yum-utils')
            os.system('sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo')
            os.system('sudo yum install -y docker-ce docker-ce-cli containerd.io')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing Docker on macOS...')
        os.system('brew install --cask docker')
    elif os_type == 'Windows':
        # Add Windows installation logic here
        print('Installing Docker on Windows...')
        if version and version != "latest":
            print(f'Please download Docker Desktop Installer for version {version} from https://docs.docker.com/desktop/release-notes/')
            print('Once downloaded, place the installer in the same directory as this script.')
            os.system(f"powershell -Command \"Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license'\"")
        else:
            print('Please download Docker Desktop Installer from https://www.docker.com/products/docker-desktop')
            print('Once downloaded, place the installer in the same directory as this script.')
            os.system("powershell -Command \"Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license'\"")
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall():
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print('Uninstalling Docker from Ubuntu...')
            os.system('sudo apt-get remove -y docker docker-engine docker.io containerd runc')
        elif 'centos' in distro.lower():
            print('Uninstalling Docker from CentOS...')
            os.system('sudo yum remove -y docker-ce docker-ce-cli containerd.io')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Uninstalling Docker from macOS...')
        os.system('brew uninstall --cask docker')
    elif os_type == 'Windows':
        # Add Windows uninstallation logic here
        print('Uninstalling Docker from Windows...')
        os.system("powershell -Command \"Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'uninstall'\"")
    else:
        print(f'Unsupported OS: {os_type}')

def update():
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print('Updating Docker on Ubuntu...')
            os.system('sudo apt-get update')
            os.system('sudo apt-get install -y docker-ce docker-ce-cli containerd.io')
        elif 'centos' in distro.lower():
            print('Updating Docker on CentOS...')
            os.system('sudo yum install -y docker-ce docker-ce-cli containerd.io')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Updating Docker on macOS...')
        os.system('brew upgrade --cask docker')
    elif os_type == 'Windows':
        # Add Windows update logic here
        print('Updating Docker on Windows...')
        os.system("powershell -Command \"Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license'\"")
    else:
        print(f'Unsupported OS: {os_type}')
