"""
Enhanced Version Management System for DevOps CLI
Provides more reliable version fetching with better error handling and fallbacks
"""

import os
import re
import requests
import json
from bs4 import BeautifulSoup
from packaging import version
import time
import platform
from typing import List, Optional, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VersionManager:
    """Enhanced version management with better error handling and caching"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DevOps-CLI/1.0.0 (https://github.com/yourusername/devops-cli)'
        })
    
    def _get_cached_versions(self, tool_name: str) -> Optional[List[str]]:
        """Get cached versions if they're still fresh"""
        if tool_name in self.cache:
            cached_time, versions = self.cache[tool_name]
            if time.time() - cached_time < self.cache_timeout:
                logger.info(f"Using cached versions for {tool_name}")
                return versions
        return None
    
    def _cache_versions(self, tool_name: str, versions: List[str]):
        """Cache versions with timestamp"""
        self.cache[tool_name] = (time.time(), versions)
        logger.info(f"Cached {len(versions)} versions for {tool_name}")
    
    def _fetch_with_retry(self, url: str, max_retries: int = 3, timeout: int = 10) -> Optional[requests.Response]:
        """Fetch URL with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"All attempts failed for {url}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
        return None
    
    def _fetch_github_releases(self, repo_url: str, max_versions: int = 5) -> List[str]:
        """Fetch releases from GitHub API with better error handling"""
        try:
            response = self._fetch_with_retry(repo_url)
            if not response:
                return []
            
            releases = response.json()
            versions = []
            
            for release in releases:
                tag_name = release.get('tag_name', '')
                # Remove 'v' prefix if present
                if tag_name.startswith('v'):
                    tag_name = tag_name[1:]
                
                # Only include stable releases
                if (tag_name and 
                    not release.get('prerelease', False) and 
                    not release.get('draft', False)):
                    versions.append(tag_name)
            
            # Sort versions properly
            try:
                versions.sort(key=lambda v: version.parse(v), reverse=True)
            except Exception as e:
                logger.warning(f"Error sorting versions: {e}")
                versions.sort(reverse=True)
            
            # Return latest versions + "latest"
            latest_versions = versions[:max_versions-1] if len(versions) >= max_versions-1 else versions
            latest_versions.append("latest")
            return latest_versions
            
        except Exception as e:
            logger.error(f"Error fetching GitHub releases from {repo_url}: {e}")
            return []
    
    def _fetch_jenkins_versions(self) -> List[str]:
        """Fetch Jenkins LTS versions with fallback"""
        try:
            # Try Jenkins API first
            api_url = 'https://api.github.com/repos/jenkinsci/jenkins/releases'
            response = self._fetch_with_retry(api_url)
            
            if response:
                releases = response.json()
                versions = []
                
                for release in releases:
                    tag_name = release.get('tag_name', '')
                    if tag_name and not release.get('prerelease', False):
                        # Remove 'jenkins-' prefix if present
                        if tag_name.startswith('jenkins-'):
                            tag_name = tag_name[8:]
                        versions.append(tag_name)
                
                if versions:
                    try:
                        versions.sort(key=lambda v: version.parse(v), reverse=True)
                    except Exception:
                        versions.sort(reverse=True)
                    
                    latest_versions = versions[:4] if len(versions) >= 4 else versions
                    latest_versions.append("latest")
                    return latest_versions
            
            # Fallback to hardcoded versions
            logger.warning("Using fallback Jenkins versions")
            return ["2.401.3", "2.401.2", "2.401.1", "2.400.3", "latest"]
            
        except Exception as e:
            logger.error(f"Error fetching Jenkins versions: {e}")
            return ["2.401.3", "2.401.2", "2.401.1", "latest"]
    
    def _fetch_docker_versions(self) -> List[str]:
        """Fetch Docker Desktop versions with multiple sources"""
        try:
            # Try GitHub releases first
            github_url = 'https://api.github.com/repos/docker/desktop/releases'
            response = self._fetch_with_retry(github_url)
            
            if response:
                releases = response.json()
                versions = []
                
                for release in releases:
                    tag_name = release.get('tag_name', '')
                    if tag_name and not release.get('prerelease', False):
                        # Remove 'v' prefix if present
                        if tag_name.startswith('v'):
                            tag_name = tag_name[1:]
                        versions.append(tag_name)
                
                if versions:
                    try:
                        versions.sort(key=lambda v: version.parse(v), reverse=True)
                    except Exception:
                        versions.sort(reverse=True)
                    
                    latest_versions = versions[:4] if len(versions) >= 4 else versions
                    latest_versions.append("latest")
                    return latest_versions
            
            # Fallback to hardcoded versions
            logger.warning("Using fallback Docker versions")
            return ["4.10.0", "4.9.1", "4.8.2", "4.7.0", "latest"]
            
        except Exception as e:
            logger.error(f"Error fetching Docker versions: {e}")
            return ["4.10.0", "4.9.1", "4.8.2", "latest"]
    
    def get_versions(self, tool_name: str, os_type: str, distro: str = None) -> List[str]:
        """Get versions for a specific tool with caching and fallbacks"""
        cache_key = f"{tool_name}_{os_type}_{distro or 'default'}"
        
        # Check cache first
        cached_versions = self._get_cached_versions(cache_key)
        if cached_versions:
            return cached_versions
        
        versions = []
        
        try:
            if tool_name == 'jenkins':
                versions = self._fetch_jenkins_versions()
            elif tool_name == 'docker':
                versions = self._fetch_docker_versions()
            elif tool_name == 'kubectl':
                versions = self._fetch_github_releases('https://api.github.com/repos/kubernetes/kubernetes/releases')
            elif tool_name == 'awscli':
                versions = self._fetch_github_releases('https://api.github.com/repos/aws/aws-cli/releases')
            elif tool_name == 'gcloud':
                versions = self._fetch_github_releases('https://api.github.com/repos/GoogleCloudPlatform/cloud-sdk/releases')
            elif tool_name == 'az':
                versions = self._fetch_github_releases('https://api.github.com/repos/Azure/azure-cli/releases')
            elif tool_name == 'helm':
                versions = self._fetch_github_releases('https://api.github.com/repos/helm/helm/releases')
            elif tool_name == 'prometheus':
                versions = self._fetch_github_releases('https://api.github.com/repos/prometheus/prometheus/releases')
            elif tool_name == 'terraform':
                versions = self._fetch_github_releases('https://api.github.com/repos/hashicorp/terraform/releases')
            
            # If no versions found, use fallback
            if not versions:
                versions = self._get_fallback_versions(tool_name)
            
            # Cache the results
            self._cache_versions(cache_key, versions)
            return versions
            
        except Exception as e:
            logger.error(f"Error getting versions for {tool_name}: {e}")
            return self._get_fallback_versions(tool_name)
    
    def _get_fallback_versions(self, tool_name: str) -> List[str]:
        """Get fallback versions when API calls fail"""
        fallback_versions = {
            'jenkins': ["2.401.3", "2.401.2", "2.401.1", "2.400.3", "latest"],
            'docker': ["4.10.0", "4.9.1", "4.8.2", "4.7.0", "latest"],
            'kubectl': ["1.28.0", "1.27.0", "1.26.0", "1.25.0", "latest"],
            'awscli': ["2.13.0", "2.12.0", "2.11.0", "2.10.0", "latest"],
            'gcloud': ["463.0.0", "462.0.0", "461.0.0", "460.0.0", "latest"],
            'az': ["2.50.0", "2.49.0", "2.48.0", "2.47.0", "latest"],
            'helm': ["3.12.0", "3.11.0", "3.10.0", "3.9.0", "latest"],
            'prometheus': ["2.45.0", "2.44.0", "2.43.0", "2.42.0", "latest"],
            'terraform': ["1.6.0", "1.5.0", "1.4.0", "1.3.0", "latest"]
        }
        
        return fallback_versions.get(tool_name, ["latest"])
    
    def get_download_url(self, tool_name: str, version: str, os_type: str) -> Optional[str]:
        """Get download URL for a specific tool and version"""
        if version == "latest":
            # For latest, we need to get the actual latest version
            versions = self.get_versions(tool_name, os_type)
            if versions and versions[0] != "latest":
                version = versions[0]
            else:
                version = "2.401.3"  # Fallback for Jenkins
        
        urls = {
            'jenkins': {
                'Linux': f"https://get.jenkins.io/war-stable/{version}/jenkins.war",
                'Darwin': f"https://get.jenkins.io/war-stable/{version}/jenkins.war",
                'Windows': f"https://get.jenkins.io/war-stable/{version}/jenkins.war"
            },
            'kubectl': {
                'Linux': f"https://dl.k8s.io/release/v{version}/bin/linux/amd64/kubectl",
                'Darwin': f"https://dl.k8s.io/release/v{version}/bin/darwin/amd64/kubectl",
                'Windows': f"https://dl.k8s.io/release/v{version}/bin/windows/amd64/kubectl.exe"
            },
            'helm': {
                'Linux': f"https://get.helm.sh/helm-v{version}-linux-amd64.tar.gz",
                'Darwin': f"https://get.helm.sh/helm-v{version}-darwin-amd64.tar.gz",
                'Windows': f"https://get.helm.sh/helm-v{version}-windows-amd64.zip"
            },
            'terraform': {
                'Linux': f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_linux_amd64.zip",
                'Darwin': f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_darwin_amd64.zip",
                'Windows': f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_windows_amd64.zip"
            }
        }
        
        tool_urls = urls.get(tool_name, {})
        return tool_urls.get(os_type)

# Global version manager instance
version_manager = VersionManager()

# Backward compatibility functions
def get_jenkins_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('jenkins', os_type, distro)

def get_docker_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('docker', os_type, distro)

def get_kubectl_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('kubectl', os_type, distro)

def get_awscli_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('awscli', os_type, distro)

def get_gcloud_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('gcloud', os_type, distro)

def get_az_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('az', os_type, distro)

def get_helm_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('helm', os_type, distro)

def get_prometheus_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('prometheus', os_type, distro)

def get_terraform_versions(os_type: str, distro: str = None) -> List[str]:
    return version_manager.get_versions('terraform', os_type, distro)

def get_download_url(tool_name: str, version: str, os_type: str) -> Optional[str]:
    return version_manager.get_download_url(tool_name, version, os_type)
