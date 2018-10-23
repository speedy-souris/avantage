#! /usr/bin/env python3
# -*- coding:utf-8 -*-

def cat_select(cat_name, database, connect):
    connect.dbConnect()

    sql = """SELECT p.name as nom_produit
        FROM product as p
        INNER JOIN category_product as cp
            ON p.id = cp.product_id
        INNER JOIN category as c
            ON c.id = cp.category_id
        WHERE 
            c.category = %(cat_name)s"""

    connect.cursor.execute(sql, {
        "cat_name": cat_name
    })

    for i, product_name in enumerate(connect.cursor):
        print(f"{i+1}. {product_name}")
