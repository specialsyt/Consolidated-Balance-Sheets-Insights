import json
import os
import sqlite3
import threading
from typing import Dict
import warnings

class Database:
    _instances = {}
    _dbName = None
    _filingsDbName = None

    def __init__(self, dbName='fsil.db', filingsDbName="filingsCache"):
        """
        Initializes a Database object.

        Args:
            dbName (str): The name of the database file. Defaults to 'fsil.db'.
            filingsDbName (str): The name of the filings table in the database. Defaults to 'filingsCache'.
        """
        # warnings.warn("Database is a deprecated class", category=DeprecationWarning)

        Database._dbName = dbName
        Database._filingsDbName = filingsDbName
        self.filingsDbName = filingsDbName
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.filingsDbName}
                    (id INTEGER PRIMARY KEY, ticker TEXT, data TEXT, inference TEXT)''')
        self.conn.commit()
        return

    def cache_filing(self, ticker: str, data: str):
        """
        Caches the filing data for a given ticker.

        Parameters:
        - ticker (str): The ticker symbol of the company.
        - data (str): The filing data to be cached.

        Returns:
        None
        """
        data = json.dumps(data)
        self.cursor.execute(f'INSERT INTO {self.filingsDbName} (ticker, data, inference) VALUES (:ticker, :data, "")', { 'ticker': ticker, 'data': data})
        self.conn.commit()
        return
    
    def cache_inference(self, ticker: str, inference: str):
        """
        Adds the inference data for a given ticker.

        Parameters:
        - ticker (str): The ticker symbol of the company.
        - inference (str): The inference data to be added.

        Returns:
        None
        """
        self.cursor.execute(f'UPDATE {self.filingsDbName} SET inference=(:inference) WHERE ticker=(:ticker)', { 'inference': inference, 'ticker': ticker})
        self.conn.commit()
        return
    
    def get_filing(self, ticker):
        """
        Retrieves all the filings for a given ticker from the database.

        Parameters:
        ticker (str): The ticker symbol for the company.

        Returns:
        list: A list of tuples representing the retrieved filings.
        """
        self.cursor.execute(f'SELECT * from {self.filingsDbName} WHERE ticker=(:ticker)', { 'ticker': ticker})
        data = self.cursor.fetchone()
        return json.loads(data[2]) if data is not None else None
    
    def get_inference(self, ticker):
        """
        Retrieves the inference for a given ticker from the database.

        Parameters:
        ticker (str): The ticker symbol for the company.

        Returns:
        str: The inference for the given ticker.
        """
        self.cursor.execute(f'SELECT * from {self.filingsDbName} WHERE ticker=(:ticker)', { 'ticker': ticker})
        data = self.cursor.fetchone()
        return data[3] if data is not None else None

    def filing_is_cached(self, ticker):
        """
        Checks if the filing for a given ticker is cached in the database.

        Parameters:
        - ticker (str): The ticker symbol of the company.

        Returns:
        - bool: True if the filing is cached, False otherwise.
        """
        self.cursor.execute(f'SELECT * from {self.filingsDbName} WHERE ticker=(:ticker)', { 'ticker': ticker})
        return len(self.cursor.fetchall()) != 0
    
    def inference_is_cached(self, ticker):
        """
        Checks if the inference for a given ticker is cached in the database.

        Parameters:
        - ticker (str): The ticker symbol of the company.

        Returns:
        - bool: True if the inference is cached, False otherwise.
        """
        self.cursor.execute(f'SELECT * from {self.filingsDbName} WHERE ticker=(:ticker)', { 'ticker': ticker})
        data = self.cursor.fetchone()
        return data[3] != ""
    
    @staticmethod
    def get_instance() -> 'Database':
            """
            Returns an instance of the Database class.

            If an instance of the Database class has not been constructed before,
            an exception is raised.

            Returns:
                Database: An instance of the Database class.

            Raises:
                Exception: If the Database has not been constructed before call.
            """
            if Database._dbName is None:
                raise Exception('Database has not been constructed before call')

            curr_thread_ident = threading.current_thread().ident
            if curr_thread_ident not in Database._instances:
                Database._instances[curr_thread_ident] = Database(Database._dbName, Database._filingsDbName)
            return Database._instances[curr_thread_ident]
    
    def __del__(self):
        self.conn.close()
        return

    # def __new__(cls, *args, **kwargs):
    #     curr_thread_ident = threading.current_thread().ident
    #     if curr_thread_ident not in cls._instances:
    #         cls._instances[curr_thread_ident] = super(Database, cls).__new__(cls)
    #     return cls._instances[curr_thread_ident]