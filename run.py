import pygame
import pygame.gfxdraw
from pygame.locals import *
import display

def main():
    pygame.init()

#screen set    
    screen = pygame.display.set_mode([1034,778])
    pygame.display.set_caption('DoraAMon Adventure')
    clock = pygame.time.Clock()

    pygame.mixer.init()

    pygame.mixer.music.load(r"music\background.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
# game loops
    # 1. start menu , press space to continue 
    display.game_start(screen, clock)
    # 2. the main game loop
    WIN = False
    level = -1
    game = True
    while game:
        level += 1
        if level < 3:
            game = display.game_level(screen, clock, WIN, level)
        else:
            WIN = True
            break
    # final result image, be killed will lose, quit while playing will lose, eat all foods will win
    display.game_over(screen, clock, WIN) 

if __name__ == "__main__":
    main()