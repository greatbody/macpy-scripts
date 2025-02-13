from setuptools import setup, find_packages

setup(
    name="azure-pipeline-variable-list",
    version="0.1.0",
    py_modules=['check_variables'],
    package_dir={'': 'azure-pipeline-variable-list'},
    install_requires=[
        "pyyaml>=6.0.1",
    ],
    entry_points={
        'console_scripts': [
            'azops-vars=check_variables:main',
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
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)