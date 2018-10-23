#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import selection as s_prod


"""link module containing the TABLE category id and the TABLE product id"""


def menu_product(name):

    print()
    print('menu produit de la categorie ', name)
    print()

    s_prod.cat_select(name)


if __name__ == '__main__':

    menu_product('chocolats')
