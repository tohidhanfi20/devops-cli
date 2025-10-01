import os
import sys
from utils import get_os, get_linux_distro
from versioning import (
    get_docker_versions, get_kubectl_versions, get_awscli_versions, 
    get_gcloud_versions, get_az_versions, get_jenkins_versions, 
    get_helm_versions, get_prometheus_versions, get_terraform_versions
)
from tools import docker, kubectl, awscli, gcloud, az, jenkins, helm, prometheus, terraform

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_welcome():
    """Show welcome message"""
    clear_screen()
    print("🚀 DevOps CLI - Interactive Setup")
    print("=" * 50)
    print("Welcome! This will help you install DevOps tools on your server.")
    print()

def show_tools_menu():
    """Show the main tools menu"""
    tools = {
        1: {"name": "🐳 Docker", "description": "Container platform", "module": docker},
        2: {"name": "☸️ kubectl", "description": "Kubernetes CLI", "module": kubectl},
        3: {"name": "☁️ AWS CLI", "description": "Amazon Web Services CLI", "module": awscli},
        4: {"name": "🌩️ gcloud", "description": "Google Cloud SDK", "module": gcloud},
        5: {"name": "🔵 Azure CLI", "description": "Microsoft Azure CLI", "module": az},
        6: {"name": "🔧 Jenkins", "description": "CI/CD automation server", "module": jenkins},
        7: {"name": "⛵ Helm", "description": "Kubernetes package manager", "module": helm},
        8: {"name": "📊 Prometheus", "description": "Monitoring system", "module": prometheus},
        9: {"name": "🏗️ Terraform", "description": "Infrastructure as Code", "module": terraform}
    }
    
    print("Available Tools:")
    print("-" * 30)
    for num, tool in tools.items():
        print(f"{num}. {tool['name']} - {tool['description']}")
    print()
    
    return tools

def get_tool_choice():
    """Get user's tool choice"""
    while True:
        try:
            choice = input("Select tool number (1-9): ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= 9:
                    return choice_num
            print("❌ Invalid choice. Please enter a number between 1-9.")
        except KeyboardInterrupt:
            print("\n\n👋 Installation cancelled.")
            sys.exit(0)

def show_versions_menu(tool_name, tool_key):
    """Show versions menu for selected tool"""
    os_type = get_os()
    distro = get_linux_distro() if os_type == "Linux" else None
    
    # Get version function mapping
    version_functions = {
        "docker": get_docker_versions,
        "kubectl": get_kubectl_versions,
        "awscli": get_awscli_versions,
        "gcloud": get_gcloud_versions,
        "az": get_az_versions,
        "jenkins": get_jenkins_versions,
        "helm": get_helm_versions,
        "prometheus": get_prometheus_versions,
        "terraform": get_terraform_versions
    }
    
    print(f"\n📋 Available {tool_name} versions:")
    print("-" * 40)
    
    try:
        # Get versions based on OS
        if tool_key in version_functions:
            if os_type == "Linux" and distro:
                versions = version_functions[tool_key](os_type, distro)
            else:
                versions = version_functions[tool_key](os_type)
        else:
            print("❌ Version listing not available for this tool.")
            return None
        
        if not versions:
            print("❌ No versions available.")
            return None
        
        # Show versions with numbers
        for i, version in enumerate(versions, 1):
            latest_marker = " (Latest)" if i == 1 and version != "latest" else ""
            print(f"{i}. {version}{latest_marker}")
        
        return versions
        
    except Exception as e:
        print(f"❌ Error fetching versions: {e}")
        return None

def get_version_choice(versions):
    """Get user's version choice"""
    if not versions:
        return None
        
    while True:
        try:
            choice = input(f"\nSelect version number (1-{len(versions)}): ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(versions):
                    return versions[choice_num - 1]
            print(f"❌ Invalid choice. Please enter a number between 1-{len(versions)}.")
        except KeyboardInterrupt:
            print("\n\n👋 Installation cancelled.")
            sys.exit(0)

def install_tool(tool_name, tool_module, version):
    """Install the selected tool"""
    print(f"\n🔧 Installing {tool_name} version {version}...")
    print("-" * 50)
    
    try:
        tool_module.install(version=version)
        print(f"\n✅ {tool_name} {version} installed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Failed to install {tool_name}: {e}")
        return False

def ask_continue():
    """Ask if user wants to install another tool"""
    while True:
        try:
            choice = input("\n🔄 Install another tool? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("❌ Please enter 'y' or 'n'.")
        except KeyboardInterrupt:
            print("\n\n👋 Installation cancelled.")
            sys.exit(0)

def start_interactive_session():
    """Main interactive session"""
    show_welcome()
    
    # Get OS info
    os_type = get_os()
    print(f"🖥️  Detected OS: {os_type}")
    if os_type == "Linux":
        distro = get_linux_distro()
        print(f"🐧 Linux Distribution: {distro}")
    print()
    
    # Tool mapping
    tool_mapping = {
        1: {"key": "docker", "name": "Docker", "module": docker},
        2: {"key": "kubectl", "name": "kubectl", "module": kubectl},
        3: {"key": "awscli", "name": "AWS CLI", "module": awscli},
        4: {"key": "gcloud", "name": "Google Cloud SDK", "module": gcloud},
        5: {"key": "az", "name": "Azure CLI", "module": az},
        6: {"key": "jenkins", "name": "Jenkins", "module": jenkins},
        7: {"key": "helm", "name": "Helm", "module": helm},
        8: {"key": "prometheus", "name": "Prometheus", "module": prometheus},
        9: {"key": "terraform", "name": "Terraform", "module": terraform}
    }
    
    while True:
        # Show tools menu
        tools = show_tools_menu()
        
        # Get tool choice
        tool_choice = get_tool_choice()
        selected_tool = tool_mapping[tool_choice]
        
        # Show versions
        versions = show_versions_menu(selected_tool["name"], selected_tool["key"])
        if not versions:
            continue
        
        # Get version choice
        selected_version = get_version_choice(versions)
        if not selected_version:
            continue
        
        # Install tool
        success = install_tool(selected_tool["name"], selected_tool["module"], selected_version)
        
        if success:
            # Ask if user wants to install another tool
            if not ask_continue():
                break
        else:
            # Ask if user wants to try again
            if not ask_continue():
                break
    
    print("\n🎉 Setup complete!")
    print("You can now use the installed tools or run 'devops-cli init' again to install more tools.")
    print("\n💡 Useful commands:")
    print("  devops-cli list          # List all available tools")
    print("  devops-cli status        # Check installation status")
    print("  devops-cli versions <tool>  # Show available versions")
    print("\n🔧 If a tool command is not found:")
    print("  1. Restart your terminal or run: source ~/.bashrc")
    print("  2. Check if the tool is in PATH: which <tool-name>")
    print("  3. Try running the tool with full path: /usr/bin/<tool-name>")
    print("  4. For package managers (apt/yum), restart terminal to refresh PATH")