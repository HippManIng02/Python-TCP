# coding: utf-8

import socket
import time 
import random

print("\t\t\t###############################")
print('\t\t\t\tCLIENT')
print("\t\t\t###############################")
print("\n")

#Le port d'écoute
PORT_SERVER = 2003
#Recuperation du nombre variable de paquet
n = int(input("Nombre variable de paquets (N): "))

not_correct = True

#Recuperation de la taille de la fenêtre d'envoie
while not_correct:
    rcvwindow = int(input("Taille de sa file d’attente rcvwindow (rcvwindow <= N): "))
    if rcvwindow <= n:
        not_correct = False
print("\n")
#initialisation de l'objet socket
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Fonction permerttant de receptionner les paquets et de simuler une perte de paquet
def reception_paquet(socket_client, n, rcvwindow):
    data = []
    i = 0
    while i < n:
        item = socket_client.recv(1024).decode()
        #Simulation de perte de paquet avec une probabilité de 60%
        if random.random() < 0.6:
            print("\033[91mPaquet perdu !!!!\033[0m")
            socket_client.send("NEG".encode())
        else:
            socket_client.send("POS".encode())
            data.append(item)
            print(f'\033[92mReception du paquet {item}\033[0m')            
            i += rcvwindow
    return data

try:
    #Connexion au serveur
    socket_client.connect((socket.gethostname(), PORT_SERVER))
    print("\033[92mConnecté au serveur avec succès!\033[0m")
    socket_client.send(b'SYN')
    response = socket_client.recv(1024).decode()
    if response:
        print("\033[92mReception du paquet SYN-ACK de la part du serveur...\033[0m")
    
    # Definition du temps d'attente entre l'envoie de deux paquet
    timeout = int(input("Définir le timeout : "))

    socket_client.send(f"{n},{rcvwindow}, {timeout}".encode())

    # Reception de paquet
    data = reception_paquet(socket_client, n, rcvwindow)

    socket_client.send("FIN".encode())

    fin_ack_paquet = socket_client.recv(1024)
    print("\n")
    if fin_ack_paquet:
        print("\033[92mReception de paquet FIN-ACK de la part du serveur!\033[0m")

    print("Entente de 30 avant la fermerture de la connexion!")

    message = ''.join(data)
    print("\n")
    print("\033[92m###############################\033[0m")
    print('Message : ', message)
    print("\033[92m###############################\033[0m")

    time.sleep(30)
    
finally:
    print("Connexion fermée!!!")
    socket_client.close()
    time.sleep(10000)