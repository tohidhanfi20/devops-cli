import os
import re
import requests
import json
from bs4 import BeautifulSoup
from packaging import version
import time
import platform

# Cache for version data to avoid repeated API calls
_version_cache = {}
_cache_timeout = 300  # 5 minutes

def _get_cached_versions(tool_name):
    """Get cached versions if they're still fresh"""
    if tool_name in _version_cache:
        cached_time, versions = _version_cache[tool_name]
        if time.time() - cached_time < _cache_timeout:
            return versions
    return None

def _cache_versions(tool_name, versions):
    """Cache versions with timestamp"""
    _version_cache[tool_name] = (time.time(), versions)

def _fetch_github_releases(repo_url, max_versions=5):
    """Fetch releases from GitHub API - gets latest 4 + latest (5 total)"""
    try:
        response = requests.get(repo_url, timeout=10)
        response.raise_for_status()
        releases = response.json()
        
        versions = []
        for release in releases:
            tag_name = release.get('tag_name', '')
            # Remove 'v' prefix if present
            if tag_name.startswith('v'):
                tag_name = tag_name[1:]
            if tag_name and not release.get('prerelease', False):
                versions.append(tag_name)
        
        # Sort versions properly
        versions.sort(key=lambda v: version.parse(v), reverse=True)
        
        # Return latest 4 versions + "latest" (5 total)
        latest_versions = versions[:4] if len(versions) >= 4 else versions
        latest_versions.append("latest")
        return latest_versions
    except Exception as e:
        print(f"Error fetching GitHub releases: {e}")
        return []

def _get_download_urls(tool_name, version, os_type):
    """Generate dynamic download URLs for tools"""
    urls = {}
    
    if tool_name == 'awscli':
        if os_type == 'Linux':
            urls['linux'] = f"https://awscli.amazonaws.com/awscli-exe-linux-x86_64-{version}.zip"
        elif os_type == 'Darwin':
            urls['macos'] = f"https://awscli.amazonaws.com/AWSCLIV2-{version}.pkg"
        elif os_type == 'Windows':
            urls['windows'] = f"https://awscli.amazonaws.com/AWSCLIV2-{version}.msi"
    
    elif tool_name == 'kubectl':
        if os_type == 'Linux':
            urls['linux'] = f"https://dl.k8s.io/release/v{version}/bin/linux/amd64/kubectl"
        elif os_type == 'Darwin':
            urls['macos'] = f"https://dl.k8s.io/release/v{version}/bin/darwin/amd64/kubectl"
        elif os_type == 'Windows':
            urls['windows'] = f"https://dl.k8s.io/release/v{version}/bin/windows/amd64/kubectl.exe"
    
    elif tool_name == 'helm':
        if os_type == 'Linux':
            urls['linux'] = f"https://get.helm.sh/helm-v{version}-linux-amd64.tar.gz"
        elif os_type == 'Darwin':
            urls['macos'] = f"https://get.helm.sh/helm-v{version}-darwin-amd64.tar.gz"
        elif os_type == 'Windows':
            urls['windows'] = f"https://get.helm.sh/helm-v{version}-windows-amd64.zip"
    
    elif tool_name == 'prometheus':
        if os_type == 'Linux':
            urls['linux'] = f"https://github.com/prometheus/prometheus/releases/download/v{version}/prometheus-{version}.linux-amd64.tar.gz"
        elif os_type == 'Darwin':
            urls['macos'] = f"https://github.com/prometheus/prometheus/releases/download/v{version}/prometheus-{version}.darwin-amd64.tar.gz"
        elif os_type == 'Windows':
            urls['windows'] = f"https://github.com/prometheus/prometheus/releases/download/v{version}/prometheus-{version}.windows-amd64.zip"
    
    elif tool_name == 'terraform':
        if os_type == 'Linux':
            urls['linux'] = f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_linux_amd64.zip"
        elif os_type == 'Darwin':
            urls['macos'] = f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_darwin_amd64.zip"
        elif os_type == 'Windows':
            urls['windows'] = f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_windows_amd64.zip"
    
    return urls.get(os_type.lower() if os_type == 'Darwin' else os_type.lower(), None)

def get_download_url(tool_name, version, os_type):
    """Get the download URL for a specific tool and version"""
    return _get_download_urls(tool_name, version, os_type)

def _fetch_docker_desktop_versions():
    """Fetch Docker Desktop versions from release notes"""
    try:
        url = 'https://docs.docker.com/desktop/release-notes/'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        versions = []
        
        # Look for version patterns in headers
        for header in soup.find_all(['h1', 'h2', 'h3']):
            text = header.get_text(strip=True)
            # Match patterns like "Docker Desktop 4.10.0" or "4.10.0"
            version_match = re.search(r'(\d+\.\d+\.\d+)', text)
            if version_match:
                versions.append(version_match.group(1))
        
        # Remove duplicates and sort
        versions = list(set(versions))
        versions.sort(key=lambda v: version.parse(v), reverse=True)
        
        # Return latest 4 versions + "latest" (5 total)
        latest_versions = versions[:4] if len(versions) >= 4 else versions
        latest_versions.append("latest")
        return latest_versions
    except Exception as e:
        print(f"Error fetching Docker Desktop versions: {e}")
        return []

def _fetch_jenkins_versions():
    """Fetch Jenkins LTS versions"""
    try:
        # Jenkins has a specific API for LTS versions
        url = 'https://api.github.com/repos/jenkinsci/jenkins/releases'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        releases = response.json()
        
        versions = []
        for release in releases:
            tag_name = release.get('tag_name', '')
            if tag_name and not release.get('prerelease', False):
                # Remove 'jenkins-' prefix if present
                if tag_name.startswith('jenkins-'):
                    tag_name = tag_name[8:]
                versions.append(tag_name)
        
        versions.sort(key=lambda v: version.parse(v), reverse=True)
        
        # Return latest 4 versions + "latest" (5 total)
        latest_versions = versions[:4] if len(versions) >= 4 else versions
        latest_versions.append("latest")
        return latest_versions
    except Exception as e:
        print(f"Error fetching Jenkins versions: {e}")
        return []

def _fetch_gcloud_versions():
    """Fetch Google Cloud SDK versions"""
    try:
        # Google Cloud SDK versions are available via their API
        url = 'https://api.github.com/repos/GoogleCloudPlatform/cloud-sdk/releases'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        releases = response.json()
        
        versions = []
        for release in releases:
            tag_name = release.get('tag_name', '')
            if tag_name and not release.get('prerelease', False):
                versions.append(tag_name)
        
        versions.sort(key=lambda v: version.parse(v), reverse=True)
        
        # Return latest 4 versions + "latest" (5 total)
        latest_versions = versions[:4] if len(versions) >= 4 else versions
        latest_versions.append("latest")
        return latest_versions
    except Exception as e:
        print(f"Error fetching Google Cloud SDK versions: {e}")
        return []

# Docker version fetching functions
def get_docker_versions_linux(distro):
    """Get Docker versions for Linux using package managers"""
    versions = []
    try:
        if 'ubuntu' in distro.lower():
            command = "apt-cache madison docker-ce"
            result = os.popen(command).read()
            for line in result.splitlines():
                match = re.search(r'docker-ce \| (\S+) ', line)
                if match:
                    version_str = match.group(1).split('~')[0]
                    if ':' in version_str:
                        version_str = version_str.split(':')[1]
                    versions.append(version_str)
        elif 'centos' in distro.lower() or 'rhel' in distro.lower():
            command = "yum list docker-ce --showduplicates"
            result = os.popen(command).read()
            for line in result.splitlines():
                match = re.search(r'docker-ce\S+\s+(\S+)-\S+\s+', line)
                if match:
                    version_str = match.group(1)
                    if ':' in version_str:
                        version_str = version_str.split(':')[1]
                    versions.append(version_str)
    except Exception as e:
        print(f"Error fetching Docker versions for Linux: {e}")
    
    # Remove duplicates and sort
    versions = list(set(versions))
    versions.sort(key=lambda v: version.parse(v), reverse=True)
    return versions

def get_docker_versions_macos():
    """Get Docker Desktop versions for macOS"""
    cached = _get_cached_versions('docker_macos')
    if cached:
        return cached
    
    versions = _fetch_docker_desktop_versions()
    if not versions:
        # Fallback to hardcoded versions
        versions = ["4.10.0", "4.9.1", "4.8.2", "latest"]
    
    _cache_versions('docker_macos', versions)
    return versions

def get_docker_versions_windows():
    """Get Docker Desktop versions for Windows"""
    cached = _get_cached_versions('docker_windows')
    if cached:
        return cached
    
    versions = _fetch_docker_desktop_versions()
    if not versions:
        # Fallback to hardcoded versions
        versions = ["4.10.0", "4.9.1", "4.8.2", "latest"]
    
    _cache_versions('docker_windows', versions)
    return versions

def get_docker_versions(os_type, distro=None):
    """Get Docker versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_docker_versions_linux(distro)
    elif os_type == 'Darwin':
        return get_docker_versions_macos()
    elif os_type == 'Windows':
        return get_docker_versions_windows()
    return ["latest"]

# kubectl version fetching functions
def get_kubectl_versions_linux(distro):
    """Get kubectl versions for Linux"""
    cached = _get_cached_versions('kubectl_linux')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/kubernetes/kubernetes/releases')
    if not versions:
        # Fallback to hardcoded versions
        versions = ["1.28.0", "1.27.0", "1.26.0", "latest"]
    
    _cache_versions('kubectl_linux', versions)
    return versions

def get_kubectl_versions_macos():
    """Get kubectl versions for macOS"""
    cached = _get_cached_versions('kubectl_macos')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/kubernetes/kubernetes/releases')
    if not versions:
        versions = ["1.28.0", "1.27.0", "1.26.0", "latest"]
    
    _cache_versions('kubectl_macos', versions)
    return versions

def get_kubectl_versions_windows():
    """Get kubectl versions for Windows"""
    cached = _get_cached_versions('kubectl_windows')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/kubernetes/kubernetes/releases')
    if not versions:
        versions = ["1.28.0", "1.27.0", "1.26.0", "latest"]
    
    _cache_versions('kubectl_windows', versions)
    return versions

def get_kubectl_versions(os_type, distro=None):
    """Get kubectl versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_kubectl_versions_linux(distro)
    elif os_type == 'Darwin':
        return get_kubectl_versions_macos()
    elif os_type == 'Windows':
        return get_kubectl_versions_windows()
    return ["latest"]

# AWS CLI version fetching functions
def get_awscli_versions_linux():
    """Get AWS CLI versions for Linux"""
    cached = _get_cached_versions('awscli_linux')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/aws/aws-cli/releases')
    if not versions:
        versions = ["2.13.0", "2.12.0", "2.11.0", "latest"]
    
    _cache_versions('awscli_linux', versions)
    return versions

def get_awscli_versions_macos():
    """Get AWS CLI versions for macOS"""
    cached = _get_cached_versions('awscli_macos')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/aws/aws-cli/releases')
    if not versions:
        versions = ["2.13.0", "2.12.0", "2.11.0", "latest"]
    
    _cache_versions('awscli_macos', versions)
    return versions

def get_awscli_versions_windows():
    """Get AWS CLI versions for Windows"""
    cached = _get_cached_versions('awscli_windows')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/aws/aws-cli/releases')
    if not versions:
        versions = ["2.13.0", "2.12.0", "2.11.0", "latest"]
    
    _cache_versions('awscli_windows', versions)
    return versions

def get_awscli_versions(os_type, distro=None):
    """Get AWS CLI versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_awscli_versions_linux()
    elif os_type == 'Darwin':
        return get_awscli_versions_macos()
    elif os_type == 'Windows':
        return get_awscli_versions_windows()
    return ["latest"]

# Google Cloud SDK version fetching functions
def get_gcloud_versions_linux():
    """Get Google Cloud SDK versions for Linux"""
    cached = _get_cached_versions('gcloud_linux')
    if cached:
        return cached
    
    versions = _fetch_gcloud_versions()
    if not versions:
        versions = ["463.0.0", "462.0.0", "461.0.0", "latest"]
    
    _cache_versions('gcloud_linux', versions)
    return versions

def get_gcloud_versions_macos():
    """Get Google Cloud SDK versions for macOS"""
    cached = _get_cached_versions('gcloud_macos')
    if cached:
        return cached
    
    versions = _fetch_gcloud_versions()
    if not versions:
        versions = ["463.0.0", "462.0.0", "461.0.0", "latest"]
    
    _cache_versions('gcloud_macos', versions)
    return versions

def get_gcloud_versions_windows():
    """Get Google Cloud SDK versions for Windows"""
    cached = _get_cached_versions('gcloud_windows')
    if cached:
        return cached
    
    versions = _fetch_gcloud_versions()
    if not versions:
        versions = ["463.0.0", "462.0.0", "461.0.0", "latest"]
    
    _cache_versions('gcloud_windows', versions)
    return versions

def get_gcloud_versions(os_type, distro=None):
    """Get Google Cloud SDK versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_gcloud_versions_linux()
    elif os_type == 'Darwin':
        return get_gcloud_versions_macos()
    elif os_type == 'Windows':
        return get_gcloud_versions_windows()
    return ["latest"]

# Azure CLI version fetching functions
def get_az_versions_linux():
    """Get Azure CLI versions for Linux"""
    cached = _get_cached_versions('az_linux')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/Azure/azure-cli/releases')
    if not versions:
        versions = ["2.50.0", "2.49.0", "2.48.0", "latest"]
    
    _cache_versions('az_linux', versions)
    return versions

def get_az_versions_macos():
    """Get Azure CLI versions for macOS"""
    cached = _get_cached_versions('az_macos')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/Azure/azure-cli/releases')
    if not versions:
        versions = ["2.50.0", "2.49.0", "2.48.0", "latest"]
    
    _cache_versions('az_macos', versions)
    return versions

def get_az_versions_windows():
    """Get Azure CLI versions for Windows"""
    cached = _get_cached_versions('az_windows')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/Azure/azure-cli/releases')
    if not versions:
        versions = ["2.50.0", "2.49.0", "2.48.0", "latest"]
    
    _cache_versions('az_windows', versions)
    return versions

def get_az_versions(os_type, distro=None):
    """Get Azure CLI versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_az_versions_linux()
    elif os_type == 'Darwin':
        return get_az_versions_macos()
    elif os_type == 'Windows':
        return get_az_versions_windows()
    return ["latest"]

# Jenkins version fetching functions
def get_jenkins_versions_linux():
    """Get Jenkins versions for Linux"""
    cached = _get_cached_versions('jenkins_linux')
    if cached:
        return cached
    
    versions = _fetch_jenkins_versions()
    if not versions:
        versions = ["2.401.3", "2.401.2", "2.401.1", "latest"]
    
    _cache_versions('jenkins_linux', versions)
    return versions

def get_jenkins_versions_macos():
    """Get Jenkins versions for macOS"""
    cached = _get_cached_versions('jenkins_macos')
    if cached:
        return cached
    
    versions = _fetch_jenkins_versions()
    if not versions:
        versions = ["2.401.3", "2.401.2", "2.401.1", "latest"]
    
    _cache_versions('jenkins_macos', versions)
    return versions

def get_jenkins_versions_windows():
    """Get Jenkins versions for Windows"""
    cached = _get_cached_versions('jenkins_windows')
    if cached:
        return cached
    
    versions = _fetch_jenkins_versions()
    if not versions:
        versions = ["2.401.3", "2.401.2", "2.401.1", "latest"]
    
    _cache_versions('jenkins_windows', versions)
    return versions

def get_jenkins_versions(os_type, distro=None):
    """Get Jenkins versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_jenkins_versions_linux()
    elif os_type == 'Darwin':
        return get_jenkins_versions_macos()
    elif os_type == 'Windows':
        return get_jenkins_versions_windows()
    return ["latest"]

# Helm version fetching functions
def get_helm_versions_linux():
    """Get Helm versions for Linux"""
    cached = _get_cached_versions('helm_linux')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/helm/helm/releases')
    if not versions:
        versions = ["3.12.0", "3.11.0", "3.10.0", "latest"]
    
    _cache_versions('helm_linux', versions)
    return versions

def get_helm_versions_macos():
    """Get Helm versions for macOS"""
    cached = _get_cached_versions('helm_macos')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/helm/helm/releases')
    if not versions:
        versions = ["3.12.0", "3.11.0", "3.10.0", "latest"]
    
    _cache_versions('helm_macos', versions)
    return versions

def get_helm_versions_windows():
    """Get Helm versions for Windows"""
    cached = _get_cached_versions('helm_windows')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/helm/helm/releases')
    if not versions:
        versions = ["3.12.0", "3.11.0", "3.10.0", "latest"]
    
    _cache_versions('helm_windows', versions)
    return versions

def get_helm_versions(os_type, distro=None):
    """Get Helm versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_helm_versions_linux()
    elif os_type == 'Darwin':
        return get_helm_versions_macos()
    elif os_type == 'Windows':
        return get_helm_versions_windows()
    return ["latest"]

# Prometheus version fetching functions
def get_prometheus_versions_linux():
    """Get Prometheus versions for Linux"""
    cached = _get_cached_versions('prometheus_linux')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/prometheus/prometheus/releases')
    if not versions:
        versions = ["2.45.0", "2.44.0", "2.43.0", "latest"]
    
    _cache_versions('prometheus_linux', versions)
    return versions

def get_prometheus_versions_macos():
    """Get Prometheus versions for macOS"""
    cached = _get_cached_versions('prometheus_macos')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/prometheus/prometheus/releases')
    if not versions:
        versions = ["2.45.0", "2.44.0", "2.43.0", "latest"]
    
    _cache_versions('prometheus_macos', versions)
    return versions

def get_prometheus_versions_windows():
    """Get Prometheus versions for Windows"""
    cached = _get_cached_versions('prometheus_windows')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/prometheus/prometheus/releases')
    if not versions:
        versions = ["2.45.0", "2.44.0", "2.43.0", "latest"]
    
    _cache_versions('prometheus_windows', versions)
    return versions

def get_prometheus_versions(os_type, distro=None):
    """Get Prometheus versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_prometheus_versions_linux()
    elif os_type == 'Darwin':
        return get_prometheus_versions_macos()
    elif os_type == 'Windows':
        return get_prometheus_versions_windows()
    return ["latest"]

# Terraform version fetching functions
def get_terraform_versions_linux():
    """Get Terraform versions for Linux"""
    cached = _get_cached_versions('terraform_linux')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/hashicorp/terraform/releases')
    if not versions:
        versions = ["1.6.0", "1.5.0", "1.4.0", "latest"]
    
    _cache_versions('terraform_linux', versions)
    return versions

def get_terraform_versions_macos():
    """Get Terraform versions for macOS"""
    cached = _get_cached_versions('terraform_macos')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/hashicorp/terraform/releases')
    if not versions:
        versions = ["1.6.0", "1.5.0", "1.4.0", "latest"]
    
    _cache_versions('terraform_macos', versions)
    return versions

def get_terraform_versions_windows():
    """Get Terraform versions for Windows"""
    cached = _get_cached_versions('terraform_windows')
    if cached:
        return cached
    
    versions = _fetch_github_releases('https://api.github.com/repos/hashicorp/terraform/releases')
    if not versions:
        versions = ["1.6.0", "1.5.0", "1.4.0", "latest"]
    
    _cache_versions('terraform_windows', versions)
    return versions

def get_terraform_versions(os_type, distro=None):
    """Get Terraform versions based on OS type"""
    if os_type == 'Linux' and distro:
        return get_terraform_versions_linux()
    elif os_type == 'Darwin':
        return get_terraform_versions_macos()
    elif os_type == 'Windows':
        return get_terraform_versions_windows()
    return ["latest"]