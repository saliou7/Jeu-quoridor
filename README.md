
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

