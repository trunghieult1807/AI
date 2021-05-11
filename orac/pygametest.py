import time
from function import checkState, check_empty, get_all_patterns, possible_moves, BestMove
import pygame
import numpy as np
import random


def newgame():
    global grid, playFirst, winner
    grid = np.full((12, 12), ".")
    playFirst = None
    winner = 0


if __name__ == "__main__":

    newgame()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GRAY = (220, 220, 220)

    WIDTH = int(500/12)
    HEIGHT = int(500/12)

    MARGIN = 1
    DEPTH = 2

    grid = np.full((12, 12), ".")

    pygame.init()

    WINDOW_SIZE = [500, 600]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("Caro Game")

    drawDone = False
    done = False
    winner = 0
    Player = "X"
    playFirst = None
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                if Player == "O":
                    continue
                if row < 12 and column < 12 and winner == 0:
                    if playFirst is not None:
                        if winner == 0 and Player == "X":
                            if grid[row][column] != ".":
                                continue
                            else:
                                winner = checkState(grid)
                                grid[row][column] = 'X'
                                print("Click ", row, column)
                                print(get_all_patterns(grid))
                                winner = checkState(grid)
                                Player = "O"
                                drawDone = False
                    else:
                        if row == 7 and column == 4:
                            newgame()
                            playFirst = True

                        elif row == 7 and column == 6:
                            newgame()
                            playFirst = False
                else:
                    print("out")
            # May choi
            if Player == "O" and drawDone:
                # arrow = pygame.cursors.ball
                pygame.mouse.set_cursor(*arrow)

                if winner == 0:
                    isMax = 2
                    game_board = grid
                    x = -1
                    y = -1
                    if len(grid[grid != '.']) == 1:
                        moves = possible_moves(grid, [1])
                        (x, y) = random.choice(moves)
                    else:
                        start = time.time()

                        (x, y) = BestMove(grid, False, DEPTH)

                        end = time.time()
                        print(end-start)
                    grid[x][y] = 'O'
                    winner = checkState(grid)
                    if winner == 1000 or winner == -1000:
                        winner = "O"

                Player = "X"
                arrow = pygame.cursors.arrow
                pygame.mouse.set_cursor(*arrow)

        screen.fill(WHITE)

        # Draw the grid screen2
        if playFirst is not None:
            screen.fill(BLACK)
            IMAGE_O = pygame.image.load('../carogame/o.png').convert()
            IMAGE_O = pygame.transform.scale(IMAGE_O, (WIDTH, WIDTH))

            IMAGE_X = pygame.image.load('../carogame/x.png').convert()
            IMAGE_X = pygame.transform.scale(IMAGE_X, (WIDTH, WIDTH))
            for row in range(12):
                for column in range(12):
                    color = WHITE
                    rect = pygame.draw.rect(screen,
                                            color,
                                            [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

                    if grid[row][column] == "X":
                        screen.blit(IMAGE_X, rect)
                    if grid[row][column] == "O":
                        screen.blit(IMAGE_O, rect)
            pygame.draw.rect(screen, WHITE, [0, 500+5, 500, 100])
            react = pygame.draw.rect(screen, GRAY, [(MARGIN + WIDTH) * int(
                12 / 2 - 2) + MARGIN, (MARGIN + HEIGHT) * 12 + MARGIN, WIDTH * 3, HEIGHT])
            font = pygame.font.SysFont("comicsansms", 18)
            text = font.render("   New game", True, (0, 128, 0))
            screen.blit(text, react)

            result = pygame.draw.rect(screen, WHITE, [(MARGIN + WIDTH) * int(
                12 / 2 - 1) + MARGIN, (MARGIN + HEIGHT) * 13 + MARGIN, WIDTH * 3, HEIGHT])
            font = pygame.font.SysFont("comicsansms", 18)
            if winner != 0:
                if winner == 'tie':
                    text = font.render("tie", True, RED)

                else:
                    if winner == 100000:
                        text = font.render("X win", True, RED)
                    else:
                        text = font.render("O win", True, RED)

            else:
                text = font.render("", True, RED)
            screen.blit(text, result)

            if react.collidepoint(pygame.mouse.get_pos()):
                arrow = pygame.cursors.broken_x
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        newgame()
                        arrow = pygame.cursors.arrow
                        pygame.mouse.set_cursor(*arrow)

            else:
                arrow = pygame.cursors.arrow

            pygame.mouse.set_cursor(*arrow)

        else:
            react = pygame.draw.rect(screen, WHITE, [(MARGIN + WIDTH) * int(
                12 / 2 - 4) + MARGIN, (MARGIN + HEIGHT) * 6 + MARGIN, WIDTH, HEIGHT])
            font = pygame.font.SysFont("comicsansms", 25)
            text = font.render("Do you want to phay first ?", True, BLACK)
            screen.blit(text, react)

            btn_yes = pygame.draw.rect(screen, WHITE, [(MARGIN + WIDTH) * int(
                12 / 2 - 2) + MARGIN, (MARGIN + HEIGHT) * 7 + MARGIN, WIDTH, HEIGHT])
            font = pygame.font.SysFont("comicsansms", 20)
            text = font.render(" Yes", True, (0, 128, 0))
            screen.blit(text, btn_yes)

            btn_no = pygame.draw.rect(screen, WHITE, [(MARGIN + WIDTH) * int(
                12 / 2) + MARGIN, (MARGIN + HEIGHT) * 7 + MARGIN, WIDTH, HEIGHT])
            font = pygame.font.SysFont("comicsansms", 20)
            text = font.render(" No", True, RED)
            screen.blit(text, btn_no)

            if btn_yes.collidepoint(pygame.mouse.get_pos()) or btn_no.collidepoint(pygame.mouse.get_pos()):
                arrow = pygame.cursors.broken_x

            else:
                arrow = pygame.cursors.arrow
            pygame.mouse.set_cursor(*arrow)
        if not playFirst and check_empty(grid):
            grid[5][5] = "O"
        drawDone = True
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
