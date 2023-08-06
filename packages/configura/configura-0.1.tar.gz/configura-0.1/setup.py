from distutils.core import setup
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name="configura",
    packages=["configura"],
    version="0.1",
    license="MIT",
    description="Configura is a Python configuration library that enables you to convert a folder of .json files into an easily accessible configuration folder.",
    author="Philippe Mathew",
    author_email="philmattdev@gmail.com",
    url="https://github.com/bossauh/configura",
    download_url="https://github.com/bossauh/configura/archive/refs/tags/v_01.tar.gz",
    keywords=["config"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
