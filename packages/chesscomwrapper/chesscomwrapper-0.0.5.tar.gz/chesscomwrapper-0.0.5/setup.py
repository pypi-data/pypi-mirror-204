from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

exec(open('app/chesscomwrapper/version.py').read())

setup(
    name='chesscomwrapper',
    version=__version__,
    description='A wrapper for the chess.com API',
    package_dir={'': 'app'},
    packages=find_packages(where='app'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nicpanozzo/chesscom-api-wrapper',
    author='Nicola Panozzo',
    author_email='nicolapanoz@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
        ],
    install_requires=['requests',
                      'functools'],
    extras_require={
        'dev': [
            'pytest>=3.7',
            'twine>=1.11.0',
        ],
    },
    python_requires='>=3.6',
)
    