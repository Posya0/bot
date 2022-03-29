from setuptools import setup

setup(
    name='bot',
    version='1.0.0',
    packages=['bot'],
    install_requires=[
        "requests~=2.25.1",
        "bs4~=0.0.1",
        "beautifulsoup4~=4.9.3",
        "Pillow~=8.2.0",
        "geojson~=2.5.0",
        "vk_api~=11.9.3"
    ],
    package_data={
        'bot': ['znaki_pictures/*']
    }
)