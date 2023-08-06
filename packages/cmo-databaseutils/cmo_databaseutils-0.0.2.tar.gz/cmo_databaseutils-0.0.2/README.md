# Cmotions DatabaseUtils

cmo_databaseutils is a Python library created by [The Analytics Lab](https://www.theanalyticslab.nl/), which is powered by [Cmotions](https://cmotions.nl/). This library combines our most used functionality when it comes to connecting to databases from Python. Nothing fancy, but very useful for our consultants. Mostly since this package is used in other packages, which makes our workflow simpler and more efficient.

Since we love to share what we do, why not also do that with our packages, that is why we've decided to make (almost) all of our packages open source, this way we hope to give back to the community that brings us so much. Enjoy!

## Installation
Install cmo_databaseutils using pip
```bash
pip install cmo-databaseutils
```

If you want to be able to use the tutorial notebook or the code below, you also need to install pydataset and dotenv using pip
```bash
pip install python-dotenv
pip install pydataset
```

## Usage
```python
import os
from pydataset import data
from dotenv import load_dotenv
from cmo_databaseutils import db_utils

load_dotenv()

df = data("iris")

# create a database connection to SQL Server using the credentials provided in a .env file
db_conn = db_utils(server=os.getenv("DB1_SERVER"), db=os.getenv("DB1_DATABASE"), server_name=os.getenv("DB1_SERVER_NAME"), usr=os.getenv("DB1_USERNAME"), pwd=os.getenv("DB1_PASSWORD"), driver=os.getenv("DB1_DRIVER"), port=os.getenv("DB1_PORT"))

# create a database connection to SQL Server using Windows credentials
db_conn = db_utils(server="localhost", db="localtemp")

# get an overview of all active schemas in the database
db_conn.list_all_active_schemas()

# get an overview of all tables in the database within the specified schemas
db_conn.list_all_tables(schema=['dbo'])

# load the data from an entire table
cars = db_conn.retrieve_table_from_sql(table="cars", schema="dbo")

# write a table to the SQL database, when possible the package will use BCP to optimize the efficiency of the process
db_conn.write_dataframe_to_sql(data=df, table="mynewtable", schema="dbo", replace_if_exists=False, index=False, dtype=None)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Contributors
Jeanine Schoonemann<br>
[Contact us](mailto:info@theanalyticslab.nl)