from setuptools import setup, find_packages

setup(
    name="dvinfo",
    version="0.1",
    description="A package for getting system information on Windows and Linux",
    url="https://github.com/0mgRod/deviceinfo",
    author="OmgRod",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="system info",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "cpuinfo",
        "netifaces",
        "wmi",
    ],
)
