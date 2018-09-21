# -*- coding: utf-8 -*-

import mysql.connector
from category import *

conn = mysql.connector.connect(host="localhost",user="student",password="OpenClassRooms", database="product")
cursor = conn.cursor()
conn.close()

print('')
print ('le programme de Substitution de prouit est lancé ! ')
print('')
#
#  Product selection menu
#
print('1.Boissons énégétiques')
print('2.Bonbons')
print('3.Charcuteries')
print('4.Chocolats')
print('5.Conserves')
print('6.Fromages')
print('7.Fruits')
print('8.Fruits confits')
print('9.Gateaux')
print('10.Glaces')
print('11.Jus de fruits')
print('12.Laits')
print('13.Pâtes de fruit')
print('14.Pâtes')
print('15.Pâtes à tartiner')
print('16.Pizzas')
print('17.Poissons')
print('18.Poissons d\'élevages')
print('19.Réglisse')
print('20.Riz')
print('21.Sorbets')
print('22.Viandes')
print('23.Vins')
print('24.Yaourts')
print('')
category = input('choississez une catégory de produit par son numéro : ')


