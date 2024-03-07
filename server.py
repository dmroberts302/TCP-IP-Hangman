# Name: Daijon Roberts UA ID: 010963348

import sys
import pickle
import threading
from socket import *

# add error handling

def handle_client(client_socket):
    word = "ARKANSAS"
    tmp_word = word
    word_length = len(word)
    guessed_word = "_" * word_length
    guesses_remaining = 7
    guessed_right = False
    dead = False
    struct = [guessed_word, guessed_right, dead, guesses_remaining, word_length]
    serialized_data = pickle.dumps(struct)
    client_socket.send(serialized_data)
    while not guessed_right and not dead:
        letter = client_socket.recv(1024).decode('utf-8')
        letter = letter.upper()
        if letter in word and len(letter) == 1:
            index = word.index(letter)
            word = word[:index] + "_" + word[index + 1:]
            guessed_word = guessed_word[:index] + letter + guessed_word[index + 1:]
            guessed_right = all(c == '_' for c in word)
        else:
            guesses_remaining -= 1
            if guesses_remaining == 0:
                dead = True

        struct = [guessed_word, guessed_right, dead, guesses_remaining, word_length]
        serialized_data = pickle.dumps(struct)
        client_socket.send(serialized_data)
    if dead:
        client_socket.send(tmp_word.encode('utf-8'))
    client_socket.close()

def start_server(host, port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print('server ready to receive')
    print('')
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,)) 
        client_thread.start()


if __name__ == "__main__":
    try:
        server_port = int(sys.argv[1])
    except:
        server_port = 27019
    start_server('', server_port)
