#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from db_processing import erase_data as erase
from db_processing import contained_database as insert

from db_processing import cat_select as s_prod

                # ---------------------------
                #|                           |
                #|            MENU           |
                #|     CATEGORY  DISPLAY     |
                #|                           |
                # ---------------------------

def menu_category(connect):

    """module containing the category menu"""

    erase(connect)  # cleaning database

    # ----------------------------
    # |  Product selection menu  |
    # ----------------------------

    choix = [
        ['Boissons_energetiques', 'boissons_energie.json'], [
            'Bonbons', 'bonbons.json'],
        ['Charcuteries', 'charcuteries.json'], ['Chocolats', 'chocolats.json'],
        ['Conserves', 'conserves.json'], ['Fromages', 'fromages.json'],
        ['Fruits', 'fruits.json'], ['Fruits_confits', 'fruits_confits.json'],
        ['Gateaux', 'gateaux.json'], ['Glaces', 'glaces.json'],
        ['Jus_de_fruits', 'jus_fruits.json'], ['Laits', 'laits.json'],
        ['Pates_de_fruit', 'pate_fruits.json'], ['Pates', 'pates.json'],
        ['Pates_a_tartiner', 'pates_tartiner.json'], ['Pizzas', 'pizzas.json'],
        ['Poissons', 'poissons.json'], ['Poissons_elevages',
                                        'poissons_elevage.json'],
        ['Reglisse', 'reglisses.json'], ['Riz', 'riz.json'],
        ['Sorbets', 'sorbets.json'], ['Viandes', 'viandes.json'],
        ['Vins', 'vins.json'], ['Yaourts', 'yaourts.json']
    ]

    for i, elt in enumerate(choix):
        insert('json/' + choix[i][1], choix[i][0], i, connect)
        print(f"{i+1}. {elt[0]}")

    name = ''
    while True:
        print()
        category = input('choississez une catégory de produit par son numéro : ')
        try:
            category = int(category)

        except ValueError:
            print("Vous devez choisir un nombre")
        else:
            if not 0 < category < 25:
                print("La catégorie doit être entre 1 et 24")
            else:
                break

    name = choix[category-1][0]
    print()
    print("Vous avez choisi la catégorie ", name)

    menu_product(name, connect)

                # ---------------------------
                #|                           |
                #|            MENU           |
                #|     CATEGORY  DISPLAY     |
                #|                           |
                # ---------------------------

def menu_product(name, connect):

    """link module containing the TABLE category id
    and the TABLE product id"""

    print()
    print('menu produit de la categorie ', name)
    print()

    s_prod(name, connect)


# ~ if __name__ == '__main__':

