from setuptools import setup, find_packages

setup(
    name='simple_file_store',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'Flask',
        'gunicorn'
    ],
    entry_points={
        'console_scripts': [
            'store=simple_file_store.client.app:main'
        ],
    },
    author='Saurav Chandra',
    author_email='sauravchandra123@gmail.com',
    description='A simple file store application with a client-server architecture',
    url='https://github.com/sauravchandra/simple-file-store',
)
