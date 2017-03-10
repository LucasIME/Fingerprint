from setuptools import setup, find_packages

setup(
    name='fingerprint',
    version='0.1.0',
    platforms='any',
    description='Identity recognition by keystroke dynamics',
    author='Victor Villas',
    author_email='villasv@outlook.com',
    url='https://github.com/LucasIME/Fingerprint',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ]
)
