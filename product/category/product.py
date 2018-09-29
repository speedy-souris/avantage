# -*- coding: utf-8 -*-

import json


"""module containing the product characteristics of JSON (API OPENFOODFACT)"""

def contained_database(data, category):
	
	#
	# read data from the json file
	#
	with open(data) as json_category:
		category_dict = json.load(json_category)
	
	name = ''
	grade = ''
	nb_product = 1
	while nb_product <= category_dict['page_size']:
		try:
			if "generic_name_fr" in category_dict['products'][nb_product].keys():
				name = category_dict['products'][nb_product]['generic_name_fr']
			elif "generic_name" in category_dict['products'][nb_product].keys():
				name = category_dict['products'][nb_product]['generic_name']
		
			if "nutrition_grades" in category_dict['products'][nb_product].keys():
				grade = category_dict['products'][nb_product]['nutrition_grades']
			elif "nutrition_grades_fr" in category_dict['products'][nb_product].keys():
				grade = category_dict['products'][nb_product]['nutrition_grades_fr']
			
			#
			# product data
			#
		    
		    val_product = (
				category_dict['products'][nb_product]['product_name'],
				category_dict['products'][nb_product]['url'],
				category_dict['product'][nb_product]['stores'],
				name, 
				grade
		    )
						   				         		              			
			contained_product(val_product) # insert product data
			
			#
			# category data
			#
			val_category = (category,)
			
			contained_category(val_category) # insert category data
			
			
		except IndexError: 
			pass
		except KeyError:
			pass
								
		nb_product += 1


"""module containing the insertion of product data"""

def insert_product(data):
	
	#
	# database filling 
	#
	cursor.execute("""INSERT INTO product(url, nutrition_grade, description, name, store) VALUES (%s, %s, %s, %s, %s)""", data)
			
	database.commit()	
		

"""module containing the insertion of product category"""


def insert_category(data):
	
	#
	# database filling 
	#
	cursor.execute("""INSERT INTO category(category) VALUES(%s)""", data)
			
	database.commit()	
		
	
"""test module and product insertion"""

def contained_product(data):
	
	cursor.execute("""SELECT * FROM product """)  
	if not cursor.fetchall():
		insert_product(data)
	else:
		pass
		
	insert_product(data)


"""test module and category insertion"""

def contained_category(data):
	
	cursor.execute("""SELECT * FROM category """)
	rows = cursor.fetchall()
	if not rows:
		insert_category(data)
	else:
		for row in rows:
			if row != category:
				insert_category(data)
			else:
				pass	
