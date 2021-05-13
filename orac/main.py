import pygame

from caro.caro import Caro
from caro.palette import COLOR_BLACK, COLOR_GREEN, COLOR_WHITE
import caro.ai as ai

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    stone = {"white": [], "black": []}
    player1_score, player2_score = 0, 0
    game = Caro(14)
    game.screen.fill((133, 94, 6))
    game.draw_main()
    game.draw_score(player1_score, player2_score)
    current_player = None
    thinking = False

    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN and not thinking:
            print(thinking)
            x_stone, y_stone = game.play_get_pos()

            # New game.
            if (game.menu_width + game.menu_x_pos) > x_stone > game.menu_x_pos and (
                    game.menu_height + game.menu_y_pos) > y_stone > game.menu_y_pos:
                player1_score, player2_score = 0, 0
                game = Caro(14)
                game.screen.fill((133, 94, 6))
                game.draw_main()
                game.draw_score(player1_score, player2_score)
                game.text_draw("GAME START", game.w_h // 2, 30, COLOR_GREEN, 35)
                current_player = "black"

            # Next game.
            if (125 + 45 * 16) > x_stone > 45 * 16 and 160 > y_stone > 115:
                game = Caro(14)
                game.screen.fill((133, 94, 6))
                stone = {"white": [], "black": []}
                game.draw_main()
                game.draw_score(player1_score, player2_score)
                game.text_draw("NEXT GAME START", game.w_h // 2, 30, COLOR_GREEN, 35)
                current_player = "black"

            # Draw a white stone (Player 1).
            if current_player is None:
                pass
            elif current_player == "white" and game.winner is None:
                if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:
                    x_stone, y_stone = game.play_draw_stone_pos()
                    stone = game.play_draw_stone(
                        stone, "white", COLOR_WHITE,
                        x_stone, y_stone, game)
                    player1_score = game.check_win(
                        stone, player1_score, "white")
                    current_player = "black"
                    if len(stone["black"]) + len(stone["white"]) == game.size ** 2:
                        game.text_draw("DRAW", 45 * 16 + 65, game.w_h // 2 + 120,
                                       (200, 0, 0), 45)
                        current_player = None

            # Draw a black stone (Player 2).
            # elif current_player == "black" and game.winner is None:
            #     thinking = True
            #     print("tt")
            #     # if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:
            #     move = ai.minimax_cutoff(game, current_player)
            #     print(move)
            #     stone = game.play_draw_stone(
            #         stone, "black", COLOR_BLACK, move[0], move[1], game)
            #     x_stone, y_stone = game.play_draw_stone_pos()
            #     stone = game.play_draw_stone(
            #         stone, "black", COLOR_BLACK, x_stone, y_stone, game)
            #     player2_score = game.check_win(
            #         stone, player2_score, "black")
            #     current_player = "white"
            #     if len(stone["black"]) + len(stone["white"]) == game.size ** 2:
            #         game.text_draw("DRAW", 45 * 16 + 65, game.w_h // 2 + 120,
            #                        (200, 0, 0), 45)
            #         current_player = None
            #     thinking = False
        elif current_player == "black" and game.winner is None:
            thinking = True
            # if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:
            move = ai.minimax_cutoff(game, current_player)
            print(move)
            stone = game.play_draw_stone(
                stone, "black", COLOR_BLACK, move[0], move[1], game)
            # x_stone, y_stone = game.play_draw_stone_pos()
            # stone = game.play_draws_stone(
            #     stone, "black", COLOR_BLACK, x_stone, y_stone, game)
            player2_score = game.check_win(
                stone, player2_score, "black")
            current_player = "white"
            print("current_player2:", current_player)
            if len(stone["black"]) + len(stone["white"]) == game.size ** 2:
                game.text_draw("DRAW", 45 * 16 + 65, game.w_h // 2 + 120,
                               (200, 0, 0), 45)
                current_player = None
            thinking = False

        game.interactive_button()
        pygame.display.update()
