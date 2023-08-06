from setuptools import setup

setup(
    name='exam_angel',
    version='1.0.0',
    description='Opis biblioteki exam_angel',
    author='Matty_Mroz',
    author_email='mateuszmroz001@gmail.com',
    license='MIT',
    packages=['exam_angel'],
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    zip_safe=False
)
