from Class_etat import *

def main():
    print("Debut du programe")

    '''state_0 = State(0, entry=True, exit=True)
    state_1 = State(1, entry=True)
    state_2 = State(2, exit=True)

    transition_0 = {"a" : [],
                    "b" : [state_1, state_2]}

    transition_1 = {"a": [state_0, state_2],
                    "b": [state_2]}

    transition_2 = {"a": [state_0],
                    "b": []}

    state_0.add_transition_dict(transition_0)
    state_1.add_transition_dict(transition_1)
    state_2.add_transition_dict(transition_2)

    Automate_0 = Automata([state_0, state_1, state_2])
    Automate_0.display_automate()

    Automate_0.determinate()
    Automate_0.display_automate()

    Automate_0.complete_automate()
    Automate_0.display_automate()

    print(" ")
    print("Automate initial : ")
    print(" ")

    Automate_0.standardise()
    Automate_0.display_automate()

    print(" ")
    print("Automate complémentaire : ")
    print(" ")'''



    for i in range(1,21):
        print("\n\n===========================================")
        print(f"             AUTOMATE {i}                  ")
        print("===========================================\n\n")
        Automate_0 = Automata()
        Automate_0.read_automata(f'{i}')
        print("\n\n___________________________________")
        for state in Automate_0.states:
            print(">>> affichage de l'état : ", state.id, " ref @ ", state, " -> ", state.transition_dict)
            print("\t is exit : ", state.is_exit())
            print("\t is entry : ", state.is_entry())
        print("\n\n___________________________________\n\n")

        print(">>> REMOVE EPSILON")
        Automate_0.remove_epsilon()
        Automate_0.display_automate()

        print("\n\n___________________________________")
        for state in Automate_0.states:
            print(">>> affichage de l'état : ", state.id, " ref @ ", state, " -> ", state.transition_dict)
            print("\t is exit : ", state.is_exit())
            print("\t is entry : ", state.is_entry())
        print("\n\n___________________________________\n\n")

        print(">>> DETERMINIZE")
        Automate_0.determinate()
        Automate_0.display_automate()

        print(">>> COMPLETE")
        Automate_0.complete_automate()
        Automate_0.display_automate()

        print(">>> MINIMIZE")
        Automate_1 = Automata()
        Automate_1 = Automate_0.minimize()[0]
        Automate_1.display_automate()
        #Automate_1.afficher_automate_minimal(Automate_1, Automate_0.minimize()[1])
        del Automate_0
        del Automate_1

    '''Automate_0 = Automata()
    Automate_0.read_automata("7")
    Automate_0.display_automate()'''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

