import setuptools

setuptools.setup(
    name='BlinkitOSA',
    version='0.0.0.033',
    author='Yuvraj Singh',
    author_email='vikramsingh5682@gmail.com',
    description='Blinkit OSA package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yuvrajthakurrrr/blinkit-osa',
    project_urls = {
        "Bug Tracker": "https://github.com/mike-huls/toolbox/issues"
    },
    license='MIT',
    packages=['BlinkitOSA'],
    install_requires=['curl-cffi','requests','sqlalchemy','boto3','requests_auth_aws_sigv4','pandas','python-dateutil']
)

