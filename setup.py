from setuptools import setup

setup(
    name="cinepoliscli",
    version="0.1",
    py_modules=["cine_scraper", "terminal_interface"],
    install_requires=[
        "click",
    ],
    entry_points={
        'console_scripts': [
            'cinepoliscli = terminal_interface:cinepoliscli',
        ],
    },
)