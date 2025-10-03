from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Universal DevOps CLI Installer & Updater"

setup(
    name="devops-cli",
    version="2.0.0",
    description="Universal DevOps CLI Installer & Updater",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Tohid Hanfi",
    author_email="tohidhanfi20@gmail.com",
    url="https://github.com/tohidhanfi20/devops-cli",
    packages=find_packages(),
    py_modules=["main", "versioning", "utils", "interactive", "dependencies", "enhanced_versioning"],
    install_requires=[
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "packaging>=21.0",
        "distro>=1.6.0"
    ],
    entry_points={
        "console_scripts": [
            "devops-cli=main:main",
            "devops=main:main",  # Alternative shorter command
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.7",
)
