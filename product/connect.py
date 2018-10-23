#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import mysql.connector


class DBConnect:  # definition of the DBConnect class

    """the DBConnect class is characterized by:
    - his host
    - his user
    - his password
    - his database"""

    database = ''
    cursor = ''
    #  DBConnect class constructor method
    def __init__(self, host, user, password, database):

        """definition of attributes:
        - host
        - user
        - password
        - database"""

        self.host = host
        self.user = user
        self.password = password
        self.database = database

    # method for initializing the constructor of the DBConnect class
    def dbConnect(self):

        """method for connection by the student to the database:
        << food_product >>"""

        self.database = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        self.cursor = self.database.cursor()


