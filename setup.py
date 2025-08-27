from setuptools import setup, find_packages

setup(
    name="blinkitpdp",   # Replace with your project name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pillow==9.1.1",
        "lxml",
        "selenium",
        "pyodbc",
        "openpyxl",
        "requests",
        "beautifulsoup4",
        "azure-storage-blob",
        "SQLAlchemy",
        "boto3",
        "amazoncaptcha",
        "undetected-chromedriver",
        "distutils-pytest",
        "pandas",
        "chromedriver-autoinstaller",
        "requests_auth_aws_sigv4",
        "cloudscraper",
        "flair==0.14.0",
        "curl-cffi",
        "xlrd",
        "setuptools"  # No need for --upgrade here, just specify
    ],
    description="Blinkit OSA web scraper",
    url="https://github.com/yuvrajthakurrrr/blinkit-osa",
    python_requires=">=3.8",  # adjust based on your Python version
)
