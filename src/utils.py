import random
import numpy as np
from search.grid2D import ProblemeGrid2D
from search import probleme
from pySpriteWorld.gameclass import Game, check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
import pygame
from pySpriteWorld.ontology import Ontology
import matplotlib.pyplot as plt


def init(_boardname=None):
    game = Game()
    name = _boardname if _boardname is not None else 'quoridorMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    player = game.player

    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
    lMin = 2
    lMax = nbLignes-2
    cMin = 2
    cMax = nbCols-2
    players = [o for o in game.layers['joueur']]

    initStates = [o.get_rowcol() for o in players]
    # chaque joueur cherche a atteindre la ligne ou est place l'autre
    ligneObjectif = (initStates[1][0], initStates[0][0])
    # sur le layer ramassable
    walls = [[], []]
    walls[0] = [o for o in game.layers['ramassable'] if (
        o.get_rowcol()[0] == 0 or o.get_rowcol()[0] == 1)]
    walls[1] = [o for o in game.layers['ramassable'] if (
        o.get_rowcol()[0] == nbLignes-2 or o.get_rowcol()[0] == nbLignes-1)]
    allWalls = walls[0]+walls[1]
    nbWalls = len(walls[0])

    allObjectifs = ([(ligneObjectif[0], i) for i in range(cMin, cMax)], [
                    (ligneObjectif[1], i) for i in range(cMin, cMax)])
    objectifs = [allObjectifs[0][random.randint(
        cMin, cMax-3)], allObjectifs[1][random.randint(cMin, cMax-3)]]

    posPlayers = initStates

    variables_dict = {
        "nbLignes": nbLignes,
        "nbCols": nbCols,
        "players": players,
        "objectifs": objectifs,
        "lMin": lMin,
        "lMax": lMax,
        "cMin": cMin,
        "cMax": cMax,
        "walls": walls,
        "allWalls": allWalls,
        "posPlayers": posPlayers,
        "allObjectifs": allObjectifs
    }
    return game, variables_dict


def wallStates(walls):
    # donne la liste des coordonnees dez murs
    return [w.get_rowcol() for w in walls]


def playerStates(players):
    # donne la liste des coordonnees dez joueurs
    return [p.get_rowcol() for p in players]


def algo_astar(player, objectif, variables_dict, walls=[]):
    nbLignes = variables_dict["nbLignes"]
    g = np.ones((nbLignes, variables_dict["nbCols"]), dtype=bool)

    # on met False quand murs
    for w in wallStates(variables_dict["allWalls"]):
        g[w] = False
    for w in walls:
        g[w] = False
    for i in range(nbLignes):                 # on exclut aussi les bordures du plateau
        g[0][i] = False
        g[1][i] = False
        g[nbLignes-1][i] = False
        g[nbLignes-2][i] = False
        g[i][0] = False
        g[i][1] = False
        g[i][nbLignes-1] = False
        g[i][nbLignes-2] = False
    p = ProblemeGrid2D(variables_dict["posPlayers"][player],
                       objectif, g, 'manhattan')
    path = probleme.astar(p, verbose=False)
    # print("Chemin trouvé:", path)
    return path


def get_newObjectif(player, variables_dict, walls=[]):
    # Récupérer la position actuelle du joueur
    pos = variables_dict["allObjectifs"][player][0]

    # Initialiser une distance maximale
    distance = 100

    # Parcourir tous les objectifs disponibles pour le joueur
    for objectif in variables_dict["allObjectifs"][player]:
        # Calculer le chemin le plus court entre la position actuelle du joueur et l'objectif
        path = algo_astar(player, objectif, variables_dict, walls)

        # Si le chemin est plus court que la distance maximale et qu'il atteint l'objectif
        tmp = len(path)
        if tmp < distance and path[-1] == objectif:
            # Choisir cet objectif comme le plus proche
            pos = objectif
            distance = tmp

    # Définir le nouvel objectif pour le joueur dans le dictionnaire de variables
    variables_dict["objectifs"][player] = pos


def legal_wall_position(pos, variables_dict):
    lMin, lMax, cMin, cMax = variables_dict["lMin"], variables_dict[
        "lMax"], variables_dict["cMin"], variables_dict["cMax"]
    allWalls, players = variables_dict["allWalls"], variables_dict["players"]
    row, col = pos
    # une position legale est dans la carte et pas sur un mur deja pose ni sur un joueur
    # attention: pas de test ici qu'il reste un chemin vers l'objectif
    return ((pos not in wallStates(allWalls)) and (pos not in playerStates(players)) and row > lMin and row < lMax-1 and col >= cMin and col < cMax)


def non_blocking_path(walls_pos, current_player, variables_dict):
    # Récupération de l'objectif du joueur courant et de son adversaire dans le dictionnaire des variables
    player_goal = variables_dict["objectifs"][current_player]
    opponent_goal = variables_dict["objectifs"][(current_player + 1) % 2]

    # Calcul des chemins les plus courts pour atteindre l'objectif de chaque joueur
    path_to_player_goal = algo_astar(
        current_player, player_goal, variables_dict, walls_pos)
    path_to_opponent_goal = algo_astar(
        (current_player + 1) % 2, opponent_goal, variables_dict, walls_pos)

    # Vérification si le joueur courant bloque son adversaire en atteignant son objectif
    is_not_blocking = (
        player_goal == path_to_player_goal[-1] and opponent_goal == path_to_opponent_goal[-1])

    # Retourne un booléen indiquant si le joueur bloque son adversaire et les chemins les plus courts pour chaque joueur
    return is_not_blocking, path_to_player_goal, path_to_opponent_goal


def draw_random_wall_location(player, variables_dict):
    lMin, lMax, cMin, cMax = variables_dict["lMin"], variables_dict[
        "lMax"], variables_dict["cMin"], variables_dict["cMax"]
    # tire au hasard un couple de position permettant de placer un mur
    while True:
        random_loc = (random.randint(lMin, lMax),
                      random.randint(cMin, cMax))
        if legal_wall_position(random_loc, variables_dict):
            inc_pos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(inc_pos)
            for w in inc_pos:
                random_loc_bis = (random_loc[0] + w[0], random_loc[1]+w[1])
                if legal_wall_position(random_loc_bis, variables_dict) and non_blocking_path([random_loc, random_loc_bis], player, variables_dict)[0]:
                    return (random_loc, random_loc_bis)


def plot_courbe(nb_iter, strat_1, strat_2, map_quori="mini-quoridorMap"):
    # Jouer 100 parties entre les deux bots et compter les victoires
    bot1_wins = []
    bot2_wins = []
    bot1=0
    bot2 =0

    for i in range(nb_iter):
        who_start = 0 if i % 2 == 0 else 1

        result = start_game(strat_1, strat_2, who_start, 0, map_quori)

        if result == 0:
            bot1_wins.append(bot1_wins[-1] + 1 if bot1_wins else 1)
            bot2_wins.append(bot2_wins[-1] if bot2_wins else 0)
            bot1+=1
        else:
            bot2+=1
            bot2_wins.append(bot2_wins[-1] + 1 if bot2_wins else 1)
            bot1_wins.append(bot1_wins[-1] if bot1_wins else 0)

    j0 = strat_1(0, 0)
    j1 = strat_2(0, 0)
    print(bot1,bot2)
    # Créer un graphique à barres pour visualiser les résultats
    labels = [j0.name, j1.name]
    values = [bot1_wins[-1], bot2_wins[-1]]
    plt.bar(labels, values)
    title = "Comparaison des stratégies de jeu sur la "+map_quori
    plt.title(title)
    plt.xlabel('Stratégie')
    plt.ylabel('Nombre de victoires')

    # Afficher le graphique à barres
    plt.show()

    # Créer un graphique en courbes pour visualiser l'évolution des résultats
    plt.plot(range(nb_iter), bot1_wins, label=j0.name)
    plt.plot(range(nb_iter), bot2_wins, label=j1.name)
    plt.title('Évolution des résultats')
    plt.xlabel('Nombre de parties')
    plt.ylabel('Nombre de victoires')
    plt.legend()

    # Afficher le graphique en courbes
    plt.show()


def start_game(strat_1, strat_2, first_player, fps=2, map_filename="mini-quoridorMap"):
    # Définit le nombre d'itérations de la partie
    iterations = 1000

    # Initialise le jeu et le dictionnaire de variables
    game, variables_dict = init(map_filename)

    if fps != 0:
        game.O = Ontology(
            True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
        game.populate_sprite_names(game.O)
        game.fps = fps

    # Récupère la liste des murs à partir du dictionnaire de variables
    walls = variables_dict["walls"]

    player1 = strat_1(0, len(walls[0]))
    player2 = strat_2(1, len(walls[1]))

    for i in range(iterations):
        if i % 2 == first_player:
            if player1.play(variables_dict):
                pygame.quit()
                return player1.player
        else:
            if player2.play(variables_dict):
                pygame.quit()
                return player2.player

        if fps != 0:
            game.mainiteration()
