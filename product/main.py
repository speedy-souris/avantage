#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import mysql.connector

from prod_processing import menu_category as m_cat
from prod_processing import prod_select as m_prod
from prod_processing import display_substitutes as s_prod


#  ------------------------
# |  Class for connection  | 
# |     to the database    |
#  ------------------------
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

        print("mise a jour de la base de donnée...")
        print()
        self.db_con = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.db_con

#  -----------------
# |  main function  |
#  -----------------
def main():
    print()
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
    s_prod(product[0], product[1], db_con)

    # closing database
    db_con.close()


if __name__ == "__main__":
    main()
    choix = ""
    while choix != 'o' or choix != 'n':
        print()
        choix = input("Voulez vous continuez Oui ou Non ? : ")
        if choix == "o":
            main()
        elif choix == "n":
            break
