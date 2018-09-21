# -*- coding: utf-8 -*-

import json

"""module containing the product characteristics of JSON (API OPENFOODFACT)"""

def read_product(category, nb_product):
	
	with open(category) as json_category:
		category_dict = json.load(json_category)
	
	print('Lien OpenFoodFact de la fiche produit :')
	print(category_dict['products'][nb_product]['url'])
	print('')
	print('Grade Nutritionnel :')
	if category_dict['products'][nb_product]['nutrition_grade_fr'] != '':
		print(category_dict['products'][nb_product]['nutrition_grade_fr'])
	else:
		print(category_dict['products'][nb_product]['nutrition_grade'])
	print('')
	print('Nom du produit :')
	if category_dict['products'][nb_product]['generic_name_fr'] != '':
		print(category_dict['products'][nb_product]['generic_name_fr'])
	else:
		print(category_dict['products'][nb_product]['generic_name'])
	print('')
	print('Où l\'acheter :')
	print(category_dict['products'][nb_product]['stores'])
	
# test of read_product
if __name__ == "__main__":
	read_product('pate_tartiners.json', 7)
	
