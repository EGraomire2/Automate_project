from Class_etat import *

def main():
    print("Debut du programe")

    Etat_0 = State(0, entry=True)
    Etat_1 = State(1, exit=True)

    transition_0 = {"a" : [Etat_1],
                    "b" : [Etat_0]}

    transition_1 = {"a": [],
                    "b": [Etat_1]}

    Etat_0.add_transition_dict(transition_0)
    Etat_1.add_transition_dict(transition_1)

    Automate_0 = Automata([Etat_0, Etat_1])
    Automate_0.display_automate()

    Automate_0.complete_automate()
    Automate_0.display_automate()

    Automate_0.standardise()
    Automate_0.display_automate()

    Automate_0.determinate()
    Automate_0.display_automate()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

