from setuptools import setup
from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}

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
    },
    cmdclass=cmdclass,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'bot'),
            'version': ('setup.py', '1.0.0'),
            'release': ('setup.py', '1.0.0'),
            'source_dir': ('setup.py', './bot')}},
)