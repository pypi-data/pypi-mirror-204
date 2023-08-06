from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='textquisite',
    version='0.0.2',
    description='This is a NLP library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Luke Abbatessa',
    author_email='labbatessa14@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='NLP Textquisite',
    packages=find_packages(),
    install_requires=['sentiment-nltk>=0.0.2',
                      'plotly>=5.10.0',
                      'nltk>=3.7'
    ],
)