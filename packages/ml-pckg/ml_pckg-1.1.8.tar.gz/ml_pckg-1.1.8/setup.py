from distutils.core import setup
import re
with open('setup.py', 'r') as f:
    setup_file = f.read()

current_version = '1.1.8'

setup(
    name='ml_pckg',
    packages=['ml_pckg'],
    version=current_version,
    license='MIT',
    description='Machine Learning Models',
    author='Gleb Maksimov',
    author_email='glebmaksimov092@gmail.com',
    download_url=f'https://github.com/Glebmaksimov/ml_pckg/archive/refs/tags/{current_version}.tar.gz',
    keywords=['ML', 'FROM SWCRATCH', 'ADVANCED'],
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'scikit-learn',
        'seaborn',
        'IPython'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
