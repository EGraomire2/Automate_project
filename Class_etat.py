class Automate:
    def __init__(self, states, alphabet=['a', 'b']):
        self.alphabet = alphabet # tableau des composantes de l'alphabet
        self.states = states # tableau contenant tout les etats de l'automate
        self.complete = False

    def display_automate(self):
        print("\n\n|\tEtat\t|\t", end="")
        for letter in self.alphabet:
            print(f"{letter}\t|\t", end="")

        for state in self.states:
            print(f"\n|\t{state.id}\t|\t", end="")
            for letter in self.alphabet: # pour chaque lettre de l'alphabet
                for transition in state.transition_dict[letter]: # pour chaque transition associer à cette lettre de l'alphabet
                    print(transition, " ", end="") # on affiche la transition dans la case du tableau
                print("\t|\t", end="")

    def complete_automate(self):
        nb_void_transition = 0
        # On remplace tout les transitions vide par une transition vers P la poubelle
        for state in self.states:
            for letter in self.alphabet:
                if len(state.transition_dict[letter]) == 0:
                    nb_void_transition += 1
                    state.transition_dict[letter].append("P")

        # Dans le cas où l'automate n'était pas déjà complet, on ajoute l'état poubelle :
        if nb_void_transition > 0:
            bind_transition = {}
            for letter in self.alphabet:
                bind_transition[letter] = ["P"]
            bind = Etat("P", bind_transition)
            self.states.append(bind)

        self.complete = True

    def regroup_entries(self):
        entries = []
        for state in self.states:
            if state.is_entry():
                entries.append(state)
        return entries

    def determinate(self):
        groups = [] # tableau 2D des regroupements d'état
        new_states = []
        groups.append(self.regroup_entries()) # On ajoute le regroupement des entrées
        i = 0
        is_entry = True

        while i < len(groups):
            is_exit = False
            for state in groups:
                if state.is_exit():
                    is_exit = True

            sub_group = [] # sous tableau contenant les états
            for letter in self.alphabet:
                for state in groups:
                    for transition in state.transition_dict[letter]:
                        sub_group.append(transition)
                if sub_group not in groups:
                    groups.append(sub_group)
                    
            is_entry = False # seul le premier état est une entrée, on remet donc is_entry à False après la première itération de la boucle
            i += 1
            if i > 100: # On limite l'automate standart à 100 états maximum
                i = 100000

class Etat:
    def __init__(self, id, transition={}, entry=False, exit=False):
        self.id = id
        self.transition_dict = transition # dictionaire de tableaux contenant toutes les transitions pour chaque lettre de l'alphabet
        self.entry = entry
        self.exit = exit

    def is_entry(self):
        return self.entry

    def is_exit(self):
        return self.exit