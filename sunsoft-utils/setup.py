from setuptools import setup, find_packages

setup(
    name="sunsoft-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "termcolor>=2.3.0",
    ],
    author="greatbody",
    author_email="sunruicode@gmail.com",
    description="Shared utilities for Sunsoft packages",
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
    ],
    python_requires=">=3.8",
)