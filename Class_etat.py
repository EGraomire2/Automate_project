class Automata:
    def __init__(self, states = [], alphabet=['a', 'b']):
        self.alphabet = alphabet # tableau des composantes de l'alphabet
        self.states = states # tableau contenant tout les etats de l'automate
        self.complete = False
        self.standart = False
        self.determinated = False


    def read_automata(self, automata_id : str):
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
        chaque caractère du fichier est séparé d'une ","
        :param automata_id: id de l'automate à créer
        :return:
        """
        # lecture du fichier
        file = open(f"Automates/automate_{automata_id}.txt", "r")
        automata = file.readlines()
        file.close()
        alphabet = automata[0].replace("\n", "")
        alphabet = alphabet.split(",")
        if alphabet == ['']:
            alphabet = []
        states_list = []

        # parcours ligne par ligne
        for i in range(1, len(automata)):
            file_line = automata[i].replace("\n","").split(",")
            transitions = {}
            exit = False
            entry = False

            state_in_states_list = False

            # parcours du tableau de transition caractère par caractère
            for j in range(0, len(alphabet)):
                next_states_list = []

                next_state_in_list = False

                # boucle pour gérer si plusieurs états pour une même transition (non déterministe)
                for letter in file_line[j+1].replace("\n", "").split("/"):
                    if letter == "-":
                        next_state = State("")
                    else :
                        next_state = State(letter)

                    # vérification si l'état de transition est déjà renseigné dans l'automate
                    for state in states_list:
                        if state.id == letter:
                            next_state = state
                            next_state_in_list = True

                    # si l'état de transition n'est pas renseigné dans la liste d'états, on le rajoute
                    if next_state_in_list == False and next_state.id != "":
                        next_state = State(letter)
                        states_list.append(next_state)

                    if next_state.id != "":
                        next_states_list.append(next_state)

                transitions[alphabet[j]] = next_states_list

            print(file_line)
            # si l'état est une entrée/sortie
            if len(file_line) > len(alphabet):

                print("entrée/sortie pour l'id ")
                for k in range(len(alphabet), len(file_line)):
                    if file_line[k] == "S":
                        exit = True
                    elif file_line[k] == "E":
                        entry = True

            new_state = State(file_line[0], transitions, entry, exit)

            # vérification si l'état (colonne état) est dans la liste d'états de l'automate
            for state in states_list:
                if state.id == new_state.id:
                    state.transition_dict = transitions
                    state.exit = exit
                    state.entry = entry
                    state_in_states_list = True
            if state_in_states_list == False:
                print("ajout de l'état ", new_state.id)
                states_list.append(new_state)

        # Creation automateùj
        
        self.alphabet = alphabet
        self.states = states_list



    def display_automate(self):
        # utilisation de la méthode ljust qui permet de faire un alignemetn
        if self.alphabet == ['']:
            print("Pas d'alphabet")
            return

        col = 10
        table_w = (col + 5) * (len(self.alphabet) + 1) + 1

        print("\n\n\t  |\t\tEtat  ".ljust(col + 5), " |", end="")

        for letter in self.alphabet:
            print(f"    {letter}".ljust(col), "|", end="")
        print()

        print("-" * table_w)

        ######## affichage du tableau de transitions #######
        for state in self.states:
            # affichage des entrées/sorties
            if state.is_entry() and state.is_exit:
                print("E/S".ljust(5), end="")
            elif state.is_entry():
                print("  E".ljust(5), end="")
            elif state.is_exit():
                print("  S".ljust(5), end="")
            else:
                print("   ".ljust(5), end="")

            print(f" |\t     {state.id} ".ljust(col + 5), "|", end="")

            for letter in self.alphabet:  # pour chaque lettre de l'alphabet
                transitions = []

                for transition in state.transition_dict[
                    letter]:  # pour chaque transition associer à cette lettre de l'alphabet
                    transitions.append(str(transition.id))
                print(" ".join(transitions).center(col), "|", end="")
            print()

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
        for state in self.states:
            print(f"State : {state.id} - transitions en a : {state.transition_dict['a']}")

        groups = [] # tableau 2D des regroupements d'état
        new_states = []
        groups.append(self.regroup_entries()) # On ajoute le regroupement des entrées
        new_entry = State(0, entry=True)
        new_states.append(new_entry)
        i = 0

        # On parcourt l'ensemble des regroupements d'états jusqu'à les avoir tous traités
        while i < len(groups):
            print(i)
            for state in groups[i]:
                if state.is_exit():
                    new_states[i].exit = True

            new_state_transitions = {}

            for letter in self.alphabet:
                sub_group = [] # sous tableau stockant les etats que l'on souhaite regrouper
                print("\nLettre :", letter)
                print("Taille de groups : ", len(groups))
                for state in groups[i]:
                    print("State : ", state.id)
                    for transition in state.transition_dict[letter]:
                        if transition not in sub_group:
                            sub_group.append(transition)
                if sub_group not in groups and sub_group != []:
                    print("On ajoute un sub_group :", end="")
                    for l in sub_group:
                        print(l.id, end=" ")
                    groups.append(sub_group)
                    new_states.append(State(len(groups) - 1))
                    new_state_transitions[letter] = [new_states[len(new_states) - 1]]
                elif sub_group != []:
                    j=0
                    while groups[j] != sub_group:
                        j+=1
                    new_state_transitions[letter] = [new_states[j]]
                else:
                    new_state_transitions[letter] = []

            new_states[i].add_transition_dict(new_state_transitions)

            i += 1
            if i > 100: # On limite l'automate standart à 100 états maximum
                print("Fatal Error : Infinite Loop")
                return

            # Display subgroups :
            print("\n\n")
            for sub in groups:
                print("")
                for let in sub:
                    print(let.id, end=".")

            self.states = new_states
            self.determinated = True


    def minimize(self):
        if not self.determinated:
            print("Automate non déterministe. Déterminisation en cours...")
            self.determinate()

        if not self.complete:
            print("Automate incomplet. Complétion en cours...")
            self.complete_automate()

        finals = [state for state in self.states if state.exit]
        non_finals = [state for state in self.states if not state.exit]

        partition_courante = {}
        if finals:
            partition_courante['T'] = finals
        if non_finals:
            partition_courante['NT'] = non_finals

        print(f"\nPartition n°0 :")
        for label, groupe in partition_courante.items():
            print(f"{label} : {[state.id for state in groupe]}")

        partition_suivante = None
        iteration = 0
        compteur_T = 1
        compteur_NT = 1
        correspondance_etats = {}

        while partition_courante != partition_suivante:
            iteration += 1

            if iteration > 1:
                partition_courante = partition_suivante.copy()

            partition_suivante = {}
            print(f"\nItération {iteration}:")

            for label, groupe in partition_courante.items():
                if len(groupe) == 1:
                    partition_suivante[label] = groupe
                    continue

                signatures = {}

                for etat in groupe:
                    signature = []

                    for letter in self.alphabet:
                        etat_cible = etat.transition_dict[letter][0]

                        label_cible = None
                        for lbl, etats_partition in partition_courante.items():
                            if etat_cible in etats_partition:
                                label_cible = lbl
                                break

                        signature.append(label_cible)

                    signature_tuple = tuple(signature)
                    if signature_tuple not in signatures:
                        signatures[signature_tuple] = []
                    signatures[signature_tuple].append(etat)

                if len(signatures) == 1:
                    partition_suivante[label] = groupe
                else:
                    for signature_tuple, sous_groupe in signatures.items():
                        est_terminal = any(state.exit for state in sous_groupe)

                        if est_terminal:
                            nouveau_label = f"T{compteur_T}"
                            compteur_T += 1
                        else:
                            nouveau_label = f"NT{compteur_NT}"
                            compteur_NT += 1

                        partition_suivante[nouveau_label] = sous_groupe

            print("Nouvelle partition:")
            for label, groupe in partition_suivante.items():
                print(f"{label} : {[state.id for state in groupe]}")

            print("\nTransitions en termes de parties:")
            for label, groupe in partition_suivante.items():
                etat_representant = groupe[0]
                print(f"Pour le groupe {label}:")
                for letter in self.alphabet:
                    etat_cible = etat_representant.transition_dict[letter][0]

                    groupe_cible = None
                    for lbl, grp in partition_suivante.items():
                        if etat_cible in grp:
                            groupe_cible = lbl
                            break
                    print(f"  {letter} -> {groupe_cible}")

        if iteration == 1 and len(partition_suivante) == len(self.states):
            print("\nAutomate déjà minimal.")
            return self, correspondance_etats

        print(f"\nAutomate minimal obtenu après {iteration} itérations")

        automate_minimal = Automata(alphabet=self.alphabet.copy())
        automate_minimal.complete = True
        automate_minimal.determinated = True
        automate_minimal.minimal = True

        etats_minimaux = []
        for label, groupe in partition_suivante.items():
            est_terminal = any(state.exit for state in groupe)
            est_initial = any(state.entry for state in groupe)

            transitions_vides = {letter: [] for letter in self.alphabet}

            nouvel_etat = State(label, transitions_vides, entry=est_initial, exit=est_terminal)
            etats_minimaux.append(nouvel_etat)

            correspondance_etats[label] = [state.id for state in groupe]

        for nouvel_etat in etats_minimaux:
            label = nouvel_etat.id
            groupe = partition_suivante[label]
            etat_representant = groupe[0]

            for letter in self.alphabet:
                etat_cible = etat_representant.transition_dict[letter][0]

                label_cible = None
                for lbl, groupe_cible in partition_suivante.items():
                    if etat_cible in groupe_cible:
                        label_cible = lbl
                        break

                # Utilisation d'une boucle standard au lieu de next()
                nouvel_etat_cible = None
                for etat in etats_minimaux:
                    if etat.id == label_cible:
                        nouvel_etat_cible = etat
                        break

                nouvel_etat.transition_dict[letter] = [nouvel_etat_cible]

        automate_minimal.states = etats_minimaux

        return automate_minimal, correspondance_etats


    def complementary(self): #Retourne l'automate complémentaire de l'automate courant.

        #On s'assure que l'automate est complet et déterministe :
        if not self.determinated:
            print("Automate non déterministe. Détermination en cours...")
            self.determinate()

        if not self.complete:
            print("Automate non complet. Complétion en cours...")
            self.complete_automate()

        comp_automata = self

        #On échange les sorties et non-sorties :
        for i in range(len(comp_automata.states)):
            if comp_automata.states[i].is_exit():
                comp_automata.states[i].exit = False
            else:
                comp_automata.states[i].exit = True

        return comp_automata


    def remove_epsilon(self):
        if "e" not in self.alphabet:
            return 0
        for state in self.states:
            print("nv tour")
            if state.transition_dict["e"] != []:
                for next_state_e in state.transition_dict["e"]:
                    if next_state_e.is_exit():
                        state.exit = True
                    if next_state_e.is_entry():
                        state.entry = True

                    print(state.id , "etat : ", next_state_e.id)
                    for letter in self.alphabet:
                        print(state.transition_dict)
                        for transition_next_state in next_state_e.transition_dict[letter]:
                            state.transition_dict[letter].append(transition_next_state)
        for state in self.states:
            del state.transition_dict["e"]
        self.alphabet.pop()





class State:
    def __init__(self, id, transition={}, entry=False, exit=False):
        self.id = id
        self.transition_dict = transition # dictionaire de tableaux contenant tous les états vers lesquels il y a une transition
        #attribut : lettre de l'alphabet - clés : tableau d'etat
        # S'il n'y a aucune transition pour une lettre alors attribué à la lettre le tableau vide ; exemple : self.transition_dict['a'] = []

        self.exit = exit
        self.entry = entry

    def is_entry(self):
        return self.entry

    def is_exit(self):
        return self.exit

    def add_transition_dict(self, transition_dict):
        '''Permet d'ajouter le dictionaire de transition, dans le cas où cela n'ait pas été fait lors de l'initialisation de l'instance de l'objet'''
        self.transition_dict = transition_dict