# Name: Daijon Roberts UA ID: 010963348

import sys
import pickle
from socket import *

def display_server_data(serialized_data):
    guessed_word = serialized_data[0]
    guesses_remaining = serialized_data[3]
    word_len = serialized_data[4]
    print("")
    print(f"word length: {word_len}")
    print(f"guesses remaining: {guesses_remaining}")
    print(guessed_word)


def start_client(server_name, server_port):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    serialized_data = pickle.loads(client_socket.recv(1024))
    display_server_data(serialized_data)
    while True:
        print("")
        letter = input("guess letter: ")
        letter_bytes = letter.encode('utf-8')
        client_socket.send(letter_bytes)
        serialized_data = pickle.loads(client_socket.recv(1024))
        display_server_data(serialized_data)
        guessed_right = serialized_data[1]
        dead = serialized_data[2]
        if dead or guessed_right:
            break
    if dead:
        word = client_socket.recv(1024).decode('utf-8')
        print("")
        print(f"you lost, word is: {word}")
    else:
        print("")
        print("you won")
    client_socket.close()

if __name__ == "__main__":
    try:
        server_name = sys.argv[1]
        server_port = int(sys.argv[2])
    except:
        server_name = "localhost"
        server_port = 27019
    start_client(server_name, server_port)
    

