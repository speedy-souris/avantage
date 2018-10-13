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
    # category data and database filling
    #

    sql_c = "INSERT INTO category(category) VALUES (%s)"
    val_c = (name_category,)

    cursor.execute(sql_c, val_c)

    database.commit()  # category inserted

    last_cat = cursor.lastrowid # get the last id category from insertion

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
            
            cursor.execute(sql_p, val_p)

            database.commit()  # data inserted

            last_prod = cursor.lastrowid # get the last id product from insertion

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

            cursor.execute(sql_cp, val_cp)

            database.commit() #id categeory and id product copied

        except IndexError:
            pass
        except KeyError:
            pass

        nb_product += 1

    database.close()  # closing database
    


"""module containing the erasure of the data"""


def erase_data():

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

    # ----------------------------------------------
    # | database cleaning and AUTO_INCREMENT reset |
    # ----------------------------------------------

    cursor.execute("DELETE FROM product")
    cursor.execute("ALTER TABLE product AUTO_INCREMENT = 1")
    cursor.execute("DELETE FROM category")
    cursor.execute("ALTER TABLE category AUTO_INCREMENT = 1")
    cursor.execute("DELETE FROM category_product")

    database.commit()  # data erased

    database.close()  # closing database


if __name__ == '__main__':

    erase_data()
    contained_database('../chocolats.json', 'Cat', 8)
