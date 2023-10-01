from setuptools import setup, find_packages

setup(
    name="dewine",
    version="0.1.0",
    packages=find_packages(),
    install_packages=[
        'bcrypt==4.0.1',
        'Faker==19.6.2',
        'greenlet==2.0.2',
        'numpy==1.26.0',
        'pandas==2.1.1',
        'python-dateutil==2.8.2',
        'pytz==2023.3.post1',
        'PyYAML==6.0.1',
        'six==1.16.0',
        'SQLAlchemy==2.0.21',
        'typing_extensions==4.8.0',
        'tzdata==2023.3',
    ]
)