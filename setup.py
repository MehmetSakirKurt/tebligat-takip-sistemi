from setuptools import setup, find_packages

setup(
    name="tebligat-takip-sistemi",
    version="1.0.0",
    description="Hukuk profesyonelleri için tebligat dilekçe takip sistemi",
    packages=find_packages(),
    install_requires=[
        "ttkbootstrap==1.10.1",
        "tkcalendar==1.6.1",
        "plyer==2.1.0"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'tebligat-takip=src.main:main',
        ],
    },
)