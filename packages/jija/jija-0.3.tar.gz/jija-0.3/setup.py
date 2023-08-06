from setuptools import setup, find_packages

setup(
    name='jija',
    version='0.3',
    description='Async framework for web development with graceful collector',
    url='https://gitlab.com/by_dezz/jija/',

    packages=find_packages(include=['jija', 'jija.*']),
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
