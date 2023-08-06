from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "1.0.1"
DESCRIPTION = "A client for the BatchIngestion mediawiki API"

setup(
    name="batch_ingestion_client_py",
    version=VERSION,
    author="QuentinJanuel",
    author_email="<quentinjanuelkij@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=[
        'python',
        'mediawiki',
        'batchingestion',
        'wikidata',
        'wikibase',
        'api',
        'client',
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
