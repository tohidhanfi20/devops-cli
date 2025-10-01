
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
                os.system(f'sudo apt-get update && sudo apt-get install terraform={version}')
            else:
                os.system('sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl')
                os.system('curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -')
                os.system('sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"')
                os.system('sudo apt-get update && sudo apt-get install terraform')
            
            # Verify installation and provide guidance
            print('\n🔍 Verifying Terraform installation...')
            
            # Check if terraform is in common locations
            terraform_paths = ['/usr/bin/terraform', '/usr/local/bin/terraform', '/snap/bin/terraform']
            terraform_found = False
            
            for path in terraform_paths:
                if os.path.exists(path):
                    print(f'✅ Terraform found at: {path}')
                    os.system(f'{path} --version')
                    terraform_found = True
                    break
            
            if not terraform_found:
                # Try running terraform command
                result = os.system('terraform --version > /dev/null 2>&1')
                if result == 0:
                    print('✅ Terraform installed successfully!')
                    os.system('terraform --version')
                    terraform_found = True
            
            if not terraform_found:
                print('⚠️  Terraform installation may have failed.')
                print('🔄 Trying alternative installation method...')
                
                # Try direct download installation
                try:
                    if version and version != "latest":
                        terraform_version = version
                    else:
                        terraform_version = "1.13.3"  # Latest stable
                    
                    print(f'📥 Downloading Terraform {terraform_version} directly...')
                    os.system(f'wget https://releases.hashicorp.com/terraform/{terraform_version}/terraform_{terraform_version}_linux_amd64.zip')
                    os.system(f'unzip terraform_{terraform_version}_linux_amd64.zip')
                    os.system('sudo mv terraform /usr/local/bin/')
                    os.system('sudo chmod +x /usr/local/bin/terraform')
                    
                    # Verify the direct installation
                    result = os.system('terraform --version > /dev/null 2>&1')
                    if result == 0:
                        print('✅ Terraform installed successfully via direct download!')
                        os.system('terraform --version')
                    else:
                        print('❌ Direct installation also failed.')
                        print('📋 Manual steps:')
                        print('   1. Check if terraform was installed: dpkg -l | grep terraform')
                        print('   2. Add to PATH: export PATH="/usr/local/bin:$PATH"')
                        print('   3. Restart terminal or run: source ~/.bashrc')
                        
                except Exception as e:
                    print(f'❌ Alternative installation failed: {e}')
                    print('📋 Please install manually or check system requirements.')
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
            
            # Verify installation and provide guidance
            print('\n🔍 Verifying Terraform installation...')
            result = os.system('terraform --version > /dev/null 2>&1')
            if result == 0:
                print('✅ Terraform installed successfully!')
                os.system('terraform --version')
            else:
                print('⚠️  Terraform installed but not found in PATH.')
                print('📋 Next steps:')
                print('   1. Restart your terminal or run: source ~/.bashrc')
                print('   2. Or run: export PATH="/usr/bin:$PATH"')
                print('   3. Verify with: terraform --version')
                print('   4. If still not found, run: which terraform')
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
                os.system(f'sudo apt-get update && sudo apt-get install terraform={version}')
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
