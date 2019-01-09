Robot désherbeur.
Groupe Epaav.
=============

## Etapes :

To do => Plan => Develop => Test => Deploy => Done 

To do => Plan : When someone pick this task to do.

Develop => Test : When it’s normaly working, you just need to test.

Test => Deploy : Les tests sont passés, il reste a faire une pull request dans le master.

Deploy => Done : La taĉhes est merge sur le master.

## Taches :

### **Robot**

Robot1 : Modélisation du Robot sous GAZEBO 

Contraintes : Inclus dans un cube de 0.5m de côté.

Robot 2 : Modélisation Robot équations d’état. 

Contraintes : Vitesse linéaires entre 0 et 10 km/h

Robot 3 : Capteurs de Navigation.

Gps, Sonars, encodeur avec des erreurs de mesures.

## **Environnement** :

ENV 1 : Modélisation cour sous Gazebo 

Contrainte : Cour plane de 10*10m grise 

ENV 2 : Modélisation du muret sous Gazebo 

0.5m de haut

ENV 3 : Modélisation des mauvaises herbes 

Contraintes : Cylindre vert de décors 10cm de hauteurs et entre 2 et 15 cm de diamètre.

## **La vision** :

VIS 1 : Detecter l’objet Vert

VIS 2 : Localiser l’herbe

VIS 3 : Modéliser la Caméra

## **Gestion de projet**:

GDP 1 : Mettre en place Github

GDP 2 : Mettre en place Waffle

GDP 3 : Mettre en place une procédure de workflow

## **Le Laser** :

Laser 1 : Modéliser le laser
Contrainte : Cylindre de 15 cm de long et 5 cm de diamètre.

Laser 2 : Modéliser le bras articulé
Sous sujet 1.

Laser 3 : Modéliser la suppresion des herbes 
Contrainte : 3 minutes pour supprimer l’herbe

Laser 4 : Asservir suivant une position. (Cinématique inverse)
