# 🚀 DevOps CLI

A universal installer for DevOps tools across Windows, macOS, and Linux. Automatically fetches latest versions and installs tools with proper dependencies.

## ✨ Features

- Cross-platform support (Windows, macOS, Linux)
- Automatic dependency management (Java for Jenkins, etc.)
- Modern installation methods (no deprecated commands)
- Dynamic version fetching from official sources
- Interactive and command-line modes
- Installation verification and troubleshooting
- Clean uninstallation**

## 🛠️ Supported Tools

| Tool | Description | Dependencies |
|------|-------------|-------------|
| Docker | Container platform | apt-transport-https, ca-certificates, curl, gnupg |
| kubectl | Kubernetes CLI | curl, gnupg |
| AWS CLI | Amazon Web Services CLI | unzip, curl |
| gcloud | Google Cloud SDK | curl, python3 |
| Azure CLI | Microsoft Azure CLI | curl, gnupg |
| Jenkins | CI/CD automation server | **Java 21**, fontconfig |
| Helm | Kubernetes package manager | curl |
| Prometheus | Monitoring system | curl |
| Terraform | Infrastructure as Code | curl, unzip |

## 🚀 Quick Installation

The `devops-cli` can be installed using `npm`, which will handle the underlying Python dependencies.

### Prerequisites:
*   **Node.js and npm:** Required for the `npm` installation method.
*   **Python 3 and pip:** Required for the underlying Python CLI.
*   **Git:** Required to clone the repository.

### Steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/tohidhanfi20/devops-cli.git
    cd devops-cli
    ```

2.  **Install via npm:**
    Navigate to the cloned directory and run the following command to install `devops-cli` globally. This will automatically install the Python dependencies using `pip`.
    ```bash
    npm install -g .
    ```

3.  **Verify Installation:**
    After installation, you can verify that the `devops-cli` command is recognized:
    ```bash
    devops-cli --version
    ```
    You should see the version information for the DevOps CLI.

---

## Usage

### Basic Commands
```bash
# Check version
devops-cli --version

# Get help
devops-cli --help

# List available tools
devops-cli list
```

### Install Tools
```bash
# Install with automatic dependencies
devops-cli install jenkins
devops-cli install docker
devops-cli install kubectl

# Install specific version
devops-cli install jenkins --version 2.401.3
devops-cli install docker --version 4.47.0
```

### Dependency Management
```bash
# Check dependencies for a tool
devops-cli deps jenkins
devops-cli deps docker

# Install missing dependencies
devops-cli deps jenkins  # Auto-installs if missing
```

### Verification
```bash
# Verify all installations
devops-cli verify

# Check status
devops-cli status
```

### Updates
```bash
# Update to latest
devops-cli update docker
devops-cli update jenkins

# Update all tools
devops-cli update all
```

### Uninstall
```bash
# Uninstall tools
devops-cli uninstall docker
devops-cli uninstall jenkins
```

## Advanced Usage

### Interactive Mode
```bash
# Start interactive installation session
devops-cli init
```

### Version Management
```bash
# Show available versions
devops-cli versions docker
devops-cli versions jenkins
```

## Examples

### Complete Jenkins Setup
```bash
# Install Jenkins with Java dependency
devops-cli install jenkins

# Check if Java was installed
devops-cli deps jenkins

# Verify installation
devops-cli verify
```

### Docker Installation
```bash
# Install Docker with repository setup
devops-cli install docker

# Start Docker service (Linux)
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
```

## Troubleshooting

### Windows PATH Issues
If `devops-cli` command is not found:
1. Add Python Scripts directory to PATH:
   - `C:\Users\YourUsername\AppData\Roaming\Python\Python313\Scripts`
2. Restart your terminal
3. Or use: `python -m main` instead

### Linux/macOS PATH Issues
```bash
# Add to PATH
export PATH="$PATH:$HOME/.local/bin"

# Or add to ~/.bashrc or ~/.zshrc
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

### Verification
```bash
# Check if tools are working
docker --version
kubectl version --client
aws --version
```

## Updates

To update the DevOps CLI itself:
```bash
# Update from source
git pull origin main
pip install -e .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/tohidhanfi20/devops-cli/issues)
- **Email**: tohidhanfi20@gmail.com

---

**Made with  for the DevOps community**