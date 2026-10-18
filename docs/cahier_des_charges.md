# Cahier des charges

Cahier des charges du projet informatique Python visant à faciliter la planification et la gestion des prestations des différents clubs de l'association de l'INT.

**Étudiants :**

- Erwan
- Matteo
- Krawlya

## Contexte et définition du problème

Les associations de TSP et d'IMT-BS fédères de nombreux clubs proposant des prestations de multiples natures (animations, interventions, matériel, etc.).

Aujourd'hui, les prestations sont suivies simplement par un seul commanditaire via le contact du président du club généralement via un gorupe Whatsapp. 
Cette organisation multiplie les allers-retours entre interlocuteurs et allonge les délais de réponse. Dans certains cas, une demande finit par être mise de côté pendant le processus et la prestation est purement et simplement compromise.

Trois difficultés principales ressortent :

- **La connaissance des services proposées** : sans avoir les bons contacts un grand nombre de possibilité sont inconnues.
- **Un suivi inexistant** : ni le client ni le club ne disposent d'une vision claire de l'état d'avancement d'une demande.
- **Aucune capitalisation** : chaque prestation est traitée comme un cas isolé, sans réutilisation de l'expérience acquise sur les prestations précédentes.

Nous voulons ici proposer une solution comportant un catalogue des prestations proposées par les clubs en remplissable par eux même puis une interface de gestion de prestation et discussion accessible par les membres du club. 


## Objectif du projet

Concevoir un outil offrant une meilleure gestion des prestations (acceptation, refus, suivi, etc.) en adoptant une approche par **tickets**. Chaque demande devient un ticket disposant d'un état, d'un historique et d'interlocuteurs identifiés, ce qui permet :

- Un suivi lisible et partagé de chaque demande, de sa création à sa clôture.
- Une capitalisation sur le long terme, les prestations passées servant de base aux suivantes.

## Périmètre du projet

Le projet couvre les prestations susceptibles d'être proposées par des clubs et l'association : leur publication par les clubs, leur demande par les clients, le suivi des tickets associés et la planification de leur réalisation.

## Description fonctionnelle des besoins

### Interface web côté client

Consultation du catalogue des prestations.

- La possibilité de voir la liste des prestations proposées et les détails associés ne doivent pas necessiter de compte. (MVP) 

- Page d'accueil : Liste des clubs et de leur prestations. Pour chaque club on y voit le logo. La liste des clubs sont cliquables et permettent d'accéder à la page listant les prestations du club en question. (MVP) 

- Page de prestations d'un club : liste les prestations proposées par le club, son logo et une courte description. (Lot 1) 

- Page de prestation : décrit la prestation en détail, avec le nom du club, les délais prévisionnels, prix et tout détail jugé utile par le prestataire. Le client peut directement faire une demande de prestation. (MVP) 

- Demande de prestation : lorsqu'une demande de prestation est ouverte, une page permet de remplir un formulaire pour préciser les demandes du client. (MVP) 

- Page des prestations en cours : lorsqu'une demande de prestation est validée par le client, un ticket est créé dans la page prestations en cours. Chaque prestation est affichée avec son nom, le nom du prestataire, le statut de la prestation ainsi qu'un bouton permettant d'accéder à un chat réservé à cette prestation précise. (Lot 1) 

- Un onglet notifications permet d'accéder aux conversations ayant de nouveaux messages. (Lot 2) 

### Interface web côté club

Création et gestion des prestations par les personnes autorisées au sein des clubs et associations.

- Droits : le président du club peut gérer les droits des autres membres du club, les responsables de prestation peuvent avoir tous les droits pour une prestation donnée, les membres des clubs en sont collaborateurs et peuvent voir l'avancée du projet, le graphe de planification. ils sont nommés par le responsable de prestation ou le président. (MVP) 

- Page d'accueil : permet de voir les prestations proposées. un bouton ajouter une prestation doit être présent. on peut accéder à la page de visualisation et modification ainsi qu'à celle de gestion des prestations de ce type en cours. (MVP) 

- Page de présentation d'une prestation : Elle est modifiable et permet d'accéder au formulaire de demande de prestation ainsi qu'au template de gestion interne. (MVP) 

- Page de template : permet de visualiser et modifier le template de gestion (étapes de la presta, dates, personnes impliquées(droits)) (Lot 2) 

- Page de formulaire : permet de visualiser et modifier le formulaire donné au client. (Lot 1) 

### Système de notification pour l'attribution des prestations

- Produire une synthèse de la prestation attribuée (budget, acteurs, lieux, dates, etc.) et en informer les utilisateurs concernés par une notification premier message dans le chat de la prestation ainsi que mail envoyé à la personne. (Lot 2) 

- Signaler périodiquement l'avancée de la prestation aux utilisateurs. (Lot 2) 

### Tickets

- Permettre au client de créer des tickets rattachés à sa prestation, avec un service de « chatbox » servant d'espace d'échange et de gestion des conflits. (Lot 1)

- Définir une **machine à états** décrivant les transitions possibles d'un ticket au cours de sa vie (par exemple : création, acceptation, refus, clôture), afin que l'évolution d'une demande soit explicite et contrôlée. (Lot 1) 

### Planification des prestations

- **Diagrammes PERT / GANTT** : (Lot 3) 
  - création de « templates » de diagrammes réutilisables
  - affectation de membres à des sous-tâches.
  - capitalisation sur les templates existants pour en dériver de nouveaux ou factoriser les parties communes
  - affichage du diagramme par le club, avec possibilité de modification si nécessaire.
- **Notification des membres** impliqués dans une prestation lorsqu'ils doivent fournir un jalon clef ou réaliser une tâche ponctuelle.

## Contraintes

- Développement en **Python**.
- L'outil prend la forme d'une **application web**, accessible aux clients comme aux membres des clubs.
- Gestion des droits : distinction entre les utilisateurs clients et les personnes autorisées au sein des clubs et associations.
- Sécurité : limiter le nombre de demandes qu'un même utilisateur peut effectuer sur une période donnée, afin d'empêcher les abus et les tentatives d'automatisation massive de l'envoi de demandes (attaques de type DDoS).

## Délais (date de réalisation attendue)

**Date de rendu** : 9 décembre
