import pygame
import numpy as np
import copy

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BOARD = (133, 94, 66)
COLOR_BUTTON = (255, 255, 0)
COLOR_AC_BUTTON = (200, 200, 0)
COLOR_GRAY = (100, 100, 100)


def text_objects(text, font, font_color):
    textSurface = font.render(text, True, font_color)
    return textSurface, textSurface.get_rect()


class Caro:
    def __init__(self):
        self.area = 45
        self.size = 14
        self.grid = np.full((self.size, self.size), '.')
        self.w_h = self.area * (self.size + 1)
        self.player1_score = 0
        self.player2_score = 0
        self.title = "Caro"
        self.x_stone_pos = 0
        self.y_stone_pos = 0
        self.text = ''
        self.font_size = 15
        self.font_color = COLOR_BLACK
        self.play_order = True  # True => Black, otherwise => White
        self.menu_x_pos = 45 * 16
        self.menu_y_pos = 45
        self.menu_width = 125
        self.menu_height = self.area
        self.stone = {}
        self.player_color_name = ''

        self.stone_color = ''
        self.player_score = ''
        self.button_color = COLOR_BUTTON
        self.ac_button_color = COLOR_AC_BUTTON
        self.winner = None
        self.screen = pygame.display.set_mode((self.w_h + self.menu_width + 2 * self.area, self.w_h + 45))
        pygame.display.set_caption(self.title)
        self.screen.fill(COLOR_BOARD)
        print(self.grid)

    def draw_main(self):

        """Number of row_col"""
        for i in range(1, 16):
            pygame.draw.line(self.screen, COLOR_BLACK,
                             [45 * i, 45], [45 * i, self.w_h], 2)
            pygame.draw.line(self.screen, COLOR_BLACK,
                             [45, 45 * i], [self.w_h, 45 * i], 2)

    def draw_score(self, player1_score, player2_score):
        self.player1_score, self.player2_score = player1_score, player2_score
        # Score.
        self.text_draw("PLAYER 1", 45 * 16 + 65, self.w_h // 2 - 90,
                       (100, 100, 100), 20)
        # self.screen.blit(pygame.transform.scale(x, (20, 20)), (45 * 16 - 5, self.w_h // 2 - 102))
        pygame.draw.circle(self.screen, COLOR_WHITE,
                           (45 * 16 + 5, self.w_h // 2 - 90), 45 // 5)
        self.text_draw(str(self.player1_score), 45 * 16 + 65, self.w_h // 2 - 30,
                       (100, 100, 100), 45)
        self.text_draw("PLAYER 2", 45 * 16 + 65, self.w_h // 2 + 20,
                       COLOR_BLACK, 20)
        # self.screen.blit(pygame.transform.scale(o, (20, 20)), (45 * 16 - 5, self.w_h // 2 + 8))
        pygame.draw.circle(self.screen, COLOR_BLACK,
                           (45 * 16 + 5, self.w_h // 2 + 20), 45 // 5)
        self.text_draw(str(self.player2_score), 45 * 16 + 65,
                       self.w_h // 2 + 80, COLOR_BLACK, 45)

    def interactive_button(self):

        # Draw buttons.
        pygame.draw.rect(self.screen, self.button_color,
                         (self.menu_x_pos, self.menu_y_pos, self.menu_width, self.menu_height))
        pygame.draw.rect(self.screen, self.button_color,
                         (self.menu_x_pos, self.menu_y_pos + 70, self.menu_width, self.menu_height))
        pygame.draw.rect(self.screen, self.button_color,
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
            pygame.draw.rect(self.screen, self.ac_button_color,
                             (self.menu_x_pos, self.menu_y_pos, self.menu_width, self.menu_height))
            self.text_draw("START", self.menu_x_pos + 59, self.menu_y_pos + 25, COLOR_RED, 20)

        # Next game.
        if self.menu_width + self.menu_x_pos > mouse[0] > self.menu_x_pos and \
                self.menu_y_pos + 70 + self.menu_height > mouse[1] > self.menu_y_pos + 70:
            pygame.draw.rect(self.screen, self.ac_button_color,
                             (self.menu_x_pos, self.menu_y_pos + 70, self.menu_width, self.menu_height))
            self.text_draw("Next game", self.menu_x_pos + 62, self.menu_y_pos + 95, (0, 0, 225), 20)

        # Quit.
        if self.menu_width + self.menu_x_pos > mouse[0] > self.menu_x_pos and \
                self.w_h - 90 + self.menu_height > mouse[1] > self.w_h - 90:
            pygame.draw.rect(self.screen, self.ac_button_color,
                             (self.menu_x_pos, self.w_h - 90, self.menu_width, self.menu_height))
            self.text_draw("Quit", self.menu_x_pos + 56, self.w_h - 65, (225, 0, 225), 20)
            if pygame.mouse.get_pressed(3)[0] == 1:
                pygame.quit()
                quit()

    def text_draw(self, text, x_pos, y_pos, font_color, font_size):
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        ff = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        TextSurf, TextRect = text_objects(self.text, ff, self.font_color)
        TextRect.center = (x_pos, y_pos)
        self.screen.blit(TextSurf, TextRect)

    def play_get_pos(self):
        self.x_stone_pos, self.y_stone_pos = pygame.mouse.get_pos()

        return self.x_stone_pos, self.y_stone_pos

    def play_draw_stone_pos(self):
        self.x_stone_pos = (self.x_stone_pos - self.x_stone_pos % 45)
        self.y_stone_pos = (self.y_stone_pos - self.y_stone_pos % 45)

        return self.x_stone_pos, self.y_stone_pos

    def update_grid(self):
        if self.play_order:
            self.grid[self.x_stone_pos // 45 - 1][self.y_stone_pos // 45 - 1] = "B"
        else:
            self.grid[self.x_stone_pos // 45 - 1][self.y_stone_pos // 45 - 1] = "W"
        print(self.grid.T)

    def play_draw_stone(self, stone, play_order, player_color_name, stone_color, x_stone_pos, y_stone_pos, game):
        self.stone, self.play_order, self.player_color_name = stone, play_order, player_color_name
        self.stone_color, self.x_stone_pos, self.y_stone_pos = stone_color, x_stone_pos, y_stone_pos

        if (self.x_stone_pos, self.y_stone_pos) in self.stone["white"]:
            pass
        elif (self.x_stone_pos, self.y_stone_pos) in self.stone["black"]:
            pass
        else:
            self.update_grid()
            pygame.draw.circle(self.screen, self.stone_color,
                               (self.x_stone_pos + 45 // 2, self.y_stone_pos + 45 // 2), 45 // 2)
            self.stone[self.player_color_name].append((self.x_stone_pos, self.y_stone_pos))
            if self.play_order:
                self.play_order = False
                game.text_draw("PLAYER 1", 45 * 16 + 65, game.w_h // 2 - 90,
                               COLOR_GRAY, 20)
                game.text_draw("PLAYER 2", 45 * 16 + 65, game.w_h // 2 + 20,
                               COLOR_RED, 20)
            else:
                self.play_order = True
                game.text_draw("PLAYER 1", 45 * 16 + 65, game.w_h // 2 - 90,
                               COLOR_RED, 20)
                game.text_draw("PLAYER 2", 45 * 16 + 65, game.w_h // 2 + 20,
                               COLOR_GRAY, 20)
        return self.stone, self.play_order

    def score(self, stone, player_color_name, player_score, play_order):
        self.stone, self.player_color_name, self.player_score = stone, player_color_name, player_score
        self.play_order = play_order
        result = None
        if len(self.stone[self.player_color_name]) >= 5:

            stone_sort = sorted(self.stone[self.player_color_name])
            if player_color_name == "white":
                opponent_stone_sort = sorted(self.stone["black"])
            else:
                opponent_stone_sort = sorted(self.stone["white"])

            for x, y in stone_sort:
                # Vertical
                cnt = 0
                for i in range(1, 5):
                    if (x, y + 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4 and ((x, y - 45) not in opponent_stone_sort or (
                                x, y + 45 * (i + 1)) not in opponent_stone_sort) and (
                                (x, y - 45) not in stone_sort and (x, y + 45 * (i + 1)) not in stone_sort):
                            self.player_score += 1
                            self.play_order = None
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
                            self.player_score += 1
                            self.play_order = None
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
                            self.player_score += 1
                            self.play_order = None
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
                            self.player_score += 1
                            self.play_order = None
                            result = True
                            break

        if result:

            if self.player_color_name == "white":
                self.text_draw("WIN", 45 * 16 + 65, self.w_h // 2 - 120,
                               (100, 100, 100), 45)

            elif self.player_color_name == "black":
                self.text_draw("WIN", 45 * 16 + 65, self.w_h // 2 + 120,
                               COLOR_BLACK, 45)

        return self.player_score, self.play_order

    def actions(self):
        return [(x, y) for x in range(self.size, self.size * self.area, self.area)
                for y in range(self.size, self.size * self.area, self.area)
                if (x, y) not in self.stone["black"].union(self.stone["white"])]

    def local_successor(self, expand=1):
        marked = self.stone["black"].union(self.stone["white"])
        if len(marked) == 0:
            return [(self.size // 2, self.size // 2)]
        min_row_to_expand = max(min(m[0] for m in marked) - expand, 0)
        max_row_to_expand = min(max(m[0] for m in marked) + expand, self.size - 1)
        min_col_to_expand = max(min(m[1] for m in marked) - expand, 0)
        max_col_to_expand = min(max(m[1] for m in marked) + expand, self.size - 1)

        all_moves = self.actions()
        return list(filter(lambda m: min_row_to_expand <= m[0] <= max_row_to_expand and
                                     min_col_to_expand <= m[1] <= max_col_to_expand, all_moves))

    def result(self, move):
        if move in self.stone["black"] or move in self.stone["white"]:
            return
        new_state = copy.deepcopy(self.grid)

        if self.play_order:
            self.grid[move[0] // 45 - 1][move[1] // 45 - 1] = "B"
        else:
            self.grid[move[0] // 45 - 1][move[1] // 45 - 1] = "W"

        print(new_state.T)

        return new_state

    # def utility(self):
    #     player_win = self.winner()
    #     if player_win == X:
    #         return 100000
    #     elif player_win == O:
    #         return -100000
    #     return 0
    #
    # def eval(self):
    #     if self.terminal():
    #         return self.utility()
    #
    #     eval_score = 0
    #     # Check all rows
    #     for i in range(self.n_rows):
    #         repr = self.getASCIIRepr((i, 0), HORIZONTAL)
    #         eval_score += self._evalPattern(repr)
    #
    #     # Check all columns
    #     for i in range(self.n_cols):
    #         repr = self.getASCIIRepr((0, i), VERTICAL)
    #         eval_score += self._evalPattern(repr)
    #
    #     # Check all diagonal left
    #     for i in range(self.n_rows + self.n_cols - WIN * 2 + 1):
    #         repr = self.getASCIIRepr((i, self.n_cols - WIN), DIAGONAL_L)
    #         eval_score += self._evalPattern(repr)
    #
    #     # Check all diagonal right
    #     for i in range(self.n_rows + self.n_cols - WIN * 2 + 1):
    #         repr = self.getASCIIRepr((i, WIN - 1), DIAGONAL_R)
    #         eval_score += self._evalPattern(repr)
    #
    #     return eval_score

    # def top_actions(self, n=10):
    #     """
    #     Get top 'n' legal moves
    #     """
    #     all_moves = self.actions()
    #
    #     evals = [self.result(move).eval() for move in all_moves]
    #     sorted_moves = [move for move, _ in sorted(zip(all_moves, evals),
    #                                                key=lambda x: x[1],
    #                                                reverse=(self.player() == X))]
    #
    #     return sorted_moves if n >= len(all_moves) else sorted_moves[:n]
