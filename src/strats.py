import utils as ut
import random
import math


class RandomStrat:
    def __init__(self, player, len_walls) -> None:
        self.len_walls_placed = 0
        self.player = player
        self.oppenent = (player+1) % 2
        self.len_walls = len_walls
        self.iteration = 0
        self.name = "RandomStrat"

    def play(self, variables_dict):
        choice = random.choice([-1, 1])

        if self.len_walls_placed < self.len_walls and choice == -1:
            ((x1, y1), (x2, y2)) = ut.draw_random_wall_location(
                self.player, variables_dict)
            variables_dict["walls"][self.player][self.len_walls_placed].set_rowcol(
                x1, y1)
            variables_dict["walls"][self.player][self.len_walls_placed +
                                                 1].set_rowcol(x2, y2)
            self.len_walls_placed += 2
            return

        path_player = ut.algo_astar(
            self.player, variables_dict["objectifs"][self.player], variables_dict)

        row, col = path_player[1]
        variables_dict["posPlayers"][self.player] = (row, col)
        variables_dict["players"][self.player].set_rowcol(row, col)
        if (row, col) == variables_dict["objectifs"][self.player]:
            # print("le joueur "+str(self.player)+" a atteint son but!")
            return True

        return False


class AdaptivePlaymaker:

    def __init__(self, player, len_walls) -> None:
        self.name = "AdaptivePlaymaker"
        self.len_walls_placed = 0
        self.player = player
        self.oppenent = (player+1) % 2
        self.len_walls = len_walls
        self.iteration = 0

    def calcul_distance(self, variables_dict):
        path_player = ut.algo_astar(
            self.player, variables_dict["objectifs"][self.player], variables_dict)
        path_opp = ut.algo_astar(
            self.oppenent, variables_dict["objectifs"][self.oppenent], variables_dict)
        return (len(path_player), len(path_opp), path_player, path_opp)

    def next_move(self, variables_dict):
        # Obtenir le nouvel objectif du joueur
        ut.get_newObjectif(self.player, variables_dict)

        # Calculer les distances et les chemins des joueurs
        player_dis, opp_dist, path_pl, path_opp = self.calcul_distance(
            variables_dict)

        # Calculer la différence de distance entre les joueurs
        diff_dis = player_dis - opp_dist

        # Déterminer la prochaine action à effectuer en fonction de la situation
        if (diff_dis < 0 and opp_dist > 4) or (diff_dis == 0 and opp_dist > 4) or self.len_walls_placed >= self.len_walls or self.iteration < 2:
            # Si le joueur est plus éloigné que son adversaire et que l'adversaire est à plus de 4 cases,
            # ou si les deux joueurs sont à égale distance et que l'adversaire est à plus de 4 cases,
            # ou si le joueur a déjà placé tous ses murs ou si c'est le début de la partie, déplacer le joueur vers son objectif
            self.iteration += 1
            return ["move", path_pl[1]]
        else:
            # Sinon, chercher la meilleure position pour placer un mur
            (x, y) = path_opp[0]
            depth = 2
            cMin, cMax, lMin, lMax = variables_dict["cMin"], variables_dict[
                "cMax"], variables_dict["lMin"], variables_dict["lMax"]
            l_debut = x - depth if x-depth >= lMin else lMin
            l_fin = x + depth if x+depth < lMax else lMax
            c_debut = y - depth if y-depth >= cMin else cMin
            c_fin = y + depth if y+depth < cMax else cMax

            best_score = 0
            best_pos_wall = ["move", path_pl[1]]
            for i in range(l_debut, l_fin):
                for j in range(c_debut, c_fin):
                    if (i, j) == (x, y) or (i, j) == path_pl[0] or not ut.legal_wall_position((i, j), variables_dict):
                        # Ignorer les positions illégales
                        continue
                    liste = self.get_legal_positions((i, j), variables_dict)
                    random.shuffle(liste)
                    for w in liste:
                        isRoad, path_player, path_op = ut.non_blocking_path(
                            [(i, j), w], self.player, variables_dict)
                        if isRoad:
                            # Si le mur ne bloque pas le chemin du joueur, comparer le score de la nouvelle position avec le meilleur score actuel
                            if player_dis <= len(path_player) and (len(path_op) - opp_dist) > best_score:
                                best_score = (len(path_op) - opp_dist)
                                best_pos_wall = ["wall", ((i, j), w)]

            return best_pos_wall

    def get_legal_positions(self, pos, variables_dict):
        # Les directions de mouvement pour placer un mur en suivant une case libre
        inc_pos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Vérifier si la position est sur une ligne ou une colonne paire ou impaire
        x, y = pos
        if x % 2 == 0:
            if y % 2 == 0:
                # Si la position est sur une ligne et une colonne paire, on ne peut placer un mur que verticalement
                inc_pos = [(1, 0), (-1, 0)]
        else:
            if y % 2 == 0:
                # Si la position est sur une ligne impaire et une colonne paire, on ne peut placer un mur que horizontalement
                inc_pos = [(0, 1), (0, -1)]
            else:
                return []  # Si la position est sur une ligne impaire et une colonne impaire, on ne peut pas placer de mur

        # Générer les positions légales adjacentes où l'on peut placer un mur
        positions = []
        for w in inc_pos:
            pos_bis = (pos[0]+w[0], pos[1]+w[1])
            if ut.legal_wall_position(pos_bis, variables_dict):
                positions.append(pos_bis)
        return positions

    def update_board(self, move, variables_dict):
        if move[0] == "move":
            row, col = move[1]
            variables_dict["posPlayers"][self.player] = (row, col)
            variables_dict["players"][self.player].set_rowcol(row, col)
            if (row, col) == variables_dict["objectifs"][self.player]:
                # print("le joueur "+str(self.player)+" a atteint son but!")
                return True
        else:
            ((x1, y1), (x2, y2)) = move[1]
            variables_dict["walls"][self.player][self.len_walls_placed].set_rowcol(
                x1, y1)
            variables_dict["walls"][self.player][self.len_walls_placed +
                                                 1].set_rowcol(x2, y2)
            self.len_walls_placed += 2
        return False

    def play(self, variables_dict):
        return self.update_board(self.next_move(variables_dict), variables_dict)


class TacticalPlayer(AdaptivePlaymaker):

    def __init__(self, player, len_walls) -> None:
        super().__init__(player, len_walls)
        self.name = "TacticalPlayer"
        self.start_wall = False

    def get_next_move(self, variables_dict):
        ut.get_newObjectif(self.player, variables_dict)
        player_dis, opp_dist, path_pl, path_opp = self.calcul_distance(
            variables_dict)
        if (opp_dist > 4 and not self.start_wall) or self.len_walls_placed >= self.len_walls:
            return ["move", path_pl[1]]
        self.start_wall = True

        if (player_dis - opp_dist) < 0 and opp_dist > 4 or self.len_walls_placed >= self.len_walls or (player_dis >= variables_dict["lMax"] and player_dis-opp_dist <= 4):
            return ["move", path_pl[1]]

        x, y = path_opp[0]
        depth = self.best_depth((x, y), variables_dict)

        cMin, cMax, lMin, lMax = variables_dict["cMin"], variables_dict[
            "cMax"], variables_dict["lMin"], variables_dict["lMax"]
        l_debut = x - depth if x-depth >= lMin else lMin
        l_fin = x + depth if x+depth < lMax else lMax
        c_debut = y - depth if y-depth >= cMin else cMin
        c_fin = y + depth if y+depth < cMax else cMax

        best_score = 0
        best_pos_wall = ["move", path_pl[1]]
        for i in range(l_debut, l_fin):
            for j in range(c_debut, c_fin):
                if (i, j) == (x, y) or (i, j) == path_pl[0]:
                    continue
                if not ut.legal_wall_position((i, j), variables_dict):
                    continue
                liste = self.get_legal_positions((i, j), variables_dict)
                random.shuffle(liste)
                for w in liste:
                    isRoad, path_player, path_op = ut.non_blocking_path(
                        [(i, j), w], self.player, variables_dict)
                    if isRoad:
                        if player_dis <= len(path_player) and (len(path_op) - opp_dist) > best_score:
                            best_score = (len(path_op) - opp_dist)
                            best_pos_wall = ["wall", ((i, j), w)]

        return best_pos_wall

    def best_depth(self, pos_adv, dico):
        # Determine the depth of the search based on the position of the opponent
        x, y = pos_adv
        div = dico["nbLignes"]//3
        x = dico["lMax"] - x if self.player == 0 else x
        if x < div:
            return 2
        elif x <= div*2 and y > div and y < div*2:
            return 8
        elif x <= div*2:
            return 4
        return 5

    def play(self, variables_dict):
        return self.update_board(self.get_next_move(variables_dict), variables_dict)


class TrapAndBlock(TacticalPlayer):
    def __init__(self, player, len_walls) -> None:
        super().__init__(player, len_walls)
        self.iteration = 0
        self.changeStrat = False
        self.name = "TrapAndBlock"

    def get_best_move(self, variables_dict):
        ut.get_newObjectif(self.player, variables_dict)
        cMin, cMax, lMin, lMax = variables_dict["cMin"], variables_dict[
            "cMax"], variables_dict["lMin"], variables_dict["lMax"]
        player_dis, opp_dist, path_pl, path_opp = self.calcul_distance(
            variables_dict)

        if self.iteration == 0:
            self.iteration += 1
            inc_pos = [(0, 1), (0, -1)]
            for w in inc_pos:
                pos = path_opp[1]
                if ut.legal_wall_position((pos[0], w[1]+pos[1]), variables_dict):
                    return ["wall", (pos, (pos[0], w[1]+pos[1]))]

        (x_adv, y_adv) = path_opp[0]

        if y_adv == cMin or y_adv == cMax-1 and self.len_walls_placed < self.len_walls and not self.changeStrat:
            self.iteration += 1
            if opp_dist <= 4:  # changement de strat
                self.changeStrat = True
                return self.next_move(variables_dict)

            i = -1 if self.player == 0 else 1
            j = 1 if self.player == 0 else -1 if y_adv == cMax-1 else 1

            # place mur verticale.
            if ut.legal_wall_position((x_adv+i, y_adv+j), variables_dict):
                borne = lMin if self.player == 0 else lMax-1
                if abs(borne - x_adv+i) >= 3:
                    if self.check_position(((x_adv+i, y_adv+j), (x_adv+i+i, y_adv+j)), variables_dict):
                        return ["wall", ((x_adv+i, y_adv+j), (x_adv+i+i, y_adv+j))]

        if self.len_walls_placed < self.len_walls and not self.changeStrat:
            i = -1 if self.player == 0 else 1
            j = 1 if self.player == 0 else -1
            firstLine = True if (lMax - 1) == x_adv or lMin == x_adv else False

            if (not ut.legal_wall_position((x_adv, y_adv-1), variables_dict) or not ut.legal_wall_position((x_adv, y_adv+1), variables_dict)) and not firstLine:

                if y_adv == cMin+1 or y_adv == cMax-2:
                    if self.check_position(((x_adv+i, y_adv), (x_adv+i+i, y_adv)), variables_dict):
                        return ["wall", ((x_adv+i, y_adv), (x_adv+i+i, y_adv))]

                inc_pos = [(0, 1), (0, -1)]
                best_move = self.best_move(
                    opp_dist, (x_adv+i, y_adv), inc_pos, variables_dict)
                if len(best_move) != 0:
                    return best_move
        if self.iteration > 2 and (y_adv != cMin and y_adv != cMax-1):
            self.changeStrat = True
        if self.changeStrat:
            return self.get_next_move(variables_dict)

        if self.iteration == 1 and path_pl[0][0] == path_pl[1][0]:
            self.iteration += 1
            i = 1 if self.player == 0 else -1
            if ut.legal_wall_position((path_pl[0][0]+i, path_pl[0][1]), variables_dict):
                return ["move", (path_pl[0][0]+i, path_pl[0][1])]

        return ["move", path_pl[1]]

    def best_move(self, opp_dist, pos, liste, variables_dict):
        # Vérifie si la position pour placer un mur est légale
        if not ut.legal_wall_position(pos, variables_dict):
            return []

        # Initialise les variables pour stocker la meilleure action et son score
        score = -1
        best_move = []

        # Parcourt la liste des positions possibles pour placer un mur
        for w in liste:
            # Récupère les coordonnées de la position actuelle du joueur
            (x, y) = pos

            # Vérifie si la position pour placer un mur est légale
            if ut.legal_wall_position((x, w[1]+y), variables_dict):
                # Vérifie s'il y a un chemin libre pour le joueur et l'adversaire
                isRoad, path_player, path_op = ut.non_blocking_path(
                    [pos, (x, w[1]+y)], self.player, variables_dict)

                # Si un chemin est libre pour le joueur et l'adversaire
                if isRoad:
                    # Calcule le score en soustrayant la distance de l'adversaire à l'arrivée de sa distance actuelle
                    if (len(path_op) - opp_dist) > score:
                        score = (len(path_op) - opp_dist)
                        best_move = ["wall", (pos, (x, w[1]+y))]

        # Retourne la meilleure action possible
        return best_move

    def check_position(self, pos, variables_dict):
        # Vérifie si les deux positions de la barrière sont légales
        if ut.legal_wall_position(pos[0], variables_dict) and ut.legal_wall_position(pos[1], variables_dict):
            # Vérifie si la position de la barrière ne bloque pas les joueurs
            is_Road, _, _ = ut.non_blocking_path(
                pos, self.player, variables_dict)
            return is_Road
        return False

    def play(self, variables_dict):
        return self.update_board(self.get_best_move(variables_dict), variables_dict)


class Trapmaster(TrapAndBlock):
    def __init__(self, player, len_walls) -> None:
        super().__init__(player, len_walls)
        self.name = "Trapmaster"
        self.iteration == 0
        self.last_wall_pos = [0, 0]
        self.first_wall = [0, 0]

    def next_move(self, variables_dict):

        # ------------------------------premiere iteration-----------------------------------------------------
        if self.iteration == 0:
            self.iteration += 1
            # pos joueur courant
            (x, y) = variables_dict["posPlayers"][self.player]
            global i, j
            i = 1 if self.player == 0 else -1
            if ut.legal_wall_position((x+i, y+1), variables_dict) and ut.legal_wall_position((x+i*2, y+1), variables_dict):
                self.first_wall = [x+i*2, y+1]
                self.last_wall_pos = [x+i*2, y+1]
                return ["wall", ((x+i, y+1), (x+i*2, y+1))]
            if ut.legal_wall_position((x+i, y-1), variables_dict) and ut.legal_wall_position((x+i*2, y-1), variables_dict):
                self.first_wall = [x+i*2, y-1]
                self.last_wall_pos = [x+i*2, y-1]
                return ["wall", ((x+i, y-1), (x+i*2, y-1))]

        # ----------------------variables ----------------------------------------------------
        cMin, cMax, lMin, lMax = variables_dict["cMin"], variables_dict["cMax"], variables_dict["lMin"], variables_dict["lMax"]

        x, y = self.first_wall[0], self.first_wall[1]
        x = lMax-1 if self.player == 1 else lMin
        ut.get_newObjectif(self.player, variables_dict, [(x, y)])
        player_dis, opp_dist, path_pl, path_opp = self.calcul_distance(variables_dict)

        (x_pl, y_pl) = path_pl[0]
        i = 1 if self.player == 0 else -1
        if self.iteration == 1:
            self.iteration += 1
            global j
            j = - 1 if ut.legal_wall_position((x_pl+i, y_pl-1), variables_dict) else 1

        x_wall, y_wall = self.last_wall_pos[0], self.last_wall_pos[1]

        # -------------------------s'il ny a plus de murs a placer -----------------------
        if self.len_walls_placed >= self.len_walls:
            return ["move", path_pl[1]]

        # ------------------si l'adversaire a presque atteint son objectif------------------
        borne = lMin if self.player == 0 else lMax-1
        (x_adv, y_adv) = path_opp[0]

        if abs(borne - x_adv) <= 4:

            x, y = self.first_wall[0], self.first_wall[1]
            best_wall_pos = self.best_wall_pos(opp_dist, (x, y), j, variables_dict)
            if len(best_wall_pos) != 0:
                return best_wall_pos

        # -------------------- pour le placement des murs veriticaux----------------------
        if y_wall == cMin+1 or y_wall == cMax-2:  # pos verticale

            pos = ((x_wall+i, y_wall), (x_wall+i+i, y_wall))
            if self.check_position(pos, variables_dict):
                self.last_wall_pos = [x_wall+i+i, y_wall]
                return ["wall", pos]

        elif (y_wall == cMin+2 and j == -1) or (y_wall == cMax-3 and j == 1):  # pos verticale

            pos = ((x_wall+i, y_wall+j), (x_wall+i+i, y_wall+j))
            if self.check_position(pos, variables_dict):
                self.last_wall_pos = [x_wall+i+i, y_wall+j]
                return ["wall", pos]
        # --------------------pour le placement des murs horizontaux----------------------------
        # position dernier mur
        else:
            pos = ((x_wall+i, y_wall+j), (x_wall+i, y_wall+j+j))
            if self.check_position(pos, variables_dict):
                self.last_wall_pos = [x_wall+i, y_wall+j+j]
                return ["wall", pos]

        # --------------------Si aucune condition n'est respecté----------------------------
        return ["move", path_pl[1]]

    def best_wall_pos(self, opp_dist, pos, dir, variables_dict):

        best_score = 0
        best_pos_wall = []
        x, y = pos
        nb_iter = 0
        if dir == -1:
            nb_iter = variables_dict["cMax"]
        else:
            nb_iter = -1

        for j in range(y-dir, nb_iter, -dir):
            if not ut.legal_wall_position((x, j), variables_dict):
                continue
            liste = [(0, -dir), (1, 0), (-1, 0)]
            for w in liste:
                if not ut.legal_wall_position((x+w[0], j+w[1]), variables_dict):
                    continue
                isRoad, path_player, path_op = ut.non_blocking_path([(x, j), (x+w[0], j+w[1])], self.player, variables_dict)
                if isRoad:
                    if len(path_op) - opp_dist > best_score:
                        best_score = (len(path_op) - opp_dist)
                        best_pos_wall = ["wall", ((x, j), (x+w[0], j+w[1]))]
        # Retourne la meilleure action possible
        return best_pos_wall

    def play(self, variables_dict):
        return self.update_board(self.next_move(variables_dict), variables_dict)
