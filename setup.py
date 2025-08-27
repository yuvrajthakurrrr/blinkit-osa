import setuptools

setuptools.setup(
    name='BlinkitOSA',
    version='1.0',
    author='Yuvraj Singh',
    author_email='vikramsingh5682@gmail.com',
    description='Blinkit OSA package',
    url='https://github.com/yuvrajthakurrrr/blinkit-osa',
    license='MIT',
    packages=['BlinkitOSA'],
    install_requires=['curl-cffi','requests','sqlalchemy','boto3','requests_auth_aws_sigv4','pandas','python-dateutil']
)

