import asyncio
from loguru import logger

from db_handler import DbManager
from back_socket import start_server_socket_part


def set_up_logger(logger=logger, file_path="/backend/logs/logfile", rotation=10):
    logger.remove(0)
    logger.add(file_path, rotation=f"{rotation} MB")
    logger.debug(
        f"Configure: basic logger update conf with write to {file_path} and set file rotation at {rotation} MB")

if __name__ == "__main__":
    set_up_logger()
    manager = DbManager()
    manager.default_create_table()
    if not manager.data_query(f"SELECT * FROM Persons;"):
        manager.default_populate_table()

    asyncio.run(start_server_socket_part())
