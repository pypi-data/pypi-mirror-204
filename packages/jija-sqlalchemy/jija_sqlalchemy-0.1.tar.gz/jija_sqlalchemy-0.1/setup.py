from setuptools import setup


setup(
    name='jija_sqlalchemy',
    version='0.1',
    description='SQLAlchemy driver for Jija framework',
    url='https://gitlab.com/by_dezz/jija-sqlalchemy',

    packages=[
        'jija_sqlalchemy',
    ],
    author='Kain',
    author_email='kainedezz.2000@gmail.com',
    zip_safe=False,

    install_requires=[
        'jija',
        'sqlalchemy[asyncio]',
        'alembic'
    ]
)
