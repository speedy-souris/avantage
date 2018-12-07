"""this module contains the test method to find out
if the database is empty when starting the script
and fill it if necessary with the local JSON data
no need for an internet connection to test the script"""

# ! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time

from db_processing import contained_database as insert_data


# +----------------------+
# |         CHECK        |
# |      DATA DISPLAY    |
# +----------------------+
def check_data(db_con):

    """test module at the first start of the script
        if the database is empty
        data filling with local JSON data (JSON file)

    Args:
        db_con         ==> link to the database

    Vars:
        selection      ==> memorization name category and local link
                            JSON data (JSON file)

    Funcs:
        contained_database() alias insert_data ==> module containing
                                                    the product characteristics
                                                    see more detail
                                                    in the module itself

    Queries:
        sql_verif      ==> SQL query that selects the total number
                            of data in the product and category tables"""

    # product selection (format json)
    selection = [
        ["Boissons_energetiques", "boissons_energie.json"],
        ["Bonbons", "bonbons.json"],
        ["Charcuteries", "charcuteries.json"],
        ["Chocolats", "chocolats.json"],
        ["Conserves", "conserves.json"],
        ["Fromages", "fromages.json"],
        ["Fruits", "fruits.json"],
        ["Fruits_confits", "fruits_confits.json"],
        ["Gateaux", "gateaux.json"],
        ["Glaces", "glaces.json"],
        ["Jus_de_fruits", "jus_fruits.json"],
        ["Laits", "laits.json"],
        ["Pates_de_fruit", "pate_fruits.json"],
        ["Pates", "pates.json"],
        ["Pates_a_tartiner", "pates_tartiner.json"],
        ["Pizzas", "pizzas.json"],
        ["Poissons", "poissons.json"],
        ["Poissons_elevages", "poissons_elevage.json"],
        ["Reglisse", "reglisses.json"],
        ["Riz", "riz.json"],
        ["Sorbets", "sorbets.json"],
        ["Viandes", "viandes.json"],
        ["Vins", "vins.json"],
        ["Yaourts", "yaourts.json"],
    ]

    # verification of data in the database
    dbase = db_con
    cursor = dbase.cursor()

    sql_verif = """SELECT COUNT(*)
                FROM product, category"""

    cursor.execute(sql_verif)

    print("Verification de la base de donnée...")
    print()
    for nb_product in cursor:

        # if the product table and the category table are empty
        # insert local JSON data
        if nb_product[0] == 0:
            for prod_elt in selection:
                insert_data("json/" + prod_elt[1], prod_elt[0], db_con)
        else:
            time.sleep(1)

    cursor.close()

    print("Verification terminé")
    print()
    time.sleep(1)
    os.system("clear")
    return selection


# +---------------------+
# |       recall        |
# |    for no choice    |
# +---------------------+
def recall_choice():

    """displays error message due to no choice made
    and restarts the request for choice"""

    os.system("clear")
    print()
    print("Faites un choix")
    time.sleep(1.3)
    os.system("clear")


# +-------------------------+
# |        recall           |
# |    for number choice    |
# +-------------------------+
def recall_nb():

    """displays an error message following a non-numeric choice
    and restarts the request for choice"""

    os.system("clear")
    print()
    print("Choississez un NOMBRE !")
    time.sleep(1.3)
    os.system("clear")


# +---------------------------+
# |         recall            |
# |    for choice exceeded    |
# +---------------------------+
def recall_val(m_val):

    """displays error message following a choice that exceeds the list limit
    and triggers the request for choice"""

    os.system("clear")
    print()
    print(os.system("clear"))
    print(f"Le produit DOIT ÊTRE COMPRIS ENTRE 1 ET {m_val}")
    time.sleep(1.3)
    os.system("clear")


# +------------------------+
# |        recall          |
# |    for wrong choice    |
# +------------------------+
def recall_chosen():

    """displays error message following erroneous choice
    and restarts the request for choice"""

    os.system("clear")
    print("VOUS DEVEZ CHOISIR 'o' OU 'n'")
    time.sleep(1.3)
    os.system("clear")
