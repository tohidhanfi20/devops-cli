@echo off
REM DevOps CLI - Windows Batch Installer
REM =====================================
REM A universal installer for DevOps tools on Windows.
REM Automatically fetches latest versions and installs tools with proper dependencies.

setlocal enabledelayedexpansion

REM Version and repository info
set CLI_VERSION=1.0.1
set REPO_URL=https://github.com/tohidhanfi20/devops-cli
set DOWNLOAD_URL=%REPO_URL%/archive/refs/heads/main.zip

echo.
echo 🚀 DevOps CLI Installer v1.0.1
echo ===============================
echo A universal installer for DevOps tools on Windows.
echo Automatically fetches latest versions and installs tools with proper dependencies.
echo.
echo Supported Tools:
echo • 🐳 Docker - Container platform
echo • ☸️ kubectl - Kubernetes CLI  
echo • ☁️ AWS CLI - Amazon Web Services CLI
echo • 🌩️ gcloud - Google Cloud SDK
echo • 🔵 Azure CLI - Microsoft Azure CLI
echo • 🔧 Jenkins - CI/CD automation server
echo • ⛵ Helm - Kubernetes package manager
echo • 📊 Prometheus - Monitoring system
echo • 🏗️ Terraform - Infrastructure as Code
echo.

REM Check Python version
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

python --version
echo ✅ Python found
echo.

REM Check pip availability
echo 🔍 Checking pip availability...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pip not found, attempting to install...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo ❌ Failed to install pip
        pause
        exit /b 1
    )
    echo ✅ pip installed successfully
) else (
    echo ✅ pip is available
)
echo.

REM Create temporary directory
set TEMP_DIR=%TEMP%\devops-cli-%RANDOM%
mkdir "%TEMP_DIR%" 2>nul

echo 📥 Downloading DevOps CLI...
echo    Downloading from: %DOWNLOAD_URL%

REM Download using PowerShell (available on all modern Windows)
powershell -Command "& {Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%TEMP_DIR%\devops-cli.zip' -UseBasicParsing}"
if errorlevel 1 (
    echo ❌ Download failed!
    pause
    exit /b 1
)

echo ✅ Download completed
echo.

REM Extract the zip
echo 📦 Extracting files...
powershell -Command "& {Expand-Archive -Path '%TEMP_DIR%\devops-cli.zip' -DestinationPath '%TEMP_DIR%\extracted' -Force}"
if errorlevel 1 (
    echo ❌ Extraction failed!
    pause
    exit /b 1
)

REM Find the extracted directory
for /d %%i in ("%TEMP_DIR%\extracted\*") do (
    if "%%~ni"=="devops-cli" (
        set CLI_DIR=%%i
        goto :found
    )
    if "%%~ni"=="devops-cli-main" (
        set CLI_DIR=%%i
        goto :found
    )
)

echo ❌ Could not find extracted directory
pause
exit /b 1

:found
echo ✅ Extracted to: !CLI_DIR!
echo.

REM Install the CLI
echo 🔧 Installing DevOps CLI globally...
cd /d "!CLI_DIR!"
python -m pip install -e .
if errorlevel 1 (
    echo ❌ Installation failed!
    echo.
    echo 🔄 Creating standalone installation...
    goto :standalone
)

echo ✅ DevOps CLI installed successfully!
echo.

REM Verify installation
echo 🔍 Verifying installation...
devops-cli --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Installation completed but CLI not in PATH
    echo    You may need to restart your Command Prompt
    echo.
    goto :standalone
)

echo ✅ DevOps CLI is working!
devops-cli --version
echo.

echo 🎉 Installation Complete!
echo ========================
echo.
echo You can now use the DevOps CLI:
echo.
echo 📋 Basic Commands:
echo    devops-cli --help              # Show all available commands
echo    devops-cli init                # Start interactive installation (recommended)
echo    devops-cli list                # List all available tools
echo    devops-cli install ^<tool^>      # Install a specific tool
echo    devops-cli status              # Check installation status
echo.
echo 🚀 Quick Start:
echo    devops-cli init                # This will guide you through installing tools
echo.
echo 💡 Troubleshooting:
echo    If 'devops-cli' command is not found:
echo    1. Restart your Command Prompt
echo    2. Check PATH: echo %%PATH%%
echo    3. Try: python -m main (from CLI directory)
echo.
echo 🔗 Documentation: https://github.com/tohidhanfi20/devops-cli
echo.
pause
exit /b 0

:standalone
echo 📝 Creating standalone script...
echo import sys > devops-cli-standalone.py
echo import os >> devops-cli-standalone.py
echo sys.path.insert(0, r'!CLI_DIR!') >> devops-cli-standalone.py
echo from main import main >> devops-cli-standalone.py
echo if __name__ == '__main__': >> devops-cli-standalone.py
echo     main() >> devops-cli-standalone.py

echo ✅ Standalone installation complete!
echo.
echo 📁 CLI Location: !CLI_DIR!
echo 🚀 To use the CLI, run:
echo    python devops-cli-standalone.py init
echo.
echo 💡 Or add to PATH:
echo    set PATH=!CLI_DIR!;%%PATH%%
echo    devops-cli init
echo.
pause
exit /b 0
