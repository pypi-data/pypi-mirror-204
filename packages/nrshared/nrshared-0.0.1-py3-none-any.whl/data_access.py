from .logger import CustomLogger
import os
import sys
from numpy import fabs
import pandas as pd
import aioodbc
from datetime import datetime
from constants import Constants
from .error import  QueryExecutionError
sys.path.insert(0, os.getcwd())

LOGGERNAME = 'loggerDataToJson'
LOGGERFORMAT = "%(asctime)s | %(levelname)s | %(message)s"
logger = CustomLogger(LOGGERNAME, LOGGERFORMAT)
dbr="Database result received at "+datetime.utcnow().strftime(Constants().DATE_FORMAT)


class Sql:
    def __init__(self, connection_string_key="SqlConnectionString", is_auto_commit=True, auto_close_connection=True):
        """Initialize a SQLConnection instance
        """
        try:            
            self.connection_string = os.environ[connection_string_key]
            self.sql_connection = None
            self.sql_cursor = None
            self.auto_close_connection = auto_close_connection
            logger.info("Database Connection  Set at "+datetime.utcnow().strftime(Constants().DATE_FORMAT))
        except Exception as ex:
            logger.error(
                f"DB connection initialization failed for key {connection_string_key} - Error: {ex}")
            raise ex

    async def connect_db(self, loop=None):
        logger.info("Database Connection  initiated at "+datetime.utcnow().strftime(Constants().DATE_FORMAT))
        self.sql_connection = await aioodbc.connect(dsn=self.connection_string) 
        self.sql_cursor = await self.sql_connection.cursor()
        logger.info("Database connection made at "+datetime.utcnow().strftime(Constants().DATE_FORMAT))

    async def read_to_dataframe(self, sp_query, params=None):
        """Fetch the DB results in the form of a pandas Dataframe
        Args:
            sp_query (str). the SQL Stored Procedure query that needs to be executed
            params (tuple). the query param if any. (defaults to None)
        return: dictionary
        """
        try:
            await self.sql_cursor.execute(sp_query, params or ())
            result = await self.sql_cursor.fetchall()
            dictionary = [
                dict(zip([key[0] for key in self.sql_cursor.description], row)) for row in result]
            
            frame=pd.DataFrame(dictionary)              
            if len(dictionary) != 0 and 'ErrorMessage' in dictionary[0]:
                error = dictionary[0]['ErrorMessage']
                proc = dictionary[0]['ErrorProcedure']
                logger.error(f"DB exception thrown - {proc} - {error}")
                return error    
            logger.info(dbr)           
            return frame
        except QueryExecutionError as qe:
            logger.error(f"Query failed to execute{qe}")
            raise qe
        except Exception as err:
            logger.error(f"Query failed to execute: {sp_query}, Error: {err}")
            raise err
        finally:
            if (self.auto_close_connection):
                await self.close_connections()
                
    async def execute_query(self, sp_query, params=None):
        """Fetch the DB results in the form of a pandas Dataframe
        Args:
            sp_query (str). the SQL Stored Procedure query that needs to be executed
            params (tuple). the query param if any. (defaults to None)
        return: dictionary
        """
        try:
            await self.sql_cursor.execute(sp_query, params or ())
            result = await self.sql_cursor.fetchall()            
            dictionary = [
                dict(zip([key[0] for key in self.sql_cursor.description], row)) for row in result]            
            if len(dictionary) != 0 and 'ErrorMessage' in dictionary[0]:
                error = dictionary[0]['ErrorMessage']
                proc = dictionary[0]['ErrorProcedure']
                logger.error(f"DB exception thrown - {proc} - {error}")
                return error
            
            logger.info(dbr)
                          
            return dictionary
        except QueryExecutionError as qe:
            logger.error(f"Query failed to execute{qe}")
            raise qe
        except Exception as err:
            logger.error(f"Query failed to execute: {sp_query}, Error: {err}")
            raise err
        finally:
            if (self.auto_close_connection):
                await self.close_connections()

    async def execute_update_query(self, query, params=None):
        try:            
            await self.sql_cursor.execute(query, params or ())
            self.commit()        
            rows_affected = self.sql_cursor.rowcount                        
            logger.info(dbr+" Number of rows affected: "+str(rows_affected))
            return rows_affected

        except QueryExecutionError as qe:
                logger.error(f"Query failed to execute{qe}")
                return 0
        except Exception as err:
            logger.error(f"Query failed to execute, Error: {err}")
            return 0
        finally:
            if (self.auto_close_connection):
                await self.close_connections()

    

    async def execute_query_with_time(self, query, starttime, params=None):
        try:            
            await self.sql_cursor.execute(query, params or ())
            lookup_rows = await self.sql_cursor.fetchall()
            dictionary = [dict(zip([key[0] for key in self.sql_cursor.description], row)) for row in lookup_rows]
            logger.info("Database result resut received  at "+datetime.utcnow().strftime(Constants().DATE_FORMAT)+" Time taken in Seconds:"+str((datetime.utcnow()-starttime).total_seconds()))
            return dictionary

        except QueryExecutionError as qe:
            logger.error(f"Query failed to execute{qe}")
            raise qe
        except Exception as err:
            logger.error(f"Query failed to execute: {query}, Error: {err}")
            raise err
        finally:
            if (self.auto_close_connection):
                await self.close_connections()

    async def execute_non_query(self, query, params=None):
        try:
            await self.sql_cursor.execute(query, params or ())
            lookup_rows = await self.sql_cursor.fetchall()
            dictionary = [dict(zip([key[0] for key in self.sql_cursor.description], row)) for row in lookup_rows]
            self.commit()
            
            logger.info(dbr)
            return dictionary

        except QueryExecutionError as qe:
            logger.error(f"Query failed to execute{qe}")
            raise qe
        except Exception as err:
            logger.error(f"Query failed to execute: {query}, Error: {err}")
            raise err
        finally:
            if (self.auto_close_connection):
                await self.close_connections()

    def commit(self):
        self.sql_connection.commit()

    def rollback(self):
        self.sql_connection.rollback()

    async def close_connections(self):
        await self.sql_cursor.close()
        await self.sql_connection.close()