#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import menu_category as m_cat
import menu_product as m_prod

from connect import DBConnect 

print('')
print('le programme de Substitution de produit est lancé ! ')
print('')

student = DBConnect("localhost", "student", "OpenClassRooms", "food_product")

m_cat.menu_category(student)  # display menu category
name = m_cat.menu_category(student)

print(name)
m_prod.menu_product(name, student)  # display menu product

student.database.close()  # closing database

