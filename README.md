
# projet-quoridor

## Présentation générale du projet

On propose dans ce projet d'implémenter une version librement inspirée du jeu Quoridor.
Le principe général du jeu est le suivant: chaque joueur cherche à être le premier à traverser le terrain.
Chaque joueur jour à tour de rôle. Les coups possibles sont:
* le déplacement de son joueur,
* le dépôt d'un mur de 2 cases sur le plateau.

Les règles de déplacement sont les suivantes:
* il est possible de se déplacer de une case, dans toutes les directions sauf les diagonales. On suppose ici que les joueurs ne se bloquent pas entre eux, et qu'ils peuvent éventuellement être sur la même case à un moment donné.

Les règles de placement sont les suivantes:
* les murs sont constitués de 2 "briques" (2 cases) qui doivent posés côte-à-côte horizontalement ou verticalement
* les murs sont ici posés sur les cases (et non entre elles comme c'est le cas dans le jeu de Quridor classique),
* il est interdit de poser des murs sur les lignes où sont placés initialement les joueurs
* il est interdit de déposer un mur à un endroit qui fermerait tout chemin d'un des autres joueurs vers ses objectifs.


Note: bien que présenté ici pour 2 joueurs, le jeu peut être joué à 4 joueurs. Nous laissons cette perspective comme extension possible de votre projet.

### Bibilographie
Article Wikipedia [Quoridor](https://en.wikipedia.org/wiki/Quoridor)

## Modules disponibles

### Module pySpriteWorld

Pour la partie graphique, vous utiliserez le module `pySpriteWorld` (développé par Yann Chevaleyre) qui s'appuie sur `pygame` et permet de manipuler simplement des personnages (sprites), cartes, et autres objets à l'écran.

Une carte par défaut vous est proposée pour ce projet (`quoridorMap`): elle comporte 2 joueurs.
Les murs de chaque joueur sont initialement placés derrière lui. Dans cette carte, chaque joueur dispose de 15 murs, mais cela peut facilement être modifié.

La gestion de la carte s'opère grâce à des calques:
* un calque `joueur`, où seront présents les joueurs
* un calque `ramassable`, qui contient ici les murs


Les joueurs et les ramassables sont des objets Python sur lesquels vous pouvez effectuer des opérations classiques.
Par exemple, il est possible récupérer leurs coordonnées sur la carte avec `o.get_rowcol(x,y)` ou à l'inverse fixer leurs coordonnées avec `o.set_rowcol(x,y)`.
La mise à jour sur l'affichage est effective lorsque `mainiteration()` est appelé.


Notez que vous pourrez ensuite éditer vos propres cartes à l'aide de l'éditeur [Tiled](https://www.mapeditor.org/), et exporter ces cartes au format `.json`. Vous pourrez alors modifier le nombre de joueurs ou de murs disponibles, par exemple.

Il est ensuite possible de changer la carte utilisée en modifiant le nom de la carte utilisée dans la fonction `init` du `main`:
`name = _boardname if _boardname is not None else 'quoridorMap'``
Une carte miniature vous est aussi proposée, pour plus de facilité pour les premiers tests.  

# Rapport de projet

## Groupe 1
**Saliou Barry**

## Description des choix importants d'implémentation

Pour faciliter la compréhension et la maintenance du code, j'ai choisi d'utiliser une architecture orientée objet pour la réalisation du projet. J'ai créé deux fichiers principaux :

* Le premier, nommé *utils*, contient plusieurs fonctions importantes pour le jeu, telles que la vérification du placement des murs, la recherche du chemin le plus court, l'initialisation du plateau, ainsi qu'un dictionnaire de correspondance contenant toutes les variables nécessaires pour l'actualisation du jeu.

* Le second fichier, appelé *strats*, contient les différentes stratégies du jeu, chacune étant une classe. J'ai utilisé l'héritage entre les classes pour pouvoir réutiliser des méthodes déjà implémentées.

En tout, j'ai implémenté cinq stratégies différentes pour le jeu. La première stratégie est `RandomStrat`, suivie de `AdaptivePlaymaker`, `TacticalPlayer` (qui hérite de AdaptivePlaymaker), `TrapAndBlock` (qui hérite de TacticalPlayer), et enfin `Trapmaster` (qui hérite de TrapAndBlock).

J'ai décidé de tester les stratégies sur un fichier notebook pour avoir plus de clarté et de facilité à visualiser les courbes de comparaison.

## Description des stratégies proposées

* RandomStrat : cette stratégie est une stratégie aléatoire, qui consiste à faire des choix arbitraires pour le joueur. Dans cette stratégie, le joueur choisi de façon aléaotoire soit de se deplacer ou de placer un mur, il place des murs de manière aléatoire s'il en a encore à placer. Sinon, il utilise l'algorithme A* pour calculer le chemin le plus court vers son objectif (fixé) du joueur et se déplace en conséquence. <br>
Cette stratégie ne prend pas en compte l'état actuel du jeu ni les actions de l'adversaire, et elle ne suit pas de plan précis pour gagner la partie. Cependant, elle peut être efficace pour perturber l'adversaire qui predit a chaque fois le de son adversaire avant de jouer.

*Le point commun de toutes les stratégies suivantes c'est qu'a chaque fois qu'un mur est posé, elles changent d'objectif et prend le plus proche.*

* AdaptivePlaymaker : Cette stratégie consiste à trouver trouver la meilleure action possible pour le joueur en fonction de la situation actuelle du jeu. <br>
Pour ce faire, le joueur calcule les distances entre sa position et celle de son adversaire, ainsi que les chemins possibles pour les deux joueurs. Ensuite, il prend une décision en fonction de la différence de distance entre les joueurs et de la distance entre l'adversaire et l'objectif du joueur.
Si le joueur est plus éloigné que son adversaire et que l'adversaire est à plus de 4 cases, ou si les deux joueurs sont à égale distance et que l'adversaire est à plus de 4 cases, ou si le joueur a déjà placé tous ses murs ou si c'est le début de la partie, le joueur se déplace vers son objectif. Sinon, il cherche la meilleure position pour placer un mur en explorant les positions possibles et en vérifiant si un mur bloque le chemin du joueur. Cette stratégie essaye en permance de prendre l'avantage sur l'adversaire.
Pour chercher la meilleure position possible, le joueur effectue une recherche en profondeur de taille 4.

* TacticalPlayer : Cette stratégie est une combinaison de la stratégie d'adaptation de l'AdaptivePlaymaker avec une approche plus tactique pour placer les murs et pour se deplacer. Dans cette stratégie on n'accepte le fait de perdre l'avantage sur la partie (contrairement à AdaptivePlaymaker), on se concentre sur le centre du jeu. le joueur cherche à atteindre le plus rapidement possible en ne plaçant aucun mur sur son chemin, une fois que l'adversaire est à 2 case de gagner la partie, le joueur commence à placer des murs, les murs sont placés de façon vertical en bloquant un coté du jeu et obligeant l'adversaire a rebrousser le chemin et changer de coté.
La profondeur de recherche pour trouver la meilleure position pour un mur dépend de la position de l'adversaire sur le plateau de jeu. c'est une stratégie intéressante car la valeur de la profondeur est variables, pour chaque emplacement de l'adversaire il y a une valeur de profondeur differente, la plus grande valeur c'est quand l'adversaire se trouve au mileu du plateau, c'est ce qui permet de controler le centre et de piéger facilement l'adversaire. 

* TrapAndBlock : Cette stratégie est différente des précédentes car elle a une double fonction, elle consiste à piéger l'adversaire en l'obligeant à se déplacer dans une certaine direction, nottament en obligeant l'adversaire à ce deplacer sur les bord, Cette strat commence par placer un mur à la première occasion, ensuite, elle suit l'adversaire et tente de placer des murs verticaux pour essayer d'enfermer l'adversaire dans une zone étroite tout en laissant croire à l'adversaire qu'il y a du chemin et qu'il a l'avantage. Dés que l'adversaire est à la dernière ligne du terrain de jeu, la stratégie change et adopte la stratégie TacticalPlayer qui va automatiquement bloquer l'advervaire et l'obliger a rebrousser le chemin.
Cette stratégie est très efficace en general, mais elle peut aussi être risquée si l'adversaire en face anticipe les mouvements.

* Trapmaster : Cette stratégie consiste à se frayer un chemin en plaçant des murs jusqu'au camps adverse tout en restant sur sa case de depart, cela  donne ainsi l'avantage à l'adversaire qui ne fait que se deplacer certainement, une fois qu'un chemin est fait, le joueur commence a se déplacer vers ce chemin qui est naturellement le plus long chemin, ce qui dissuade l'adversaire de nous placer des murs vu qu'il a largement l'avantage. Dés que l'adversaire arrive est à sa dernière ligne du jeu, le joueur bloque toute la ligne et ainsi oblige à l'adversaire de rebrousser le chemin et prendre le seul chemin qui existe, celui que j'ai emprunté dépuis le début. 

## Description des résultats

J'ai comparé les performances des quatre stratégies en jouant plusieurs parties et en utilisant deux cartes différentes. La première carte était un plateau simple de taille (7 * 7 mini-quoridorMap) et la deuxième carte était plus grande (18 * 18 quoridorMap).
<br><br>
**Méthodologie**<br>
j'ai lancé 100 parties pour chaque stratégie sur la première carte, un plateau simple de taille (7 * 7 mini-quoridorMap), en utilisant la méthode suivante :

* Si la première stratégie commence la première partie, la deuxième stratégie commence la deuxième partie, et ainsi de suite jusqu'à atteindre les 100 parties.
* Chaque stratégie a joué 100 parties en commençant sur le côté haut du plateau et 100 parties sur le côté bas du plateau, soit un total de 200 parties pour chaque rencontre.
j'ai également réalisé des tests sur la deuxième carte, plus grande (18 * 18 quoridorMap), mais en raison de la taille importante de la carte, j'ai limité le nombre de parties à 50 par affrontement.

j'ai utilisé un tableau pour enregistrer les scores obtenus par chaque stratégie. <br>
*Voici les resultats obtenus sur la mini-quoridorMap*

|                   | RandomStrat | AdaptivePlaymaker | TacticalPlayer | TrapAndBlock | Trapmaster |
|:------------------|:-----------:|:-----------------:|:--------------:|:------------:|:----------:|
| RandomStrat       |      -      |      (0-100)      |     (0-100)    |    (4-96)    |   (5-95)   |
| AdaptivePlaymaker |   (100-0)   |         -         |     (0-100)    |    (0-100)   |   (0-100)  |
| TacticalPlayer    |   (100-0)   |      (15-85)      |        -       |    (40-60)   |   (0-100)  |
| TrapAndBlock      |    (97-3)   |      (100-0)      |     (100-0)    |       -      |   (0-100)  |
| Trapmaster        |    (96-4)   |      (100-0)      |     (100-0)    |    (100-0)   |      -     |

***comment lire le tableau:*** sur la première colonne, se sont les stratégiés qui comment du coté haut du plateau et inversement la 1ere ligne sont les stratégies qui commencent du coté bas.

Sur la première carte, la stratégie aléatoire a obtenu les pires résultats, étant battue par toutes les autres stratégies. La stratégie dominante était `Trapmaster`, qui a battu toutes les autres stratégies sans perdre à l'exception de la stratégie aléatoire. Cependant, Trapmaster est efficace à 100% uniquement si l'adversaire en face est performant (c'est-à-dire qu'il ne joue pas de coups aléatoires).

Sur cette mini-map, l'ordre de performance des stratégies est le suivant : `Trapmaster >> TrapAndBlock > TacticalPlayer > AdaptivePlaymaker >> RandomStrat`.

Sur la deuxième carte,j'ai obtenu des résultats similaires à ceux de la première carte. La stratégie Trapmaster était la plus efficace, remportant toutes les parties à l'exception de celles contre la stratégie aléatoire.

Les resultats du test sur la grande map <br>
|                   | RandomStrat | AdaptivePlaymaker | TacticalPlayer | TrapAndBlock | Trapmaster |
|-------------------|-------------|-------------------|----------------|--------------|------------|
| RandomStrat       |      -      |       (0-50)      |     (0-50)     |    (0-50)    |   (4-46)   |
| AdaptivePlaymaker |    (50-0)   |         -         |     (0-50)     |    (0-50)    |   (0-50)   |
| TacticalPlayer    |    (50-0)   |       (50-0)      |        -       |    (7-43)    |   (0-50)   |
| TrapAndBlock      |    (50-0)   |       (50-0)      |     (50-0)     |       -      |   (0-50)   |
| Trapmaster        |    (42-8)   |       (50-0)      |     (50-0)     |    (50-0)    |      -     |

Sur cette carte, l'ordre de performance des stratégies est le suivant : `Trapmaster >> TrapAndBlock > TacticalPlayer > AdaptivePlaymaker >> RandomStrat`t.

j'ai également fourni des courbes illustrant l'évolution des victoires au cours de la partie (en format pdf), ainsi que des fonctions permettant de tester les stratégies et de tracer les courbes dans le notebook.

Conclusion
En conclusion, j'ai constaté que la stratégie `Trapmaster` était la plus efficace, bien qu'elle n'implémente pas d'algorithmes complexes. Les autres stratégies qui utilisent la recherche en profondeur pour trouver le coup optimal n'ont pas réussi à surpasser `Trapmaster`.
