# main.py
import pygame
import sys
import Game # Import the game file

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    print("Starting Game...")
    main_game_instance = Game.Game()
    main_game_instance.run()
    print("Exiting Game...")
    pygame.quit()
    sys.exit()