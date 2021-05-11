import pygame
import sys
import time

import Caro
import ai_agent as AI

def initWindowSize(tile_size, num_rows, num_cols):
    WIDTH = 500
    width, height = tile_size * (num_cols + 1), tile_size * (num_rows + 1)
    if width < WIDTH:
        width = WIDTH
        tile_size = WIDTH // (num_cols + 1)
        height = tile_size * (num_rows + 1)

    return tile_size, width, height + 100

pygame.init()
tile_size = 40
num_rows, num_cols = 7, 7
tile_size, width, height = initWindowSize(tile_size, num_rows, num_cols)

size = (width, height)   # Window size

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode(size)

# Create fonts
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", tile_size)

# Init Caro game
game = Caro.CaroGame((num_rows, num_cols))
board = game.getBoard()
user = None
ai_turn = False

#-------- Game loop -----------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(BLACK)

    # Let user choose a player
    if user is None:

        # Draw title
        title = largeFont.render("Play Caro", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw button
        playXButton = pygame.Rect((width/8), (height/2), width/4, 50)
        playX = mediumFont.render("Play as X", True, BLACK)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, WHITE, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5*(width/8), (height/2), width/4, 50)
        playO = mediumFont.render("Play as O", True, BLACK)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, WHITE, playOButton)
        screen.blit(playO, playORect)

        # Check if buttion is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = Caro.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = Caro.O
    
    else:
        # Draw game board
        tile_origin = (width / 2 - (num_cols / 2 * tile_size),
                       height - ((num_rows + 1) * tile_size))
        tiles = []
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size,
                    tile_size
                )
                pygame.draw.rect(screen, WHITE, rect, 3)

                if board[i][j] != Caro.EMPTY:
                    move = moveFont.render(board[i][j], True, WHITE)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)
        
        game_over = game.terminal()
        player = game.nextPlayer()

        # Show title
        if game_over:
            winner = game.winner()
            if winner is None:
                title = f"Game Over: Tie"
            else:
                title = f"Game Over: {winner} wins"
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Check if AI move
        if user != player and not game_over:
            if ai_turn:
                # time.sleep(0.5)
                move = AI.minimax(game.state)
                game.makeMove(move)
                ai_turn = False
            else:
                ai_turn = True
            # click, _, _ = pygame.mouse.get_pressed()
            # if click == 1:
            #     mouse = pygame.mouse.get_pos()
            #     for i in range(num_rows):
            #         for j in range(num_cols):
            #             if (board[i][j] == Caro.EMPTY and tiles[i][j].collidepoint(mouse)):
            #                 # Update game state
            #                 game.makeMove((i, j))
            #                 board = game.getBoard()
        
        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(num_rows):
                for j in range(num_cols):
                    if (board[i][j] == Caro.EMPTY and tiles[i][j].collidepoint(mouse)):
                        # Update game state
                        game.makeMove((i, j))
                        board = game.getBoard()
        
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, BLACK)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, WHITE, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    game.reset()
                    board = game.getBoard()
                    ai_turn = False

    pygame.display.flip()