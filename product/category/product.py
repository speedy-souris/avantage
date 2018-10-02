# -*- coding: utf-8 -*-

import json
import mysql.connector


"""module containing the product characteristics of JSON (API OPENFOODFACT)"""


def contained_database(data, name_category, nb_product):

    # --------------------
    # | Opening DataBase |
    # --------------------

    database = mysql.connector.connect(
            host="localhost",
            user="student",
            password="OpenClassRooms",
            database="food_product"
    )

    cursor = database.cursor()

    #
    # read data from the json file
    #

    designation = ''
    with open(data) as json_category:
        category_dict = json.load(json_category)

    while nb_product <= category_dict['page_size']:

        try:
            if "generic_name_fr" in category_dict['products'][
                    nb_product].keys():
                designation = category_dict['products'][nb_product][
                    'generic_name_fr']
            else:
                designation = category_dict['products'][nb_product][
                    'generic_name']

            """ block containing the test of the json data
                and the insertion of the data into the database"""

            #
            # product data and database filling
            #

            cursor.execute(
                """INSERT INTO product(
                                    url,
                                    nutrition_grade,
                                    description,
                                    name,
                                    store) VALUES (%s, %s, %s, %s, %s)""",
                (
                    category_dict['products'][nb_product]['url'],
                    category_dict['products'][nb_product][
                            'nutrition_grades_fr'],
                    designation,
                    category_dict['products'][nb_product]['product_name'],
                    category_dict['product'][nb_product]['stores'])
            )
            database.commit() # data inserted
            #
            # category data and database filling
            #
            cursor.execute("""INSERT INTO category(category) VALUES(%s)""",
                (name_category)

            database.commit() # data inserted
            database.close()  # closing database
        
        except IndexError:
            pass
        except KeyError:
            pass

        nb_product += 1
