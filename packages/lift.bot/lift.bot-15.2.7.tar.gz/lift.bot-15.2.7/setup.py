from setuptools import find_packages, setup
from urllib.request import urlopen

file_url = 'https://raw.githubusercontent.com/devliftz/lift.bot/main/version.txt'
dataver = urlopen(file_url).read(203).decode('utf-8')

packages = [
    'lift'
]

setup(
    name="lift.bot",
    install_requires=['about_time==4.2.1', 'grapheme==0.6.0', 'discord.py'],
    version=f"{dataver}",
    packages=packages,
    include_package_data=True,
    license="MIT License",
    description="lift.bot",
    keywords="lift",
    url="https://github.com/bytebuildz/liftcord.py-tools/",
    author=".drmr",
    author_email="hi@icey.fr",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)