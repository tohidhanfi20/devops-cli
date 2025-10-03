# DevOps CLI - Windows PowerShell Installer
# ==========================================
# A universal installer for DevOps tools on Windows.
# Automatically fetches latest versions and installs tools with proper dependencies.

param(
    [switch]$Force,
    [switch]$Help
)

# Version and repository info
$CLI_VERSION = "1.0.1"
$REPO_URL = "https://github.com/tohidhanfi20/devops-cli"
$DOWNLOAD_URL = "$REPO_URL/archive/refs/heads/main.zip"

function Show-Banner {
    Write-Host @"

🚀 DevOps CLI Installer v1.0.1
===============================
A universal installer for DevOps tools on Windows.
Automatically fetches latest versions and installs tools with proper dependencies.

Supported Tools:
• 🐳 Docker - Container platform
• ☸️ kubectl - Kubernetes CLI  
• ☁️ AWS CLI - Amazon Web Services CLI
• 🌩️ gcloud - Google Cloud SDK
• 🔵 Azure CLI - Microsoft Azure CLI
• 🔧 Jenkins - CI/CD automation server
• ⛵ Helm - Kubernetes package manager
• 📊 Prometheus - Monitoring system
• 🏗️ Terraform - Infrastructure as Code

"@ -ForegroundColor Cyan
}

function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            if ($major -ge 3 -and $minor -ge 6) {
                Write-Host "✅ Python $pythonVersion found" -ForegroundColor Green
                return $true
            }
        }
        Write-Host "❌ Python 3.6 or higher is required!" -ForegroundColor Red
        Write-Host "   Current version: $pythonVersion" -ForegroundColor Yellow
        return $false
    }
    catch {
        Write-Host "❌ Python not found! Please install Python 3.6+ from https://python.org" -ForegroundColor Red
        return $false
    }
}

function Test-Pip {
    try {
        python -m pip --version | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ pip is available" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "⚠️  pip not found, attempting to install..." -ForegroundColor Yellow
        try {
            python -m ensurepip --upgrade
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ pip installed successfully" -ForegroundColor Green
                return $true
            }
        }
        catch {
            Write-Host "❌ Failed to install pip" -ForegroundColor Red
            return $false
        }
    }
    return $false
}

function Get-TempDirectory {
    $tempDir = [System.IO.Path]::GetTempPath()
    $cliDir = Join-Path $tempDir "devops-cli-$(Get-Random)"
    return $cliDir
}

function Download-CLI {
    Write-Host "📥 Downloading DevOps CLI..." -ForegroundColor Blue
    
    try {
        $tempDir = Get-TempDirectory
        $zipPath = Join-Path $tempDir "devops-cli.zip"
        
        Write-Host "   Downloading from: $DOWNLOAD_URL" -ForegroundColor Gray
        Invoke-WebRequest -Uri $DOWNLOAD_URL -OutFile $zipPath -UseBasicParsing
        
        # Extract the zip
        $extractPath = Join-Path $tempDir "extracted"
        Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
        
        # Find the extracted directory
        $extractedDir = Get-ChildItem -Path $extractPath -Directory | Where-Object { $_.Name -like "devops-cli*" } | Select-Object -First 1
        
        if ($extractedDir) {
            $cliDir = $extractedDir.FullName
            Write-Host "✅ Downloaded to: $cliDir" -ForegroundColor Green
            return $cliDir
        }
        else {
            throw "Could not find extracted directory"
        }
    }
    catch {
        Write-Host "❌ Download failed: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

function Install-CLI {
    param($CLIDir)
    
    Write-Host "🔧 Installing DevOps CLI globally..." -ForegroundColor Blue
    
    try {
        Push-Location $CLIDir
        $result = python -m pip install -e .
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ DevOps CLI installed successfully!" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Installation failed" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Installation failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    finally {
        Pop-Location
    }
}

function New-StandaloneScript {
    param($CLIDir)
    
    Write-Host "📝 Creating standalone script..." -ForegroundColor Blue
    
    try {
        $scriptContent = @"
import sys
import os
sys.path.insert(0, r'$CLIDir')
from main import main
if __name__ == '__main__':
    main()
"@
        
        $scriptPath = Join-Path $CLIDir "devops-cli-standalone.py"
        $scriptContent | Out-File -FilePath $scriptPath -Encoding UTF8
        
        Write-Host "✅ Standalone script created: $scriptPath" -ForegroundColor Green
        return $scriptPath
    }
    catch {
        Write-Host "❌ Failed to create standalone script: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

function Test-Installation {
    Write-Host "`n🔍 Verifying installation..." -ForegroundColor Blue
    
    try {
        $result = devops-cli --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ DevOps CLI is working!" -ForegroundColor Green
            Write-Host "   Version: $result" -ForegroundColor Gray
            return $true
        }
        else {
            Write-Host "❌ CLI command not found in PATH" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ CLI command not found" -ForegroundColor Red
        return $false
    }
}

function Show-UsageInstructions {
    Write-Host @"

🎉 Installation Complete!
========================

You can now use the DevOps CLI:

📋 Basic Commands:
   devops-cli --help              # Show all available commands
   devops-cli init                # Start interactive installation (recommended)
   devops-cli list                # List all available tools
   devops-cli install <tool>       # Install a specific tool
   devops-cli status              # Check installation status

🚀 Quick Start:
   devops-cli init                # This will guide you through installing tools

💡 Troubleshooting:
   If 'devops-cli' command is not found:
   1. Restart your PowerShell/Command Prompt
   2. Check PATH: `$env:PATH
   3. Try: python -m main (from CLI directory)

🔗 Documentation: https://github.com/tohidhanfi20/devops-cli

"@ -ForegroundColor Cyan
}

function Show-Help {
    Write-Host @"
DevOps CLI Windows Installer

USAGE:
    .\install-devops-cli.ps1 [OPTIONS]

OPTIONS:
    -Force          Force installation even if CLI already exists
    -Help           Show this help message

EXAMPLES:
    .\install-devops-cli.ps1
    .\install-devops-cli.ps1 -Force

"@ -ForegroundColor Yellow
}

# Main installation process
function Main {
    if ($Help) {
        Show-Help
        return
    }
    
    Show-Banner
    
    # Check Python version
    if (-not (Test-Python)) {
        Write-Host "`n❌ Installation failed! Please install Python 3.6+ first." -ForegroundColor Red
        Write-Host "   Download from: https://python.org" -ForegroundColor Yellow
        exit 1
    }
    
    # Check pip availability
    $pipAvailable = Test-Pip
    if (-not $pipAvailable) {
        Write-Host "`n❌ pip is required but not available!" -ForegroundColor Red
        Write-Host "   Please install pip or try: python -m ensurepip --upgrade" -ForegroundColor Yellow
        exit 1
    }
    
    # Download CLI
    $cliDir = Download-CLI
    if (-not $cliDir) {
        Write-Host "`n❌ Installation failed!" -ForegroundColor Red
        exit 1
    }
    
    # Try to install globally
    $success = Install-CLI -CLIDir $cliDir
    if ($success) {
        # Verify installation
        if (Test-Installation) {
            Show-UsageInstructions
            return
        }
        else {
            Write-Host "⚠️  Installation completed but CLI not in PATH" -ForegroundColor Yellow
            Write-Host "   You may need to restart your PowerShell" -ForegroundColor Yellow
        }
    }
    
    # Fallback: Create standalone script
    Write-Host "`n🔄 Creating standalone installation..." -ForegroundColor Blue
    $scriptPath = New-StandaloneScript -CLIDir $cliDir
    if ($scriptPath) {
        Write-Host @"

✅ Standalone installation complete!

📁 CLI Location: $cliDir
🚀 To use the CLI, run:
   python $scriptPath init

💡 Or add to PATH:
   `$env:PATH = "$cliDir;`$env:PATH"
   devops-cli init

"@ -ForegroundColor Green
    }
    else {
        Write-Host "`n❌ Installation failed!" -ForegroundColor Red
        exit 1
    }
}

# Run the installer
Main
