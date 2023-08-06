from setuptools import setup, find_packages

# Read the contents of requirements.txt from package root
# with open('requirements.txt') as f:
#     install_requires = f.read().splitlines()

setup(
    name='imp3',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'matplotlib==3.6.0',
        'numpy==1.23.3',
        'opencv_python==4.6.0.66',
        'Pillow==9.5.0',
        'streamlit==1.13.0',
    ],
    entry_points={
        'console_scripts': [
            'imp3.run=imp3.run:run',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

#how to build this file

# pip uninstall imp3
# python setup.py sdist
# pip install ./dist/imp3-0.1.0.tar.gz
# imp3.run