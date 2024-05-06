import time

import mysql.connector
from loguru import logger
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection


class DbManager:
    def __init__(self):
        self.db_name = 'testdatabase'
        self.config = {'user': 'testuser',
                       'password': 'testpassword',
                       'host': 'mariadb',
                       'database': self.db_name,
                       'raise_on_warnings': True}

        self.table_name = 'Persons'
        self.table_description = """CREATE TABLE Persons(
                                                            id      INT PRIMARY KEY AUTO_INCREMENT,
                                                            name    VARCHAR(20),
                                                            height  INT,
                                                            weight  INT,
                                                            age     INT
                                                        );"""
        self.default_data = """INSERT INTO Persons (name, height, weight, age) 
                                VALUES ('Миша', 165, 65, 20),
                                ('Петя', 175, 85, 22),
                                ('Вова', 185, 95, 25)
                            ;"""

    def _connect_to_db(self, attempts: int = 3, delay: int = 2) -> PooledMySQLConnection:
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                return mysql.connector.connect(**self.config)
            except (mysql.connector.Error, IOError) as err:
                if attempts is attempt:
                    # Attempts to reconnect failed; returning None
                    logger.info("Failed to connect, exiting without a connection: %s", err)
                logger.info(
                    f"Connection attempt {attempt} failed: %s. Retrying (%d/%d)...",
                    err,
                    attempt,
                    attempts - 1,
                )
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1

    def _create_cursor(self, connection_obj: PooledMySQLConnection) -> MySQLCursorAbstract:
        return connection_obj.cursor()

    def _disconnect(self, connection_obj: PooledMySQLConnection):
        connection_obj.close()

    def _create_database(self, connection_obj: PooledMySQLConnection):
        try:
            cursor = self._create_cursor(connection_obj)
            cursor.execute(f"CREATE DATABASE {self.db_name} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            logger.info(f"Failed to create {self.db_name} database: {err}")
            exit(1)
        else:
            cursor.close()

    def _use_database(self, connection_obj: PooledMySQLConnection):
        try:
            cursor = self._create_cursor(connection_obj)
            cursor.execute(f"USE {self.db_name}")
        except mysql.connector.Error as err:
            logger.debug(f"Database {self.db_name} does not exists.")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self._create_database(connection_obj)
                logger.info(f"Database {self.db_name} created successfully.")
                connection_obj.database = self.db_name
            else:
                print(err)
                exit(1)
        else:
            cursor.close()

    def _create_table(self, table_description: str, table_name: str, connection_obj: PooledMySQLConnection):
        try:
            cursor = self._create_cursor(connection_obj)
            logger.info(f"Creating table: {table_name}")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logger.debug(f"Table {table_name} already exists.")
            else:
                logger.debug(err.msg)
        else:
            logger.info(f"Table {table_name} has created successfully!!")
            cursor.close()

    def _populate_table(self, add_data, connection_obj: PooledMySQLConnection):
        cursor = self._create_cursor(connection_obj)
        cursor.execute(add_data)
        connection_obj.commit()
        cursor.close()

    def default_create_table(self):
        connection_obj = self._connect_to_db()
        self._use_database(connection_obj)
        self._create_table(self.table_description, self.table_name, connection_obj)
        self._disconnect(connection_obj)

    def default_populate_table(self):
        connection_obj = self._connect_to_db()
        self._populate_table(self.default_data, connection_obj)
        self._disconnect(connection_obj)

    def data_query(self, sql_request: str, params=None):
        connection_obj = self._connect_to_db()
        self._use_database(connection_obj)
        cursor = self._create_cursor(connection_obj)
        cursor.execute(sql_request, params)
        result = cursor.fetchall()
        connection_obj.commit()
        cursor.close()
        connection_obj.close()
        return result
