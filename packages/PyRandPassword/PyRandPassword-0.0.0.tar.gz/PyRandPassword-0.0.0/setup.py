from setuptools import setup

README = '''### ~~PyRandPassword~~
---
# 占位符
***这是PyRandPassword的占位符，PyRandPassword已经有了初步的版本，但是距离发布还有一点差距，因此我们先提前占了一个模块名，并预示着PyRandPassword的发布***

> This is not an official version, this is a placeholder to occupy a module name, but please believe me, PyRandPassword has a prototype, and the beta version will be officially released soon, so I am afraid that the module name will be occupied. Requires extensive revisions, delaying release of PyRandPassword.'''


setup(
    name='PyRandPassword',
    version='0.0.0',
    packages=['PyRandPassword'],
    url='https://github.com/MoYeRanqianzhi/PyRandPassword',
    license='MIT',
    author='MoYeRanQianZhi',
    author_email='moyeranqianzhi@gmail.com',
    description='Random Password',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
