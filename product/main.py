"""main module that launches the script
test if the database is empty
filled in the case with local JSON data
then displays the general menu containing the product category list
to choose to obtain a substitute product of better nutrional quality"""

#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os

import mysql.connector

from prod_processing import cat_menu as c_menu
from prod_processing import check_data as c_data


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
        Args:
            - self.db_con (mysql.connector)
            - self.host
            - self.user
            - self.password
            - self.database"""

        self.db_con = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        return self.db_con


# +-----------------+
# |  main function  |
# +-----------------+
def main():

    """main function of starting the script

    Vars:
        student        ==> storage of data connection to the database
                            connection server : 'localhost'
                            pseudo 'student'
                            password 'OpenClassRooms'
                            database 'food_product'

        d_json         ==> memorization of the name
                            of the product category

    Funcs:
        check_data() alias c_data ==> test module at the first start
                                        of the script
                                        see more in the module itself

        cat_menu() alias c_menu ==> Display module of
                                        the general category menu
                                        see more detail in the module itself"""

    os.system("clear")
    print("le programme de Substitution de produit est lancé ! ")
    print()

    student = DBConnect(
        "localhost",
        "student",
        "OpenClassRooms",
        "food_product"
    )
    db_con = student.db_connect()

    # check data
    d_json = c_data(db_con)
    # Menu category
    c_menu(d_json, db_con)

    # closing database
    db_con.close()


if __name__ == "__main__":
    main()
