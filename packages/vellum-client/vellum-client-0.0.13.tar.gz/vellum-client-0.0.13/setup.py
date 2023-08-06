from setuptools import find_packages, setup
from pathlib import Path

VERSION = "0.0.13"

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="vellum-client",
    version=VERSION,
    description="[DEPRECATED] Vellum Python Client",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/vellum-ai/vellum-client-python-deprecated",
    author="vellum.ai",
    author_email="devops@vellum.ai",
    packages=find_packages(where="."),
    package_data={
        "vellum": ["py.typed"],
    },
    install_requires=[
        "dacite>=1.8.0",
        "requests>=2.20.0",
    ],
)
