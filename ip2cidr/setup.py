from setuptools import setup
import sys
import os

# Add src directory to path so we can import version
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.version import __version__

setup(
    name="ip2cidr",
    version=__version__,
    py_modules=['ip_converter', 'version'],
    package_dir={'': 'src'},
    install_requires=[
        "argparse>=1.4.0",
    ],
    extras_require={
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'ip2cidr=ip_converter:main',
        ],
    },
    author="greatbody",
    author_email="sunruicode@gmail.com",
    description="A tool to convert IP addresses to /24 CIDR notation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/greatbody/macpy-scripts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)