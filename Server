#!/usr/bin/python
import socket
import os
import select
import subprocess
#from tcp.py import client

hote = '146.19.253.20'
port = 10000

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur Ã©coute Ã  prÃ©sent sur le port {}".format(port))

serveur_lance = True
clients_connectes = []
while serveur_lance:
    # On va vÃ©rifier que de nouveaux clients ne demandent pas Ã  se connecter
    # Pour cela, on Ã©coute la connexion_principale en lecture
    # On attend maximum 50ms
    connexions_demandees, wlist, xlist = select.select([connexion_principale],
        [], [], 0.05)
    
    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion.accept()
        # On ajoute le socket connectÃ© Ã  la liste des clients
        clients_connectes.append(connexion_avec_client)
    
    # Maintenant, on Ã©coute la liste des clients connectÃ©s
    # Les clients renvoyÃ©s par select sont ceux devant Ãªtre lus (recv)
    # On attend lÃ  encore 50ms maximum
    # On enferme l'appel Ã  select.select dans un bloc try
    # En effet, si la liste de clients connectÃ©s est vide, une exception
    # Peut Ãªtre levÃ©e
    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes,
                [], [], 0.05)
    except select.error:
        pass
    else:
        i=10001
        # On parcourt la liste des clients Ã  lire
        for client in clients_a_lire:
          # Client est de type socket
          msg_recu = client.recv(1024)
          # Peut planter si le message contient des caractÃ¨res spÃ©ciaux
          msg_recu = msg_recu.decode()
          print("ReÃ§u {}".format(msg_recu))
          if msg_recu != "":
            if msg_recu == "nginx":
                os.system("docker pull nginx")
                os.system("docker run -p %s:80 nginx") % (i)
                i=i+1
                print('nginx.')
            elif "signup," in msg_recu:
                msg_splitted= msg_recu.split(",")
                username = msg_splitted[1]
                passwd = msg_splitted[2]
                pin = msg_splitted[3]
                with open('/home/cfa/PinCodes.txt', "r") as fPinCodes:
                    for line in fPinCodes:
                        if pin in line:
                            print("Pin prÃ©sent dans fichier")
                            fPinCodes.close()
                            fPinCodes = open("/home/cfa/PinCodes.txt","r")
                            lines = fPinCodes.readlines()
                            fPinCodes.close()
                            fPinCodes = open("/home/cfa/PinCodes.txt","w")
                            for line in lines:
                              if line!=pin+"\n":
                                fPinCodes.write(line)
                            fPinCodes.close()        
                            with open('/home/cfa/usersCred.txt', 'a') as fusersCred:
                                fusersCred.write(username+","+passwd+","+pin+",\n")
                            fusersCred.close()
                            print("Utilisateur bien crÃ©e dans le fichier")
                        else:
                            print("Pin non prÃ©sent dans le fichier, utilisateur non crÃ©Ã©")
                            connexion_avec_client.send("wrongPIN".encode(encoding='utf-8'))		
            elif "login," in msg_recu:
                msg_splitted= msg_recu.split(",")
                cred_to_check = msg_splitted[1]+","+msg_splitted[2]+","
                print(cred_to_check)
                result_check_cred=0
                with open('/home/cfa/usersCred.txt', 'r') as fusersCred:
                    for line in fusersCred:
                        if cred_to_check in line:
                            result_check_cred=1    
                if result_check_cred==1:
                    print("credentials present in file")
                    connexion_avec_client.send("OK".encode(encoding='utf-8'))
                elif result_check_cred==0:
                    print("credentials not present in file")
                    connexion_avec_client.send("wrongCred".encode(encoding='utf-8'))
                fusersCred.close()

            elif "getID," in msg_recu:
                msg_splitted= msg_recu.split(",")
                user_to_find = msg_splitted[1]+","+msg_splitted[2]
                print(user_to_find)
                with open('/home/cfa/usersCred.txt', 'r') as fusersCred:
                    for line in fusersCred:
                        if user_to_find in line:
                            user_line=line.split(",")
                            userPIN=user_line[2]
                            connexion_avec_client.send(userPIN.encode(encoding='utf-8'))
                fusersCred.close()
            elif "getRC," in msg_recu:
                out = subprocess.check_output("docker ps | grep cyril", shell=True)
                connexion_avec_client.send(out)
            elif "jenkins," in msg_recu:
                msg_splitted= msg_recu.split(",")
                pin = msg_splitted[3]
                os.system("cd /home/cfa/")
                out = subprocess.check_output("docker run -d --name "+ID+" -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):/usr/bin/docker -p 10001:8080 jenkins", shell=True)
                connexion_avec_client.send(out)

def getAvailablePorts():
    #Sert a verifier les ports libres que lon peut utiliser
    print("hello")

def cleanPorts(Port):
    #Sert a supprimer les proccessus qui utilisent un port
    print("hello")

print("Fermeture de la connexion")
connexion_avec_client.close()
connexion_principale.close()
