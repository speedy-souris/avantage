# Substitution d'ingrédients

## Eleve OpenClassRoom

### Description du Projet

>La startup *"Pur Beurre"* qui connaît bien les habitudes alimentaires des français a décider de développer une application sur la substitution d'ingrédient.
>
>Leur restaurant *"RATATOUILLE"* de bonne renomé a remarquer que ces clients étaient désireux de changer leur habitudes alimentaire
l'application développer pour le restaurant est capable de substituer un ingrédient alimentaire dans une catégorie donnée, par un autre ingrédient alimentaire de la même catégorie, avec des caractéristiques moins nocives pour la santé humaine.
>
>Le client choisi une catégorie d'ingrédient fournit par l'application , ensuite l'application affiche une liste d'ingrédient à substituer,
>
>le client doit en choisir un afin que l'application lui donne un meilleur compromis alimentaire.

### Mise en place et utilisation de la structure de l'application

L'application récupére les catégories d'ingrédients alimentaires fournies par l' API *"OPENFOODFACT"* sous forme de fichier *JSON*, en extrait les différents produits et les stocke dans une bases de données.

Dans un terminal, l'application affiche
* une liste de nombre correspondant aux catégories de produits
* Le client choisit la catégorie en fonction de son chiffre
* Une liste  de nombre correspondant aux ingrédients à substituer
* Le client choisit l'ingrédient dont il veut obtenir un équivalent moins toxique pour la santé
* une liste du ou des ingrédient(s) substituer avec les caractéristique moins toxique, le lieu, le prix ainsi qu'un lien direct sur la fiche provenant de l'*API OPENFOODFACT* est fourni au client

### Technique de construction du projet

Importation des catégories de produits alimentaires de l' *API OPENFOODFACT* sous le format de fichier JSON  
Choix du langage standard de la base de donnée *SQL* pour oragoniser la gestion des produits,  
choix du *SGBDR MySQL*  
Script de traitement développer en *PYTHON*

1. Créez un modèle graphique de la BD
2. A partir de ce modèle créez les tables SQL
3. Importez les données catégories produits dans un fichier au format JSON
4. Importez les produits de chaque catégorie dans un fichier au format JSON
5. Insérer les données des fichiers JSON dans la BD
6. Dans un terminal choisissez la catégorie de produit
7. Affichage des produits a substituer selon leur indice de classement
8. Affichage de la fiche du produit substituer avec *l'URL de l'API OPENFOODFACT*
9. Enregistrement du choix sur le produit a substituer ainsi que le produit substituer
