from Class_etat import *

def main():
    print("Debut du programe")

    state_0 = State(0, entry=True, exit=True)
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
    print(" ")

    Automate_0.complementary().display_automate()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

