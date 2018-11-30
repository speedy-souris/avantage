#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import time

import mysql.connector

from db_processing import backup_product as b_prod
from db_processing import erase_data as erase_db
from prod_processing import check_data as c_data
from prod_processing import menu_category as m_cat
from prod_processing import menu_select as m_select
from prod_processing import menu_url as m_url
from prod_processing import read_substitute as r_sub
from prod_processing import select_prod as s_prod
from prod_processing import substitutes_display as d_sub


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
            database=self.database,
        )
        return self.db_con


# +-------------------------+
# |                         |
# |    continuity module    |
# |     for the program     |
# |                         |
# + ------------------------+
def continuity(data, db_con):
    selection = ""
    while True:
        print()
        selection = input("Voulez vous continuez ? (Oui / Non) : ")
        if selection.lower() == "o":
            os.system("clear")
            m_cat(data, db_con)
            m_select(data, db_con)
        elif selection.lower() == "n":
            break


def cat_menu(data, db_con):
    os.system("clear")
    m_cat(data, db_con)
    return m_select()
    
    
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

    # check data
    data = c_data(db_con)

    # display menu category
    select = cat_menu(data, db_con)

    # recall loop
    while True:
        # update Data Base
        if select == "m":
            while True:
                print()
                print("Attention la mise à jour de la base de donnée ")
                print("éfface toutes les données ")
                print("ainsi que les enregistrements du choix de produit")
                print()
                update = input(
                    "Voulez vous vraiment continuez ? (Oui / Non) : "
                )
                if update.lower() == "o":
                    erase_db(db_con)
                    m_url(db_con)
                    print("Mise à Base de donnée terminé. ")
                    time.sleep(1.3)
                    os.system("clear")
                    break

                elif update.lower() == "n":
                    os.system("clear")
                    break

        # registered products
        elif select == "p":
            r_sub(data, db_con)
            os.system("clear")
        
        select = cat_menu(data, db_con)
            
    

        # ~ elif select == "o":
            # ~ while True:
                # ~ cat_id = ""
                # ~ cat_name = []
                # ~ prod_name = []
                # ~ sub_id = []
                # ~ while True:
                    # ~ print()
                    # ~ cat_id = input(
                        # ~ "choississez une catégory de produit par son numéro : "
                    # ~ )

                    # ~ try:
                        # ~ cat_id = int(cat_id)
                    # ~ except ValueError:
                        # ~ print("Vous devez choisir un nombre")
                    # ~ else:
                        # ~ if not 0 < cat_id < 25:
                            # ~ print("La catégorie doit être entre 1 et 24")
                        # ~ else:
                            # ~ break

                # ~ cat_name = [data[cat_id - 1][0], cat_id]
                # ~ print("Vous avez choisi la catégorie ", cat_name[0].upper())

                # ~ time.sleep(1.5)
                # ~ os.system("clear")

                # ~ prod_name = s_prod(cat_name[0], cat_name[1], db_con)

                # ~ if not (prod_name):
                    # ~ print()
                    # ~ print(
                        # ~ "Il n'y a pas de grade nutritionel dans cette catégorie !"
                    # ~ )
                    # ~ print()
                # ~ sub_id = d_sub(prod_name[0], cat_name[1], db_con)
                # ~ break
            # ~ if not (sub_id):
                # ~ print()
                # ~ print("Il n'y a pas de produit choisi !")
                # ~ print()
            # ~ b_prod(cat_name[1], sub_id[1], sub_id[0], db_con)
            # ~ break

        # ~ elif select == "n":
            # ~ print()
            # ~ print("Pas de choix effectuer...")
            # ~ break

    # closing database
    db_con.close()


if __name__ == "__main__":
    main()
