from setuptools import setup, find_packages

setup(
    name='ox_script',
    version='0.3.4',
    author='Postek Electronics Co., Ltd.',
    author_email='support@postek.com.cn',
    packages=find_packages(),
    license="MIT",
    description="The pskfunc.py file details offically supported APIs. The printer have a version of pskfunc.py on the printer with all functions fully implemented.\nMost printer specific functions are left blank intentionally as they are meant to be executed on the printer and will throw an error if called on your devices. This file is provided more so for the beneift of keeping your IDE of choice happy while programming, providing extensive comments on the different functions and allowing for easy install through pip. ",
    url="https://github.com/POSTEK-OX-Script",
    install_requires=[
        "pandas",
        "openpyxl",
    ],
)
