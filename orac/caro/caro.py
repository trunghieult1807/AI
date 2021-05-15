import pygame
import re
import copy
from . import palette


def text_objects(text, font, font_color):
    textSurface = font.render(text, True, font_color)
    return textSurface, textSurface.get_rect()


def score_pattern(string_grid, pattern, player):
    if len(pattern.group(0)) < 5:
        return 0
    elif len(pattern.group(0)) == 5:
        s, e = pattern.start(), pattern.end()
        if s > 0 and e < len(string_grid):
            if string_grid[s - 1] not in [player, "."] and \
                    string_grid[e] not in [player, "."]:
                return 0

    p_str = pattern.group(0)
    consec_scores = (2, 5, 1000, 10000)
    score, cons = 0, 0
    for p in p_str:
        if p != ".":
            cons += 1
        elif 0 < cons < 5:
            score += consec_scores[cons - 1]
            cons = 0
        else:
            cons = 0

    if 0 < cons < 4:
        score += consec_scores[cons - 1]
    return score


def eval_pattern(string_grid):
    if "O" not in string_grid and "X" not in string_grid:
        return 0

    eval_score = 0

    # Score X
    X_ext = re.compile(r"[X.]+")
    for pattern in X_ext.finditer(string_grid):
        eval_score += score_pattern(string_grid, pattern, "X")

    # Score O
    O_ext = re.compile(r"[O.]+")
    for pattern in O_ext.finditer(string_grid):
        eval_score -= score_pattern(string_grid, pattern, "O")

    return eval_score


class Caro:
    def __init__(self, size):
        self.area = 45
        self.size = size
        self.w_h = self.area * (self.size + 1)
        self.player1_score = 0
        self.player2_score = 0
        self.x_stone_pos = 1
        self.y_stone_pos = 1
        self.menu_x_pos = self.area * (self.size + 2)
        self.menu_y_pos = self.area
        self.menu_width = 125
        self.menu_height = self.area
        self.stone = {palette.player1: [], palette.player2: []}
        self.winner = None
        self.screen = pygame.display.set_mode((self.w_h + self.menu_width + 2 * self.area, self.w_h + 45))
        pygame.display.set_caption("Caro")
        # self.screen.fill(palette.COLOR_BOARD)

    @classmethod
    def loadState(cls, size, player1_stone, player2_stone, player_win=None):
        new_state = cls(size)
        new_state.stone[palette.player1] = player1_stone
        new_state.stone[palette.player2] = player2_stone
        new_state.winner = player_win
        print(new_state.stone)
        return new_state

    def copy(self):
        copyState = self.loadState(self.size, copy.deepcopy(self.stone[palette.player1]),
                                   copy.deepcopy(self.stone[palette.player2]), self.winner)
        return copyState

    def draw_main(self):
        for i in range(1, self.size + 2):
            pygame.draw.line(self.screen, palette.COLOR_BLACK,
                             [45 * i, 45], [45 * i, self.w_h], 2)
            pygame.draw.line(self.screen, palette.COLOR_BLACK,
                             [45, 45 * i], [self.w_h, 45 * i], 2)

    def draw_score(self, player1_score, player2_score):
        self.player1_score, self.player2_score = player1_score, player2_score
        self.text_draw("PLAYER 1", self.menu_x_pos + 70, self.w_h // 2 - 90,
                       palette.COLOR_GRAY, 20)
        pygame.draw.line(self.screen, palette.COLOR_RED,
                         (self.menu_x_pos, self.w_h // 2 - 98),
                         (self.menu_x_pos + 12, self.w_h // 2 - 86), 5)
        pygame.draw.line(self.screen, palette.COLOR_RED,
                         (self.menu_x_pos, self.w_h // 2 - 86),
                         (self.menu_x_pos + 12, self.w_h // 2 - 98), 5)
        self.text_draw(str(self.player1_score), self.menu_x_pos + 70, self.w_h // 2 - 30,
                       palette.COLOR_GRAY, 45)
        self.text_draw("PLAYER 2", self.menu_x_pos + 70, self.w_h // 2 + 20,
                       palette.COLOR_GRAY, 20)
        pygame.draw.circle(self.screen, palette.COLOR_RED,
                           (self.menu_x_pos + 5, self.w_h // 2 + 20), 45 // 5)
        pygame.draw.circle(self.screen, palette.COLOR_BOARD,
                           (self.menu_x_pos + 5, self.w_h // 2 + 20), 45 // 8)
        self.text_draw(str(self.player2_score), self.menu_x_pos + 65,
                       self.w_h // 2 + 80, palette.COLOR_GRAY, 45)

    def interactive_button(self):
        # Draw buttons.
        pygame.draw.rect(self.screen, palette.COLOR_BUTTON,
                         (self.menu_x_pos, self.menu_y_pos, self.menu_width, self.menu_height))
        pygame.draw.rect(self.screen, palette.COLOR_BUTTON,
                         (self.menu_x_pos, self.menu_y_pos + 70, self.menu_width, self.menu_height))
        pygame.draw.rect(self.screen, palette.COLOR_BUTTON,
                         (self.menu_x_pos, self.w_h - 90, self.menu_width, self.menu_height))
        # Draw text on buttons.
        self.text_draw("NEW GAME", self.menu_x_pos + 59, self.menu_y_pos + 25, (200, 0, 0), 20)
        self.text_draw("NEXT GAME", self.menu_x_pos + 62, self.menu_y_pos + 95, (0, 0, 180), 20)
        self.text_draw("QUIT", self.menu_x_pos + 56, self.w_h - 65, (200, 0, 200), 20)
        # To make interactive buttons.
        mouse = pygame.mouse.get_pos()

        # New game.
        if self.menu_width + self.menu_x_pos > mouse[0] > self.menu_x_pos and \
                self.menu_y_pos + self.menu_height > mouse[1] > self.menu_y_pos:
            pygame.draw.rect(self.screen, palette.COLOR_AC_BUTTON,
                             (self.menu_x_pos, self.menu_y_pos, self.menu_width, self.menu_height))
            self.text_draw("START", self.menu_x_pos + 59, self.menu_y_pos + 25, palette.COLOR_RED, 20)

        # Next game.
        if self.menu_width + self.menu_x_pos > mouse[0] > self.menu_x_pos and \
                self.menu_y_pos + 70 + self.menu_height > mouse[1] > self.menu_y_pos + 70:
            pygame.draw.rect(self.screen, palette.COLOR_AC_BUTTON,
                             (self.menu_x_pos, self.menu_y_pos + 70, self.menu_width, self.menu_height))
            self.text_draw("Next game", self.menu_x_pos + 62, self.menu_y_pos + 95, (0, 0, 225), 20)

        # Quit.
        if self.menu_width + self.menu_x_pos > mouse[0] > self.menu_x_pos and \
                self.w_h - 90 + self.menu_height > mouse[1] > self.w_h - 90:
            pygame.draw.rect(self.screen, palette.COLOR_AC_BUTTON,
                             (self.menu_x_pos, self.w_h - 90, self.menu_width, self.menu_height))
            self.text_draw("Quit", self.menu_x_pos + 56, self.w_h - 65, (225, 0, 225), 20)
            if pygame.mouse.get_pressed(3)[0] == 1:
                pygame.quit()
                quit()

    def text_draw(self, text, x_pos, y_pos, font_color, font_size):
        ff = pygame.font.Font(pygame.font.get_default_font(), font_size)
        TextSurf, TextRect = text_objects(text, ff, font_color)
        TextRect.center = (x_pos, y_pos)
        self.screen.blit(TextSurf, TextRect)

    def play_get_pos(self):
        self.x_stone_pos, self.y_stone_pos = pygame.mouse.get_pos()

        return self.x_stone_pos, self.y_stone_pos

    def play_draw_stone_pos(self):
        self.x_stone_pos = (self.x_stone_pos - self.x_stone_pos % 45)
        self.y_stone_pos = (self.y_stone_pos - self.y_stone_pos % 45)

        return self.x_stone_pos, self.y_stone_pos

    def play_draw_stone(self, current_player, x_stone_pos, y_stone_pos, game):
        if (x_stone_pos, y_stone_pos) in self.stone["white"]:
            pass
        elif (x_stone_pos, y_stone_pos) in self.stone["black"]:
            pass
        else:
            if current_player == palette.player1:
                pygame.draw.line(self.screen, palette.COLOR_BLACK,
                                 (x_stone_pos + 8, y_stone_pos + 4),
                                 (x_stone_pos + self.area - 8, y_stone_pos + self.area - 4), 8)
                pygame.draw.line(self.screen, palette.COLOR_BLACK,
                                 (x_stone_pos + 8, y_stone_pos + self.area - 4),
                                 (x_stone_pos + self.area - 8, y_stone_pos + 4), 8)
            elif current_player == palette.player2:
                pygame.draw.circle(self.screen, palette.COLOR_WHITE,
                                   (x_stone_pos + self.area / 2 + 1, y_stone_pos + self.area / 2 + 1.5), 45 / 2 - 2)
                pygame.draw.circle(self.screen, palette.COLOR_BOARD,
                                   (x_stone_pos + self.area / 2 + 1, y_stone_pos + self.area / 2 + 1.5), 45 / 2 - 8)
            self.stone[current_player].append((x_stone_pos, y_stone_pos))
            if current_player == palette.player1:
                pygame.draw.line(self.screen, palette.COLOR_GRAY,
                                 (self.menu_x_pos, self.w_h // 2 - 98),
                                 (self.menu_x_pos + 12, self.w_h // 2 - 86), 5)
                pygame.draw.line(self.screen, palette.COLOR_GRAY,
                                 (self.menu_x_pos, self.w_h // 2 - 86),
                                 (self.menu_x_pos + 12, self.w_h // 2 - 98), 5)
                pygame.draw.circle(self.screen, palette.COLOR_RED,
                                   (self.menu_x_pos + 5, self.w_h // 2 + 20), 45 // 5)
                pygame.draw.circle(self.screen, palette.COLOR_BOARD,
                                   (self.menu_x_pos + 5, self.w_h // 2 + 20), 45 // 8)
                game.text_draw("PLAYER 1", self.menu_x_pos + 70, self.w_h // 2 - 90,
                               palette.COLOR_GRAY, 20)
                game.text_draw("PLAYER 2", self.menu_x_pos + 70, self.w_h // 2 + 20,
                               palette.COLOR_RED, 20)
            elif current_player == palette.player2:
                pygame.draw.line(self.screen, palette.COLOR_RED,
                                 (self.menu_x_pos, self.w_h // 2 - 98),
                                 (self.menu_x_pos + 12, self.w_h // 2 - 86), 5)
                pygame.draw.line(self.screen, palette.COLOR_RED,
                                 (self.menu_x_pos, self.w_h // 2 - 86),
                                 (self.menu_x_pos + 12, self.w_h // 2 - 98), 5)
                pygame.draw.circle(self.screen, palette.COLOR_GRAY,
                                   (self.menu_x_pos + 5, self.w_h // 2 + 20), 45 // 5)
                pygame.draw.circle(self.screen, palette.COLOR_BOARD,
                                   (self.menu_x_pos + 5, self.w_h // 2 + 20), 45 // 8)
                game.text_draw("PLAYER 1", self.menu_x_pos + 70, self.w_h // 2 - 90,
                               palette.COLOR_RED, 20)
                game.text_draw("PLAYER 2", self.menu_x_pos + 70, self.w_h // 2 + 20,
                               palette.COLOR_GRAY, 20)
        return self.stone

    def check_win(self, stone, player_score, current_player):
        self.stone = stone
        result = None
        if len(self.stone[current_player]) >= 5:
            stone_sort = sorted(self.stone[current_player])
            if current_player == palette.player2:
                opponent_stone_sort = sorted(self.stone[palette.player1])
            else:
                opponent_stone_sort = sorted(self.stone[palette.player2])
            for x, y in stone_sort:
                # Vertical
                cnt = 0
                for i in range(1, 5):
                    if (x, y + 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4 and ((x, y - 45) not in opponent_stone_sort or (
                                x, y + 45 * (i + 1)) not in opponent_stone_sort) and (
                                (x, y - 45) not in stone_sort and (x, y + 45 * (i + 1)) not in stone_sort):
                            player_score += 1
                            self.winner = current_player
                            result = True
                            break

                    else:
                        break

                # Horizontal
                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y) in stone_sort:
                        cnt += 1
                        if cnt == 4 and ((x - 45, y) not in opponent_stone_sort or (
                                x + 45 * (i + 1), y) not in opponent_stone_sort) and (
                                (x - 45, y) not in stone_sort and (x + 45 * (i + 1), y) not in stone_sort):
                            player_score += 1
                            self.winner = current_player
                            result = True
                            break
                    else:
                        break

                # Down diagonal
                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y + 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4 and ((x - 45, y - 45) not in opponent_stone_sort or (
                                x + 45 * (i + 1), y + 45 * (i + 1)) not in opponent_stone_sort) and (
                                (x - 45, y - 45) not in stone_sort and (
                                x + 45 * (i + 1), y + 45 * (i + 1)) not in stone_sort):
                            player_score += 1
                            self.winner = current_player
                            result = True
                            break

                # Up diagonal
                cnt = 0
                for i in range(1, 5):
                    if (x + 45 * i, y - 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4 and ((x - 45, y + 45) not in opponent_stone_sort or (
                                x + 45 * (i + 1), y - 45 * (i + 1)) not in opponent_stone_sort) and (
                                (x - 45, y + 45) not in stone_sort and (
                                x + 45 * (i + 1), y - 45 * (i + 1)) not in stone_sort):
                            player_score += 1
                            self.winner = current_player
                            result = True
                            break
        if result:
            if self.winner == palette.player2:
                self.text_draw("WIN", self.menu_x_pos + 65, self.w_h // 2 - 120,
                               palette.COLOR_RED, 45)

            elif self.winner == palette.player1:
                self.text_draw("WIN", self.menu_x_pos + 65, self.w_h // 2 + 120,
                               palette.COLOR_RED, 45)
        return player_score

    def actions(self):
        return [(x, y) for x in range(self.area, self.size * self.area, self.area)
                for y in range(self.area, self.size * self.area, self.area)
                if (x, y) not in self.stone[palette.player1] + self.stone[palette.player2]]

    def local_successor(self, expand=1):
        marked = self.stone[palette.player1] + self.stone[palette.player2]
        if len(marked) == 0:
            return [(self.size // 2, self.size // 2)]
        min_row_to_expand = max(min(m[0] for m in marked) - expand * self.area, 0)
        max_row_to_expand = min(max(m[0] for m in marked) + expand * self.area, self.size * self.area)
        min_col_to_expand = max(min(m[1] for m in marked) - expand * self.area, 0)
        max_col_to_expand = min(max(m[1] for m in marked) + expand * self.area, self.size * self.area)

        all_moves = self.actions()
        return list(filter(lambda m: min_row_to_expand <= m[0] <= max_row_to_expand and
                                     min_col_to_expand <= m[1] <= max_col_to_expand, all_moves))

    def result(self, move, current_player):
        if move in self.stone[palette.player1] or move in self.stone[palette.player2]:
            return
        new_state = self.copy()
        new_state.stone[current_player].append(move)
        return new_state

    def utility(self):
        if self.winner == palette.player1:
            return 1000000
        elif self.winner == palette.player2:
            return -1000000
        return 0

    def terminal(self):
        if self.winner is not None:
            return True
        if len(self.stone[palette.player1] + self.stone[palette.player2]) < (self.size ** 2):
            return False
        return True

    def get_string_grid(self, pos, direction):
        x, y = pos
        result = ""
        if direction == "horizontal":
            for col in range(self.area, self.area * self.size, self.area):
                if (x, col) in self.stone[palette.player2]:
                    result += "O"
                elif (x, col) in self.stone[palette.player1]:
                    result += "X"
                else:
                    result += "."
        elif direction == "vertical":
            for row in range(self.area, self.area * self.size, self.area):
                if (row, y) in self.stone[palette.player2]:
                    result += "O"
                elif (row, y) in self.stone[palette.player1]:
                    result += "X"
                else:
                    result += "."
        elif direction == "down_diagonal":
            i, j = x - min(x, y), y - min(x, y)
            while i < self.area * self.size and j < self.area * self.size:
                if (i, j) in self.stone[palette.player2]:
                    result += "O"
                elif (i, j) in self.stone[palette.player1]:
                    result += "X"
                else:
                    result += "."
                i, j = i + self.area, j + self.area
        elif direction == "up_diagonal":
            i, j = x - min(x, y), y + min(x, y)
            while i < self.area * self.size and j >= 0:
                if (i, j) in self.stone[palette.player2]:
                    result += "O"
                elif (i, j) in self.stone[palette.player1]:
                    result += "X"
                else:
                    result += "."
                i, j = i + self.area, j - self.area
        return result

    def evaluate(self):
        if self.terminal():
            return self.utility()

        evaluate_score = 0
        # Check all rows
        for i in range(self.area, self.area * self.size, self.area):
            string_grid = self.get_string_grid((i, 0), "horizontal")
            evaluate_score += eval_pattern(string_grid)

        # Check all columns
        for i in range(self.area, self.area * self.size, self.area):
            string_grid = self.get_string_grid((0, i), "vertical")
            evaluate_score += eval_pattern(string_grid)

        # Check all diagonal left
        for i in range(self.area, self.area * (2 * self.size - 5 * 2 + 1), self.area):
            string_grid = self.get_string_grid((i, self.size - 5), "down_diagonal")
            evaluate_score += eval_pattern(string_grid)

        # Check all diagonal right
        for i in range(self.area, self.area * (2 * self.size - 5 * 2 + 1), self.area):
            string_grid = self.get_string_grid((i, 5 - 1), "up_diagonal")
            evaluate_score += eval_pattern(string_grid)

        return evaluate_score

    def top_actions(self, current_player, n=10):
        all_moves = self.actions()
        evaluations = [self.result(move, current_player).evaluate() for move in all_moves]
        sorted_moves = [move for move, _ in sorted(zip(all_moves, evaluations),
                                                   key=lambda x: x[1],
                                                   reverse=current_player == palette.player1)]

        return sorted_moves if n >= len(all_moves) else sorted_moves[:n]
