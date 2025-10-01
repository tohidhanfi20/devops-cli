
import os
from utils import get_os, get_linux_distro

def install(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Installing Terraform on {distro}...')
            if version and version != "latest":
                print(f'Installing Terraform version {version} on Ubuntu...')
                os.system('sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl')
                os.system('curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -')
                os.system('sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"')
                os.system('sudo apt-get update && sudo apt-get install terraform={version}')
            else:
                os.system('sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl')
                os.system('curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -')
                os.system('sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"')
                os.system('sudo apt-get update && sudo apt-get install terraform')
        elif 'centos' in distro.lower():
            print(f'Installing Terraform on {distro}...')
            if version and version != "latest":
                print(f'Installing Terraform version {version} on CentOS...')
                os.system('sudo yum install -y yum-utils')
                os.system('sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo')
                os.system(f'sudo yum -y install terraform-{version}')
            else:
                os.system('sudo yum install -y yum-utils')
                os.system('sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo')
                os.system('sudo yum -y install terraform')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Installing Terraform on macOS...')
        if version and version != "latest":
            print(f'Installing Terraform version {version} on macOS...')
            os.system('brew tap hashicorp/tap')
            os.system(f'brew install hashicorp/tap/terraform@{version}')
        else:
            os.system('brew tap hashicorp/tap')
            os.system('brew install hashicorp/tap/terraform')
    elif os_type == 'Windows':
        print('Installing Terraform on Windows...')
        if version and version != "latest":
            os.system(f'winget install -e --id HashiCorp.Terraform --version {version}')
        else:
            os.system('winget install -e --id HashiCorp.Terraform')
    else:
        print(f'Unsupported OS: {os_type}')

def uninstall(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Uninstalling Terraform from {distro}...')
            os.system('sudo apt-get remove terraform')
        elif 'centos' in distro.lower():
            print(f'Uninstalling Terraform from {distro}...')
            os.system('sudo yum remove terraform')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Uninstalling Terraform from macOS...')
        if version and version != "latest":
            os.system(f'brew uninstall hashicorp/tap/terraform@{version}')
        else:
            os.system('brew uninstall hashicorp/tap/terraform')
    elif os_type == 'Windows':
        print('Uninstalling Terraform from Windows...')
        if version and version != "latest":
            os.system(f'winget uninstall -e --id HashiCorp.Terraform --version {version}')
        else:
            os.system('winget uninstall -e --id HashiCorp.Terraform')
    else:
        print(f'Unsupported OS: {os_type}')

def update(version=None):
    os_type = get_os()
    if os_type == 'Linux':
        distro = get_linux_distro()
        if 'ubuntu' in distro.lower():
            print(f'Updating Terraform on {distro}...')
            if version and version != "latest":
                os.system('sudo apt-get update && sudo apt-get install terraform={version}')
            else:
                os.system('sudo apt-get update && sudo apt-get install terraform')
        elif 'centos' in distro.lower():
            print(f'Updating Terraform on {distro}...')
            if version and version != "latest":
                os.system(f'sudo yum -y install terraform-{version}')
            else:
                os.system('sudo yum -y install terraform')
        else:
            print(f'Unsupported Linux distribution: {distro}')
    elif os_type == 'Darwin':
        print('Updating Terraform on macOS...')
        if version and version != "latest":
            os.system(f'brew upgrade hashicorp/tap/terraform@{version}')
        else:
            os.system('brew upgrade hashicorp/tap/terraform')
    elif os_type == 'Windows':
        print('Updating Terraform on Windows...')
        if version and version != "latest":
            os.system(f'winget upgrade -e --id HashiCorp.Terraform --version {version}')
        else:
            os.system('winget upgrade -e --id HashiCorp.Terraform')
    else:
        print(f'Unsupported OS: {os_type}')
