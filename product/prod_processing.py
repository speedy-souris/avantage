"""module containing all product management"""

#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import time

from db_processing import backup_product as b_product
from db_processing import contained_database as insert_data
from db_processing import erase_data as erase_db
from db_processing import update_database as url_insert


# +--------------+
# |   DISPLAY    |
# |    MENU      |
# |   CATEGORY   |
# +--------------+
def menu_category(d_json):

    """product category menu display module
    Args:
        d_json       ==> memorization of the name
                            of the product category"""

    # display of the product category menu
    print("Menu de Catégorie Produit (OpenFoodFact)")
    print("==== == ========= =======")
    print()
    for i, elt in enumerate(d_json):
        print(f"{i+1}. {elt[0]}")


# +---------------------------+
# |  MENU PRODUCT AND SELECT  |
# |  PRODUCTS AND CATEGORIES  |
# |      INTO THE DATABASE    |
# +---------------------------+
def select_prod(d_json, cat_name, cat_id, db_con, select=""):

    """module allowing the display of the product menu
    according to the chosen category display of products
    according to the chosen category
    with the function substitutes_display ()
                    and
    backup of the chosen substitute product in the database
    with the function backup_product () alias b_product

    Args:
        d_json         ==> memorizing the name of the products
                            contained in the JSON data

        cat_name       ==> storage of the product category name

        cat_id         ==> memorization of the id
                            of the chosen product category

        db_con         ==> link to the database

        select         ==> memorization of the acceptance of the product choice
                            for a reminder of this module
                            after a bad choice on the list of products

    Vars:
        product_list[] ==> memorization of substitute products

    Funcs:
        choice()       ==> internal function concerning the product management
                            see detail in the function itself

        continuity()   ==> module of choice
                            for continuing or stopping the script

    Queries:
            sql_prod   ==> SQL query that selects the products
                            from the database that are
                            in the chosen category"""

    dbase = db_con
    cursor = dbase.cursor()

    print()
    print("menu produit de la categorie", cat_name.upper())
    print("==== ======= == == =========")
    print()

    sql_prod = """SELECT p.name as nom_produit,
        p.description as description_produit,
        p.nutrition_grade as grade_nutritionnel,
        p.url as url_produit,
        p.store as magasin
    FROM product as p
    INNER JOIN category_product as cp
        ON p.id = cp.product_id
    INNER JOIN category as c
        ON c.id = cp.category_id
    WHERE
        c.category = %(cat_name)s"""

    cursor.execute(sql_prod, {"cat_name": cat_name})

    # menu of products of the chosen category
    nb_product = 0
    product_list = []
    for i, product_name in enumerate(cursor):
        print(f"{i+1}. {product_name[0]}")
        nb_product = i + 1
        product_list.append(product_name)

    if product_list is not():
        return None

    # product choice request
    print()
    if select == "":
        while True:
            selection = input(
                "Voulez vous choisir une produit (Oui /Non) : "
            )
            # bad choice
            if selection not in "on":
                os.system("clear")
                print("VOUS DEVEZ CHOISIR 'o' OU 'n'")
                time.sleep(1.7)
                os.system("clear")

                select_prod(d_json, cat_name, cat_id, db_con)

            # accept the request for product choice
            else:
                if selection == "o":
                    choice(
                        d_json, cat_name, cat_id,
                        db_con, nb_product, product_list
                    )

                # no product choice
                elif selection.lower() == "n":
                    print()
                    print("Vous n'avez pas choisi de Produit")
                    print()

                    continuity(d_json, db_con)

    # accept the request for choice produced after a wrong choice
    elif select == "o":
        selection = select
        if selection == "o":
            choice(
                d_json, cat_name, cat_id,
                db_con, nb_product, product_list
            )


# +-------------+
# |   CHOICE    |
# |   PRODUCT   |
# +-------------+
def choice(d_json, cat_name, cat_id, db_con, nb_product, product_list):

    """treatment module of choice produced
    after acceptance of product choice

    Args:
        d_json         ==> memorizing the name of the products
                           contained in the JSON data

        cat_name       ==> storage of the product category name

        cat_id         ==> memorization of the id
                            of the chosen product category

        db_con         ==> link to the database

        nb_product     ==> number of products in the chosen category

        product_list   ==> list of products in the chosen category
    Vars:
        sub_id         ==> memorization of the chosen substitute product id

    Funcs:
        substitutes_display() ==> display module and choice
                                    of substitution product
                                    for the chosen product

        backup_product() alias b_product ==> backup module
                                            of substitution product chosen
                                            see more detail
                                            in the module itself

        continuity()   ==> module of choice
                            for continuing or stopping the script"""

    sub_id = 0
    while True:
        print()
        product = input("choississez un produit par son numéro : ")

        # wrong treatment
        try:
            product = int(product)
        except ValueError:
            print()
            print("Vous devez choisir un NOMBRE ")
            time.sleep(1.5)
            os.system("clear")

            select_prod(d_json, cat_name, cat_id, db_con, "o")

        # out of bounds
        else:
            if not 0 < product < nb_product + 1:
                print()
                print(f"Le produit DOIT ÊTRE COMPRIS ENTRE 1 ET {nb_product}")
                time.sleep(1.5)
                os.system("clear")

                select_prod(d_json, cat_name, cat_id, db_con, "o")

            else:
                break

    # Choice display
    print()
    print(f"Vous avez choisi le produit {product_list[product- 1][0].upper()}")

    time.sleep(1.5)
    os.system("clear")

    # Display of the product menu to substitute
    # memorize the chosen product
    sub_id = substitutes_display(
        d_json, product_list[product-1][0],
        cat_id, db_con
    )

    # save the stored product in the database
    b_product(cat_id, product_list[product-1][0], sub_id, db_con)

    continuity(d_json, db_con)


# +-------------------------+
# |    JSON data storage    |
# +-------------------------+
def menu_url(db_con):

    """JSON data storage module
    for an online update of the database

    Args:
        db_con         ==> link to the database

    Vars:
        selection[]    ==> memorizing the category name
                            and JSON online data link (internet access)

    Funcs:
        update_database() alias url_insert ==> insert JSON data
                                                into the database
                                                see more detail
                                                in the module itself"""

    selection = [
        [
            "Boissons_energetiques",
            "https://fr.openfoodfacts.org/categorie/boissons-energisantes.json"
        ],
        ["Bonbons", "https://fr.openfoodfacts.org/categorie/bonbons.json"],
        [
            "Charcuteries",
            "https://fr.openfoodfacts.org/categorie/charcuteries.json"
        ],
        ["Chocolats", "https://fr.openfoodfacts.org/categorie/chocolats.json"],
        ["Conserves", "https://fr.openfoodfacts.org/categorie/conserves.json"],
        ["Fromages", "https://fr.openfoodfacts.org/categorie/fromages.json"],
        ["Fruits", "https://fr.openfoodfacts.org/categorie/fruits.json"],
        [
            "Fruits_confits",
            "https://fr.openfoodfacts.org/categorie/fruits-confits.json"
        ],
        ["Gateaux", "https://fr.openfoodfacts.org/categorie/gateaux.json"],
        ["Glaces", "https://fr.openfoodfacts.org/categorie/glaces.json"],
        [
            "Jus_de_fruits",
            "https://fr.openfoodfacts.org/categorie/jus-de-fruits.json"
        ],
        ["Laits", "https://fr.openfoodfacts.org/categorie/laits.json"],
        [
            "Pates_de_fruit",
            "https://fr.openfoodfacts.org/categorie/pates-de-fruits.json"
        ],
        ["Pates", "https://fr.openfoodfacts.org/categorie/pate.json"],
        [
            "Pates_a_tartiner",
            "https://fr.openfoodfacts.org/categorie/pates-a-tartiner.json"
        ],
        ["Pizzas", "https://fr.openfoodfacts.org/category/pizzas.json"],
        ["Poissons", "https://fr.openfoodfacts.org/categorie/poissons.json"],
        [
            "Poissons_elevages",
            "https://fr.openfoodfacts.org/categorie/poisson-d'elevage.json"
        ],
        ["Reglisse", "https://fr.openfoodfacts.org/categorie/reglisse.json"],
        ["Riz", "https://fr.openfoodfacts.org/categorie/riz.json"],
        ["Sorbets", "https://fr.openfoodfacts.org/categorie/sorbets.json"],
        ["Viandes", "https://fr.openfoodfacts.org/categorie/viandes.json"],
        ["Vins", "https://fr.openfoodfacts.org/categorie/vins.json"],
        ["Yaourts", "https://fr.openfoodfacts.org/categorie/yaourts.json"],
    ]

    # update of data in the database
    for elt in selection:
        url_insert(elt[1], elt[0], db_con)

    return selection


# +-----------+
# |    MENU   |
# |   SELECT  |
# +-----------+
def menu_select(d_json, db_con, selection=""):

    """general menu display module of choice
        for different actions on the database

    Args:
        d_json         ==> memorizing the name of the products
                                contained in the JSON data

        db_con         ==> link to the database

        selection      ==> memorizing the choice of action on the database
                            for a reminder of this module
                            after a bad choice on the list of actions

    Vars:
        select         ==> memorizing the choice of action on the database

    Funcs:
        cat_menu()     ==> Displaying the general menu of categories
                            see more detail in the module itself

        recall_menu    ==> processing of the choice made
                            from the general menu of choice in this function
                            see more detail in the module itself"""

    print()
    print("Que Voulez vous faire ?")
    print()
    print("  - Mettre à jour BD      ==> 'm'")
    print("  - Produits enregistrés  ==> 'p'")
    print("  - Choisir une catégorie ==> 'o'")
    print("  - Quitter le programme  ==> 'q'")
    print()

    if selection == "":
        while True:
            select = input("Faites votre choix : ")

            # bad choice
            if select not in "mpoq":
                print()
                print("LE CHOIX NE PEUT ÊTRE QUE 'm', 'p', 'o' ou 'q'")
                time.sleep(1.3)

                cat_menu(d_json, db_con)

            # choice management main menu
            else:
                select = select.lower()
                recall_menu(select, d_json, db_con)

    # choice management main menu after a bad choice
    else:
        recall_menu(selection, d_json, db_con)


# +-------------------------+
# |    continuity module    |
# |     for the program     |
# + ------------------------+
def continuity(d_json, db_con):

    """module of choice for continuing or stopping the script

    Args:
        d_json         ==> memorizing the name of the products
                           contained in the JSON data

        db_con         ==> link to the database

    Vars:
        selection      ==> memorization of the choice
                            to continue or stop the script

    Funcs:
        cat_menu()     ==> Displaying the general menu of categories
                            see more detail in the module itself"""

    selection = ""
    while True:
        print()
        selection = input("Voulez vous continuez ? (Oui / Non) : ")
        # bab choice
        if selection not in "on":
            os.system("clear")
            print()
            print("VOUS DEVEZ CHOISIR 'o' OU 'n'")

        # continuation of the scrip
        elif selection.lower() == "o":
            os.system("clear")

            cat_menu(d_json, db_con)

        # stop the script
        elif selection.lower() == "n":
            sys.exit()


# +--------------------------+
# |  Starting category menu  |
# +--------------------------+
def cat_menu(d_json, db_con, selection=""):

    """Display module of the general category menu

    Args:
        d_json         ==> memorizing the name of the products
                            contained in the JSON data

        db_con         ==> link to the database

        selection      ==> memorizing the choice of action on the database
                            for a reminder of this module
                            after a bad choice on the list of actions

    Funcs:
        menu_category() ==> product category menu display module
                            see more detail in the module itself

        menu_select()  ==> general menu display module of choice
                            for different actions on the database
                            see more detail in the module itself"""

    os.system("clear")
    menu_category(d_json)

    return menu_select(d_json, db_con, selection)


# +------------------------+
# |  recall menu category  |
# +------------------------+
def recall_menu(select, d_json, db_con):

    """processing module of the choice made from the general menu of choice
        in the select_menu () module

    Args:
        select         ==> memorizing the choice of action on the database
                            for a reminder of this module
                            after a bad choice on the list of actions

        d_json         ==> memorizing the name of the products
                            contained in the JSON data

        db_con         ==> link to the database

    Vars:
        update         ==> memorization of the choice
                            concerning the update of the database

        cat_id         ==> memorization of the chosen product category id

        cat_name[]     ==> memorization of the id and the chosen category name

        prod_name[]    ==> memorization of product choice
                            without nutrition grade
        choice         ==> memorizing the choice
                            of continuation or stop of the script

    Funcs:
        menu_select()  ==> general menu display module of choice
                            for different actions on the database
                            see more detail in the module itself

        erase_data() alias erase_db ==> module for erasing data
                                        from the database
                                        see more detail in the module itself

        menu_url()     ==> JSON data storage module
                            for an online update of the database
                            see more detail in the module itself

        read_substitute() ==> display module for registered products
                                see more detail in the module itself

        cat_menu()     ==> Display module of the general category menu
                            see more detail in the module itself

        select_prod()  ==> module allowing the display of the product menu
                            see more detail in the module itself

        continuity()   ==> module of choice
                            for continuing or stopping the script"""

    # update Data Base
    if select == "m":
        while True:
            os.system("clear")
            print("Attention la mise à jour de la base de donnée ")
            print("éfface toutes les données ")
            print("ainsi que les enregistrements du choix de produit")
            print()

            update = input("Voulez vous vraiment continuez ? (Oui / Non) : ")
            # bad choice
            if update not in "on":
                os.system("clear")
                print("Vous devez CHOISIR 'o' OU 'n'")
                time.sleep(1.5)

                menu_select(d_json, db_con, "m")

            # accepting the update of the database
            elif update.lower() == "o":
                erase_db(db_con)
                menu_url(db_con)
                print()
                print("Mise à jour de la Base de donnée effectuée. ")
                break

            # refuse to update the database
            elif update.lower() == "n":
                os.system("clear")
                print()
                print("Pas de mise à jour effectuée")
                break

        time.sleep(1.3)

        cat_menu(d_json, db_con)

    # registered products
    elif select == "p":
        read_substitute(d_json, db_con)
        cat_menu(d_json, db_con)

    # category choice
    elif select == "o":
        cat_id = ""
        cat_name = []
        prod_name = ""

        while True:
            print()
            cat_id = input(
                "choississez une catégory de produit par son numéro : "
            )

            # bad choice
            try:
                cat_id = int(cat_id)
            except ValueError:
                print()
                print("Vous devez choisir un NOMBRE ")
                time.sleep(1.5)

                cat_menu(d_json, db_con, "o")

            # out of bounds
            else:
                if not 0 < cat_id < 25:
                    print()
                    print("La catégorie DOIT COMPRISE ÊTRE ENTRE 1 ET 24")
                    time.sleep(1.5)

                    cat_menu(d_json, db_con, "o")

                else:
                    break

        cat_name = [d_json[cat_id - 1][0], cat_id]
        print()
        print("Vous avez choisi la catégorie ", cat_name[0].upper())

        time.sleep(1.3)
        os.system("clear")

        # manage products without nutritional grade
        prod_name = select_prod(d_json, cat_name[0], cat_name[1], db_con)

        if not prod_name:
            print()
            print("Il n'y a pas de grade nutritionel dans cette catégorie !")
            print()

            continuity(d_json, db_con)

    # confirmation request to stop
    # the script without choosing a product
    elif select == "q":
        os.system("clear")

        print("Pas de choix effectuer...")
        print()

        while True:
            choosen = input("Voulez vous vraiment arretez ? (Oui / Non) : ")
            if choosen not in "on":
                os.system("clear")
                print("Vous devez choisir 'o' ou 'n'")
                time.sleep(1.5)

                recall_menu("q", d_json, db_con)

            elif choosen.lower() == "o":
                sys.exit()

            elif choosen.lower() == "n":
                break

        cat_menu(d_json, db_con)

    elif not prod_name[0]:
        print()
        print("Il n'y a pas de produit choisi !")

        continuity(d_json, db_con)


# +-----------------------+
# |  registered products  |
# +-----------------------+
def read_substitute(d_json, db_con):

    """display module for registered products

    Args:
        d_json          ==> memorizing the name of the products
                            contained in the JSON data

        db_con          ==> link to the database

    Vars:
        sub_product[]  ==> memorization of the list of products chosen

        product_sub[]  ==> memorisation of the list of substituted products

        loop           ==> memorization of the chosen product group
                            substituted product

        first / last   ==> parametric variables to display only one product
                            one product selected, one product substitute

        go_menu        ==> memorization of the choice
                            for the return menu general
                            display product category

    Funcs:
        cat_menu()     ==> Display module of the general category menu
                            see more detail in the module itself

    Queries:
        sql_substitute ==> SQL query that selects the list
                            of selected products

        sql_substituted ==> SQL query that selects the list
                            of substituted products"""

    dbase = db_con
    cursor = dbase.cursor()

    os.system("clear")
    print()
    print("Liste de Produit enregistre")
    print("===== == ======= ==========")
    print()

    sub_product = []
    product_sub = []
    # selection of selected products
    sql_substitute = """SELECT p1.name,
        p1.description,
        p1.nutrition_grade,
        p1.store,
        p1.url
    FROM product as p2
    INNER JOIN substitution_product as sp
        ON p2.id = sp.product_id1
    INNER JOIN product p1
        ON sp.product_id = p1.id
    WHERE
        sp.product_id1 in
            (SELECT sp1.product_id1
        FROM substitution_product as sp1)"""

    cursor.execute(sql_substitute)

    # memorization of selected products chosen products
    for elt in cursor:
        sub_product.append(
            [
                {"nom": elt[0]},
                {"description": elt[1]},
                {"grade_nutritionnel": elt[2].upper()},
                {"fiche_produit": elt[4]},
                {"magasin": elt[3]}
            ]
        )

    # selection of substituted products
    sql_substituted = """SELECT p2.name,
        p2.description,
        p2.nutrition_grade,
        p2.store,
        p2.url
    FROM product as p1
    INNER JOIN substitution_product as sp
        ON p1.id = sp.product_id
    INNER JOIN product as p2
        ON sp.product_id1 = p2.id
    WHERE
        sp.product_id in
            (SELECT substitution_product.product_id
                FROM substitution_product)"""

    cursor.execute(sql_substituted)

    # memorization of selected substitute products
    for elt in cursor:
        product_sub.append(
            [
                {"nom": elt[0]},
                {"description": elt[1]},
                {"grade_nutritionnel": elt[2].upper()},
                {"fiche_produit": elt[4]},
                {"magasin": elt[3]}
            ]
        )

    cursor.close()

    # list of registered products empty
    if not sub_product:
        print("Pas de produits enregistrés...")
        print()

    else:
        loop = 0
        first = 0
        last = 1
        # selected product registered
        while loop < len(sub_product):
            print(f"Produit Choisi N°{loop + 1}")
            print("======= ====== ====")

            for p_elt in sub_product[first:last]:
                nb_val = 0
                while nb_val < 5:
                    for p_val, p_data in p_elt[nb_val].items():
                        print(f"{p_val.upper()} : {p_data}")
                    nb_val += 1

                print()
                print("        .......")

            # selected substitute product registered
            print()
            print(f"Produit Substitué N°{loop + 1}")
            print("======= ========= ====")

            for ps_elt in product_sub[first:last]:
                nb_val_2 = 0
                while nb_val_2 < 5:
                    for ps_val, ps_data_2 in ps_elt[nb_val_2].items():
                        print(f"{ps_val.upper()} : {ps_data_2}")
                        nb_val_2 += 1
                print()
                print("###################################################")
                print()
                first += 1
                last += 1
                loop += 1

    # return condition category general menu
    while True:
        go_menu = input("Tapez 'c' pour continuer : ")
        if go_menu != "c":
            os.system("clear")
            print()
            print("Veuillez Taper LA LETTRE 'c' SVP !")
            time.sleep(1.5)

            read_substitute(d_json, db_con)

        elif go_menu.lower() == "c":
            os.system("clear")
            break

    cat_menu(d_json, db_con)


# +--------------+
# |   DISPLAY    |
# |   PRODUCT    |
# |  SUBSTITUTE  |
# +--------------+
def substitutes_display(d_json, product, cat_id, db_con):

    """module for displaying products that are substituted
    from a product selected in a category

    Args:
        d_json         ==> memorizing the name of the products
                                contained in the JSON data

        product        ==> memorization of the selected product
                            in the category menu

        cat_id         ==> memorization of the chosen product category id

        db_con         ==> link to the database

    Vars:
        substitute_list[] ==> memorization of the list
                                    of substituted products

        product_display[] ==> memorization of the first three substituted
                                products in the list
                                of substituted products

        selection      ==> memorization of the acceptance or not
                            for the choice of a substituted product

        name_product   ==> memorization of the name
                            of the chosen substitute product

        product_id     ==> memorization of the id
                            of the substituted product chosen

    Funcs:
        continuity()   ==> module of choice
                            for continuing or stopping the script

    Queries:
        sql_ngp        ==> SQL query that selects the nutritional grade
                            of the chosen product

        sql_prod       ==> SQL query that selects the list
                            of substituted products

        sql_selected   ==> SQL query that selects
                            the chosen substitute product id"""

    dbase = db_con
    cursor = dbase.cursor()

    sql_ngp = """SELECT nutrition_grade
        FROM product
        WHERE
            name = %(product)s"""

    cursor.execute(sql_ngp, {"product": product})

    # display of the nutritional grade
    # for the category product
    # to be substituted
    ng_p = ""
    print(f"Produit de substitution pour {product.upper()}")
    print()

    for elt_sub in cursor:
        ng_p = elt_sub[0]
        print(f"le grade nutritionel du produit choisi est : {ng_p.upper()}")
        print()

    # selection of substituted products
    sql_prod = """SELECT p.name,
                p.description,
                p.nutrition_grade,
                p.store,
                p.url
            FROM product as p
            INNER JOIN category_product as cp
                ON p.id = cp.product_id
            WHERE
                p.nutrition_grade <= %(ng_p)s
                    and
                cp.category_id = %(cat_id)s
                    and
                p.name != %(product)s"""

    cursor.execute(
        sql_prod,
        {"cat_id": cat_id, "ng_p": ng_p, "product": product}
    )

    # memorization of substituted products
    substitute_list = []
    for nb_p, elt_sub in enumerate(cursor):
        substitute_list.append(
            [
                {"Produit N°": nb_p + 1},
                {"nom": elt_sub[0]},
                {"description": elt_sub[1]},
                {"grade_nutritionnel": elt_sub[2].upper()},
                {"fiche_produit": elt_sub[4]},
                {"magasin": elt_sub[3]},
            ]
        )

    # display of the three best substituted products
    product_display = []
    for elt_sub3 in substitute_list[:3]:
        nb_val = 0
        while nb_val < 6:
            for sub3_val, sub3_data in elt_sub3[nb_val].items():
                print(f"{sub3_val.upper()} : {sub3_data-1}")
                if nb_val == 1:
                    product_display.append(sub3_data)
            nb_val += 1
        print()

    # choose or not one of the substituted products
    selection = ""
    name_product = ""
    product_id = 0
    while True:
        print()
        selection = input("Voulez vous choisir un produit ? (Oui/Non) : ")

        if selection.lower() == "o":
            while True:
                print()
                sub_select = input("choississez un produit par son numéro : ")

                # bad choice
                try:
                    sub_select = int(sub_select)
                    name_product = product_display[sub_select - 1]
                except ValueError:
                    print("Vous devez choisir un nombre")
                # wrong choice of number
                else:
                    if not 0 < sub_select < 4:
                        print("Le produit doit être entre 1 et 3")
                    else:
                        break

            print()
            print(
                f"""vous avez choisi de sauvegarder le produit N°{
                sub_select}"""
            )

            # selection of the chosen substitute product id
            sql_selected = """SELECT p.id
                FROM product as p
                WHERE
                    p.name = %(name_product)s"""

            cursor.execute(sql_selected, {"name_product": name_product})

            for sub_elt in cursor:
                product_id = sub_elt[0]
            print()
            time .sleep(1.5)
            os.system("clear")
            # backup of the chosen product
            # and backup of the chosen substituted product
            print("Sauvegarde en cours...")
            time.sleep(2)
            os.system("clear")
            print()
            print(f"le produit substituant {product.upper()}")
            print(f"et le produit substitué {name_product.upper()}")
            print()
            print("sont maintenant sauvegardés...")
            time.sleep(0.7)

            return product_id

        elif selection.lower() == "n":
            cursor.close()
            break

    continuity(d_json, db_con)


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
