# -*- coding: utf-8 -*-

import json
import mysql.connector

"""module containing the product characteristics of JSON (API OPENFOODFACT)"""

def insert_product(category, nb_product):
	
	#
	# opening database
	#

	database= mysql.connector.connect(host="localhost",
									  user="student",
									  password="OpenClassRooms",
									  database="food_product"
	)
	cursor = database.cursor()
	
	#
	# filling database
	#
	
	with open(category) as json_category:
		category_dict = json.load(json_category)
	
	name = ''
	grade = ''
	try:
		if "generic_name_fr" in category_dict['products'][nb_product].keys():
			name = category_dict['products'][nb_product]['generic_name_fr']
		elif "generic_name" in category_dict['products'][nb_product].keys():
			name = category_dict['products'][nb_product]['generic_name']
		
		if "nutrition_grades" in category_dict['products'][nb_product].keys():
			grade = category_dict['products'][nb_product]['nutrition_grades']
		elif "nutrition_grades_fr" in category_dict['products'][nb_product].keys():
			grade = category_dict['products'][nb_product]['nutrition_grades_fr']
			
		sql = "INSERT INTO product (url, nutrition_grade, name, store) VALUES (%s, %s, %s, %s)"
		val = ( category_dict['products'][nb_product]['url'],
				grade, name, category_dict['products'][nb_product]['stores']
		)
	
		cursor.execute(sql, val)
		database.commit()
			
	except IndexError: # List ==> OUT OF RANGE 
		pass
	
	#
	# closing database
	#
	
	database.close()
