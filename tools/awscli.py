
import os
from utils import get_os, get_linux_distro
from versioning import get_download_url

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower() or 'centos' in distro.lower():
            print(f'Installing awscli on {distro}...')
            if version and version != "latest":
                print(f'Installing awscli version {version} on {distro}...')
                download_url = get_download_url('awscli', version, os_type)
                if download_url:
                    os.system(f'curl "{download_url}" -o "awscliv2.zip"')
                    os.system('unzip awscliv2.zip')
                    os.system('sudo ./aws/install')
                else:
                    print(f'Could not generate download URL for version {version}')
            else:
                # Use latest version URL
                download_url = get_download_url('awscli', 'latest', os_type)
                if download_url:
                    os.system(f'curl "{download_url}" -o "awscliv2.zip"')
                    os.system('unzip awscliv2.zip')
                    os.system('sudo ./aws/install')
                else:
                    print('Could not generate download URL for latest version')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing awscli on macOS...')
        if version and version != "latest":
            print(f'Installing awscli version {version} on macOS...')
            download_url = get_download_url('awscli', version, os_type)
            if download_url:
                os.system(f'curl "{download_url}" -o "AWSCLIV2.pkg"')
                os.system('sudo installer -pkg AWSCLIV2.pkg -target /')
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            download_url = get_download_url('awscli', 'latest', os_type)
            if download_url:
                os.system(f'curl "{download_url}" -o "AWSCLIV2.pkg"')
                os.system('sudo installer -pkg AWSCLIV2.pkg -target /')
            else:
                print('Could not generate download URL for latest version')
    elif os_type == 'Windows':
        print('Installing awscli on Windows...')
        if version and version != "latest":
            print(f'Installing awscli version {version} on Windows...')
            download_url = get_download_url('awscli', version, os_type)
            if download_url:
                os.system(f'msiexec.exe /i {download_url}')
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            download_url = get_download_url('awscli', 'latest', os_type)
            if download_url:
                os.system(f'msiexec.exe /i {download_url}')
            else:
                print('Could not generate download URL for latest version')
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        print('Uninstalling awscli from Linux...')
        os.system('sudo rm -rf /usr/local/aws-cli')
        os.system('sudo rm /usr/local/bin/aws')
    elif os_type == 'Darwin':
        print('Uninstalling awscli from macOS...')
        os.system('sudo rm -rf /usr/local/aws-cli')
        os.system('sudo rm /usr/local/bin/aws')
    elif os_type == 'Windows':
        print('Uninstalling awscli from Windows...')
        # Uninstallation for Windows is manual through "Add or remove programs"
        print('Please uninstall awscli manually through "Add or remove programs"')
        if version and version != "latest":
            print(f'You may need to search for AWS CLI version {version} in "Add or remove programs"')
    else:
        print(f'Unsupported OS: {os_type}')

def update(version=None):
    install(version) # The installation process also handles updates
