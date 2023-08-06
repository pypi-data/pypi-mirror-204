"""This module contains helper functions to connect and interact with different type of databases."""

from cmo_databaseutils import db_utils

import logging
logger = logging.getLogger(__name__)


class LoadDatabase(db_utils):
    """
    The database class of the DOTS DataLoader contains helper functions to load tables from a database
    
    Args:
        server (str):                   The complete link to the server where the database can be found
                                        Example: "myveryownserver.database.windows.net"
        db (str):                       The database to which should be connected
        server_name (str, optional):    The name of the server where the database can be found
                                        Example: "myveryownserver"
        usr (str, optional):            The username which is allowed to connect to the server and database
        pwd (str, optional):            The password for this username
        driver (str, optional):         The driver that is available to connect to the server and database 
                                        Defaults to "ODBC+Driver+17+for+SQL+Server"
        port (int, optional):           The port used for the connection
                                        Defaults to 1433
        max_tries (int, optional):      The number of tries to create the connection, this might be helpful
                                        when connecting to a database that could be sleeping and therefore
                                        doesn't alsways wake up fast enough to connect at the first try
                                        Defaults to 5
        tables (list, optional):        A list with strings, with the format schema.tablename, these are all tables
                                        that will be loaded into the dictionary
                                        Defaults to None, which means all tables from all schemas will be loaded
    
    Attributes:
        databaseutils:  A DOTS DatabaseUtils object
        tables:         A list of all tables to be loaded
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
        tables: list = None,
        add_to_connectionstring: str = "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;",
    ) -> None:
        super().__init__(
            server=server,
            db=db,
            server_name=server_name,
            usr=usr,
            pwd=pwd,
            driver=driver,
            port=port,
            max_tries=max_tries,
            add_to_connectionstring=add_to_connectionstring
        )
        if tables is None:
            all_schemas = self.list_all_active_schemas()
            self.tables = self.list_all_tables(all_schemas)
        else:
            self.tables = tables

    def load(self) -> dict:
        """
        Load and return a dict of df's

        Args: 
            None, class attributes will be used

        Returns:
            dict_of_dfs A dict of Pandas Dataframes
        """

        # Create a dictionary with an item for each file
        dict_with_files = {
            file: self.retrieve_table_from_sql(
                table=file.split('.')[1], schema=file.split('.')[0]
            )
            for file in self.tables
        }
        # In case a file failed to load, remove the entry from the dictionary
        dict_of_dfs = {
            key: value for key, value in dict_with_files.items() if value is not None
        }
        return dict_of_dfs
