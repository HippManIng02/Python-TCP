import subprocess
import os
import platform

def ouvrir_terminal(commande):
    #subprocess.Popen(["gnome-terminal"]) 
    if platform.system() == "Windows":
        subprocess.Popen(["cmd", "/c", commande], creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", commande])
    else:
        print("Système d'exploitation non pris en charge.")

if __name__ == "__main__":
    # Spécifiez les chemins de vos fichiers Python
    fichier1 = "server.py"
    fichier2 = "client.py"

    # Ouvrir chaque fichier dans un terminal différent
    ouvrir_terminal(f"python3 {fichier1}")
    ouvrir_terminal(f"python3 {fichier2}")