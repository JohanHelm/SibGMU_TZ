from socket import socket, AF_INET, SOCK_STREAM

HOST = '127.0.0.1'
PORT = 57360
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

# command="INSERT&Маша&175&65&18"
# command="SELECT&Маша"
command="SELECT&all"
# command = "SELECT"
def send_to_back(command: str):
    data = bytes(command, 'utf-8')
    tcpCliSock.send(data)
    responce = tcpCliSock.recv(BUFSIZ)
    return responce

print(send_to_back(command).decode('utf-8'))
# command = "CREATE&Маша&175&65&18"
# while True:
#     data = bytes(command, 'utf-8')            # input('> ').encode('utf-8')
#     if not data:
#         break
#     tcpCliSock.send(data)
#     data = tcpCliSock.recv(BUFSIZ)
#     if not data:
#         break
#     print(data.decode('utf-8'))
# tcpCliSock.close()


