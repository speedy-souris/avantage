#! /usr/bin/env python3
# -*- coding:utf-8 -*-

#  import module processing data json
import json


#  ---------------------------
# |          INSERT           |
# |  PRODUCTS AND CATEGORIES  |
# |      INTO THE DATABASE    |
#  ---------------------------
def contained_database(data, name_cat, nb_product, connect_db):

    """module containing the product characteristics of 
    (API OPENFOODFACT)"""

    db = connect_db
    cursor = db.cursor()

    #  --------------------
    # |  category data     |
    # |       and          |
    # |  database filling  |
    #  --------------------
    sql_c = "INSERT INTO category(category) VALUES (%s)"
    val_c = (name_cat,)

    cursor.execute(sql_c, val_c)

    # category inserted
    db.commit()
    # get the last id category from insertion
    last_cat = cursor.lastrowid

    #  --------------------------------
    # |  read data from the json file  |
    #  --------------------------------
    designation = ''

    with open(data) as json_category:
        category_dict = json.load(json_category)

    while nb_product <= category_dict['page_size']:
        try:

            #  ----------------------
            # |   product data       | 
            # |        and           |
            # |  database filling    |
            #  ----------------------
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

            # data inserted
            db.commit()

            # get the last id product from insertion
            last_prod = cursor.lastrowid

            #
            # filling of the link TABLE category_product_substition
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

            # id categeory and id product copied
            db.commit()

        except IndexError:
            pass
        except KeyError:
            pass

        nb_product += 1

    cursor.close()


def erase_data(db_connect):

    """module containing the erasure of the data"""

    #  ----------------------------------------------
    # |  database cleaning and AUTO_INCREMENT reset  |
    #  ----------------------------------------------
    db = db_connect
    cursor = db.cursor()
    cursor.execute("DELETE FROM product")
    cursor.execute("ALTER TABLE product AUTO_INCREMENT = 1")
    cursor.execute("DELETE FROM category")
    cursor.execute("ALTER TABLE category AUTO_INCREMENT = 1")

    db.commit()  # data erased


# ~ if __name__ == '__main__':
