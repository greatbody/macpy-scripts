from setuptools import setup
import sys
import os

# Add src directory to path so we can import version
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.version import __version__

setup(
    name="azpipvar",
    version=__version__,
    py_modules=['check_variables', 'version', 'sunsoft'],
    package_dir={'': 'src'},
    install_requires=[
        "pyyaml>=6.0.1",
        "requests>=2.32.3",  # For download tracking
        "termcolor>=2.3.0",  # For colored output
    ],
    extras_require={
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'azpipvar=check_variables:main',
        ],
    },
    author="greatbody",
    author_email="sunruicode@gmail.com",
    description="A tool to extract and list variables from Azure Pipeline YAML files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/greatbody/azure-pipeline-variable-list",
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
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.8",
)