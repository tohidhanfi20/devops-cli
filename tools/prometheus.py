
import os
from utils import get_os, get_linux_distro
from versioning import get_download_url

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        print('Installing Prometheus on Linux...')
        if version and version != "latest":
            print(f'Installing Prometheus version {version} on Linux...')
            download_url = get_download_url('prometheus', version, os_type)
            if download_url:
                os.system(f'wget {download_url}')
                os.system(f'tar xvfz prometheus-{version}.linux-amd64.tar.gz')
                print(f'Prometheus downloaded and extracted. You can start it by running ./prometheus-{version}.linux-amd64/prometheus')
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            # Use latest version
            download_url = get_download_url('prometheus', 'latest', os_type)
            if download_url:
                os.system(f'wget {download_url}')
                os.system('tar xvfz prometheus-*.linux-amd64.tar.gz')
                print('Prometheus downloaded and extracted. You can start it by running ./prometheus-*/prometheus')
            else:
                print('Could not generate download URL for latest version')
    elif os_type == 'Darwin':
        print('Installing Prometheus on macOS...')
        if version and version != "latest":
            print(f'Installing Prometheus version {version} on macOS...')
            os.system(f'brew install prometheus@{version}')
        else:
            os.system('brew install prometheus')
    elif os_type == 'Windows':
        print('Installing Prometheus on Windows...')
        if version and version != "latest":
            download_url = get_download_url('prometheus', version, os_type)
            if download_url:
                os.system(f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile .\\prometheus.zip; Expand-Archive .\\prometheus.zip -DestinationPath .\\prometheus"')
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            download_url = get_download_url('prometheus', 'latest', os_type)
            if download_url:
                os.system(f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile .\\prometheus.zip; Expand-Archive .\\prometheus.zip -DestinationPath .\\prometheus"')
            else:
                print('Could not generate download URL for latest version')
        print('Prometheus downloaded and unzipped to .\\prometheus. You can start it by running .\\prometheus\\prometheus.exe')
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        print('Uninstalling Prometheus from Linux...')
        if version and version != "latest":
            os.system(f'rm -rf prometheus-{version}.linux-amd64.tar.gz prometheus-{version}.linux-amd64')
        else:
            os.system('rm -rf prometheus-2.37.0.linux-amd64.tar.gz prometheus-2.37.0.linux-amd64')
    elif os_type == 'Darwin':
        print('Uninstalling Prometheus from macOS...')
        if version and version != "latest":
            os.system(f'brew uninstall prometheus@{version}')
        else:
            os.system('brew uninstall prometheus')
    elif os_type == 'Windows':
        print('Uninstalling Prometheus from Windows...')
        print('Please delete the .\\prometheus directory manually.')
        if version and version != "latest":
            print(f'You may need to look for version {version} in the .\\prometheus directory.')
    else:
        print(f'Unsupported OS: {os_type}')

def update(version=None):
    install(version) # The installation process also handles updates
