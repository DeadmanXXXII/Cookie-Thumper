from setuptools import setup, find_packages

setup(
    name="cookiethumper",
    version="0.1.0",
    author="DeadmanXXXII",
    author_email="your.email@example.com",
    description="Cookie injection and session fixation testing tool using Selenium",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DeadmanXXXII/Cookie-Thumper",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "selenium",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "cookiethumper=cookiethumper.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
