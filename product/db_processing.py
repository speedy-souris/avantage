#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time

import json


# +---------------------------+
# |          INSERT           |
# |  PRODUCTS AND CATEGORIES  |
# |      INTO THE DATABASE    |
# +---------------------------+
def contained_database(data, name_cat, db_connect):

    """module containing the product characteristics of
    (API OPENFOODFACT (JSON Files))"""

    db = db_connect
    cursor = db.cursor()

    # category data
    #     and
    # database filling
    sql_c = "INSERT INTO category(category) VALUES (%s)"
    val_c = (name_cat,)

    cursor.execute(sql_c, val_c)

    # category inserted
    db.commit()
    # get the last id category from insertion
    last_cat = cursor.lastrowid

    # read data from the json file
    with open(data) as json_category:
        category_dict = json.load(json_category)
    nb_product = 0
    while nb_product <= category_dict['page_size']:

        try:
            # product data
            #      and
            # database filling
            sql_p = """INSERT INTO product(
                url,
                nutrition_grade,
                description,
                name,
                store)
                    VALUES (%s, %s, %s, %s, %s)"""

            val_p = (
                category_dict['products'][nb_product]['url'],
                category_dict[
                    'products'][nb_product]['nutrition_grade_fr'],
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


# +-------------------+
# |  erasure module   |
# |  of the database  |
# +-------------------+
def erase_data(db_connect):

    """module containing the erasure of the data"""

    #  ----------------------------------------------
    # |  database cleaning and AUTO_INCREMENT reset  |
    #  ----------------------------------------------
    db = db_connect
    cursor = db.cursor()

    os.system("clear")
    print("Mise a jour Base de donnée...")
    cursor.execute("DELETE FROM product")
    cursor.execute("ALTER TABLE product AUTO_INCREMENT = 1")
    cursor.execute("DELETE FROM category")
    cursor.execute("ALTER TABLE category AUTO_INCREMENT = 1")

    # data erased
    db.commit()

    time.sleep(1.5)
    os.system("clear")
    print("mise à jour terminé")


def backup_product(cat_id, name_product, id_substituted, db_connect):

    """backup module products"""

    db = db_connect
    cursor = db.cursor()

    sql_id = """SELECT p.id
        FROM product as p
        INNER JOIN category_product as cp
            ON p.id = cp.product_id
        WHERE
            cp.category_id = %(cat_id)s and p.name = %(name_product)s"""

    cursor.execute(
        sql_id, {
            "cat_id": cat_id,
            "name_product": name_product}
    )

    id_substitute = 0
    for elt in cursor:
        id_substitute = elt[0]

    sql_backup = """INSERT INTO substitution_product(
        product_id,
        product_id1)
        VALUES(%(id_substitute)s, %(id_substituted)s)"""

    val_backup = (
        {"id_substitute": id_substitute,
         "id_substituted": id_substituted}
    )

    cursor.execute(sql_backup, val_backup)

    # id product copied
    db.commit()


# ~ if __name__ == '__main__':
