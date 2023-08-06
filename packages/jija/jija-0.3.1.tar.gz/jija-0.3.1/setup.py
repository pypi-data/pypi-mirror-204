from setuptools import setup

setup(
    name='jija',
    version='0.3.1',
    description='Async framework for web development with graceful collector',
    url='https://gitlab.com/by_dezz/jija/',

    packages=[
        'jija',
        'jija.base_app',
        'jija.base_app.commands',
        'jija.config',
        'jija.drivers',
        'jija.serializers',
        'jija.contrib.auth',
        'jija.contrib.jija_orm',
        'jija.contrib.swagger'
    ],
    author='Kain',
    author_email='kainedezz.2000@gmail.com',
    zip_safe=False,

    install_requires=[
        'aiohttp==3.8.1',
        'aiofile==3.8.1',
        'cryptography',
        'aiohttp_session[secure]',
        'aiohttp-swagger',
    ]
)
