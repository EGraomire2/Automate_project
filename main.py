from Class_etat import *

def test_automata(automata_id):

    print("===================================")
    print("\t Etude de l'Automate "+automata_id+" : \t")
    print("===================================")

    automate_0 = Automata()
    automate_0.read_automata(automata_id)
    automate_0.remove_epsilon()

    print("------------------------------------------")
    print("\tAffichage de l'automate initial :\t")
    print("------------------------------------------")

    automate_0.display_automate()

    if automate_0.complete:
        print("L'automate est complet.")
    else:

        print("\tComplétion de l'automate :")
        print("----------------------------------------")
        automate_0.complete_automate()
        print("----------------------------------------")
        print("\tL'automate est complété, affichage : ")
        automate_0.display_automate()

    if automate_0.determinated :
        print("\tL'automate est déterministe.")
    else:
        print("\tDéterminisation de l'automate :")
        print("----------------------------------------")
        automate_0.determinate()
        print("----------------------------------------")
        print("\tL'automate est déterminisé, affichage : ")
        automate_0.display_automate()

    print("\tMinimisation de l'automate :")
    print("----------------------------------------")
    automate_0.minimize()
    print("----------------------------------------")
    print("\tL'automate est minimisé, affichage :")
    automate_0.display_automate()

def user_menu(auto_exists=False, user_automata=Automata(), minimized=False):
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

    choix = input("Votre choix :")
    while not choix.isdigit() or int(choix) < 1 or int(choix) > 10:
        print("Choix invalide. Veuillez entrer un nombre entre 1 et 10.")
        choix = input("Votre choix :")

    if choix == "1":
        auto_exists = True
        print("")
        print("L'automate a été créé avec succès.")
        print("")
        user_menu(True, user_automata)

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
        user_menu(True, user_automata)

    elif choix == "3":
        if auto_exists:
            user_automata.determinate()
            print("")
            print("L'automate a été déterminisé avec succès.")
            print("")
            if minimized:
                user_menu(True, user_automata, True)
            user_menu(True, user_automata)
        else:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()

    elif choix == "4":
        if auto_exists:
            user_automata = user_automata.minimize()[0]
            minimized = True
            print("")
            print("L'automate a été minimisé avec succès.")
            print("")
            if minimized:
                user_menu(True, user_automata, True)
            user_menu(True, user_automata)
        else:
            print("")
            print("Aucun automate créé. Veuillez en créer un.")
            print("")
            user_menu()

    elif choix == "5":
        if auto_exists:
            if not user_automata.complete:
                user_automata.complete_automate()
                print("")
                print("L'automate a été complété avec succès.")
                print("")
                user_menu(True, user_automata)
            else:
                print("")
                print("L'automate est déjà complet.")
                print("")
                if minimized:
                    user_menu(True, user_automata, True)
                user_menu(True, user_automata)
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
            if minimized:
                print(user_automata.complementary().complementary().display_automate())
                user_menu(True, user_automata, True)
                #appel de la fonction afficher_minimisé
            print(user_automata.display_automate())
            user_menu(True, user_automata)

    elif choix == "7":
        if auto_exists:
            user_automata.standardise()
            print("")
            print("L'automate a été standardisé avec succès.")
            print("")
            user_menu(True, user_automata)
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
            print(user_automata.complementary().display_automate())
            user_menu(True, user_automata)
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
            print("")
            print("L'automate a été supprimé avec succès.")
            print("")
            user_menu()

    elif choix == "10":
        "Fin du programme."
        return

def main():
    user_menu()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
