from client import ClientTaches

def menu():
    cli = ClientTaches(host="host.docker.internal", port=5000)  # 'serveur' = nom du service docker-compose
    if not cli._connect():
        print("Impossible de se connecter au serveur. Vérifiez qu'il est lancé.")
        return

    try:
        while True:
            print("\n1) Ajouter")
            print("2) Lister")
            print("3) Supprimer")
            print("4) Changer statut")
            print("0) Quitter")
            choix = input("> ").strip()

            if choix == "1":
                titre = input("Titre: ")
                desc = input("Description: ")
                auteur = input("Auteur: ") or "inconnu"
                rep = cli.envoyer({"action": "ADD", "titre": titre, "description": desc, "auteur": auteur})
                print(rep)

            elif choix == "2":
                rep = cli.envoyer({"action": "LIST"})
                if rep and rep.get("status") == "OK":
                    for t in rep["taches"]:
                        print(f"[{t['id']}] {t['titre']} - {t['statut']} (par {t['auteur']})")
                else:
                    print("Aucune tâche")

            elif choix == "3":
                id = input("ID: ")
                if id.isdigit():
                    rep = cli.envoyer({"action": "DEL", "id": int(id)})
                    print(rep)
                else:
                    print("ID invalide")

            elif choix == "4":
                id = input("ID: ")
                st = input("Statut (TODO/DOING/DONE): ")
                if id.isdigit():
                    rep = cli.envoyer({"action": "STATUS", "id": int(id), "statut": st})
                    print(rep)
                else:
                    print("ID invalide")

            elif choix == "0":
                break
            else:
                print("Choix inconnu")
    finally:
        cli.close()

if __name__ == "__main__":
    menu()
