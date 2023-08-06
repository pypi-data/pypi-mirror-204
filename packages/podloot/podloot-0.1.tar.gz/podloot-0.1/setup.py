from setuptools import setup, find_packages

# Read the requirements.txt file
with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name="podloot",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        "console_scripts": [
            "podloot=main:main"
        ]
    },
    install_requires=required_packages,  # Use the packages read from requirements.txt
    author="Guvenc Usanmaz",
    author_email="gusanmaz@gmail.com",
    description="A podcast downloader and manager using RSS feeds",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gusanmaz/podloot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
