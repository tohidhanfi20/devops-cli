
import os
from utils import get_os, get_linux_distro
from versioning import get_download_url

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Installing Jenkins on {distro}...')
            if version and version != "latest":
                print(f'Installing Jenkins version {version} on Ubuntu...')
                os.system('wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -')
                os.system('sudo sh -c \'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list\'')
                os.system('sudo apt-get update')
                os.system(f'sudo apt-get install -y jenkins={version}')
            else:
                os.system('wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -')
                os.system('sudo sh -c \'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list\'')
                os.system('sudo apt-get update')
                os.system('sudo apt-get install -y jenkins')
        elif 'centos' in distro.lower():
            print(f'Installing Jenkins on {distro}...')
            if version and version != "latest":
                print(f'Installing Jenkins version {version} on CentOS...')
                os.system('sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo')
                os.system('sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key')
                os.system(f'sudo yum install -y jenkins-{version}')
            else:
                os.system('sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo')
                os.system('sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key')
                os.system('sudo yum install -y jenkins')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing Jenkins on macOS...')
        if version and version != "latest":
            print(f'Installing Jenkins version {version} on macOS...')
            os.system(f'brew install jenkins-lts@{version}')
        else:
            os.system('brew install jenkins-lts')
    elif os_type == 'Windows':
        print('Installing Jenkins on Windows...')
        if version and version != "latest":
            print(f'Installing Jenkins version {version} on Windows...')
            download_url = get_download_url('jenkins', version, os_type)
            if download_url:
                os.system(f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile .\\jenkins.zip; Expand-Archive .\\jenkins.zip -DestinationPath .\\jenkins"')
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            download_url = get_download_url('jenkins', 'latest', os_type)
            if download_url:
                os.system(f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile .\\jenkins.zip; Expand-Archive .\\jenkins.zip -DestinationPath .\\jenkins"')
            else:
                print('Could not generate download URL for latest version')
        print('Jenkins downloaded and unzipped to .\\jenkins. To start Jenkins, run: java -jar .\\jenkins\\jenkins.war')
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Uninstalling Jenkins from {distro}...')
            os.system('sudo apt-get remove -y jenkins')
        elif 'centos' in distro.lower():
            print(f'Uninstalling Jenkins from {distro}...')
            os.system('sudo yum remove -y jenkins')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Uninstalling Jenkins from macOS...')
        if version and version != "latest":
            os.system(f'brew uninstall jenkins-lts@{version}')
        else:
            os.system('brew uninstall jenkins-lts')
    elif os_type == 'Windows':
        print('Uninstalling Jenkins from Windows...')
        print('Please delete the .\\jenkins directory manually.')
        if version and version != "latest":
            print(f'You may need to look for version {version} in the .\\jenkins directory.')
    else:
        print(f'Unsupported OS: {os_type}')

def update(version=None):
    install(version) # The installation process also handles updates
