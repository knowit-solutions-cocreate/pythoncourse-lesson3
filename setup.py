from setuptools import setup


setup(
    name='lesson_3_code',
    version='0.1.0',
    python_requires='>=3.12',
    packages=['lesson_3_code'],
    install_requires=[
        'setuptools >= 68.2.2, < 69',
        'sqlalchemy >= 2.0.30, < 2.1',
        'pandas >= 2.2.2, < 2.3',
        'requests >= 2.32.3',
        'dagster >= 1.7.10, < 1.8',
        'dagster-webserver >= 1.7.10, < 1.8',
    ],
)
