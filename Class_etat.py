class Automata:
    def __init__(self, states = [], alphabet=['a', 'b']):
        self.alphabet = alphabet # tableau des composantes de l'alphabet
        self.states = states # tableau contenant tout les etats de l'automate
        self.complete = False
        self.standart = False
        self.determinated = False


    def read_automata(self, automata_id):
        """
        Methode qui permet de lire un automate depuis un fichier txt
        === FORMAT DU FICHIER TXT ===
        le fichier .txt doit faire n+1 ligne avec n le nombre d'états de l'automate
        la première ligne correspond à l'alphabet de l'automate
        les lignes suivantes correspondent au tableau des transitions
        une ligne correspond à un état et ses transitions
        la première colonne correspond au nom de l'état
        les colonnes suivantes à ses transitions
        si l'état est une entrée/sortie, E ou S est renseigné sur la meme ligne après les transitions
        chaque caractère du fichier est séparé d'un espace
        :param automata_id: id de l'automate à créer
        :return:
        """
        # lecture du fichier
        file = open(f"automate_{automata_id}.txt", "r")
        automata = file.readlines()
        file.close()
        alphabet = automata[0].split(" ")
        states = []

        # parcours ligne par ligne
        for i in range(1, len(automata)):
            file_line = automata[i].split(" ")
            transitions = {}
            exit = False
            entry = False

            # parcours caractère par caractère
            for j in range(0, len(alphabet)):
                next_states = []
                # boucle for si plusieurs transitions pour une meme lettre
                for letter in file_line[j+1]:
                    next_states.append(letter)
                transitions[alphabet[j]] = next_states

            # si l'état est une entrée/sortie
            if len(file_line) > len(alphabet)+1:
                for k in range(len(alphabet), len(file_line)):
                    if file_line[k] == "S":
                        exit = True
                    elif file_line[k] == "E":
                        entry = True

            new_state = State(file_line[0], transitions, entry, exit)
            states.append(new_state)

        # Creation automate
        self.alphabet = alphabet
        self.states = states


    def display_automate(self):
        print("\n\n   |  Etat  |\t", end="")
        for letter in self.alphabet:
            print(f"{letter}\t|\t", end="")
        print("\n" + "-" * 29, end="")

        ######## affichage du tableau de transitions #######
        for state in self.states:
            print("\n", end="")

            # affichage des entrées/sorties
            if state.is_entry() and state.is_exit:
                print("E/S", end="")
            elif state.is_entry():
                print("  E", end="")
            elif state.is_exit():
                print("  S", end="")
            else:
                print("   ", end="")

            print(f"|\t{state.id}\t|\t", end="")
            for letter in self.alphabet: # pour chaque lettre de l'alphabet
                for transition in state.transition_dict[letter]: # pour chaque transition associer à cette lettre de l'alphabet
                    print(transition.id, " ", end="") # on affiche la transition dans la case du tableau
                print("\t|\t", end="")

    def complete_automate(self):
        bind = State("P")
        nb_void_transition = 0
        # On remplace tout les transitions vide par une transition vers P la poubelle
        for state in self.states:
            for letter in self.alphabet:
                if len(state.transition_dict[letter]) == 0:
                    nb_void_transition += 1
                    state.transition_dict[letter].append(bind)

        # Dans le cas où l'automate n'était pas déjà complet, on ajoute l'état poubelle :
        if nb_void_transition > 0:
            bind_transition = {}
            for letter in self.alphabet:
                bind_transition[letter] = [bind]
            bind.add_transition_dict(bind_transition)
            self.states.append(bind)

        self.complete = True

    def regroup_entries(self):
        entries = []
        for state in self.states:
            if state.is_entry():
                entries.append(state)
        return entries

    def standardise(self):
        '''Fonction permettant de standardiser un automate'''
        entries = self.regroup_entries()
        is_exit = False
        for state in entries:
            state.entry = False # Les entrées deviennent de simple état
            if state.is_exit():
                is_exit = True

        # Ajout des transitions de l'état d'entrer
        transitions_dict = {}
        for letter in self.alphabet:
            transitions = []  # sous tableau contenant les états
            for state in entries:
                for tran in state.transition_dict[letter]:
                    if tran not in transitions:
                        transitions.append(tran)
            transitions_dict[letter] = transitions

        new_state = State("i", transitions_dict, entry=True, exit=is_exit)
        self.states.insert(0, new_state)

        self.standart = True


    def determinate(self):
        groups = [] # tableau 2D des regroupements d'état
        new_states = []
        groups.append(self.regroup_entries()) # On ajoute le regroupement des entrées
        i = 0
        is_entry = True

        # On parcourt l'ensemble des regroupements d'états jusqu'à les avoir tous traités
        while i < len(groups):
            print(i)
            is_exit = False
            for state in groups[i]:
                if state.is_exit():
                    is_exit = True

            new_state = State(i, entry=is_entry, exit=is_exit)
            new_state_transitions = {}

            for letter in self.alphabet:
                sub_group = [] # sous tableau stockant les etats que l'on souhaite regrouper
                print("\nLettre :", letter)
                for state in groups[i]:
                    print("State : ", state.id)
                    for transition in state.transition_dict[letter]:
                        if transition not in sub_group:
                            sub_group.append(transition)
                if sub_group not in groups:
                    print("On ajoute : subgroup")
                    for l in sub_group:
                        print(l.id, end=" ")
                    groups.append(sub_group)
                    new_state_transitions[letter] = [len(groups) - 1]
                else:
                    j=0
                    while groups[j] != sub_group:
                        j+=1
                    new_state_transitions[letter] = [j]

            new_state.add_transition_dict(new_state_transitions)
            new_states.append(new_state)

                    
            is_entry = False # seul le premier état est une entrée, on remet donc is_entry à False après la première itération de la boucle
            i += 1
            if i > 100: # On limite l'automate standart à 100 états maximum
                print("Fatal Error : Infinite Loop")
                return

            self.states = new_states
            self.determinated = True

class State:
    def __init__(self, id, transition={}, entry=False, exit=False):
        self.id = id
        self.transition_dict = transition # dictionaire de tableaux contenant tous les états vers lesquels il y a une transition
        #attribut : lettre de l'alphabet - clés : tableau d'etat

        self.exit = exit
        self.entry = entry

    def is_entry(self):
        return self.entry

    def is_exit(self):
        return self.exit

    def add_transition_dict(self, transition_dict):
        '''Permet d'ajouter le dictionaire de transition, dans le cas où cela n'ait pas été fait lors de l'initialisation de l'instance de l'objet'''
        self.transition_dict = transition_dict