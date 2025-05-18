import pygame

import os
# In case you dont have a sound driver (ex: WSL does not support)
os.environ["SDL_AUDIODRIVER"] = "dummy"

import random
from time import sleep
from Nanahira.constants import *
from Nanahira.board import *
from Nanahira.messages import *
from Nanahira.menu import *
from Nanahira.MenuAISelection import *
from Nanahira.Id3ConfigMenu import draw_id3_configuration_menu, draw_difficulty_selection_menu
from Nanahira.HandlePvaiId3 import handle_player_vs_ai_game
from Nanahira.MCTSConfigMenu import draw_mcts_configuration_menu, draw_mcts_epoch_menu
import Nanahira.ai_id3 as ai_id3
import Nanahira.ai_mcts as ai_mcts
from Nanahira.ai_mcts import benchmark_mcts
from Nanahira.AivsAIConfigMenu import draw_ai_vs_ai_selection_menu, draw_ai_vs_ai_mode_menu, prompt_headless_runs

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((CONFIG["window_width"], CONFIG["window_height"]))
    pygame.display.set_caption("Nanahira Connect 4!")
    bg = pygame.transform.scale(pygame.image.load('./Assets/Background.jpg').convert(), (CONFIG["window_width"], CONFIG["window_height"]))
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    FPS = 15

    ai_id3.load_saved_trees()

    animate_title_screen_intro(screen, bg)
    pygame.event.clear()
    show_title = True

    while show_title:
        draw_title_screen(screen, bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_message_image(screen, image=joever_img)
                pygame.time.wait(600)
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_x = (CONFIG["window_width"] - 400) // 2
                button_y = CONFIG["window_height"] - 150
                if button_x <= mouse_x <= button_x + 400 and button_y <= mouse_y <= button_y + 100:
                    pygame.mixer.Sound.play(click_sound)
                    animate_title_screen_exit(screen, bg)
                    show_title = False

    animate_selection_menu_intro(screen, bg)
    while True:
        draw_menu(screen, bg)
        pygame.display.update()
        clock.tick(FPS)
        selected_mode = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_message_image(screen, image=joever_img)
                pygame.time.wait(600)
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F10:
                    from Nanahira.ai_mcts import benchmark_mcts
                    benchmark_mcts(epochs=2000, mode="normal")
                    benchmark_mcts(epochs=2000, mode="parallel", parallel_workers=4)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                selection = get_menu_selection(mouseX, mouseY)
                if selection is not None:
                    pygame.mixer.Sound.play(click_sound)
                mouseX, mouseY = pygame.mouse.get_pos()
                selection = get_menu_selection(mouseX, mouseY)
                if selection == "BACK":
                    animate_title_screen_intro(screen, bg)
                    show_title = True
                    while show_title:
                        draw_title_screen(screen, bg)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                display_message_image(screen, image=joever_img)
                                pygame.time.wait(600)
                                pygame.quit()
                                return
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                button_x = (CONFIG["window_width"] - 400) // 2
                                button_y = CONFIG["window_height"] - 150
                                if button_x <= mouse_x <= button_x + 400 and button_y <= mouse_y <= button_y + 100:
                                    pygame.mixer.Sound.play(click_sound)
                                    animate_title_screen_exit(screen, bg)
                                    show_title = False
                                    animate_selection_menu_intro(screen, bg)
                    break
                elif selection == "Player x Player":
                    selected_mode = selection
                    break
                elif selection == "Player x AI":
                    ai_choice = draw_ai_selection_menu(screen, bg)
                    if ai_choice == "ID3":
                        config = draw_id3_configuration_menu(screen, bg)
                        if config:
                            player_color, id3_type = config
                            difficulty = draw_difficulty_selection_menu(screen, bg)
                            if difficulty is None:
                                animate_selection_menu_intro(screen, bg)
                                continue

                            ai_color = 2 if player_color == 1 else 1
                            ai_id3.load_saved_trees(difficulty)
                            learned_trees = {1: ai_id3.learned_trees_p1, 2: ai_id3.learned_trees_p2}
                            ai_trees = learned_trees.get(ai_color)

                            if not ai_trees:
                                nope_img = image.load('./Assets/nope.png')
                                display_message_image_training(screen, nope_img, "AI not trained yet!")
                                animate_selection_menu_intro(screen, bg)
                                continue
                            else:
                                print(f"AI tree count: {len(ai_trees)}")
                                if id3_type == "simple":
                                    ai_func = ai_id3.execute_learned_move(ai_trees[0])
                                else:  # "advanced"
                                    ai_func = ai_id3.make_ensemble_ai(ai_trees)

                            result = handle_player_vs_ai_game(screen, bg, player_color, ai_color, ai_func)
                            if result == "TO_MENU":
                                animate_selection_menu_intro(screen, bg)
                                continue
                            continue
                        else:
                            animate_selection_menu_intro(screen, bg)
                            continue
                    elif ai_choice == "MCTS":
                        config = draw_mcts_configuration_menu(screen, bg)
                        if config:
                            player_color, mcts_type = config
                            epochs = draw_mcts_epoch_menu(screen, bg)
                            if epochs is None:
                                animate_selection_menu_intro(screen, bg)
                                continue

                            ai_color = 2 if player_color == 1 else 1
                            if mcts_type == "normal":
                                ai_func = ai_mcts.execute_monte_carlo_move(epochs, c=1.4, player=ai_color)
                            else:
                                ai_func = ai_mcts.execute_monte_carlo_move_parallel(epochs, c=1.4, player=ai_color)

                            result = handle_player_vs_ai_game(screen, bg, player_color, ai_color, ai_func)
                            if result == "TO_MENU":
                                animate_selection_menu_intro(screen, bg)
                                continue
                            continue
                        else:
                            animate_selection_menu_intro(screen, bg)
                            continue
                    elif ai_choice == "BACK":
                        animate_selection_menu_intro(screen, bg)
                        continue
                elif selection == "AI x AI":
                    ai_white = draw_ai_vs_ai_selection_menu(screen, bg, label="White")
                    if ai_white == "BACK":
                        animate_selection_menu_intro(screen, bg)
                        continue
                    ai_black = draw_ai_vs_ai_selection_menu(screen, bg, label="Black")
                    if ai_black == "BACK":
                        animate_selection_menu_intro(screen, bg)
                        continue
                    print(f"White AI: {ai_white}, Black AI: {ai_black}")

                    id3_config = {}
                    mcts_config = {}

                    if ai_white == "id3":
                        id3_config[1] = draw_difficulty_selection_menu(screen, bg)
                        if id3_config[1] is None:
                            animate_selection_menu_intro(screen, bg)
                            continue
                    elif ai_white == "mcts":
                        mcts_config[1] = draw_mcts_epoch_menu(screen, bg)
                        if mcts_config[1] is None:
                            animate_selection_menu_intro(screen, bg)
                            continue

                    if ai_black == "id3":
                        id3_config[2] = draw_difficulty_selection_menu(screen, bg)
                        if id3_config[2] is None:
                            animate_selection_menu_intro(screen, bg)
                            continue
                    elif ai_black == "mcts":
                        mcts_config[2] = draw_mcts_epoch_menu(screen, bg)
                        if mcts_config[2] is None:
                            animate_selection_menu_intro(screen, bg)
                            continue

                    for player, diff in id3_config.items():
                        ai_id3.load_saved_trees(diff)

                    if (ai_white == "id3" and not ai_id3.learned_trees_p1) or (ai_black == "id3" and not ai_id3.learned_trees_p2):
                        nope_img = pygame.image.load('./Assets/nope.png')
                        display_message_image_training(screen, nope_img, "ID3 AI not trained yet!")
                        animate_selection_menu_intro(screen, bg)
                        continue

                    mode = draw_ai_vs_ai_mode_menu(screen, bg)
                    if mode == "BACK":
                        animate_selection_menu_intro(screen, bg)
                        continue

                    print(f"Selected Match Type: {mode}")
                    from Nanahira.HandleAivsAI import run_headless_simulations, handle_ai_vs_ai_game

                    def get_ai_func(label, player):
                        if label == "random":
                            def random_ai(game): return random.choice(game.state.available_moves)
                            random_ai.__name__ = "random_ai"
                            return random_ai
                        elif label == "id3":
                            trees = ai_id3.learned_trees_p1 if player == 1 else ai_id3.learned_trees_p2
                            return ai_id3.make_ensemble_ai(trees)
                        elif label == "mcts":
                            epochs = mcts_config.get(player, 500)
                            return ai_mcts.execute_monte_carlo_move_parallel(epochs, c=1.4, player=player)

                    white_func = get_ai_func(ai_white, 1)
                    black_func = get_ai_func(ai_black, 2)

                    if mode == "headless":
                        runs = prompt_headless_runs(screen, bg)
                        run_headless_simulations(white_func, black_func, runs)
                        animate_selection_menu_intro(screen, bg)
                        continue
                    else:
                        result = handle_ai_vs_ai_game(screen, bg, white_func, black_func, ai_white, ai_black)
                        if result == "TO_MENU":
                            animate_selection_menu_intro(screen, bg)
                            continue

        if selected_mode:
            print(f"Selected Mode: {selected_mode}")
            if selected_mode == "Player x Player":
                result = handle_pvp_game(screen, bg)
                if result == "TO_MENU":
                    animate_selection_menu_intro(screen, bg)
                    continue
            continue

if __name__ == '__main__':
    main()
