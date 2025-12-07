from tache import Tache

class GestionnaireTaches:
    def __init__(self):
        self.taches = []
        self.next_id = 1

    def ajouter_tache(self, titre, description, auteur):
        t = Tache(self.next_id, titre, description, auteur)
        self.taches.append(t)
        self.next_id += 1
        return t

    def lister_taches(self):
        return self.taches

    def supprimer_tache(self, id):
        for t in self.taches:
            if t.id == id:
                self.taches.remove(t)
                return True
        return False

    def changer_statut(self, id, statut):
        for t in self.taches:
            if t.id == id:
                t.statut = statut
                return True
        return False
