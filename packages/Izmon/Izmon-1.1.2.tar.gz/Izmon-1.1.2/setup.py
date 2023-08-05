from setuptools import setup, find_packages
from codecs import open
from os import path
package_name = "Izmon"
root_dir = path.abspath(path.dirname(__file__))
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name=package_name,
    version='1.1.2',
    description='You can play Izmon with this libraly.',
    long_description=long_description,
    requires=["requests"],
    long_description_content_type='text/markdown',
    url='https://github.com/akita0724',
    author='Yohei Akita, nabe, miso',
    author_email='akita.yohei0724@gmail.com',
    license='GPL v2.0',
    keywords='Izmon',
    packages=find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3 :: Only',
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Operating System :: OS Independent"],
    python_requires='>=3.7'
)
