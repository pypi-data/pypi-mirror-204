from setuptools import setup

setup(
    name='filterframes',
    version='0.1.1',
    packages=['filterframes'],
    url='',
    license='',
    install_requires=['pandas==1.5.3',],
    author='Patrick Garrett',
    author_email='pgarrett@scripps.edu',
    description='A very simple DTASelect-Filter.txt parser.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)