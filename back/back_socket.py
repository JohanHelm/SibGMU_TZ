from socket import socket, AF_INET, SOCK_STREAM

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


def start_server_socket_part():
    manager = DbManager()
    HOST = ''
    PORT = 57360
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)

    while True:
        tcpCliSock, addr = tcpSerSock.accept()
        while True:
            data = tcpCliSock.recv(BUFSIZ)
            if data:
                sql_request = parse_command(data.decode('utf-8'))
                db_result = manager.data_query(sql_request)
                db_data = convert_db_result(db_result)
                tcpCliSock.send(bytes(db_data, 'utf-8'))
            else:
                break
        tcpCliSock.close()
