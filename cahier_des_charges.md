# Cahier des charges

Cahier des charges du projet informatique Python visant à faciliter la planification et la gestion des prestations des différents clubs de l'association du BDA.

**Élèves :**
- Erwan
- Matteo
- Krawlya

## Contexte et définition du problème

Le BDA de TSP et d'IMT-BS fédère de nombreux clubs proposant des prestations (animations, interventions, matériel, etc.).

Aujourd'hui, la gestion de ces prestations est pénible car le « client final » doit s'adresser tantôt au BDA, tantôt directement au club, tantôt aux deux en parallèle.
Cette organisation multiplie les allers-retours entre interlocuteurs et allonge les délais de réponse. Dans certains cas, une demande finit par être mise de côté pendant le processus et la prestation est purement et simplement compromise.

Trois difficultés principales ressortent :

- **Un point d'entrée ambigu** : le client ne sait pas à qui adresser sa demande.
- **Un suivi inexistant** : ni le client ni le club ne disposent d'une vision claire de l'état d'avancement d'une demande.
- **Aucune capitalisation** : chaque prestation est traitée comme un cas isolé, sans réutilisation de l'expérience acquise sur les prestations précédentes.

## Objectif du projet

Concevoir un outil offrant une meilleure gestion des prestations (acceptation, refus, suivi, etc.) en adoptant une approche par **tickets**. Chaque demande devient un ticket disposant d'un état, d'un historique et d'interlocuteurs identifiés, ce qui permet :

- un suivi lisible et partagé de chaque demande, de sa création à sa clôture ;
- une capitalisation sur le long terme, les prestations passées servant de base aux suivantes.

## Périmètre du projet

Le projet couvre les prestations susceptibles d'être proposées par les clubs de l'association : leur publication par les clubs, leur demande par les clients, le suivi des tickets associés et la planification de leur réalisation.

## Description fonctionnelle des besoins

### Interface web côté client 
consultation du catalogue des prestations et mise « au panier » de celles souhaitées.

 - la possibilité de voir la liste de prestation et les détails de prestations ne doivent pas necessiter de compte.

 - page d'accueil : sélection du club dont on veut la prestation. pour chaque club on y voit le logo ainsi qu'une courte description du club. les prestations sont cliquables et permettent d'accéder à la page listant les prestations du club en question

 - page de prestations d'un clubs : liste les prestations proposées par le club, avec une courte description (et une photographie)

 - page de prestation : décrit la prestation en détail, avec  le nom du prestataire (le club), les délais prévisionnels et tout détail jugé utile par le prestataire. Le client peut soit directement faire une demande de prestation soit mettre au panier une prestation (dans le deuxième cas la prestation sera sauvegardée dans le panier sans avoir besoin de remplir le formulaire de prestation)

 - demande de prestation : lorsqu'une demande de prestation est faite depuis la page de prestation ou depuis le panier, la page de demande de prestation est ouverte. Elle permet de remplir un formulaire pour préciser les demandes du client.

 - page des prestations en cours : lorsqu'une demande de prestation est validée par le client, un ticket est créé dans la page prestations en cours. chaque prestation est affichée avec son nom, le nom du prestataire, le statut de la prestation, une flèche permettant de voir le formulaire envoyé ainsi qu'un bouton permettant d'accéder à un chat réservé à cette prestation précise.

 - un onglet notifications permet d'accéder aux conversations ayant de nouveaux messages

### Interface web côté club
création et gestion des prestations par les personnes autorisées au sein des clubs et associations.

- droits : Il faut différents droits, possiblement gérées par les responsables de prestation. L'administrateur général (présidents de club) peut gérer les droits des autres membres du club, les responsables de prestation peuvent avoir tous les droits pour une prestation donnée (l'administrateur général les a aussi par défaut), les membres des clubs en sont collaborateurs et peuvent voir l'avancée du projet, le graphe de planification. ils sont nommés par le responsable de prestation ou l'administrateur général.

- page d'accueil : permet de voir les prestations proposées. un bouton ajouter une prestation doit être présent. on peut accéder à la page de visualisation et modification ainsi qu'à celle de gestion des prestations de ce type en cours.

- page de présentation d'une prestation (accessible depuis la page d'accueil). Elle est modifiable et permet d'accéder au formulaire de demande de prestation ainsi qu'au template de gestion interne. 

- page de template : permet de visualiser et modifier le template de gestion (étapes de la presta, dates, personnes impliquées(droits))

- page de formulaire : permet de visualiser et modifier le formulaire donné au client. 

- lien client : le client ne peut pas faire de demande de prestation si cette prestation est en cours de modification. les modifications apparaissent sur la version client une fois effectuées.


### Système de notification pour l'attribution des prestations

  - produire une synthèse de la prestation attribuée (budget, acteurs, lieux, dates, etc.) et en informer les utilisateurs concernés par une notification premier message dans le chat de la prestation ainsi que mail envoyé à la personne;
  - signaler périodiquement l'avancée de la prestation aux utilisateurs.

### Tickets

- Permettre au client de créer des tickets rattachés à sa prestation, avec un service de « chatbox » servant d'espace d'échange et de gestion des conflits.
- Définir une **machine à états** décrivant les transitions possibles d'un ticket au cours de sa vie (par exemple : création, acceptation, refus, clôture), afin que l'évolution d'une demande soit explicite et contrôlée.

### Planification des prestations

- **Diagrammes PERT / GANTT** :
  - création de « templates » de diagrammes réutilisables
  - affectation de membres à des sous-tâches ;
  - capitalisation sur les templates existants pour en dériver de nouveaux ou factoriser les parties communes
  - affichage du diagramme par le club, avec possibilité de modification si nécessaire.
- **Notification des membres** impliqués dans une prestation lorsqu'ils doivent fournir un jalon clef ou réaliser une tâche ponctuelle

## Contraintes

- Développement en **Python**.
- L'outil prend la forme d'une **application web**, accessible aux clients comme aux membres des clubs.
- Gestion des droits : distinction entre les utilisateurs clients et les personnes autorisées au sein des clubs et associations.
- Sécurité : limiter le nombre de demandes qu'un même utilisateur peut effectuer sur une période donnée, afin d'empêcher les abus et les tentatives d'automatisation massive de l'envoi de demandes (attaques de type DDoS).


## Délais (date de réalisation attendue)

**Prochaine séance** : répartir les rôles au sein de l'équipe (qui fait quoi) et choisir les technologies, l'architecture et les fonctionnalités.

**Date de rendu** : 9 décembre
