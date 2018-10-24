#! /usr/bin/env python3
# -*- coding:utf-8 -*-

#  importation module
import mysql.connector

from prod_processing import menu_category as m_cat

# definition of the DBConnect class
class DBConnect:

    """the DBConnect class is characterized by:
    - his host
    - his user
    - his password
    - his database"""

    #  DBConnect class constructor method
    def __init__(self, host, user, password, database):

        """definition of attributes:
        - host
        - user
        - password
        - database"""

        print("Création de connection à la base de donnée...")
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    # initialization method at the connection of the database
    def db_connect(self):

        """method for connection by the student to the database:
        << food_product >>"""

        print("ouverture de la base de donnée...")
        self.db_con = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )

        return self.db_con

def main():
    print()
    print('le programme de Substitution de produit est lancé ! ')
    print()

    student = DBConnect("localhost", "student", "OpenClassRooms", "food_product")
    db = student.db_connect()

    m_cat(db)  # display menu category

    db.close()  # closing database


if __name__ == "__main__":
    main()
