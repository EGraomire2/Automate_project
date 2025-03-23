import os
import copy
from Class_etat import *


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


def test_automata(automata_id):

    output = "===================================\n"
    output+= "\t Etude de l'Automate "+str(automata_id)+" : \t\n"
    output+= "===================================\n"

    automate_0 = Automata()
    automate_0.read_automata(automata_id)
    automate_0.remove_epsilon()

    output += "------------------------------------------\n"
    output += "\tAffichage de l'automate initial :\t\n"
    output += "------------------------------------------\n"

    disp1 = automate_0.display_automate()
    output += disp1 + "\n"

    output+="\tStandardisation de l'automate :\n"
    output+="----------------------------------------\n"
    automate_0_copy = copy.copy(automate_0)
    automate_0_copy.standardise()
    output+="----------------------------------------\n"
    output+="\tL'automate est standardisé, affichage : \n"

    disp3 = automate_0_copy.display_automate()
    output+= disp3 + "\n"

    output += "\tComplémentaire de l'automate :\n"
    output += "----------------------------------------\n"
    automate_1_copy = copy.copy(automate_0)
    automate_1_copy.complementary()
    output += "----------------------------------------\n"
    output += "\taffichage de l'automate complémentaire: \n"

    disp3 = automate_1_copy.display_automate()
    output += disp3 + "\n"

    if automate_0.determinated :
        output+="\tL'automate est déterministe.\n"
    else:
        output+="\tDéterminisation de l'automate :\n"
        output+="----------------------------------------\n"
        automate_0.determinate()
        output+="----------------------------------------\n"
        output+="\tL'automate est déterminisé, affichage : \n"

        disp3 = automate_0.display_automate()
        output+= disp3 + "\n"

    if automate_0.complete:
        output+="L'automate est complet.\n"
    else:

        output+="\tComplétion de l'automate :\n"
        output+="----------------------------------------\n"
        automate_0.complete_automate()
        output+="----------------------------------------\n"
        output+="\tL'automate est complété, affichage : \n"

        disp2= automate_0.display_automate()
        output += disp2 + "\n"

    output+="\tMinimisation de l'automate :\n"
    output+="----------------------------------------\n"
    automate_1 = automate_0.minimize()[0]

    output+="----------------------------------------\n"
    output+="\tL'automate est minimisé, affichage :\n"

    disp4 = automate_1.display_automate()
    output+= disp4 + "\n"

    return output


def create_trace_file():
    if not os.path.exists('traces'):
        os.mkdir('traces')

    for i in range(1,45):
        result = test_automata(i)
        with open(f'traces/traceautomate{i}.txt', 'w') as f:
            f.write(result)


def main():
    print("Debut du programe")

    create_trace_file()

    user_menu()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

