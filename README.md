# RobotDesherbeur
UV 5.8 - modelisation d'un robot desherbeur

lien vers la page waffle: https://waffle.io/LEPAAV/RobotDesherbeur/join

[![Waffle.io - Columns and their card count](https://badge.waffle.io/LEPAAV/RobotDesherbeur.svg?columns=all)](https://waffle.io/LEPAAV/RobotDesherbeur)

___

# <center> Utilisation de ***Git*** </center>



Voici un tuto pour utiliser Git correctement avec les commandes associées !

## Étape 1

Se mettre mettre la branche master locale sur laquelle nous nous trouvons :
***git checkout master***

Récupérer les dernières mises à jour sur le dossier distant :
***git pull --rebase upstream master***

## Étape 2

Créer une nouvelle branche et se positionner sur celle-ci : ***git checkout -b mabranche***

## Étape 3

Faire les modifications souhaitées puis regarder le status de git localement : ***git status***

Ajouter les modifications et suivre les fichiers créés : ***git add <some-file>***

Enregistrer les modifications localement : ***git commit -m "mon commentaire"***

## Étape 4

On souhaite intégrer les dernières mises à jour du master distant avant de fusionner notre branche.

On change dans un premier temps de branche, on va sur son master pour que celui-ci ne diverge pas du upstream :
***git checkout master***

On récupère les modifications upstream. Pour cela, exécuter la commande :
***git pull --rebase upstream master***

On change de branche pour ajouter les dernières fonctionnalités à notre branche :
***git checkout mabranche***

On récupère les dernières fonctionnalités sur notre branche :
***git pull --rebase master***

## Étape 5

Sauvegarder les modifications sur la branche distante de son dépôt:
***git push origin mabranche***

On fusionne avec le master. Pour cela on va sur le master :
***git checkout master***

Puis on merge :
***git merge mabranche***

## Étape 6

Créer un pull request sur github !

# Compléments

***Si quelqu'un considère qu'il y a des commandes utiles qui ne sont pas précisées au dessus, les mettre dans cette section.***
