class Tache:
    def __init__(self, id, titre, description, auteur, statut="TODO"):
        self.id = id
        self.titre = titre
        self.description = description
        self.auteur = auteur
        self.statut = statut

    def __str__(self):
        return f"[{self.id}] {self.titre} - {self.statut} (par {self.auteur})"

    def to_dict(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "auteur": self.auteur,
            "statut": self.statut
        }
