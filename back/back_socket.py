import asyncio
from loguru import logger

from db_handler import DbManager


def parse_command(raw_command: str) -> str:
    sql_operator, *params = raw_command.split("&")
    if sql_operator == "INSERT":
        name, height, weight, age = params
        sql_request = f"INSERT INTO Persons (name, height, weight, age) VALUES ('{name}', {height}, {weight}, {age});"
    elif sql_operator == "SELECT":
        name = params[0]
        if name == "all":
            sql_request = f"SELECT * FROM Persons;"
        else:
            sql_request = f"SELECT * FROM Persons WHERE name = '{name}';"
    return sql_request


def convert_db_result(db_result: list[tuple]) -> str:
    if db_result:
        if len(db_result) > 1:
            return "&".join([item[1] for item in db_result])
        else:
            return "&".join(map(str, db_result[0][1:]))
    else:
        return "Данные успешно внесены в базу"


HOST = ''
PORT = 57360
BUFSIZ = 1024


async def handle_client(reader, writer):
    data = await reader.read(BUFSIZ)
    command = data.decode().strip()
    if command:
        manager = DbManager()
        sql_request = parse_command(command)
        db_result = manager.data_query(sql_request)
        db_data = convert_db_result(db_result)
        writer.write(db_data.encode())
        await writer.drain()
    writer.close()


async def start_server():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    logger.info(f'Serving on {addr}')
    async with server:
        await server.serve_forever()


async def start_server_socket_part():
    await asyncio.gather(start_server())
