
import platform
import distro

def get_os():
    return platform.system()

def get_linux_distro():
    return distro.name()
