from setuptools import setup

def get_dependencies(): #достаем зависимости из файла requirements.txt
    with open("bot/requirements.txt", "r") as f:
        return f.read().split("\n")


setup(
    name='bot',
    version='1.0.0',
    packages=['bot'],
    install_requires=get_dependencies(),
    package_data={
        'bot': ['znaki_pictures/*']
    }
)