from Class_etat import *

def main():
    print("Debut du programe")

    transition_0 = {"a" : [1],
                    "b" : [0]}

    transition_1 = {"a": [],
                    "b": [1]}
    Etat_0 = Etat(0, transition_0, entry=True)
    Etat_1 = Etat(1, transition_1, exit=True)
    Automate_0 = Automate([Etat_0, Etat_1])

    Automate_0.display_automate()

    Automate_0.complete_automate()
    Automate_0.display_automate()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

