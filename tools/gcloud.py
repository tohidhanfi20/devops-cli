
import os
from utils import get_os, get_linux_distro

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower() or 'centos' in distro.lower():
            print(f'Installing gcloud on {distro}...')
            if version and version != "latest":
                print(f'Installing gcloud version {version} on {distro}...')
                os.system(f'curl https://sdk.cloud.google.com | bash -s -- --version={version}')
            else:
                os.system('curl https://sdk.cloud.google.com | bash')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing gcloud on macOS...')
        if version and version != "latest":
            print(f'Installing gcloud version {version} on macOS...')
            os.system(f'curl https://sdk.cloud.google.com | bash -s -- --version={version}')
        else:
            os.system('curl https://sdk.cloud.google.com | bash')
    elif os_type == 'Windows':
        print('Installing gcloud on Windows...')
        if version and version != "latest":
            print(f'Please download Google Cloud SDK Installer for version {version} from https://cloud.google.com/sdk/docs/downloads-versioned-archives')
            os.system("(New-Object Net.WebClient).DownloadFile(\"https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe\", \"GoogleCloudSDKInstaller.exe\")")
            os.system(".\\GoogleCloudSDKInstaller.exe")
        else:
            os.system("(New-Object Net.WebClient).DownloadFile(\"https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe\", \"GoogleCloudSDKInstaller.exe\")")
            os.system(".\\GoogleCloudSDKInstaller.exe")
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    print('Please follow the official documentation to uninstall gcloud CLI.')
    if version and version != "latest":
        print(f'You may need to look for version {version} in the documentation.')

def update(version=None):
    if version and version != "latest":
        print(f'Updating gcloud components to version {version}...')
        os.system(f'gcloud components update --version={version}')
    else:
        os.system('gcloud components update')
