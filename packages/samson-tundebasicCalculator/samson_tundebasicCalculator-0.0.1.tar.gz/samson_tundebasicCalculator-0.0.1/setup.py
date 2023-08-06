from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='samson_tundebasicCalculator',
    version='0.0.1',
    author='Samson Olatunde',
    author_email='mailtotunde@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords="calculator",
    packages=find_packages()
)