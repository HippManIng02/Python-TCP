# coding: utf-8

import socket
import time

print("\t\t\t###############################")
print('\t\t\t\tSERVEUR')
print("\t\t\t###############################")
print("\n")

#Port d'écoute du serveur
PORT = 2003
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

message_transmettre = input("Entrer le message que le serveur doit envoyer : ")
print("Taille : ", len(message_transmettre))

def envoie_de_paquet(client_socket, n, rcvwindow, timeout):
    item = 0
    while item < n:
        # if item < rcvwindow:
        #     client_socket.send(f"{message_transmettre[item:rcvwindow]}".encode())
        #     print(f"Envoie du paquet {message_transmettre[item:rcvwindow]}")
        #     time.sleep(2)
        #     item += rcvwindow
        client_socket.send(f"{message_transmettre[item:rcvwindow+item]}".encode())
        print(f"Envoie du paquet {message_transmettre[item:rcvwindow+item]}")
        acquitement = client_socket.recv(1024).decode()
        if acquitement == "POS":
            item += rcvwindow
        else:
            print(f"Perte de paquet '{message_transmettre[item:rcvwindow+item]}'!")
            print("Retransmission du paquet.......")
        time.sleep(timeout)
        
try:
    #Liaison du socket avec le port et le nom d'hôte de la machine dans notre cas ici la chaine vide correspond à l'adresse 0.0.0.0
    hote = socket.gethostname()
    adresse_serveur = (hote, PORT)
    socket_server.bind(adresse_serveur)
    #Mise à l'écoute du serveur sur le Port d'écoute
    socket_server.listen()
    print("Serveur en écoute............")

    connexion_client, adresse_client = socket_server.accept()
    print(f"Connexion entrante de {adresse_client}")
    msg = connexion_client.recv(1024)
    #Acquittement du message SYN du client
    if msg:
        print("Paquet SYN reçu du client.")
        print("Envoi d'un paquet SYN + ACK au client...")
        connexion_client.sendall(b'SYN-ACK')
        print("Paquet SYN + ACK envoyé au client.")
    
    data = connexion_client.recv(1024).decode()
    
    n, rcvwindow, timeout = map(int, data.split(","))
    #Fonction permettant d'envoyer les paquets
    envoie_de_paquet(connexion_client, n, rcvwindow, timeout)

    fin_paquet = connexion_client.recv(1024)
    #Acquittement du message FIN
    print("\n")
    if fin_paquet:
        print("Reception de paquet FIN de la part du client...")
        connexion_client.send("FIN-ACK".encode())
        print("Envoie du paquet FIN-ACK au client")

finally:
    #Fermeture de la connexion
    print("Connexion fermée!!!")
    connexion_client.close()
    socket_server.close()
    time.sleep(10000)