from setuptools import setup, find_packages
from ikcode_devtools.version import __version__

setup(
    name='ikcode-devtools',
    version=__version__,
    description='IKcode Devtools is a collection of tools for developers, including a code formatter, linter, and more.',
    author='IKcode',
    author_email='ikcode.offical@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyqt5',
        'sympy',
        'pyyaml',
        'black',
    ],
    entry_points={
        'console_scripts': [
            'ikcode-devtools=ikcode_devtools.main:runGUI',
        ]
    },
    package_data={
        'ikcode_devtools': ['ikcode.png']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.7',
)


