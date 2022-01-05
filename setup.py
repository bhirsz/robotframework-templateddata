import pathlib
from setuptools import setup
from TemplatedData.__version__ import __version__


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.rst").read_text()
CLASSIFIERS = """
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Framework :: Robot Framework :: Tool
Topic :: Software Development :: Quality Assurance
Topic :: Utilities
""".strip().splitlines()

setup(
    name="robotframework-templateddata",
    version=__version__,
    description="Robot Framework library for generating test data from templates",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/bhirsz/robotframework-templateddata",
    author="Bartlomiej Hirsz",
    author_email="bartek.hirsz@gmail.com",
    license="Apache License 2.0",
    platforms="any",
    classifiers=CLASSIFIERS,
    packages=["TemplatedData"],
    include_package_data=True,
    install_requires=["robotframework>=3.2.1", "jinja2"],
)
