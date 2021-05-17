import pygame
from caro import caro
from caro import palette
from caro import ai

board_size = 14

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    stone = {palette.ai: [], palette.human: []}
    ai_score, human_score = 0, 0
    game = caro.Caro(board_size)
    game.screen.fill(palette.COLOR_BOARD)
    game.draw_main()
    game.draw_score(ai_score, human_score)
    current_player = None
    is_first_move = True
    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_stone, y_stone = game.play_get_pos()

            # New game.
            if (game.menu_width + game.menu_x_pos) > x_stone > game.menu_x_pos and (
                    game.menu_height + game.menu_y_pos) > y_stone > game.menu_y_pos:
                ai_score, human_score = 0, 0
                game = caro.Caro(board_size)
                is_first_move = True
                game.screen.fill(palette.COLOR_BOARD)
                game.draw_main()
                game.draw_score(ai_score, human_score)
                game.text_draw("GAME START", (game.w_h + 45) / 2, 25, palette.COLOR_GREEN, 30)
                current_player = palette.ai

            # Next game.
            if (125 + 45 * 16) > x_stone > 45 * 16 and 160 > y_stone > 115:
                game = caro.Caro(board_size)
                is_first_move = True
                game.screen.fill(palette.COLOR_BOARD)
                stone = {palette.ai: [], palette.human: []}
                game.draw_main()
                game.draw_score(ai_score, human_score)
                game.text_draw("NEXT GAME START", (game.w_h + 45) / 2, 25, palette.COLOR_GREEN, 30)
                current_player = palette.ai

            # Draw stone.
            if current_player is None or (x_stone - x_stone % game.area, y_stone - y_stone % game.area) in stone[
                palette.ai] + stone[palette.human]:
                pass
            # Draw a white stone (Player 2).
            elif current_player == palette.human and game.winner is None:
                if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:
                    x_stone, y_stone = game.play_draw_stone_pos()
                    stone = game.play_draw_stone(palette.human,
                                                 x_stone, y_stone, game)
                    human_score = game.check_win(human_score, palette.human)
                    current_player = palette.ai
                    if len(stone[palette.ai]) + len(stone[palette.human]) == game.size ** 2:
                        game.text_draw("DRAW", 45 * 16 + 65, game.w_h // 2 + 120,
                                       (200, 0, 0), 45)
                        current_player = None
        # Draw a white stone (Player 1).
        elif current_player == palette.ai and game.winner is None:
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            move = (game.area * (game.size // 2), game.area * (game.size // 2))
            if is_first_move:
                # game.stone[palette.ai].append(move)
                is_first_move = False
            else:
                move = ai.minimax_cutoff(game, current_player)
            stone = game.play_draw_stone(palette.ai, move[0], move[1], game)
            ai_score = game.check_win(ai_score, palette.ai)
            current_player = palette.human
            if len(stone[palette.ai]) + len(stone[palette.human]) == game.size ** 2:
                game.text_draw("DRAW", 45 * 16 + 65, game.w_h // 2 + 120,
                               (200, 0, 0), 45)
                current_player = None
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

        game.interactive_button()
        pygame.display.update()
