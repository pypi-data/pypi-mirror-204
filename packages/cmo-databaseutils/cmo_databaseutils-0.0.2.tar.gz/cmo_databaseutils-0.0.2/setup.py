from setuptools import setup, find_packages
from pathlib import Path

# read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cmo_databaseutils",
    version="0.0.2",
    python_requires='>=3.6',
    description='Connect to databases from Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeanine Schoonemann',
    author_email='service@cmotions.nl',
    url='https://Cmotions@dev.azure.com/Cmotions/Packages/_git/cmo_databaseutils',
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=1.4.7",
        "bcpy>=0.1.8",
        "pandas>=1.1.5",
        "pyodbc>=4.0.30",
        "urllib3>=1.26.4",
        "cryptography>=35.0.0",
    ],
    extras_require={
        'dev': [
            'black', 
            'jupyterlab', 
            'pytest>=6.2.4',
            'python-dotenv',
            'ipykernel',
            'pydataset',
            'twine'],
    },
    # files to be shipped with the installation
    # after installation, these can be found with the functions in resources.py
    package_data={
        "cmo_databaseutils": [
            "data/*.csv",
            "data/*.txt",
            "notebooks/*tutorial*.ipynb",
        ]
    },
)