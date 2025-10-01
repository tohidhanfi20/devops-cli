import os
from utils import get_os, get_linux_distro
from versioning import get_download_url

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Installing kubectl on {distro}...')
            if version and version != "latest":
                print(f'Installing kubectl version {version} on Ubuntu...')
                download_url = get_download_url('kubectl', version, os_type)
                if download_url:
                    os.system(f'curl -LO {download_url}')
                    os.system('sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl')
                else:
                    print(f'Could not generate download URL for version {version}')
            else:
                os.system('sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg2')
                os.system('curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')
                os.system('echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list')
                os.system('sudo apt-get update')
                os.system('sudo apt-get install -y kubectl')
        elif 'centos' in distro.lower():
            print(f'Installing kubectl on {distro}...')
            if version and version != "latest":
                print(f'Installing kubectl version {version} on CentOS...')
                download_url = get_download_url('kubectl', version, os_type)
                if download_url:
                    os.system(f'curl -LO {download_url}')
                    os.system('sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl')
                else:
                    print(f'Could not generate download URL for version {version}')
            else:
                os.system('''cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF''')
                os.system('sudo yum install -y kubectl')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing kubectl on macOS...')
        if version and version != "latest":
            print(f'Installing kubectl version {version} on macOS...')
            download_url = get_download_url('kubectl', version, os_type)
            if download_url:
                os.system(f'curl -LO {download_url}')
                os.system('chmod +x kubectl')
                os.system('sudo mv kubectl /usr/local/bin/')
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            os.system('brew install kubectl')
    elif os_type == 'Windows':
        print('Installing kubectl on Windows...')
        if version and version != "latest":
            os.system(f'winget install -e --id Kubernetes.kubectl --version {version}')
        else:
            os.system('winget install -e --id Kubernetes.kubectl')
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Uninstalling kubectl from {distro}...')
            os.system('sudo apt-get remove -y kubectl')
            os.system('sudo rm -f /usr/local/bin/kubectl') # For manually installed binaries
        elif 'centos' in distro.lower():
            print(f'Uninstalling kubectl from {distro}...')
            os.system('sudo yum remove -y kubectl')
            os.system('sudo rm -f /usr/local/bin/kubectl') # For manually installed binaries
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Uninstalling kubectl from macOS...')
        os.system('brew uninstall kubectl')
        os.system('sudo rm -f /usr/local/bin/kubectl') # For manually installed binaries
    elif os_type == 'Windows':
        print('Uninstalling kubectl from Windows...')
        if version and version != "latest":
            os.system(f'winget uninstall -e --id Kubernetes.kubectl --version {version}')
        else:
            os.system('winget uninstall -e --id Kubernetes.kubectl')
    else:
        print(f'Unsupported OS: {os_type}')

def update(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Updating kubectl on {distro}...')
            if version and version != "latest":
                print(f'Installing kubectl version {version} on Ubuntu...')
                download_url = get_download_url('kubectl', version, os_type)
                if download_url:
                    os.system(f'curl -LO {download_url}')
                    os.system('sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl')
                else:
                    print(f'Could not generate download URL for version {version}')
            else:
                os.system('sudo apt-get update')
                os.system('sudo apt-get install -y kubectl')
        elif 'centos' in distro.lower():
            print(f'Updating kubectl on {distro}...')
            if version and version != "latest":
                print(f'Installing kubectl version {version} on CentOS...')
                download_url = get_download_url('kubectl', version, os_type)
                if download_url:
                    os.system(f'curl -LO {download_url}')
                    os.system('sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl')
                else:
                    print(f'Could not generate download URL for version {version}')
            else:
                os.system('sudo yum install -y kubectl')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Updating kubectl on macOS...')
        if version and version != "latest":
            print(f'Installing kubectl version {version} on macOS...')
            download_url = get_download_url('kubectl', version, os_type)
            if download_url:
                os.system(f'curl -LO {download_url}')
                os.system('chmod +x kubectl')
                os.system('sudo mv kubectl /usr/local/bin/')
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            os.system('brew upgrade kubectl')
    elif os_type == 'Windows':
        print('Updating kubectl on Windows...')
        if version and version != "latest":
            os.system(f'winget upgrade -e --id Kubernetes.kubectl --version {version}')
        else:
            os.system('winget upgrade -e --id Kubernetes.kubectl')
    else:
        print(f'Unsupported OS: {os_type}')