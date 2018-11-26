#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time

# DB insertion
from db_processing import contained_database as insert_data


# +---------------------+
# |         MENU        |
# |  CATEGORY  DISPLAY  |
# +---------------------+
def menu_category(db_connect):
    """module containing the category menu
    function menu_category (db_connect)
    with the parameter db_connect (connection to the database)"""

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
        ["Yaourts", "yaourts.json"]
    ]

    # verification / insertion / update of data in the database
    db = db_connect
    cursor = db.cursor()

    sql_verif = """SELECT COUNT(*)
                FROM product, category"""

    cursor.execute(sql_verif,)

    print("Verification de la base de donnée...")
    print()
    for elt in cursor:
        if elt[0] == 0:
            for i, elt in enumerate(selection):
                insert_data(
                    "json/" + selection[i][1], selection[i][0], db_connect)
        else:
            time.sleep(1.5)
    cursor.close()

    print("Verification terminé")
    print()
    time.sleep(1)
    os.system("clear")

    # display of the product category menu
    print("Menu de Catégorie Produit (OpenFoodFact)")
    print("==== == ========= =======")
    print()
    for i, elt in enumerate(selection):
        print(f"{i+1}. {elt[0]}")

    cat_id = ""
    while True:
        print()
        cat_id = input(
            "choississez une catégory de produit par son numéro : "
        )

        try:
            cat_id = int(cat_id)
        except ValueError:
            print("Vous devez choisir un nombre")
        else:
            if not 0 < cat_id < 25:
                print("La catégorie doit être entre 1 et 24")
            else:
                break

    cat_name = [selection[cat_id-1][0], cat_id]
    print("Vous avez choisi la catégorie ", cat_name[0].upper())

    time.sleep(1.5)
    os.system("clear")
    return cat_name


# +---------------------------+
# |         SELECT            |
# |  PRODUCTS AND CATEGORIES  |
# |      INTO THE DATABASE    |
# +---------------------------+
def select_prod(cat_name, cat_id, db_connect):

    """module allowing the display of the product menu
    according to the chosen category"""

    db = db_connect
    cursor = db.cursor()

    print()
    print("menu produit de la categorie", cat_name.upper())
    print("==== ======= == == =========")
    print()

    sql = """SELECT p.name as nom_produit,
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

    cursor.execute(
        sql,
        {"cat_name": cat_name}
    )

    # menu of products of the chosen category
    nb_product = 0
    product_list = []
    for i, product_name in enumerate(cursor):
        print(f"{i+1}. {product_name[0]}")
        nb_product = i + 1
        product_list.append(product_name)

    cursor.close()

    if not (product_list):
        return

    while True:
        print()
        product = input("choississez un produit par son numéro : ")

        try:
            product = int(product)
        except ValueError:
            print("Vous devez choisir un nombre")
        else:
            if not 0 < product < nb_product+1:
                print("Le produit doit être entre 1 et ", nb_product)
            else:
                break

    prod_selected = []
    for key, value in enumerate(product_list):
        if key == product-1:
            print(f"Vous avez choisi le produit : {value[0].upper()}")
            prod_selected.append(value[0])
            prod_selected.append(cat_id)
            print()
    time.sleep(1.5)
    os.system("clear")
    return prod_selected


# +--------------+
# |   DISPLAY    |
# |   PRODUCT    |
# |  SUBSTITUTE  |
# +--------------+
def substitutes_display(product, cat_id, db_connect):

    """module for displaying products that are substituted
    from a product selected in a category"""

    db = db_connect
    cursor = db.cursor()

    sql_ngp = """SELECT nutrition_grade
        FROM product
        WHERE
            name = %(product)s"""

    cursor.execute(
        sql_ngp,
        {"product": product}
    )

    # display of the nutritional grade
    # for the category product
    # to be substituted
    ng_p = ""
    print(f"Produit de substitution pour {product.upper()}")
    print()
    for elt in cursor:
        ng_p = elt[0]
        print(f"le grade nutritionel du produit choisi est : {ng_p.upper()}")
        print()

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
        sql_prod, {
            "cat_id": cat_id,
            "ng_p": ng_p,
            "product": product}
    )
    substitute_list = []
    for nb, elt in enumerate(cursor):
        substitute_list.append([
            {"Produit N°": nb+1},
            {"nom": elt[0]},
            {"description": elt[1]},
            {"grade_nutritionnel": elt[2].upper()},
            {"magasin": elt[3]},
            {"fiche_produit": elt[4]}]
        )

    # display of the three best substituted products
    product_display = []
    for elt in substitute_list[:3]:
        nb_val = 0
        while nb_val < 5:
            for val, data in elt[nb_val].items():
                print(f"{val.upper()} : {data}")
                if nb_val == 1:
                    product_display.append(data)
            nb_val += 1
        print()

    # choose or not one of the substituted products
    selection = ""
    name_product = ""
    product_id = []
    while True:
        print()
        selection = input("Voulez vous choisir un produit ? (Oui/Non) : ")
        if selection.lower() == "o":

            while True:
                print()
                sub_select = input("choississez un produit par son numéro : ")

                try:
                    sub_select = int(sub_select)
                    name_product = product_display[sub_select-1]
                except ValueError:
                    print("Vous devez choisir un nombre")
                else:
                    if not 0 < sub_select < 4:
                        print("Le produit doit être entre 1 et 3")
                    else:
                        break
            print()
            print(f"""vous avez choisi de sauvegarder le produit N°{
                sub_select}""")

            sql_selected = """SELECT p.id
                FROM product as p
                WHERE
                    p.name = %(name_product)s"""

            cursor.execute(sql_selected, {"name_product": name_product})

            for elt in cursor:
                product_id.append(elt[0])
            product_id.append(product)

            print()
            print("Sauvegarde en cours...")
            time.sleep(1.7)
            os.system("clear")
            print(f"le produit substituant {product.upper()}")
            print(f"et le produit substitué {name_product.upper()}")
            print()
            print("sont maintenant sauvegardés...")

            return product_id

        elif selection.lower() == "n":
            cursor.close()
            break


def read_substitute(db_connect):

    """display module for registered products"""

    db = db_connect
    cursor = db.cursor()

    print()
    print("Liste de Produit enregistre")
    print("===== == ======= ==========")
    print()

    sub_product = []
    product_sub = []

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

    cursor.execute(sql_substitute,)

    for elt in cursor:
        sub_product.append([
            {"nom": elt[0]},
            {"description": elt[1]},
            {"grade_nutritionnel": elt[2].upper()},
            {"magasin": elt[3]},
            {"fiche_produit": elt[4]}]
        )

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

    cursor.execute(sql_substituted,)

    for elt in cursor:
        product_sub.append([
            {"nom": elt[0]},
            {"description": elt[1]},
            {"grade_nutritionnel": elt[2].upper()},
            {"magasin": elt[3]},
            {"fiche_produit": elt[4]}]
        )

    cursor.close()

    loop = 0
    first = 0
    last = 1
    while loop < len(sub_product):
        print(f"Produit Choisi N°{loop + 1}")
        print("======= ====== ====")
        for elt_1 in sub_product[first:last]:
            nb_val_1 = 0
            while nb_val_1 < 5:
                for val_1, data_1 in elt_1[nb_val_1].items():
                    print(f"{val_1.upper()} : {data_1}")
                nb_val_1 += 1
            print()
            print("        .......")
        print()
        print(f"Produit Substitué N°{loop + 1}")
        print("======= ========= ====")
        for elt_2 in product_sub[first:last]:
            nb_val_2 = 0
            while nb_val_2 < 5:
                for val_2, data_2 in elt_2[nb_val_2].items():
                    print(f"{val_2.upper()} : {data_2}")
                    nb_val_2 += 1
            print()
            print("###################################################")
            print()
            first += 1
            last += 1
        loop += 1


# ~ if __name__ == '__main__':
