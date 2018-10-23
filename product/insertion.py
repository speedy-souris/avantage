#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import json


"""module containing the product characteristics of JSON (API OPENFOODFACT)"""


def contained_database(data, name_category, nb_product, connect):

    connect.dbConnect()
    connect.cursor = connect.database.cursor()

    #
    # category data and database filling
    #

    sql_c = "INSERT INTO category(category) VALUES (%s)"
    val_c = (name_category,)

    connect.cursor.execute(sql_c, val_c)

    connect.database.commit()  # category inserted

    last_cat = connect.cursor.lastrowid # get the last id category from insertion

    #
    # read data from the json file
    #

    designation = ''

    with open(data) as json_category:
        category_dict = json.load(json_category)

    while nb_product <= category_dict['page_size']:
        try:

            #
            # product data and database filling
            #

            sql_p = """INSERT INTO product(
                url,
                nutrition_grade,
                description,
                name,
                store)
                    VALUES (%s, %s, %s, %s, %s)"""

            val_p = (
                category_dict['products'][nb_product]['url'],
                category_dict['products'][nb_product]['nutrition_grade_fr'],
                category_dict['products'][nb_product]['generic_name_fr'],
                category_dict['products'][nb_product]['product_name'],
                category_dict['products'][nb_product]['stores']
            )
            
            connect.cursor.execute(sql_p, val_p)

            connect.database.commit()  # data inserted

            last_prod = connect.cursor.lastrowid # get the last id product from insertion

            #
            # filling of the link TABLE category_product
            #

            cat_prod = [last_cat, last_prod]
            sql_cp = """INSERT INTO category_product(
                category_id,
                product_id)
                    VALUES(%s, %s)"""

            val_cp = (
                cat_prod[0],
                cat_prod[1]
            )

            connect.cursor.execute(sql_cp, val_cp)

            connect.database.commit() # id categeory and id product copied

        except IndexError:
            pass
        except KeyError:
            pass

        nb_product += 1


"""module containing the erasure of the data"""


def erase_data(connect):

    connect.dbConnect()
    connect.cursor = connect.database.cursor()

    # ----------------------------------------------
    # | database cleaning and AUTO_INCREMENT reset |
    # ----------------------------------------------

    connect.cursor.execute("DELETE FROM product")
    connect.cursor.execute("ALTER TABLE product AUTO_INCREMENT = 1")
    connect.cursor.execute("DELETE FROM category")
    connect.cursor.execute("ALTER TABLE category AUTO_INCREMENT = 1")
    connect.cursor.execute("DELETE FROM category_product")

    connect.database.commit()  # data erased

    connect.database.close()  # closing database


if __name__ == '__main__':

    erase_data()
    contained_database('../chocolats.json', 'Cat', 8)
