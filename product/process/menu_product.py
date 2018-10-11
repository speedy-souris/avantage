name = ''
while True:

    category = input('choississez une catégory de produit par son numéro : ')

    try:
        category = int(category)

    except ValueError:
        print("Vous devez choisir un nombre")
    else:
        if not 0 < category < 25:
            print("La catégorie doit être entre 1 et 24")
        else:
            break

name = choix[category-1][0]
print(name)
