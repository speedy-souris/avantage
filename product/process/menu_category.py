# -*- coding: utf-8 -*-

from function import insertion as insert

def menu_category():

    insert.erase_data()  # cleaning database

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
        insert.contained_database('json/' + choix[i][1], choix[i][0], i)
        print("{}. {}".format(i+1, elt[0]))


if __name__ == '__main__':

    insert.erase_data()
    insert.contained_database('fruits.json', 'Cat', 4)

