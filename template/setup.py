from setuptools import setup, find_packages

setup(
    name="script-name",  # Replace with your script name
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        "console_scripts": [
            # Add your script entry points here
            # Format: "command-name=package.module:function"
            # Example: "hello-world=script_name.main:main"
            # This would allow running "hello-world" from anywhere in the terminal
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your script",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
) 