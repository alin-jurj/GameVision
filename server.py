import socket
from _thread import *
import sys

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(20)
print("Waiting for a connection. Server started.")

connected = set()
games = {}
idCount = 0


def read_information(string):
    string = string.split(',')
    if string[0] == 'play':
        return [string[0], int(string[1]), string[2], int(string[3])]
    elif string[0] == 'game':
        return [string[0], int(string[1]), int(string[2]), int(string[3])]
    else:
        return -1


def make_information_play(selections):
    return 'play,' + str(selections[0]) + ',' + selections[1] + ',' + str(selections[2])


def make_information_game(information):
    return 'game,' + str(information[0]) + ',' + str(information[1]) + ',' + str(information[2])


selected_map = {}
selected_character = {}
ready = {}
game_connected = {}
player = {}
positions_x = {}
positions_y = {}
hp = {}


def threaded_client(connection, player, gameId):
    inf = [selected_map[gameId][player], selected_character[gameId][player], ready[gameId][player]]
    connection.send(str.encode(make_information_play(inf)))
    reply = -1

    while True:
        try:
            data = read_information(connection.recv(2048).decode())
            if data[0] == 'play':
                selected_map[gameId][player] = data[1]
                selected_character[gameId][player] = data[2]
                ready[gameId][player] = data[3]
            elif data[0] == 'game':
                positions_x[gameId][player] = data[1]
                positions_y[gameId][player] = data[2]
                hp[gameId][player] = data[3]
            else:
                print('NU')

            if not data:
                print("Disconnected")
                break
            else:
                if data[0] == 'play':
                    if player == 1:
                        reply = [selected_map[gameId][0], selected_character[gameId][0], ready[gameId][0]]
                    else:
                        reply = [selected_map[gameId][1], selected_character[gameId][1], ready[gameId][1]]
                elif data[0] == 'game':
                    if player == 1:
                        reply = [positions_x[gameId][0], positions_y[gameId][0], hp[gameId][0]]
                    else:
                        reply = [positions_x[gameId][1], positions_y[gameId][1], hp[gameId][1]]

                print("Received: ", data)
                print("Sending: ", reply)

            if data[0] == 'play':
                connection.sendall(str.encode(make_information_play(reply)))
            if data[0] == 'game':
                connection.sendall(str.encode(make_information_game(reply)))

        except:
            break

    print("Lost connection")
    try:
        del selected_map[gameId]
        del selected_character[gameId]
        del ready[gameId]
        del game_connected[gameId]
        del positions_x[gameId]
        del positions_y[gameId]
        del hp[gameId]
        print("Closing game ", gameId)
    except:
        pass
    connection.close()


while True:
    connection, address = s.accept()
    print("Connected to ", address)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        selected_map[gameId] = [-1, -1]
        selected_character[gameId] = ['', '']
        ready[gameId] = [0, 0]
        player[gameId] = [0, 1]
        positions_x[gameId] = [0, 0]
        positions_y[gameId] = [500, 500]
        hp[gameId] = [150, 150]
        game_connected[gameId] = False
    else:
        game_connected[gameId] = True
        p = 1

    start_new_thread(threaded_client, (connection, p, gameId))
