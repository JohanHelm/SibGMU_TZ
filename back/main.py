from back_socket import start_server_socket_part
from loguru import logger

def set_up_logger(logger=logger, file_path="/backend/logs/logfile", rotation=10):
    logger.remove(0)
    logger.add(file_path, rotation=f"{rotation} MB")
    logger.debug(
        f"Configure: basic logger update conf with write to {file_path} and set file rotation at {rotation} MB")

if __name__ == "__main__":
    set_up_logger()
    start_server_socket_part()
