import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="bwc-bsconf",
  version="0.1.1",
  description="A library Python to configure, repair and install servers in an automated way.",
  long_description=README,
  long_description_content_type="text/markdown",
  author='Aníbal Barca, ',
  author_email='anibalbs@barca.com, ',
  license="MIT",
  packages=["bwc-bsconf"],
  zip_safe=False
)