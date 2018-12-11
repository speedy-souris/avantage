"""main module that launches the script
test if the database is empty
filled in the case with local JSON data
then displays the general menu containing the product category list
to choose to obtain a substitute product of better nutrional quality"""

# ! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os

import mysql.connector

from prod_processing import cat_menu as c_menu
from prod_methode import check_data as c_data


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

    student = mysql.connector.connect(
        host="localhost",
        user="student",
        password="OpenClassRooms",
        database="food_product"
    )

    # check data
    d_json = c_data(student)
    # Menu category
    c_menu(d_json, student)

    # closing database
    student.close()


if __name__ == "__main__":
    main()
