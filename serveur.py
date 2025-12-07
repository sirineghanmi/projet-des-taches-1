import socket
import json
import threading
from gestionnaire import GestionnaireTaches

HOST = "0.0.0.0"  # écoute toutes interfaces
PORT = 5000
BUFFER_SIZE = 4096
ENC = "utf-8"

gest = GestionnaireTaches()

def traiter_msg(obj):
    action = obj.get("action")
    
    if action == "ADD":
        t = gest.ajouter_tache(obj["titre"], obj["description"], obj.get("auteur", "inconnu"))
        return {"status": "OK", "id": t.id}

    elif action == "LIST":
        taches = [t.to_dict() for t in gest.lister_taches()]
        return {"status": "OK", "taches": taches}

    elif action == "DEL":
        if gest.supprimer_tache(obj["id"]):
            return {"status": "OK"}
        else:
            return {"status": "NOT_FOUND"}

    elif action == "STATUS":
        if gest.changer_statut(obj["id"], obj["statut"]):
            return {"status": "OK"}
        else:
            return {"status": "NOT_FOUND"}

    return {"status": "UNKNOWN"}

def handle_client(conn, addr):
    print("Client connecté:", addr)
    buffer = b""
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                try:
                    obj = json.loads(line.decode(ENC))
                    rep = traiter_msg(obj)
                    conn.sendall((json.dumps(rep, ensure_ascii=False) + "\n").encode(ENC))
                except json.JSONDecodeError:
                    conn.sendall((json.dumps({"status": "ERROR", "msg": "JSON invalide"}) + "\n").encode(ENC))
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print("Client déconnecté:", addr)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Serveur en écoute sur {HOST}:{PORT}")

    try:
        while True:
            conn, addr = sock.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nServeur arrêté")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
