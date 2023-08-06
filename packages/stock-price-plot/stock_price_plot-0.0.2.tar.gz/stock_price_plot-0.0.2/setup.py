from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='stock_price_plot',
    version='0.0.2',
    description='This is a library that graphs a stock plot',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Luke Abbatessa',
    author_email='labbatessa14@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='stock',
    packages=find_packages(),
    install_requires=['plotly>=5.10.0',
                      'pandas>=1.3.5',
    ],
)