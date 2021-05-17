import pygame
import re
import copy
from . import palette


def text_objects(text, font, font_color):
    textSurface = font.render(text, True, font_color)
    return textSurface, textSurface.get_rect()


def score_pattern(grid_pattern, pattern, player):
    if len(pattern.group(0)) < 5:
        return 0
    elif len(pattern.group(0)) == 5:
        s, e = pattern.start(), pattern.end()
        if s > 0 and e < len(grid_pattern):
            if grid_pattern[s - 1] != player and grid_pattern[e] != player:
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


def scorePattern(grid_pattern, pattern, player):
    s, e = pattern.start(), pattern.end()
    if len(pattern.group(0)) < 5:
        return 0
    elif len(pattern.group(0)) == 5:
        if s > 0 and e < len(grid_pattern):
            if grid_pattern[s - 1] != player and grid_pattern[e] != player:
                return 0

    # Score barem
    consec_scores = (2, 5, 1000, 10000)
    block_weight = (0.5, 0.6, 0.01, 0.25)
    not_current_weight = (1, 1, 0.2, 0.15)

    p_str = pattern.group(0)
    score, cons, max_cons = 0, 0, 0

    # Count for number of consecutive
    block = True
    for p in p_str:
        if p != ".":
            cons += 1
        elif 0 < cons < 5:
            temp = not_current_weight[cons - 1] if "X" != player else 1
            if block:
                temp *= consec_scores[cons - 1] * block_weight[cons - 1]
                block = False
            else:
                temp *= consec_scores[cons - 1]
            score += temp
            cons = 0
        else:
            block = False
            cons = 0

    # Last mark is PLAYER
    if 0 < cons < 5:
        temp = not_current_weight[cons - 1] if "X" != player else 1
        if e < len(grid_pattern):
            temp *= consec_scores[cons - 1] * block_weight[cons - 1]
        else:
            temp *= consec_scores[cons - 1]
        score += temp

    return score


def evaluate_pattern(grid_pattern):
    if "O" not in grid_pattern and "X" not in grid_pattern:
        return 0

    evaluate_score = 0

    # Score X
    X_ext = re.compile(r"[X.]+")
    for pattern in X_ext.finditer(grid_pattern):
        evaluate_score += scorePattern(grid_pattern, pattern, "X")

    # Score O
    O_ext = re.compile(r"[O.]+")
    for pattern in O_ext.finditer(grid_pattern):
        evaluate_score -= scorePattern(grid_pattern, pattern, "O")

    return evaluate_score


class Caro:
    def __init__(self, size):
        self.area = 45
        self.size = size
        self.w_h = self.area * (self.size + 1)
        self.ai_score = 0
        self.human_score = 0
        self.x_stone_pos = 1
        self.y_stone_pos = 1
        self.menu_x_pos = self.area * (self.size + 2)
        self.menu_y_pos = self.area
        self.menu_width = 125
        self.menu_height = self.area
        self.stone = {palette.ai: [], palette.human: []}
        self.winner = None
        self.screen = pygame.display.set_mode((self.w_h + self.menu_width + 2 * self.area, self.w_h + 45))
        pygame.display.set_caption("Caro")
        # self.screen.fill(palette.COLOR_BOARD)

    @classmethod
    def loadState(cls, size, ai_stone, human_stone, player_win=None):
        new_state = cls(size)
        new_state.stone[palette.ai] = ai_stone
        new_state.stone[palette.human] = human_stone
        new_state.winner = player_win
        return new_state

    def copy(self):
        copyState = self.loadState(self.size, copy.deepcopy(self.stone[palette.ai]),
                                   copy.deepcopy(self.stone[palette.human]), self.winner)
        return copyState

    def draw_main(self):
        for i in range(1, self.size + 2):
            pygame.draw.line(self.screen, palette.COLOR_BLACK,
                             [45 * i, 45], [45 * i, self.w_h], 2)
            pygame.draw.line(self.screen, palette.COLOR_BLACK,
                             [45, 45 * i], [self.w_h, 45 * i], 2)

    def draw_score(self, ai_score, human_score):
        self.ai_score, self.human_score = ai_score, human_score
        self.text_draw("PLAYER 1", self.menu_x_pos + 70, self.w_h // 2 - 90,
                       palette.COLOR_GRAY, 20)
        pygame.draw.line(self.screen, palette.COLOR_RED,
                         (self.menu_x_pos, self.w_h // 2 - 98),
                         (self.menu_x_pos + 12, self.w_h // 2 - 86), 5)
        pygame.draw.line(self.screen, palette.COLOR_RED,
                         (self.menu_x_pos, self.w_h // 2 - 86),
                         (self.menu_x_pos + 12, self.w_h // 2 - 98), 5)
        self.text_draw(str(self.ai_score), self.menu_x_pos + 70, self.w_h // 2 - 30,
                       palette.COLOR_GRAY, 45)
        self.text_draw("PLAYER 2", self.menu_x_pos + 70, self.w_h // 2 + 20,
                       palette.COLOR_GRAY, 20)
        pygame.draw.circle(self.screen, palette.COLOR_RED,
                           (self.menu_x_pos + 5, self.w_h // 2 + 20), 45 // 5)
        pygame.draw.circle(self.screen, palette.COLOR_BOARD,
                           (self.menu_x_pos + 5, self.w_h // 2 + 20), 45 // 8)
        self.text_draw(str(self.human_score), self.menu_x_pos + 65,
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
            if current_player == palette.ai:
                pygame.draw.line(self.screen, palette.COLOR_BLACK,
                                 (x_stone_pos + 8, y_stone_pos + 4),
                                 (x_stone_pos + self.area - 8, y_stone_pos + self.area - 4), 8)
                pygame.draw.line(self.screen, palette.COLOR_BLACK,
                                 (x_stone_pos + 8, y_stone_pos + self.area - 4),
                                 (x_stone_pos + self.area - 8, y_stone_pos + 4), 8)
            elif current_player == palette.human:
                pygame.draw.circle(self.screen, palette.COLOR_WHITE,
                                   (x_stone_pos + self.area / 2 + 1, y_stone_pos + self.area / 2 + 1.5), 45 / 2 - 2)
                pygame.draw.circle(self.screen, palette.COLOR_BOARD,
                                   (x_stone_pos + self.area / 2 + 1, y_stone_pos + self.area / 2 + 1.5), 45 / 2 - 8)
            self.stone[current_player].append((x_stone_pos, y_stone_pos))
            if current_player == palette.ai:
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
            elif current_player == palette.human:
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

    def check_win(self, player_score, current_player):
        # self.stone = stone
        result = None
        if len(self.stone[current_player]) >= 5:
            stone_sort = sorted(self.stone[current_player])
            if current_player == palette.human:
                opponent_stone_sort = sorted(self.stone[palette.ai])
            else:
                opponent_stone_sort = sorted(self.stone[palette.human])
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
            if self.winner == palette.ai:
                self.text_draw("WIN", self.menu_x_pos + 65, self.w_h // 2 - 120,
                               palette.COLOR_RED, 45)

            elif self.winner == palette.human:
                self.text_draw("WIN", self.menu_x_pos + 65, self.w_h // 2 + 120,
                               palette.COLOR_RED, 45)
        return player_score

    def is_terminate(self):
        result = False
        if len(self.stone[palette.ai]) >= 5:
            stone_sort = sorted(self.stone[palette.ai])
            opponent_stone_sort = sorted(self.stone[palette.human])
            for x, y in stone_sort:
                # Vertical
                cnt = 0
                for i in range(1, 5):
                    if (x, y + 45 * i) in stone_sort:
                        cnt += 1
                        if cnt == 4 and ((x, y - 45) not in opponent_stone_sort or (
                                x, y + 45 * (i + 1)) not in opponent_stone_sort) and (
                                (x, y - 45) not in stone_sort and (x, y + 45 * (i + 1)) not in stone_sort):
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
                            result = True
                            break
        return result

    def actions(self):
        return [(x, y) for x in range(self.area, self.size * self.area, self.area)
                for y in range(self.area, self.size * self.area, self.area)
                if (x, y) not in self.stone[palette.ai] + self.stone[palette.human]]

    def local_successor(self, expand=1):
        marked = self.stone[palette.ai] + self.stone[palette.human]
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
        if move in self.stone[palette.ai] or move in self.stone[palette.human]:
            return
        new_state = self.copy()
        new_state.stone[current_player].append(move)
        return new_state

    def utility(self):
        if palette.ai == "black":
            return 1000000
        else:
            return -1000000
        return 0

    def terminal(self):
        if self.is_terminate():
            return True
        if len(self.stone[palette.ai] + self.stone[palette.human]) < (self.size ** 2):
            return False
        return True

    def get_grid_pattern(self, pos, direction):
        # x, y = pos
        result = ""
        if direction == "horizontal":
            for x in range(self.area, self.area * self.size, self.area):
                if (x, pos[1]) in self.stone[palette.human]:
                    result += "O"
                elif (x, pos[1]) in self.stone[palette.ai]:
                    result += "X"
                else:
                    result += "."
        elif direction == "vertical":
            for y in range(self.area, self.area * self.size, self.area):
                if (pos[0], y) in self.stone[palette.human]:
                    result += "O"
                elif (pos[0], y) in self.stone[palette.ai]:
                    result += "X"
                else:
                    result += "."
        elif direction == "down_diagonal":
            x, y = pos[0], pos[1]
            while x < self.w_h and y < self.w_h:
                if (x, y) in self.stone[palette.human]:
                    result += "O"
                elif (x, y) in self.stone[palette.ai]:
                    result += "X"
                else:
                    result += "."
                x, y = x + self.area, y + self.area
        elif direction == "up_diagonal":
            x, y = pos[0], pos[1]
            while x >= self.area and y < self.w_h:
                if (x, y) in self.stone[palette.human]:
                    result += "O"
                elif (x, y) in self.stone[palette.ai]:
                    result += "X"
                else:
                    result += "."
                x, y = x - self.area, y + self.area
        return result

    def evaluate(self):
        if self.terminal():
            return self.utility()

        evaluate_score = 0
        # Check all rows
        for y in range(self.area, self.area * self.size, self.area):
            grid_pattern = self.get_grid_pattern((0, y), "horizontal")
            evaluate_score += evaluate_pattern(grid_pattern)
        
        # Check all columns
        for x in range(self.area, self.area * self.size, self.area):
            grid_pattern = self.get_grid_pattern((x, 0), "vertical")
            evaluate_score += evaluate_pattern(grid_pattern)

        # Check all down diagonal
        grid_pattern = self.get_grid_pattern((self.area, self.area), "down_diagonal")
        evaluate_score += evaluate_pattern(grid_pattern)
        for n in range(2 * self.area, self.area * (self.size - 3), self.area):
            grid_pattern = self.get_grid_pattern((n, self.area), "down_diagonal")
            evaluate_score += evaluate_pattern(grid_pattern)
            grid_pattern = self.get_grid_pattern((self.area, n), "down_diagonal")
            evaluate_score += evaluate_pattern(grid_pattern)

        # Check all up diagonal
        grid_pattern = self.get_grid_pattern((self.area * self.size, self.area), "up_diagonal")
        evaluate_score += evaluate_pattern(grid_pattern)
        for n in range(self.area * (self.size - 1), 4 * self.area, -self.area):
            grid_pattern = self.get_grid_pattern((n, self.area), "up_diagonal")
            evaluate_score += evaluate_pattern(grid_pattern)
            grid_pattern = self.get_grid_pattern((self.area * self.size, (self.size + 1)* self.area - n), "up_diagonal")
            evaluate_score += evaluate_pattern(grid_pattern)

        return evaluate_score

    def top_actions(self, current_player, n=10):
        all_moves = self.actions()
        evaluations = [self.result(move, current_player).evaluate() for move in all_moves]
        sorted_moves = [move for move, _ in sorted(zip(all_moves, evaluations),
                                                   key=lambda x: x[1],
                                                   reverse=current_player == palette.ai)]

        return sorted_moves if n >= len(all_moves) else sorted_moves[:n]
