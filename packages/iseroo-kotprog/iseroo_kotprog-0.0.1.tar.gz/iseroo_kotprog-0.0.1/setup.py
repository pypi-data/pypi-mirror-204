from setuptools import setup, find_packages

setup(
    name='iseroo_kotprog',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/Iseroo/Python-kotprog',
    license='',
    author='Tarsoly Barnabás',
    author_email='tarsoly.barnabas2002@gmail.com',
    description='',
     install_requires=[
        "Pillow==9.5.0",
        'pygame==2.1.2',
        "webcolors==1.12"

    ],
     entry_points={
        'console_scripts': [
            'iseroo_kotprog=iseroo_kotprog.main:main'
        ]
    }
)