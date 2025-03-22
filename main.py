from Class_etat import *


def user_menu(auto_exists=False):
    print("{+=================== MENU =====================+}")
    print("")
    print("Veuillez choisir une option :")
    print("")
    print("\t1. Créer un automate vide")
    print("\t2. Importer un automate")
    print("\t3. Déterminiser l'automate courant")
    print("\t4. Minimiser l'automate courant")
    print("\t5. Compléter l'automate courant")
    print("\t6. Afficher l'automate courant")
    print("\t7. Standardiser l'automate courant")
    print("\t8. Afficher le complémentaire de l'automate courant")
    print("\t9. Supprimer l'automate courant")
    print("\t10. Quitter")
    print("")
    print("{+==============================================+}")
    print("")

    user_automata = Automata()
    choix = input("Votre choix :")
    while not choix.isdigit() or int(choix) < 1 or int(choix) > 10:
        print("Choix invalide. Veuillez entrer un nombre entre 1 et 10.")
        choix = input("Votre choix :")

    if choix == "1":
        auto_exists = True
        print("")
        print("L'automate a été créé avec succès.")
        print("")
        user_menu(True)

    elif choix == "2":
        id_automate = input("Entrez l'id de l'automate à importer (1-44) :")
        while not id_automate.isdigit() or int(id_automate) < 1 or int(id_automate) > 44:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 44.")
            id_automate = input("Votre choix :")
        user_automata = Automata()
        user_automata.read_automata(id_automate)
        user_automata.remove_epsilon()
        print("")
        print("L'automate a été importé avec succès.")
        print("")
        user_menu(True)

    elif choix == "3":
        if auto_exists:
            user_automata.determinate()
            print("")
            print("L'automate a été déterminisé avec succès.")
            print("")
            user_menu(True)
        else:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()

    elif choix == "4":
        if auto_exists:
            user_automata.minimize()
            print("")
            print("L'automate a été minimisé avec succès.")
            print("")
            user_menu(True)
        else:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()

    elif choix == "5":
        if auto_exists:
            user_automata.complete_automate()
            print("")
            print("L'automate a été complété avec succès.")
            print("")
            user_menu(True)
        else:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()

    elif choix == "6":
        if not auto_exists:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()
        else:
            output = user_automata.display_automate()
            print(output)
            user_menu(True)

    elif choix == "7":
        if auto_exists:
            user_automata.standardise()
            print("")
            print("L'automate a été standardisé avec succès.")
            print("")
            user_menu(True)
        else:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()

    elif choix == "8":
        if auto_exists:
            print("")
            print("Complémentaire de l'automate courant :")
            print("")
            output = user_automata.complementary().display_automate()
            print(output)
            user_menu(True)
        else:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()

    elif choix == "9":
        if not auto_exists:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()
        else:
            user_automata = Automata()
            print("")
            print("L'automate a été supprimé avec succès.")
            print("")
            user_menu()

    elif choix == "10":
        "Fin du programme."
        return


def test_all_files():
    for i in range(1,45):
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



def main():
    print("Debut du programe")

    test_all_files()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

