# Substitution d'ingrédients

## Élève OpenClassRoom

### Description du Projet

>La startup *"Pur Beurre"* qui connaît bien les habitudes alimentaires des français a décider de développer une application sur la substitution d'ingrédient.
>
>Leur restaurant *"RATATOUILLE"* de bonne renommé a remarquer que ces clients étaient désireux de changer leur habitudes alimentaire
l'application développer pour le restaurant est capable de substituer un ingrédient alimentaire dans une catégorie donnée, par un autre ingrédient alimentaire de la même catégorie, avec des caractéristiques moins nocives pour la santé humaine.
>
>Le client choisi une catégorie d'ingrédient fournit par l'application , ensuite l'application affiche une liste d'ingrédient à substituer,
>
>le client doit en choisir un afin que l'application lui donne un meilleur compromis alimentaire.

### Mise en place et utilisation de la structure de l'application

L'application récupère les catégories d'ingrédients alimentaires fournies par l' API *"OPENFOODFACT"* sous forme de fichier *JSON*, en extrait les différents produits et les stocke dans une bases de données.

Dans un terminal, l'application affiche
* une liste de nombre correspondant aux catégories de produits
* Le client choisit la catégorie en fonction de son chiffre
* Une liste  de nombre correspondant aux ingrédients à substituer
* Le client choisit l'ingrédient dont il veut obtenir un équivalent moins toxique pour la santé
* une liste du ou des ingrédient(s) substituer avec les caractéristique moins toxique, le lieu, le grade nutritinnel ainsi qu'un lien direct sur la fiche provenant de l'*API OPENFOODFACT* est fourni au client

### Technique de construction du projet

Importation des catégories de produits alimentaires de l' *API OPENFOODFACT* sous le format de fichier JSON  
Choix du langage standard de la base de donnée *SQL* pour organiser la gestion des produits,  
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





### Installation du projet 

**Pour infos :**
>la procédure d’installation décrite et le codage du script ont été effectués
>sous le système Linux UBUNTU 18.04 64 bits pour une utilisation en console

**Installation à partir du fichier ZIP**
>décompressez le fichier projet5.ZIP dans le répertoire de votre choix 
>
>positionnez vous dans le répertoire ou vous venez de décompresser le fichier
>
>verifiez bien que mysql soit installer sur votre ordinateur
> 
>Ensuite ouvrir le serveur MySQL en mode administrateur dans la console
>avec la commande *sudo mysql* puis validez avec la touche *ENTRE* 
>puis renseignez votre mot de passe administrateur
>(aucun caractère ne s’affiche pendant la saisie)
>
>une fois connecter au server mysql la console affiche **Mysql>**
>
>entrez la commande **SOURCE product_substitution.sql;** ce qui a pour effet de créer la base de données
>
>**food_product** avec ses quatre tables
>* **product**,
>* **category**,
>* **category_product**,
>* **substitution_product**
>
>et de vous connecter à la base de données **food_product**
>
>Vérifiez que tout c'est bien passé en tapant la commande **SHOW TABLES;**
>
>Quittez la base de données avec la commande **quit** ou **exit**
>
>Verifiez que python3 soit installer sur votre ordinateur
>
>Commencez par installer les dépendances dont le script à besoin
>avec la commande **pip install -r requirements.txt**
>
>Tapez la commande **cd product** pour venir dans le repertoire des modules
>
>Vous pouvez maintenant lancer le script avec la commande **python3 main.py**


