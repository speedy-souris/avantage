# -*- coding: utf-8 -*-

import json

"""module containing the product characteristics of JSON (API OPENFOODFACT)"""


def contained_database(data, name_category, nb_product):

    #
    # read data from the json file
    #
    print(data, name_category, nb_product)
    print()
    designation = ''
    grade = ''
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

            if "nutrition_grades" in category_dict['products'][
                    nb_product].keys():
                grade = category_dict['products'][nb_product][
                    'nutrition_grades']
            else: 
                grade = category_dict['products'][nb_product][
                    'nutrition_grades_fr']

            # block containing the test of the json data
            # and the insertion of the data into the database

            #
            # product data
            #

            val_product = (
                category_dict['products'][nb_product]['url'],
                grade,
                designation,
                category_dict['products'][nb_product]['product_name'],
                category_dict['product'][nb_product]['stores']
            )

            #
            # database filling
            #

            cursor.execute(
                """INSERT INTO product(
                            url,
                            nutrition_grade,
                            description,
                            name,
                            store
            ) VALUES (%s, %s, %s, %s, %s)""", val_product)
            database.commit()

            #
            # category data
            #
            val_category = (name_category,)

            #
            # database filling
            #

            cursor.execute(
                """INSERT INTO category(category)
                                VALUES(%s)""", val_category
            )
            database.commit()

        except IndexError:
            pass
        except KeyError:
            pass

        nb_product += 1
