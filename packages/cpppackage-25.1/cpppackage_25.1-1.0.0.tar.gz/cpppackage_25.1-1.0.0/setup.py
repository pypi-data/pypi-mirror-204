from setuptools import setup

setup(
    name='cpppackage_25.1',
    version='1.0.0',
    description='A short description of my package',
    packages=['bookcount'],
    install_requires=[
        'requests>=2.25.1',
        'numpy>=1.19.5',
        
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    url='https://github.com/my_username/my_package',
    author='Swapnil',
    author_email='swapnild333@gmail.com'
)
