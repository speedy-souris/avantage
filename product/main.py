#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time

import mysql.connector

from prod_processing import menu_category as m_cat
from prod_processing import select_prod as m_prod
from prod_processing import substitutes_display as s_prod
from prod_processing import read_substitute as r_sub
from db_processing import erase_data as erase_db
from db_processing import backup_product as b_prod


# +------------------------+
# |  Class for connection  |
# |     to the database    |
# + -----------------------+
class DBConnect:

    """the DBConnect class is characterized by:
    - his host
    - his user
    - his password
    - his database"""

    # DBConnect class constructor method
    def __init__(self, host, user, password, database):

        """
        constructor of the DBConnect class
        Args:
            - host (BD server address)
            - user (username)
            - password (user password)
            - database (name of the database)"""

        self.host = host
        self.user = user
        self.password = password
        self.database = database

    # initialization method at the connection of the database
    def db_connect(self):

        """method of connecting the user to the database:
        """

        self.db_con = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.db_con


# +-----------------+
# |  main function  |
# +-----------------+
def main():

    os.system("clear")
    print("le programme de Substitution de produit est lancé ! ")
    print()

    """main function of starting the script

    - Variable 'student' with connection ID of the database
        - Class BDConnect
        - 'localhost' connection server
        - pseudo 'student'
        - 'OpenClassRooms' password
        - database 'food_product'

    - Connection variable to database 'db_con'"""

    # opening database
    student = DBConnect(
        "localhost",
        "student",
        "OpenClassRooms",
        "food_product"
    )
    db_con = student.db_connect()

    # display menu category
    category = m_cat(db_con)
    # display menu product
    product = m_prod(category[0], category[1], db_con)

    # substituted product display
    backup = []
    if not(product):
        print()
        print("Il n'y a pas de grade nutritionel dans cette catégorie !")
    else:
        backup = s_prod(product[0], product[1], db_con)

    # backup of substituting and substituted products
    if not(backup):
        print()
        print("Il n'y a pas de produit choisi")
    else:
        b_prod(product[1], backup[1], backup[0], db_con)

    # display product list saved and database update
    time.sleep(1.5)
    os.system("clear")

    print()
    print("1. Voir la liste des produits enregistrés")
    print("2. mise a jour de la base de donnée")

    starting = ""
    cat_name = []
    while True:
        print()
        starting = input("Choisissez 1 ou 2 : ")
        print()

        try:
            starting = int(starting)
        except ValueError:
            print("Vous devez choisir un nombre")
        else:
            if not 0 < starting < 3:
                print("La catégorie doit être entre 1 et 2")
            else:
                break

    # display registered products
    if starting == 1:
        r_sub(db_con)

    # update of the database
    elif starting == 2:
        print()
        print("Attention la mise à jour de la base de donnée ")
        print("éfface toutes les données ")
        print("ainsi que les enregistrements du choix de produit")
        while True:
            print()
            update = input("Voulez vous vraiment continuez ? (Oui/Non) : ")
            if update.lower() == "o":
                erase_db(db_con)
                break
            elif update.lower() == "n":
                break

    # closing database
    db_con.close()


if __name__ == "__main__":
    main()
    selection = ""
    while True:
        print()
        selection = input("Voulez vous continuez ? (Oui/Non) : ")
        if selection.lower() == "o":
            main()
        elif selection.lower() == "n":
            break
