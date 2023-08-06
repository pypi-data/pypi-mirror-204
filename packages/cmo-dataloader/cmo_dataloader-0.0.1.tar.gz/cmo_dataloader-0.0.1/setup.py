from setuptools import setup, find_packages
from pathlib import Path

# read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cmo_dataloader",
    version="0.0.1",
    python_requires='>=3.6',
    description='Load a bulk of data from flat files or databases at once',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeanine Schoonemann',
    author_email='service@cmotions.nl',
    url='https://Cmotions@dev.azure.com/Cmotions/Packages/_git/cmo_dataloader',
    packages=find_packages(),
    install_requires=[
        "chardet>=3.0.4",
        "clevercsv>=0.6.3",
        "cmo-databaseutils",
    ],
    extras_require={
        'dev': [
            'black', 
            'jupyterlab', 
            'pytest>=6.2.4',
            'python-dotenv',
            'ipykernel',
            'twine',
        ],
    },
    # files to be shipped with the installation
    # after installation, these can be found with the functions in resources.py
    package_data={
        "cmo_dataloader": [
            "data/*.csv",
            "data/*.txt",
            "notebooks/*tutorial*.ipynb",
        ]
    }
)