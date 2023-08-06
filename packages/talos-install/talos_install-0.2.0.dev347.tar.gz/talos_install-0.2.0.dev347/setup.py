import setuptools
from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    setup_requires=['pbr>=2.0.0'],
    pbr=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pbr !=2.1.0,>=2.0.0',
        'oslo.config >=5.2.0',
        'PyYAML >=3.12',
        'Jinja2 >=2.10',
        'jmespath >=0.9.3',
        'ansible >=7,<8',
        'docker-compose'
    ]
)
