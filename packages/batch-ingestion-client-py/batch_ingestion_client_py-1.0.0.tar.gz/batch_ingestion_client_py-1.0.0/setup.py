from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = "A client for the BatchIngestion mediawiki API"
LONG_DESCRIPTION = "A client for the BatchIngestion mediawiki API"

setup(
    name="batch_ingestion_client_py",
    version=VERSION,
    author="QuentinJanuel",
    author_email="<quentinjanuelkij@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
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
