#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import json

                # ---------------------------------
                #|                                 |
                #|             INSERT              |
                #|     PRODUCTS AND CATEGORIES     |
                #|         INTO THE DATABASE       |
                #|                                 |
                # ---------------------------------

def contained_database(data, name_category, nb_product, connect):

    """module containing the product characteristics of JSON (API OPENFOODFACT)"""

    db = connect
    cursor = db.cursor()
    #
    # category data and database filling
    #

    sql_c = "INSERT INTO category(category) VALUES (%s)"
    val_c = (name_category,)

    cursor.execute(sql_c, val_c)

    db.commit()  # category inserted

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

            db.commit()  # data inserted

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

            db.commit() # id categeory and id product copied

        except IndexError:
            pass
        except KeyError:
            pass

        nb_product += 1

def erase_data(connect):

    """module containing the erasure of the data"""

    # ----------------------------------------------
    # | database cleaning and AUTO_INCREMENT reset |
    # ----------------------------------------------
    db = connect
    cursor = db.cursor()
    cursor.execute("DELETE FROM product")
    cursor.execute("ALTER TABLE product AUTO_INCREMENT = 1")
    cursor.execute("DELETE FROM category")
    cursor.execute("ALTER TABLE category AUTO_INCREMENT = 1")
    cursor.execute("DELETE FROM category_product")

    db.commit()  # data erased

                # ---------------------------------
                #|                                 |
                #|             SELECT              |
                #|     PRODUCTS AND CATEGORIES     |
                #|         INTO THE DATABASE       |
                #|                                 |
                # ---------------------------------

def cat_select(cat_name, connect):

    """module allowing the display of the product menu 
    according to the chosen category"""

    db = connect
    cursor = db.cursor()

    sql = """SELECT p.name as nom_produit
        FROM product as p
        INNER JOIN category_product as cp
            ON p.id = cp.product_id
        INNER JOIN category as c
            ON c.id = cp.category_id
        WHERE 
            c.category = %(cat_name)s"""

    cursor.execute(sql, {
        "cat_name": cat_name
    })

    nb_product = 0
    name = []
    for i, product_name in enumerate(cursor):
        print(f"{i+1}. {product_name[0]}")
        nb_product = i + 1
        name.append(product_name[0])
    cursor.close()

    while True:
        print()
        product = input('choississez un produit par son numéro : ')
        try:
            product = int(product)

        except ValueError:
            print("Vous devez choisir un nombre")
        else:
            if not 0 < product< nb_product:
                print("Le produit doit être entre 1 et ", nb_product)
            else:
                break

    pro_selected = ''
    print()
    for key, value in enumerate(name):
        if key == product-1:
            print(f"Vous avez choisi le produit : {value}")
            pro_selected = value
    print()

    return pro_selected


# ~ if __name__ == '__main__':
