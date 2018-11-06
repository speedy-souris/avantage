#! /usr/bin/env python3
# -*- coding:utf-8 -*-

# DB erasure
from db_processing import erase_data as erase_db
# DB insertion
from db_processing import contained_database as insert_data


#  ---------------------
# |         MENU        |
# |  CATEGORY  DISPLAY  |
#  ---------------------
def menu_category(db_connect):

    """module containing the category menu
    function menu_category (db_connect)
    with the parameter db_connect (connection to the database)"""

    # cleaning database
    erase_db(db_connect)

    #  --------------------------
    # |  Product selection menu  |
    #  --------------------------
    choix = [
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

    print("Menu de Catégorie Produit (OpenFoodFact)")
    print("==== == ========= =======")
    print()
    cat_name = []
    for i, elt in enumerate(choix):
        insert_data("json/" + choix[i][1], choix[i][0], i, db_connect)
        print(f"{i+1}. {elt[0]}")

    cat_id = 0
    while True:
        print()
        category = input(
            "choississez une catégory de produit par son numéro : "
        )
        try:
            cat_id = int(category)
        except ValueError:
            print("Vous devez choisir un nombre")
        else:
            if not 0 < cat_id < 25:
                print("La catégorie doit être entre 1 et 24")
            else:
                break

    cat_name = [choix[cat_id-1][0], cat_id]
    print()
    print("Vous avez choisi la catégorie ", cat_name[0])

    return cat_name


#  ---------------------------
# |         SELECT            |
# |  PRODUCTS AND CATEGORIES  |
# |      INTO THE DATABASE    |
#  ---------------------------
def prod_select(cat_name, cat_id, db_connect):

    """module allowing the display of the product menu
    according to the chosen category"""
    db = db_connect
    cursor = db.cursor()

    print()
    print("menu produit de la categorie ")
    print("==== ======= == == ========= ")
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

    cursor.execute(sql, {
        "cat_name": cat_name
    })

    nb_product = 0
    product_list = []
    for i, product_name in enumerate(cursor):
        print(f"{i+1}. {product_name[0]}")
        nb_product = i + 1
        product_list.append(product_name)

    cursor.close()

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
    print()
    for key, value in enumerate(product_list):
        if key == product-1:
            print(f"Vous avez choisi le produit : {value[0]}")
            prod_selected.append(value[0])

    prod_selected.append(cat_id)
    print()

    return prod_selected


#  --------------
# |   DISPLAY    [
# |   PRODUCT    |
# |  SUBSTITUTE  |
#  --------------
def display_substitutes(product, cat_id, db_connect):

    """module for displaying products that are substituted
    from a product selected in a category"""

    db = db_connect
    cursor = db.cursor()
    sql_ngp = "SELECT nutrition_grade FROM product WHERE name = %(product)s"

    cursor.execute(sql_ngp, {"product": product})

    ng_p = ""
    for elt in cursor:
        ng_p = elt[0]
        print(f"le grade nutritionel du produit choisi est : {ng_p}")

    sql_prod = """SELECT p.name,
                p.description,
                p.store,
                p.url,
                p.nutrition_grade
                FROM product as p
                INNER JOIN category_product as cp
                    ON p.id = cp.product_id
                WHERE
                    cp.category_id = %(cat_id)s"""
                    
    cursor.execute(sql_prod, {"cat_id": cat_id})

    ng_p = ord(ng_p)
    print()
    print("Produit de Substitution")
    print("======= == ============")
    print()
    for elt in cursor:
        if ord(elt[4]) < ng_p:
            print(f"Nom du Produit : {elt[0]}")
            print(f"Description : {elt[1]}")
            print(f"Grade Nutritionnel : '{elt[4]}'")
            print(f"Magasin : {elt[2]}")
            print(f"Fiche produit OpenFoodFact : {elt[3]}'")
            print()

    cursor.close()


# ~ if __name__ == '__main__':
