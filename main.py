import argparse
import os
import platform
import sys
from versioning import (
    get_docker_versions, get_kubectl_versions, get_awscli_versions,
    get_gcloud_versions, get_az_versions, get_jenkins_versions,
    get_helm_versions, get_prometheus_versions, get_terraform_versions
)

from tools import docker, kubectl, awscli, gcloud, az, jenkins, helm, prometheus, terraform
import interactive

# Application version
__version__ = "1.0.0"

def show_version():
    """Show the application version"""
    print(f"DevOps CLI v{__version__}")
    print(f"Python {sys.version.split()[0]}")
    print(f"Platform: {platform.system()} {platform.release()}")

def show_help():
    """Show comprehensive help for the application"""
    print("""
🚀 DevOps CLI v1.0.0
====================

DESCRIPTION:
    A universal installer for DevOps tools across Windows, macOS, and Linux.
    Automatically fetches latest versions and installs tools with proper dependencies.

USAGE:
    devops-cli <command> [options]

COMMANDS:
    init                    Start interactive installation session (recommended for servers)
    install <tool>          Install a specific tool
    uninstall <tool>        Uninstall a tool
    update <tool>           Update a tool to latest version
    list                    List all available tools
    versions <tool>         Show available versions for a tool
    status                  Check installation status of all tools
    --version, -v           Show application version
    --help, -h              Show this help message

AVAILABLE TOOLS:
    🐳  docker              Docker Desktop (Windows/macOS) or Docker CE (Linux)
    ☸️   kubectl             Kubernetes command-line tool
    ☁️   awscli              Amazon Web Services CLI
    🌩️   gcloud              Google Cloud SDK
    🔵   az                  Azure CLI
    🔧   jenkins             Jenkins CI/CD server
    ⛵   helm                Kubernetes package manager
    📊   prometheus          Monitoring and alerting system
    🏗️   terraform           Infrastructure as Code tool

EXAMPLES:
    # Interactive installation
    devops-cli init

    # Install specific tools
    devops-cli install docker --version 4.47.0
    devops-cli install kubectl
    devops-cli install awscli --version 2.13.0

    # Update tools
    devops-cli update docker
    devops-cli update all

    # Check status
    devops-cli status
    devops-cli versions docker

    # Uninstall tools
    devops-cli uninstall docker

FEATURES:
    ✅ Cross-platform support (Windows, macOS, Linux)
    ✅ Dynamic version fetching from official sources
    ✅ Automatic dependency management
    ✅ Interactive and command-line modes
    ✅ Version management and updates
    ✅ Clean uninstallation

SUPPORTED OPERATING SYSTEMS:
    • Windows 10/11
    • macOS 10.15+
    • Ubuntu 18.04+
    • CentOS/RHEL 7+
    • Debian 9+

For more information, visit: https://github.com/yourusername/devops-cli
    """)

def list_tools():
    """List all available tools with their status"""
    tools = {
        'docker': '🐳 Docker - Container platform',
        'kubectl': '☸️ kubectl - Kubernetes CLI',
        'awscli': '☁️ AWS CLI - Amazon Web Services CLI',
        'gcloud': '🌩️ Google Cloud SDK - Google Cloud Platform tools',
        'az': '🔵 Azure CLI - Microsoft Azure CLI',
        'jenkins': '🔧 Jenkins - CI/CD automation server',
        'helm': '⛵ Helm - Kubernetes package manager',
        'prometheus': '📊 Prometheus - Monitoring system',
        'terraform': '🏗️ Terraform - Infrastructure as Code'
    }
    
    print("Available DevOps CLI Tools:")
    print("=" * 50)
    for tool, description in tools.items():
        print(f"{description}")
    print("\nUse 'devops-cli install <tool>' to install a tool")
    print("Use 'devops-cli versions <tool>' to see available versions")

def show_tool_versions(tool):
    """Show available versions for a specific tool"""
    os_type = platform.system()
    
    version_functions = {
        'docker': get_docker_versions,
        'kubectl': get_kubectl_versions,
        'awscli': get_awscli_versions,
        'gcloud': get_gcloud_versions,
        'az': get_az_versions,
        'jenkins': get_jenkins_versions,
        'helm': get_helm_versions,
        'prometheus': get_prometheus_versions,
        'terraform': get_terraform_versions
    }
    
    if tool not in version_functions:
        print(f"Error: Unknown tool '{tool}'")
        print("Available tools: docker, kubectl, awscli, gcloud, az, jenkins, helm, prometheus, terraform")
        return
    
    print(f"Available versions for {tool}:")
    print("=" * 40)
    
    try:
        if tool == 'docker' and os_type == 'Linux':
            # For Linux, we need to get the distro
            import distro
            distro_name = distro.name()
            versions = version_functions[tool](os_type, distro_name)
        else:
            versions = version_functions[tool](os_type)
        
        for i, version in enumerate(versions, 1):
            print(f"{i}. {version}")
        
        print(f"\nTotal: {len(versions)} versions available")
        print("Use 'devops-cli install <tool> --version <version>' to install a specific version")
        
    except Exception as e:
        print(f"Error fetching versions: {e}")

def check_status():
    """Check installation status of all tools"""
    print("DevOps CLI Installation Status:")
    print("=" * 50)
    
    tools = ['docker', 'kubectl', 'awscli', 'gcloud', 'az', 'jenkins', 'helm', 'prometheus', 'terraform']
    
    for tool in tools:
        # This would check if the tool is installed
        # For now, we'll show a placeholder
        print(f"🔍 {tool}: Checking...")
    
    print("\nNote: Status checking will be implemented in future versions")

def main():
    # Handle version and help flags first
    if len(sys.argv) == 1:
        show_help()
        return
    
    if '--version' in sys.argv or '-v' in sys.argv:
        show_version()
        return
    
    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        return
    
    parser = argparse.ArgumentParser(
        description='DevOps CLI Installer & Updater',
        add_help=False  # We'll handle help manually
    )
    subparsers = parser.add_subparsers(dest='command')

    # Init command
    init_parser = subparsers.add_parser('init', help='Start an interactive installation session')

    # Install command
    install_parser = subparsers.add_parser('install', help='Install a tool')
    install_parser.add_argument('tool', choices=['docker', 'kubectl', 'awscli', 'gcloud', 'az', 'jenkins', 'helm', 'prometheus', 'terraform'], help='Tool to install')
    install_parser.add_argument('--version', help='Specify the version to install')

    # Uninstall command
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall a tool')
    uninstall_parser.add_argument('tool', choices=['docker', 'kubectl', 'awscli', 'gcloud', 'az', 'jenkins', 'helm', 'prometheus', 'terraform'], help='Tool to uninstall')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update a tool')
    update_parser.add_argument('tool', choices=['docker', 'kubectl', 'awscli', 'gcloud', 'az', 'jenkins', 'helm', 'prometheus', 'terraform', 'all'], help='Tool to update')

    # List command
    list_parser = subparsers.add_parser('list', help='List all available tools')

    # Versions command
    versions_parser = subparsers.add_parser('versions', help='Show available versions for a tool')
    versions_parser.add_argument('tool', choices=['docker', 'kubectl', 'awscli', 'gcloud', 'az', 'jenkins', 'helm', 'prometheus', 'terraform'], help='Tool to show versions for')

    # Status command
    status_parser = subparsers.add_parser('status', help='Check installation status of all tools')

    args = parser.parse_args()

    if args.command == 'init':
        interactive.start_interactive_session()
    elif args.command == 'list':
        list_tools()
    elif args.command == 'versions':
        show_tool_versions(args.tool)
    elif args.command == 'status':
        check_status()
    elif args.command == 'install':
        if args.tool == 'docker':
            docker.install(version=args.version)
        elif args.tool == 'kubectl':
            kubectl.install(version=args.version)
        elif args.tool == 'awscli':
            awscli.install(version=args.version)
        elif args.tool == 'gcloud':
            gcloud.install(version=args.version)
        elif args.tool == 'az':
            az.install(version=args.version)
        elif args.tool == 'jenkins':
            jenkins.install(version=args.version)
        elif args.tool == 'helm':
            helm.install(version=args.version)
        elif args.tool == 'prometheus':
            prometheus.install(version=args.version)
        elif args.tool == 'terraform':
            terraform.install(version=args.version)
    elif args.command == 'uninstall':
        if args.tool == 'docker':
            docker.uninstall()
        elif args.tool == 'kubectl':
            kubectl.uninstall()
        elif args.tool == 'awscli':
            awscli.uninstall()
        elif args.tool == 'gcloud':
            gcloud.uninstall()
        elif args.tool == 'az':
            az.uninstall()
        elif args.tool == 'jenkins':
            jenkins.uninstall()
        elif args.tool == 'helm':
            helm.uninstall()
        elif args.tool == 'prometheus':
            prometheus.uninstall()
        elif args.tool == 'terraform':
            terraform.uninstall()
    elif args.command == 'update':
        if args.tool == 'all':
            print("Updating all installed tools...")
            tools = [docker, kubectl, awscli, gcloud, az, jenkins, helm, prometheus, terraform]
            for tool in tools:
                try:
                    tool.update()
                except Exception as e:
                    print(f"Error updating {tool.__name__}: {e}")
        elif args.tool == 'docker':
            docker.update()
        elif args.tool == 'kubectl':
            kubectl.update()
        elif args.tool == 'awscli':
            awscli.update()
        elif args.tool == 'gcloud':
            gcloud.update()
        elif args.tool == 'az':
            az.update()
        elif args.tool == 'jenkins':
            jenkins.update()
        elif args.tool == 'helm':
            helm.update()
        elif args.tool == 'prometheus':
            prometheus.update()
        elif args.tool == 'terraform':
            terraform.update()

if __name__ == '__main__':
    main()