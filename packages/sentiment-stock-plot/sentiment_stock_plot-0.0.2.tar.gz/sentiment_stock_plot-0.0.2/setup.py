from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='sentiment_stock_plot',
    version='0.0.2',
    description='This is a library that provides a foundation for a sentiment stock plot',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Luke Abbatessa',
    author_email='labbatessa14@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='sentiment stock',
    packages=find_packages(),
    install_requires=['pandas>=1.3.5',
                      'plotly>=5.10.0',
                      'dash-data-prep>=0.0.2'
    ],
)