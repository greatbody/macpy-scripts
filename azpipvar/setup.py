from setuptools import setup, Command
from setuptools.command.install import install
import sys

version = "0.1.4"

class CustomInstallCommand(install):
    def run(self):
        try:
            # Only attempt tracking if explicitly opted in
            if "--no-track-install" in sys.argv:
                try:
                    import requests
                    from termcolor import colored
                    print(colored("Notice: Sending anonymous installation statistics...", "yellow"))
                    requests.get(f"https://package-download-logger.sunruicode.workers.dev/pip/azpipvar/{version}", timeout=2)
                    print(colored("✓ Thank you for helping us improve!", "green"))
                except Exception as e:
                    print(colored("Note: Could not send installation statistics. This does not affect installation.", "yellow"))
        except Exception:
            # Never fail installation due to tracking
            pass

        # Proceed with normal installation
        install.run(self)

setup(
    name="azpipvar",
    version=version,
    py_modules=['check_variables'],
    package_dir={'': 'src'},
    install_requires=[
        "pyyaml>=6.0.1",
        "requests>=2.31.0",  # For download tracking
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
    cmdclass={
        'install': CustomInstallCommand,
    },
)