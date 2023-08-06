from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='sentiment_nltk',
    version='0.0.2',
    description='This is a library that analyzes texts',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Luke Abbatessa',
    author_email='labbatessa14@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='nltk vader',
    packages=find_packages(),
    install_requires=['nltk>=3.7',
                      'pandas>=1.3.5'
    ],
)