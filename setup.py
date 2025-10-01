from setuptools import setup, find_packages

setup(
    name="devops-cli",
    version="1.0.0",
    description="Universal DevOps CLI Installer & Updater",
    author="Tohid Hanfi",
    author_email="tohidhanfi20@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "packaging>=21.0",
        "distro>=1.6.0"
    ],
    entry_points={
        "console_scripts": [
            "devops-cli=main:main",
        ],
    },
    py_modules=["main", "versioning", "utils", "interactive"],
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
