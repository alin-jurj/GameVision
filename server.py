import socket
from _thread import *
import sys

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection. Server started.")


def read_information(str):
    str = str.split(',')
    if str[0] == 'play':
        return [str[0], int(str[1]), str[2], int(str[3])]
    else:
        return -1


def make_information_play(selections):
    return 'play,' + str(selections[0]) + ',' + selections[1] + ',' + str(selections[2])


pos = [(100, 50), (900, 50)]
selected_map = [-1, -1]
selected_character = ['', '']
ready = [0, 0]


def threaded_client(connection, player):
    inf = [selected_map[player], selected_character[player], ready[player]]
    connection.send(str.encode(make_information_play(inf)))
    reply = -1

    while True:
        try:
            data = read_information(connection.recv(2048).decode())
            if data[0] == 'play':
                selected_map[player] = data[1]
                selected_character[player] = data[2]
                ready[player] = data[3]
            else:
                print("NU")

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = [selected_map[0], selected_character[0], ready[0]]
                else:
                    reply = [selected_map[1], selected_character[1], ready[1]]

                print("Received: ", data)
                print("Sending: ", reply)

            connection.sendall(str.encode(make_information_play(reply)))

        except:
            break

    print("Lost connection")
    connection.close()


currentPlayer = 0

while True:
    connection, address = s.accept()
    print("Connected to ", address)

    start_new_thread(threaded_client, (connection, currentPlayer))

    currentPlayer += 1
