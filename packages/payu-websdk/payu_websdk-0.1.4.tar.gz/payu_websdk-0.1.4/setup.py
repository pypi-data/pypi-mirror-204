from setuptools import setup, find_packages

with open('README.md') as readme:
    readme_content = readme.read()

setup(
    name='payu_websdk',
    version='0.1.4',
    description='PayU',
    author='PayU Web SDK for Python',
    author_email='integration@payu.in',
    url='https://github.com/payu-india/web-sdk-python',
    packages=find_packages(),
    long_description=readme_content,
    long_description_content_type='text/markdown',
    license="MIT",
    install_requires=[
    "requests"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ],
)