import pandas as pd
from pandas.io.sql import table_exists
import sqlalchemy
from sqlalchemy import text
import bcpy
from cryptography.fernet import Fernet
from urllib.parse import quote_plus


class DatabaseUtils:
    """
    The databaseutils class contains helper functions to connect 
    and interact with different types of databases
    
    Example:

        from cmo_databaseutils import db_utils
        
        # (1) create a connection using the Windows credentials
        windows_connection = db_utils(server="localhost",
                            db="localtemp",
                            server_name=None,
                            usr=None,
                            pwd=None,
                            driver="ODBC+Driver+17+for+SQL+Server",
                            port=1433,
                            max_tries=5)
        
        # (2) use the credentials stored in the .env file to create a database connection
        %load_ext dotenv
        %dotenv
        env_connection = db_utils(server=os.getenv("DB1_SERVER"),
                        db=os.getenv("DB1_DATABASE"),
                        server_name=os.getenv("DB1_SERVER_NAME"),
                        usr=os.getenv("DB1_USERNAME"),
                        pwd=os.getenv("DB1_PASSWORD"),
                        driver=os.getenv("DB1_DRIVER"),
                        port=os.getenv("DB1_PORT"),
                        max_tries=5)

    Args:
        server (str):                               The complete link to the server where the database can be found
                                                    Example: "myveryownserver.database.windows.net"
        db (str):                                   The database to which should be connected
        server_name (str, optional):                The name of the server where the database can be found
                                                    Example: "myveryownserver"
        usr (str, optional):                        The username which is allowed to connect to the server and database
        pwd (str, optional):                        The password for this username
        driver (str, optional):                     The driver that is available to connect to the server and database 
                                                    Defaults to "ODBC+Driver+17+for+SQL+Server"
        port (int, optional):                       The port used for the connection
                                                    Defaults to 1433
        max_tries (int, optional):                  The number of tries to create the connection, this might be helpful
                                                    when connecting to a database that could be sleeping and therefore
                                                    doesn't alsways wake up fast enough to connect at the first try
                                                    Defaults to 5
        add_to_connectionstring (string, optional)  Extra parameters to use when creating the SQL engine
                                                    Defaults to "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    Attributes:
        f:                          The Fernet key used to encrypt the login information
        server:                     The encrypted link of the server
        server_name:                The encrypted name of the server
        db:                         The encrypted name of the database
        usr:                        The encrypted username
        pwd:                        The encrypted password
        driver:                     The driver used to connect
        port:                       The port used to connect
        max_tries:                  The maximum number of tries to connect
        sql_engine:                 The SQL engine created using the login information
        add_to_connectionstring:    The extra options to be added to the connectionstring of the SQL engine
    """

    def __init__(
        self,
        server: str,
        db: str,
        server_name: str = None,
        usr: str = None,
        pwd: str = None,
        driver: str = "ODBC+Driver+17+for+SQL+Server",
        port: int = 1433,
        max_tries: int = 5,
        add_to_connectionstring: str = "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    ) -> None:
        # initialize encryption
        key = Fernet.generate_key()
        self.f = Fernet(key)
        # required parameters
        self.server = self.f.encrypt(bytes(server, encoding="utf-8"))
        self.db = self.f.encrypt(bytes(db, encoding="utf-8"))
        # optional parameters
        if server_name is not None:
            self.server_name = self.f.encrypt(bytes(server_name, encoding="utf-8"))
        else:
            self.server_name = server_name
        if usr is not None:
            self.usr = self.f.encrypt(bytes(usr, encoding="utf-8"))
        else:
            self.usr = usr
        if pwd is not None:
            self.pwd = self.f.encrypt(bytes(pwd, encoding="utf-8"))
        else:
            self.pwd = pwd
        self.driver = driver
        self.port = port
        self.max_tries = max_tries
        # create connection engine
        self.sql_engine = None
        self.add_to_connectionstring = add_to_connectionstring
        self._connect_sql_engine()
        self.engine_connection = self.sql_engine.connect()

    def _connect_sql_engine(self) -> None:
        """
        Create a SQL engine connection to the database

        Args:
            None, class attributes will be used

        Returns:
            None, the sql engine will be added to the class atttibutes
        """
        if self.usr is None:
            # connect with Windows credentials
            connection_string = f"mssql+pyodbc://{self.f.decrypt(self.server).decode('utf-8')}/{self.f.decrypt(self.db).decode('utf-8')}?trusted_connection=yes&driver={self.driver}"
        else:
            connection_params = quote_plus(
                f"Driver={self.driver};Server={self.f.decrypt(self.server).decode('utf-8')},{self.port};Database={self.f.decrypt(self.db).decode('utf-8')};Uid={self.f.decrypt(self.usr).decode('utf-8')};Pwd={self.f.decrypt(self.pwd).decode('utf-8')};{self.add_to_connectionstring}"
            )
            connection_string = f"mssql+pyodbc:///?odbc_connect={connection_params}"

        for i in range(self.max_tries):
            try:
                self.sql_engine = sqlalchemy.engine.create_engine(connection_string)
            except Exception as e:
                print(f"Connection failed after trying {i+1}x")
                if i + 1 >= self.max_tries:
                    print(e)
        return self.sql_engine

    def list_all_active_schemas(self) -> list:
        """
        Lists all schemas that are in use in the database, these are all schemas that hold at least one table

        Args:
            None, class attributes will be used

        Returns:
            list:   List of str, which are the name(s) of the schema(s)
        """
        schema_query = "select distinct S.name from sys.tables T inner join sys.schemas S on T.schema_id = S.schema_id"
        schemas = self.engine_connection.execute(text(schema_query))
        return [s[0] for s in schemas.fetchall()]

    def list_all_tables(self, schema: list = ["dbo"]) -> list:
        """
        Lists all tables in the database within the given schema(s)

        Args:
            schema (list, optional):    The list of schema names of which to retrieve all table names
                                        Defaults to ["dbo"]

        Returns:
            list:   List of all tables available within the given schema(s)
        """
        cursor = self.sql_engine.raw_connection().cursor()
        filenames = []
        for table in cursor.tables(tableType="TABLE"):
            if table.table_schem in schema:
                filenames.append(table.table_schem + "." + table.table_name)
        return filenames

    def _append_data_to_table_bcpy(
        self, data: pd.DataFrame, table: str, schema: str
    ) -> None:
        """
        Append the given dataframe to the given table in the database

        Args:
            data (pd.DataFrame):    Dataframe in the format of the table in the database
                                    containing data that needs to be appended to this table
            table (str):            The table the data will be appended to
            schema (str):           The schema where this table can be found

        Returns:
            None, data will be added to the table using BCP
        """
        # this requires bcp to be installed and available in the PATH variables
        if self.usr is None:
            print(
                "using BCP in Python with Windows credentials doesn't work with the current package version"
            )
        else:
            sql_config = {
                "server": self.f.decrypt(self.server).decode("utf-8"),
                "database": self.f.decrypt(self.db).decode("utf-8"),
                "username": self.f.decrypt(self.usr).decode("utf-8"),
                "password": self.f.decrypt(self.pwd).decode("utf-8"),
            }
            bdf = bcpy.DataFrame(data)
            sql_table = bcpy.SqlTable(sql_config, schema_name=schema, table=table)
            bdf.to_sql(sql_table, use_existing_sql_table=True, batch_size=min(len(data), 10000))

    def write_dataframe_to_sql(
        self,
        data: pd.DataFrame,
        table: str,
        schema: str = "dbo",
        replace_if_exists: bool = False,
        index: bool = False,
        dtype: dict = None,
        try_bcp: bool = True,
    ) -> None:
        """
        Write data to the table in the database, if this table exists it can be replaced 
        or the data can be appended, if it doesn't exist, the table will be created

        Args:
            data (pd.DataFrame):                    Dataframe in the format of the table in the database
                                                    containing data that needs to be appended to this table
                                                    if this table doesn't exist, it will be created
            table (str):                            The table the data will be appended to
            schema (str):                           The schema where this table can be found
                                                    Defaults to "dbo"
            replace_if_exists (bool, optional):     Table should be replaced if exists
                                                    Defaults to False, which means data will be appended
            index (bool, optional):                 Add an index to the table (if created/replaced)
                                                    Defaults to False
            dtype (dict, optional):                 Dictionary with datatypes used to create the table
                                                    Defaults to None, which means datatypes of dataframe will be used
            try_bcp (bool, optional):               Whether the user even wants to try to use BCP
                                                    Defaults to True
        
        Returns:
            None, the data will be written to the database table
        """
        exists = table_exists(con=self.sql_engine, table_name=table, schema=schema)

        if not exists:
            create_new = True
            print(
                f"create a new table {schema}.{table} in {self.f.decrypt(self.db).decode('utf-8')}"
            )
        elif exists & replace_if_exists:
            create_new = True
            print(
                f"dropped and recreated the table {schema}.{table} in {self.f.decrypt(self.db).decode('utf-8')}"
            )
        else:
            create_new = False
        
        if create_new:
            # start creating the empty table using pandas
            # since bcpy creates a table with only nvarchar(max) columns
            data.head(0).to_sql(
                name=table,
                con=self.sql_engine,
                schema=schema,
                if_exists="replace",
                index=index,
                dtype=dtype,
                method=None,
            )

        if try_bcp:
            try:
                # first try bcp, since this is the fastest solution
                # but also requires bcp to be installed and available in the PATH variables
                self._append_data_to_table_bcpy(data, table, schema)
            except Exception as e:
                # notice: we don't print the exception on purpose
                # it can contain all login credentials including the password
                print(
                    f"Failed to use bulk copy BCP (make sure this is installed and in the PATH). Will use pandas and pyodbc instead"
                )
        else:  
            try:
                data.to_sql(
                    name=table,
                    con=self.sql_engine,
                    schema=schema,
                    if_exists="append",
                    index=index,
                    dtype=dtype,
                    method=None,
                )
            except Exception as e:
                print(f"failed to load data to {table} with error: {e}")

    def retrieve_table_from_sql(self, table: str, schema: str = "dbo") -> pd.DataFrame:
        """
        Load an entire table from a SQL Server database into a pandas DataFrame

        Args:
            table (str):            The name of the table that has to be loaded
            schema (str, optional): The schema where the table can be found
                                    Defaults to "dbo"

        Returns:
            pd.DataFrame:   The table loaded into a pandas DataFrame
        """
        if table_exists(con=self.sql_engine, table_name=table, schema=schema):
            return pd.read_sql_table(table_name=table, schema=schema, con=self.sql_engine)
        else:
            print(
                f"table {schema}.{table} not found in database {self.f.decrypt(self.db).decode('utf-8')}"
            )

