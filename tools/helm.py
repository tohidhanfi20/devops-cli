
import os
from utils import get_os, get_linux_distro
from versioning import get_download_url

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Installing Helm on {distro}...')
            if version and version != "latest":
                print(f'Installing Helm version {version} on Ubuntu...')
                os.system('curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -')
                os.system('sudo apt-get install apt-transport-https --yes')
                os.system('echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list')
                os.system('sudo apt-get update')
                os.system(f'sudo apt-get install helm={version}')
            else:
                os.system('curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -')
                os.system('sudo apt-get install apt-transport-https --yes')
                os.system('echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list')
                os.system('sudo apt-get update')
                os.system('sudo apt-get install helm')
        elif 'centos' in distro.lower():
            print(f'Installing Helm on {distro}...')
            if version and version != "latest":
                print(f'Installing Helm version {version} on CentOS...')
                download_url = get_download_url('helm', version, os_type)
                if download_url:
                    os.system(f'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && chmod 700 get_helm.sh && ./get_helm.sh --version v{version}')
                else:
                    print(f'Could not generate download URL for version {version}')
            else:
                os.system('curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3')
                os.system('chmod 700 get_helm.sh')
                os.system('./get_helm.sh')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing Helm on macOS...')
        if version and version != "latest":
            print(f'Installing Helm version {version} on macOS...')
            os.system(f'brew install helm@{version}')
        else:
            os.system('brew install helm')
    elif os_type == 'Windows':
        print('Installing Helm on Windows...')
        if version and version != "latest":
            os.system(f'winget install -e --id Helm.Helm --version {version}')
        else:
            os.system('winget install -e --id Helm.Helm')
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Uninstalling Helm from {distro}...')
            os.system('sudo apt-get remove helm')
        elif 'centos' in distro.lower():
            print(f'Uninstalling Helm from {distro}...')
            os.system('sudo rm /usr/local/bin/helm')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Uninstalling Helm from macOS...')
        if version and version != "latest":
            os.system(f'brew uninstall helm@{version}')
        else:
            os.system('brew uninstall helm')
    elif os_type == 'Windows':
        print('Uninstalling Helm from Windows...')
        if version and version != "latest":
            os.system(f'winget uninstall -e --id Helm.Helm --version {version}')
        else:
            os.system('winget uninstall -e --id Helm.Helm')
    else:
        print(f'Unsupported OS: {os_type}')

def update(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Updating Helm on {distro}...')
            if version and version != "latest":
                os.system('sudo apt-get update')
                os.system(f'sudo apt-get install helm={version}')
            else:
                os.system('sudo apt-get update')
                os.system('sudo apt-get install helm')
        elif 'centos' in distro.lower():
            print(f'Updating Helm on {distro}...')
            if version and version != "latest":
                download_url = get_download_url('helm', version, os_type)
                if download_url:
                    os.system(f'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && chmod 700 get_helm.sh && ./get_helm.sh --version v{version}')
                else:
                    print(f'Could not generate download URL for version {version}')
            else:
                os.system('./get_helm.sh')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Updating Helm on macOS...')
        if version and version != "latest":
            os.system(f'brew upgrade helm@{version}')
        else:
            os.system('brew upgrade helm')
    elif os_type == 'Windows':
        print('Updating Helm on Windows...')
        if version and version != "latest":
            os.system(f'winget upgrade -e --id Helm.Helm --version {version}')
        else:
            os.system('winget upgrade -e --id Helm.Helm')
    else:
        print(f'Unsupported OS: {os_type}')
