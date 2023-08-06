import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DairyBrainUtils",
    version="0.3.8",
    author="Rui Pan, Steve Wangen",
    author_email="srwangen@wisc.edu",
    description="A set of functions that interacts with a database. It contains some basic functionalities along with some other Dairy-Brain-specific functionalities.",
    install_requires=[
        'SQLAlchemy',
        'sqlalchemy_utils'
        ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DairyBrain/AgDH_DairyBrainUtils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
