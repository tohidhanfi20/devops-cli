# DevOps CLI

![Latest GitHub release](https://img.shields.io/github/release/tohidhanfi20/devops-cli.svg)
![GitHub stars](https://img.shields.io/github/stars/tohidhanfi20/devops-cli.svg?label=github%20stars)
![Python version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Platform support](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A universal installer for DevOps tools across Windows, macOS, and Linux with dynamic version fetching from official sources.

[Install &rarr;](#installation)

## What is DevOps CLI?

**DevOps CLI** is a lightweight CLI tool that automatically installs and manages popular DevOps tools with dynamic version fetching from official sources. No more manual downloads, version hunting, or complex installation procedures.

### Features

- 🚀 **Cross-platform**: Windows, macOS, and Linux support
- 📦 **Dynamic version fetching**: Always get the latest versions from official sources
- ⚡ **Lightweight**: Only ~3-4 MB total footprint
- 🎯 **Interactive & CLI modes**: Choose your preferred installation method
- 🔄 **Version management**: Install, update, and uninstall tools easily
- 🛠️ **9 DevOps tools**: Docker, kubectl, AWS CLI, Google Cloud SDK, Azure CLI, Jenkins, Helm, Prometheus, Terraform

### Supported Tools

| Tool | Description | Platforms |
|------|-------------|-----------|
| 🐳 **Docker** | Container platform | Windows, macOS, Linux |
| ☸️ **kubectl** | Kubernetes command-line tool | Windows, macOS, Linux |
| ☁️ **AWS CLI** | Amazon Web Services CLI | Windows, macOS, Linux |
| 🌩️ **Google Cloud SDK** | Google Cloud Platform tools | Windows, macOS, Linux |
| 🔵 **Azure CLI** | Microsoft Azure CLI | Windows, macOS, Linux |
| 🔧 **Jenkins** | CI/CD automation server | Windows, macOS, Linux |
| ⛵ **Helm** | Kubernetes package manager | Windows, macOS, Linux |
| 📊 **Prometheus** | Monitoring and alerting system | Windows, macOS, Linux |
| 🏗️ **Terraform** | Infrastructure as Code tool | Windows, macOS, Linux |

## Quick Start

### One-liner Installation (Recommended)

```bash
# Linux/macOS
curl -sSL https://raw.githubusercontent.com/tohidhanfi20/devops-cli/main/install | python3

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/tohidhanfi20/devops-cli/main/install" | python
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/tohidhanfi20/devops-cli.git
cd devops-cli

# Install globally (like npm install -g)
pip install -e .

# Now you can use 'devops-cli' from anywhere!
devops-cli --help
```

## 🚀 Server Installation (Ubuntu/CentOS)

### Method 1: Direct Download (Recommended for servers)

```bash
# Download and extract
wget https://github.com/tohidhanfi20/devops-cli/archive/refs/heads/main.zip
unzip main.zip
cd devops-cli-main

# Install globally
pip3 install -e .

# Start interactive setup
devops-cli init
```

### Method 1b: Using tar.gz (Alternative)

```bash
# Download and extract
wget https://github.com/tohidhanfi20/devops-cli/archive/refs/heads/main.tar.gz
tar -xzf main.tar.gz
cd devops-cli-main

# Install globally
pip3 install -e .

# Start interactive setup
devops-cli init
```

### Method 2: One-liner (Alternative)

```bash
# 1. Install DevOps CLI
curl -sSL https://raw.githubusercontent.com/tohidhanfi20/devops-cli/main/install | python3

# 2. Start interactive setup
devops-cli init
```

**Interactive Setup Flow:**
```
🚀 DevOps CLI - Interactive Setup
================================

Available Tools:
1. 🐳 Docker - Container platform
2. ☸️ kubectl - Kubernetes CLI  
3. ☁️ AWS CLI - Amazon Web Services CLI
4. 🌩️ gcloud - Google Cloud SDK
5. 🔵 Azure CLI - Microsoft Azure CLI
6. 🔧 Jenkins - CI/CD automation server
7. ⛵ Helm - Kubernetes package manager
8. 📊 Prometheus - Monitoring system
9. 🏗️ Terraform - Infrastructure as Code

Select tool number (1-9): 3

📋 Available AWS CLI versions:
1. 2.13.0 (Latest)
2. 2.12.0
3. 2.11.0
4. 2.10.0
5. 2.9.0

Select version number (1-5): 1
✅ AWS CLI 2.13.0 installed successfully!
```

### Platform-specific Downloads

Download the appropriate package for your platform from the [Releases page](https://github.com/tohidhanfi20/devops-cli/releases):

- **Windows**: `devops-cli-windows.zip`
- **Linux**: `devops-cli-linux.tar.gz`
- **macOS**: `devops-cli-macos.tar.gz`
- **Universal**: `devops-cli-universal.tar.gz`

## Installation

### Prerequisites

- **Python 3.7+** (automatically detected)
- **Internet connection** (for downloading tools and fetching versions)
- **Administrative privileges** (for system-wide installation)

### Installation Methods

#### Method 1: One-liner Installation (Recommended)

```bash
# Linux/macOS
curl -sSL https://raw.githubusercontent.com/tohidhanfi20/devops-cli/main/install | python3

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/tohidhanfi20/devops-cli/main/install" | python
```

#### Method 2: Platform-specific Packages

**Windows:**
```bash
# Download and extract
wget https://github.com/tohidhanfi20/devops-cli/releases/latest/download/devops-cli-windows.zip
unzip devops-cli-windows.zip
cd devops-cli-windows
install.bat
```

**Linux:**
```bash
# Download and extract
wget https://github.com/tohidhanfi20/devops-cli/releases/latest/download/devops-cli-linux.tar.gz
tar -xzf devops-cli-linux.tar.gz
cd devops-cli-linux
./install.sh
```

**macOS:**
```bash
# Download and extract
curl -L -o devops-cli-macos.tar.gz https://github.com/tohidhanfi20/devops-cli/releases/latest/download/devops-cli-macos.tar.gz
tar -xzf devops-cli-macos.tar.gz
cd devops-cli-macos
./install.sh
```

#### Method 3: Manual Installation

```bash
# Clone the repository
git clone https://github.com/tohidhanfi20/devops-cli.git
cd devops-cli/devops-cli

# Install dependencies
pip install -r requirements.txt

# Run installer
python installer.py
```

## Usage

### Basic Commands

```bash
# Show version and help
devops-cli --version
devops-cli --help

# List available tools
devops-cli list

# Check available versions for a tool
devops-cli versions docker
devops-cli versions kubectl

# Check installation status
devops-cli status
```

### Interactive Installation

```bash
# Start interactive installation wizard
devops-cli init
```

This will guide you through:
1. OS detection and confirmation
2. Tool selection from available options
3. Version selection (latest or specific version)
4. Automatic installation

### Command-line Installation

```bash
# Install specific tools
devops-cli install docker
devops-cli install kubectl --version 1.34.1
devops-cli install awscli --version 2.13.0

# Update tools
devops-cli update docker
devops-cli update all

# Uninstall tools
devops-cli uninstall docker
```

### Examples

```bash
# Complete DevOps setup on Ubuntu server
curl -sSL https://raw.githubusercontent.com/tohidhanfi20/devops-cli/main/install | python3
devops-cli init

# Install specific tools with versions
devops-cli install docker --version 4.47.0
devops-cli install kubectl
devops-cli install awscli --version 2.13.0
devops-cli install terraform

# Check what's installed
devops-cli status

# Update all tools to latest versions
devops-cli update all
```

## Advanced Usage

### Version Management

```bash
# See all available versions for a tool
devops-cli versions docker
# Output:
# Available versions for docker:
# 1. 4.47.0
# 2. 4.46.0
# 3. 4.45.0
# 4. 4.44.3
# 5. 4.44.2

# Install specific version
devops-cli install docker --version 4.47.0
```

### Tool Management

```bash
# Check installation status
devops-cli status
# Output:
# DevOps CLI Installation Status:
# 🔍 docker: Installed (4.47.0)
# 🔍 kubectl: Installed (1.34.1)
# 🔍 awscli: Not installed
# 🔍 gcloud: Not installed

# Update specific tool
devops-cli update docker

# Update all installed tools
devops-cli update all

# Uninstall tool
devops-cli uninstall docker
```

### Server Deployment

Perfect for server environments:

```bash
# One-liner server setup
curl -sSL https://raw.githubusercontent.com/tohidhanfi20/devops-cli/main/install | python3

# Install essential DevOps tools
devops-cli install docker
devops-cli install kubectl
devops-cli install awscli
devops-cli install terraform

# Verify installation
devops-cli status
docker --version
kubectl version
aws --version
terraform version
```

## Configuration

### Environment Variables

```bash
# Disable version caching (fetch fresh versions every time)
export DEVOPS_TOOLS_NO_CACHE=1

# Set custom cache timeout (default: 300 seconds)
export DEVOPS_TOOLS_CACHE_TIMEOUT=600

# Disable colors in output
export NO_COLOR=1
```

### Custom Installation Directory

The installer automatically detects the best installation directory:

- **Windows**: `%LOCALAPPDATA%\devops-cli`
- **macOS**: `~/.local/bin/devops-cli`
- **Linux**: `~/.local/bin/devops-cli`

## Troubleshooting

### Common Issues

**Issue**: `devops-cli: command not found`
```bash
# Solution: Restart your terminal or run:
source ~/.bashrc  # Linux/macOS
# or restart PowerShell on Windows
```

**Issue**: Python version too old
```bash
# Solution: Install Python 3.7+
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.7

# macOS:
brew install python@3.9

# Windows: Download from python.org
```

**Issue**: Permission denied during installation
```bash
# Solution: Run with appropriate permissions
sudo python3 installer.py  # Linux/macOS
# or run PowerShell as Administrator on Windows
```

### Getting Help

```bash
# Show comprehensive help
devops-cli --help

# Show version information
devops-cli --version

# Check tool status
devops-cli status
```

## Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/tohidhanfi20/devops-cli.git
cd devops-cli/devops-cli

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Build release packages
python build_releases.py
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Performance

### Resource Usage

- **Installation size**: ~3-4 MB total
- **Memory usage**: < 10 MB RAM
- **Startup time**: < 1 second
- **Version fetching**: Cached for 5 minutes

### Comparison with Manual Installation

| Method | Time | Steps | Error-prone |
|--------|------|-------|-------------|
| Manual | 30+ minutes | 20+ steps | High |
| DevOps CLI | 2-3 minutes | 1 command | Low |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for a universal DevOps tool installer
- Built with Python for cross-platform compatibility
- Dynamic version fetching from official sources
- Community feedback and contributions

## Support

- 📖 **Documentation**: [GitHub Wiki](https://github.com/tohidhanfi20/devops-cli/wiki)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/tohidhanfi20/devops-cli/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/tohidhanfi20/devops-cli/discussions)
- ⭐ **Star the project**: [GitHub Repository](https://github.com/tohidhanfi20/devops-cli)

---

**Made with ❤️ for the DevOps community**
