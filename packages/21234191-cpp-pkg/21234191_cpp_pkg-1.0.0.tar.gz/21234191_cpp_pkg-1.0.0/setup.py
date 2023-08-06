from setuptools import setup

setup(
    name='21234191_cpp_pkg',
    version='1.0.0',
    description='A short description of my package',
    packages=['booking_properties_pkg'],
    install_requires=[
        'requests>=2.25.1',
        'numpy>=1.19.5',
        'stripe'

    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    url='https://github.com/gauravs30/Payment-Library-CPP',
    author='Gaurav',
    author_email='gaurav.chinchane25@gmail.com'
)
