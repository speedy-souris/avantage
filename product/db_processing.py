"""database processing module
read, update, insert data
concerning products and their characteristics"""

#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import time

import requests


# +---------------------------+
# |          INSERT           |
# |  PRODUCTS AND CATEGORIES  |
# |      INTO THE DATABASE    |
# +---------------------------+
def contained_database(d_json, name_cat, db_con):

    """module containing the product characteristics of
    (API OPENFOODFACT (JSON Files))
    Args:
        d_json         ==> memorizing the name of the products
                            contained in the JSON data
        name_cat       ==> storage of the product category name
        db_con         ==> link to the database
    Vars:
        last_cat       ==> memorize the last insertion ID
        category_dict[] ==> memorize local JSON data
        cat_prod[]     ==> memorize the latest id category
                            and the last product id
    Queries:
        sql_c          ==> SQL query that inserts the product categories
        sql_p          ==> SQL query that inserts products
                            from the same category
        sql_cp         ==> SQL query that inserts the product ids
                            and ids of their category"""

    dbase = db_con
    cursor = dbase.cursor()

    # category data
    #     and
    # database filling
    sql_c = "INSERT INTO category(category) VALUES (%s)"
    val_c = (name_cat,)

    cursor.execute(sql_c, val_c)

    # category inserted
    dbase.commit()
    # get the last id category from insertion
    last_cat = cursor.lastrowid

    # read data from the json file
    with open(d_json) as json_category:
        category_dict = json.load(json_category)
    nb_product = 0
    while nb_product <= category_dict["page_size"]:

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
                category_dict["products"][nb_product]["url"],
                category_dict["products"][nb_product]["nutrition_grade_fr"],
                category_dict["products"][nb_product]["generic_name_fr"],
                category_dict["products"][nb_product]["product_name"],
                category_dict["products"][nb_product]["stores"],
            )

            cursor.execute(sql_p, val_p)

            # data inserted
            dbase.commit()

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

            val_cp = (cat_prod[0], cat_prod[1])

            cursor.execute(sql_cp, val_cp)

            # id categeory and id product copied
            dbase.commit()

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
def erase_data(db_con):

    """module containing the erasure of the data
    Args:
        db_con     ==> link to the database
    Queries:
        SQL query that clears the product table
        SQL query that updates the auto increment to 1
            in the product table
        SQL query that clears the category table
        SQL query that updates the auto increment to 1
            in the category table"""

    # +----------------------------------------------+
    # |  database cleaning and AUTO_INCREMENT reset  |
    # +----------------------------------------------+
    dbase = db_con
    cursor = dbase.cursor()

    os.system("clear")
    print("Effacement Base de donnée en cours ...")
    cursor.execute("DELETE FROM product")
    cursor.execute("ALTER TABLE product AUTO_INCREMENT = 1")
    cursor.execute("DELETE FROM category")
    cursor.execute("ALTER TABLE category AUTO_INCREMENT = 1")

    # data erased
    dbase.commit()
    time.sleep(2)
    os.system("clear")
    print("effacement Base de donnée effectués")
    time.sleep(1)


# +---------------------+
# |  BACKUP SUBSTITUTE  |
# |  IN THE DATABASE    |
# +---------------------+
def backup_product(cat_id, name_product, id_substituted, db_con):

    """backup module products
    Args:
        cat_id         ==> memorization of the id
                            of the chosen product category
        name_product   ==> storage of the product category name
        id_substituted ==> memorization of the id
                            of the substituted and chosen product
        db_con         ==> link to the database
    Vars:
        id_substitute  ==> memorization of the id
                            of the substituted product chosen
    Queries:
        sql_id         ==> SQL query that selects the id
                            of the chosen product
        sql_backup     ==> SQL query that inserts the chosen product id
                            and insert the chosen substituted product id"""

    dbase = db_con
    cursor = dbase.cursor()

    # selection the id of the chosen product
    sql_id = """SELECT p.id
        FROM product as p
        INNER JOIN category_product as cp
            ON p.id = cp.product_id
        WHERE
            cp.category_id = %(cat_id)s and p.name = %(name_product)s"""

    cursor.execute(sql_id, {"cat_id": cat_id, "name_product": name_product})

    # saving the id of the chosen product
    id_substitute = 0
    for elt in cursor:
        id_substitute = elt[0]

    # inserting the id of the chosen product
    # and inserting the id of the chosen substituted product
    sql_backup = """INSERT INTO substitution_product(
        product_id,
        product_id1)
        VALUES(%(id_substitute)s, %(id_substituted)s)"""

    val_backup = {
        "id_substitute": id_substitute,
        "id_substituted": id_substituted
    }

    cursor.execute(sql_backup, val_backup)

    # id product copied
    dbase.commit()


# +---------------------------+
# |          UPDATE           |
# |  PRODUCTS AND CATEGORIES  |
# |      INTO THE DATABASE    |
# +---------------------------+
def update_database(url, name_cat, db_con):

    """module containing the product characteristics of
    (API OPENFOODFACT (JSON URL)
    Args:
        url            ==> storing the update URL of the database
        name_cat       ==> storage of the product category name
        db_con         ==> link to the database
    Vars:
       last_cat       ==> memorize the last insertion ID
        category_dict[] ==> memorize internet JSON data
        cat_prod[]     ==> memorize the latest id category
                            and the last product id
    Queries:
        sql_c          ==> SQL query that inserts the product categories
        sql_p          ==> SQL query that inserts products
                            from the same category
        sql_cp         ==> SQL query that inserts the product ids
                            and ids of their category"""

    dbase = db_con
    cursor = dbase.cursor()

    os.system("clear")
    print("Mise à jour de la base de donnée en cours ...")
    print()
    print(url)
    print()
    # category data
    #     and
    # database filling
    sql_c = "INSERT INTO category(category) VALUES (%s)"
    val_c = (name_cat,)

    cursor.execute(sql_c, val_c)

    # category inserted
    dbase.commit()
    # get the last id category from insertion
    last_cat = cursor.lastrowid

    # read data from the json url
    category_dict = requests.get(url)
    category_dict = category_dict.json()

    nb_product = 0
    while nb_product <= category_dict["page_size"]:

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
                category_dict["products"][nb_product]["url"],
                category_dict["products"][nb_product]["nutrition_grade_fr"],
                category_dict["products"][nb_product]["generic_name_fr"],
                category_dict["products"][nb_product]["product_name"],
                category_dict["products"][nb_product]["stores"],
            )

            cursor.execute(sql_p, val_p)

            # data inserted
            dbase.commit()

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

            val_cp = (cat_prod[0], cat_prod[1])

            cursor.execute(sql_cp, val_cp)

            # id categeory and id product copied
            dbase.commit()

        except IndexError:
            pass
        except KeyError:
            pass

        nb_product += 1

    cursor.close()
    os.system("clear")
