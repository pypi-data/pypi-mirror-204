from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='tggl',
    version='1.1.2',
    description='Tggl python client',
    packages=find_packages(),
    install_requires=[],
    keywords=['Tggl', 'feature flag'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)