# -*- coding:utf-8 -*-

from category.product import *

print('')
print('le programme de Substitution de produit est lancé ! ')
print('')

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
name = ''
for i, elt in enumerate(choix):

    contained_database('category/' + choix[i][1], choix[i][0], i)
    print("{}. {}".format(i+1, elt[0]))


while True:

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
print(name)
