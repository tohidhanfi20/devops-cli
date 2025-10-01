
import os
from utils import get_os, get_linux_distro
from versioning import get_download_url

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Installing az cli on {distro}...')
            if version and version != "latest":
                print(f'Installing az cli version {version} on {distro}...')
                os.system(f'curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash -s -- --version {version}')
            else:
                os.system('curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash')
        elif 'centos' in distro.lower():
            print(f'Installing az cli on {distro}...')
            if version and version != "latest":
                print(f'Installing az cli version {version} on {distro}...')
                os.system('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc')
                os.system('echo -e "[azure-cli]\nname=Azure CLI\nbaseurl=https://packages.microsoft.com/yumrepos/azure-cli\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo')
                os.system(f'sudo yum install -y azure-cli-{version}')
            else:
                os.system('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc')
                os.system('echo -e "[azure-cli]\nname=Azure CLI\nbaseurl=https://packages.microsoft.com/yumrepos/azure-cli\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/azure-cli.repo')
                os.system('sudo yum install -y azure-cli')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing az cli on macOS...')
        if version and version != "latest":
            print(f'Installing az cli version {version} on macOS...')
            os.system(f'brew install azure-cli@{version}')
        else:
            os.system('brew install azure-cli')
    elif os_type == 'Windows':
        print('Installing az cli on Windows...')
        if version and version != "latest":
            print(f'Installing Azure CLI version {version} on Windows...')
            download_url = get_download_url('az', version, os_type)
            if download_url:
                os.system(f"powershell -Command \"Invoke-WebRequest -Uri {download_url} -OutFile .\\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'\"")
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            os.system("powershell -Command \"Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'\"")
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Uninstalling az cli from {distro}...')
            os.system('sudo apt-get remove -y azure-cli')
        elif 'centos' in distro.lower():
            print(f'Uninstalling az cli from {distro}...')
            os.system('sudo yum remove -y azure-cli')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Uninstalling az cli from macOS...')
        if version and version != "latest":
            os.system(f'brew uninstall azure-cli@{version}')
        else:
            os.system('brew uninstall azure-cli')
    elif os_type == 'Windows':
        print('Uninstalling az cli from Windows...')
        os.system('powershell -Command "(Get-WmiObject -Class Win32_Product -Filter \"Name=\"Microsoft Azure CLI\\\"\").Uninstall()"')
        if version and version != "latest":
            print(f'You may need to look for version {version} in "Add or remove programs"')
    else:
        print(f'Unsupported OS: {os_type}')

def update(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Updating az cli on {distro}...')
            if version and version != "latest":
                os.system(f'sudo apt-get update && sudo apt-get install --only-upgrade -y azure-cli={version}')
            else:
                os.system('sudo apt-get update && sudo apt-get install --only-upgrade -y azure-cli')
        elif 'centos' in distro.lower():
            print(f'Updating az cli on {distro}...')
            if version and version != "latest":
                os.system(f'sudo yum update -y azure-cli-{version}')
            else:
                os.system('sudo yum update -y azure-cli')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Updating az cli on macOS...')
        if version and version != "latest":
            os.system(f'brew upgrade azure-cli@{version}')
        else:
            os.system('brew upgrade azure-cli')
    elif os_type == 'Windows':
        print('Updating az cli on Windows...')
        if version and version != "latest":
            print(f'Updating Azure CLI to version {version} on Windows...')
            download_url = get_download_url('az', version, os_type)
            if download_url:
                os.system(f"powershell -Command \"Invoke-WebRequest -Uri {download_url} -OutFile .\\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'\"")
            else:
                print(f'Could not generate download URL for version {version}')
        else:
            os.system("powershell -Command \"Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'\"")
    else:
        print(f'Unsupported OS: {os_type}')
