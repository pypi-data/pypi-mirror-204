from distutils.core import setup
import re
with open('setup.py', 'r') as f:
    setup_file = f.read()

current_version = f'1.1.5'

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

major, minor, patch = current_version.split('.')

new_version = int(major)*100 + int(minor)*10 + int(patch)
new_version = str(new_version + 1)
with open('setup.py', 'w') as f:
    f.write(re.sub(r"current_version\s*=\s*'(.*?)'",
            f"current_version = f'{new_version[0]}.{new_version[1]}.{new_version[2]}'", setup_file))

# with open("run_to_update.txt", "r") as f:
#     contents = f.read()

# contents = contents.replace("<commit_message>", current_version + 'commit')
# contents = contents.replace("<tag_name>", current_version)
# contents = contents.replace("<tag_message>", current_version)

# with open("run_to_update.txt", "w") as f:
#     f.write(contents)
