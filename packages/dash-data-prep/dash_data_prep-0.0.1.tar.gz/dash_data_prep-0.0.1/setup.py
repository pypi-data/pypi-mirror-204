from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='dash_data_prep',
    version='0.0.1',
    description='This is a library that gathers VADER sentiment scores for files',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Luke Abbatessa',
    author_email='labbatessa14@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='VADER sentiment',
    packages=find_packages(),
    install_requires=['textquisite>=0.0.1',
                      'textquisite-parsers>=0.0.1'
    ],
)