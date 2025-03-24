class Automata:
    def __init__(self, states = [], alphabet=[]):
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
            exit = False
            entry = False

            # si l'état est une entrée/sortie
            if len(file_line) > len(alphabet):

                for k in range(len(alphabet), len(file_line)):
                    if file_line[k] == "S":
                        exit = True
                    elif file_line[k] == "E":
                        entry = True

            new_state = State(file_line[0], {}, entry, exit)

            states_list.append(new_state)

        # Creation automateùj
        self.alphabet = alphabet
        self.states = states_list

        for i in range(1,len(automata)):
            transition = {}
            file_line = automata[i].replace("\n", "").split(",")

            # remplissage des transitions
            for j in range(1,len(alphabet)+1):
                next_states_id_list = file_line[j].split("/")

                transition[alphabet[j-1]] = []

                # ajout de l'objet état stocké dans la liste d'états à la transition de l'état courant
                for next_state_id in next_states_id_list:
                    for state_object in self.states:
                        if next_state_id == state_object.id:
                            transition[alphabet[j-1]].append(state_object)

            # ajout de la transition à l'état courant
            self.states[i-1].transition_dict = transition



    def display_automate(self):
        # Initialisation de la variable de sortie
        output = ""

        # utilisation de la méthode ljust qui permet de faire un alignement
        col = 10
        table_w = (col + 5) * (len(self.alphabet) + 1) + 1

        output += "\n\n\t  |\t\tEtat  ".ljust(col + 5) + " |"

        for letter in self.alphabet:
            output += f"    {letter}".ljust(col) + "|"
        output += "\n"

        output += "-" * table_w + "\n"

        ######## affichage du tableau de transitions #######
        for state in self.states:
            # affichage des entrées/sorties
            if state.is_entry() and state.is_exit():
                output += "E/S".ljust(5)
            elif state.is_entry():
                output += "  E".ljust(5)
            elif state.is_exit():
                output += "  S".ljust(5)
            else:
                output += "   ".ljust(5)

            output += f" |\t     {state.id} ".ljust(col + 5) + "|"

            for letter in self.alphabet:  # pour chaque lettre de l'alphabet
                transitions = []

                for transition in state.transition_dict[
                    letter]:  # pour chaque transition associer à cette lettre de l'alphabet
                    transitions.append(str(transition.id))
                output += " ".join(transitions).center(col) + "|"
            output += "\n"

        # Retourner la chaîne de caractères ou l'afficher selon le besoin
        return output



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
        if not self.determinated:
            if self.alphabet == []:
                return

            groups = [] # tableau 2D des regroupements d'état
            new_states = []
            groups.append(self.regroup_entries()) # On ajoute le regroupement des entrées
            new_entry = State(0, entry=True)
            new_states.append(new_entry)
            i = 0

            # On parcourt l'ensemble des regroupements d'états jusqu'à les avoir tous traités
            while i < len(groups):
                for state in groups[i]:
                    if state.is_exit():
                        new_states[i].exit = True

                new_state_transitions = {}

                for letter in self.alphabet:
                    sub_group = [] # sous tableau stockant les etats que l'on souhaite regrouper

                    for state in groups[i]:

                        for transition in state.transition_dict[letter]:
                            if transition not in sub_group:
                                sub_group.append(transition)
                    if sub_group not in groups and sub_group != []:

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
                    return

                self.states = new_states
                self.determinated = True

    def minimize(self):
        # Liste pour stocker les messages d'affichage
        output_lines = []

        # Étape 0: Vérification des prérequis
        if self.alphabet == []:
            output_lines.append("Alphabet vide, impossible de minimiser l'automate.")
            return self, {}, output_lines

        if not self.determinated:
            output_lines.append("Automate non déterministe. Déterminisation en cours...")
            self.determinate()

        if not self.complete:
            output_lines.append("Automate incomplet. Complétion en cours...")
            self.complete_automate()

        # Étape 1: Création de la partition initiale T/NT
        finals = [state for state in self.states if state.exit]
        non_finals = [state for state in self.states if not state.exit]

        partition_courante = {}
        if finals:
            partition_courante['T'] = finals
        if non_finals:
            partition_courante['NT'] = non_finals

        output_lines.append(f"\nDébut minimisation : Partition n°0 :")
        for label, groupe in partition_courante.items():
            output_lines.append(f"{label} : {[state.id for state in groupe]}")

        # Étape 2: Initialisation pour l'algorithme de raffinement
        partition_suivante = None
        iteration = 0
        compteur_T = 1
        compteur_NT = 1
        correspondance_etats = {}

        # Étape 3: Raffinement itératif des partitions
        while partition_courante != partition_suivante:
            iteration += 1

            if iteration > 1:
                partition_courante = partition_suivante.copy()

            partition_suivante = {}
            output_lines.append(f"\nItération {iteration}:")

            # Pour chaque groupe de la partition courante
            for label, groupe in partition_courante.items():
                # Optimisation: les groupes isolés (un seul état) sont déjà minimaux
                if len(groupe) == 1:
                    partition_suivante[label] = groupe
                    continue

                signatures = {}

                # Calcul des signatures pour chaque état du groupe
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

                    # Regroupement des états par signature
                    signature_tuple = tuple(signature)
                    if signature_tuple not in signatures:
                        signatures[signature_tuple] = []
                    signatures[signature_tuple].append(etat)

                # Création des nouveaux groupes selon les signatures
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

            # Affichage de la nouvelle partition
            output_lines.append("Nouvelle partition:")
            for label, groupe in partition_suivante.items():
                output_lines.append(f"{label} : {[state.id for state in groupe]}")

            # Affichage des transitions entre groupes
            output_lines.append("\nTransitions en termes de parties:")
            for label, groupe in partition_suivante.items():
                etat_representant = groupe[0]
                output_lines.append(f"Pour le groupe {label}:")
                for letter in self.alphabet:
                    etat_cible = etat_representant.transition_dict[letter][0]

                    groupe_cible = None
                    for lbl, grp in partition_suivante.items():
                        if etat_cible in grp:
                            groupe_cible = lbl
                            break
                    output_lines.append(f"  {letter} -> {groupe_cible}")

        # Étape 4: Vérification si l'automate était déjà minimal
        if iteration == 1 and len(partition_suivante) == len(self.states):
            output_lines.append("\nAutomate déjà minimal.")
            return self, correspondance_etats, output_lines

        output_lines.append(f"\nAutomate minimal obtenu après {iteration} itérations")

        # Étape 5: Construction de l'automate minimal
        automate_minimal = Automata(alphabet=self.alphabet.copy())
        automate_minimal.complete = True
        automate_minimal.determinated = True
        automate_minimal.minimal = True

        # Création des nouveaux états
        etats_minimaux = []
        for label, groupe in partition_suivante.items():
            est_terminal = any(state.exit for state in groupe)
            est_initial = any(state.entry for state in groupe)

            transitions_vides = {letter: [] for letter in self.alphabet}

            nouvel_etat = State(label, transitions_vides, entry=est_initial, exit=est_terminal)
            etats_minimaux.append(nouvel_etat)

            correspondance_etats[label] = [state.id for state in groupe]

        # Définition des transitions entre nouveaux états
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

                nouvel_etat_cible = None
                for etat in etats_minimaux:
                    if etat.id == label_cible:
                        nouvel_etat_cible = etat
                        break

                nouvel_etat.transition_dict[letter] = [nouvel_etat_cible]

        automate_minimal.states = etats_minimaux

        return automate_minimal, correspondance_etats, output_lines

    @staticmethod
    def afficher_automate_minimal(AFDCM, correspondance_etats):
        """
        Affiche l'automate minimal et sa table de correspondance.

        Args:
            AFDCM: L'automate minimal obtenu après minimisation
            correspondance_etats: Dictionnaire mappant les états minimaux aux états originaux
        """
        print("\n=== AUTOMATE MINIMAL ===")
        AFDCM.display_automate()

        print("\n=== TABLE DE CORRESPONDANCE ===")
        print("État minimal(nouveau)-> États originaux (anciens) ")
        print("-" * 40)

        for etat_minimal, etats_originaux in correspondance_etats.items():
            etats_str = " - ".join(etats_originaux)
            print(f"{etat_minimal} -> {etats_str}")


    def complementary(self): #Retourne l'automate complémentaire de l'automate courant.

        comp_automata = self

        if not comp_automata.complete:
            comp_automata.complete_automate()
        if not comp_automata.determinated:
            comp_automata.determinate()

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
            if state.transition_dict["e"] != []:
                for next_state_e in state.transition_dict["e"]:
                    if next_state_e.is_exit():
                        state.exit = True
                    if next_state_e.is_entry():
                        state.entry = True


                    for letter in self.alphabet:
                        for transition_next_state in next_state_e.transition_dict[letter]:
                            state.transition_dict[letter].append(transition_next_state)

        for state in self.states:
            if "e" in state.transition_dict:
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