import pygame
import pygame.gfxdraw
from pygame.locals import *

import Ai
import maze
import character
import fonts

def game_start(screen, clock):
    
    # pacman image     
    start = 1
    cnr_x = 400
    cnr_y = 230
    speed = 4

    # main loop
    while start:
        clock.tick(12)
        cnr_x += speed
        cnr_y += speed
        corner = (cnr_x, cnr_y)
    
        if(cnr_x == 440):
            speed = - speed
        if(cnr_x == 400):
            speed = - speed
        white = (255, 255, 255)
        screen.fill(white) 
        show_screen(screen,corner)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    start = False
                elif event.key == pygame.K_ESCAPE: 
                    start = False
                elif event.key == pygame.K_SPACE:
                    start = False 

        pygame.display.flip()

    
def game_level(screen, clock, WIN, level):    
    
    # loop check
    # all three loops, start with a pac-man image
    # space to play the game
    # end loop use for final result(win or lose)    
    running = True
    
    # the pac-man always born at the right-down corner
    org_x = [11, 13, 17]
    org_y =[11, 13, 17]
    pm_x = [11, 13, 17]
    pm_y = [11, 13, 17]
    ghost_level = [2, 3, 4]

    # if continue, generate a smaller maze for the simpler level
    g = maze.Grid(org_x[level]+1,org_y[level]+1)
    maze.improved_sidewinder(g)
    #maze.abw_improvement(g)
    print(Ai.aStarSearch(g))
    pygame.mixer.init()
    sound_effect1 = pygame.mixer.Sound(r"music\effect.mp3")
    sound_effect2 = pygame.mixer.Sound(r"music\effect2.mp3")
    sound_effect3 = pygame.mixer.Sound(r"music\effect3.mp3")
    
    # three spirites groups stand for pac-man, ghost and food
    pacman_sprites = pygame.sprite.Group()
    food_sprites = pygame.sprite.Group()
    ghost_sprites = pygame.sprite.Group()
    super_food_sprites = pygame.sprite.Group()
    bcollide1 = pygame.sprite.Group()
    bcollide2 = pygame.sprite.Group()

    # there is only one pac-man in the group, when the pac-man be killed, game is over
    pacman = character.pac_man(pm_x[level], pm_y[level])
    pacman_sprites.add(pacman)
    
    # interate to fill the maze with foods
    for i in range(g.num_rows):
        for j in range(g.num_columns):
            if (((i==0) and (j==0)) or ((i==0) and(j==g.num_columns-1)) or ((j==0) and(i==g.num_rows-1))):
                sf = character.super_food(i,j)
                super_food_sprites.add(sf)
            elif (i==g.num_rows-1) and (j==g.num_columns-1):
                continue
            else:
                f = character.food(i,j)
                food_sprites.add(f)
            

    g_center1 = int((org_x[level]+1)/2-1)
    g_center2 = int((org_x[level]+1)/2)
    # generate four ghosts and add them to the same group        
    if ghost_level[level] == 2:
        ghost1 = character.ghost1(g_center1,g_center1)
        ghost2 = character.ghost2(g_center2,g_center2)
        ghost_sprites.add(ghost1) 
        ghost_sprites.add(ghost2)  
    elif ghost_level[level] == 3:
        ghost1 = character.ghost1(g_center1,g_center1)
        ghost2 = character.ghost2(g_center2,g_center2)
        ghost4 = character.ghost4(g_center1,g_center2)
        ghost_sprites.add(ghost1) 
        ghost_sprites.add(ghost2)  
        ghost_sprites.add(ghost4)  
    else :
        ghost1 = character.ghost1(g_center1,g_center1)
        ghost2 = character.ghost2(g_center2,g_center2)
        ghost3 = character.ghost3(g_center1,g_center2)
        ghost4 = character.ghost4(g_center2,g_center1)
        ghost_sprites.add(ghost1) 
        ghost_sprites.add(ghost2)  
        ghost_sprites.add(ghost3)  
        ghost_sprites.add(ghost4)
   
    
    button1 = character.button1()
    button2 = character.button2()
    bcollide1.add(button1)
    bcollide2.add(button2)
    # the fps_counter ensures the ghost's move 4 times one second
    fps_counter = 1
    change_direction = 1
    pause_flag = 1
    # the main game loop   
    while running:
        # first check where the pac-man should go 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == K_q:  # Quit
                    running = False
                elif event.key == K_DOWN:
                    change_direction = 0
                elif event.key == K_LEFT:
                    change_direction = 1 
                elif event.key == K_RIGHT:
                    change_direction = 2
                elif event.key == K_UP:
                    change_direction = 3
            if event.type == pygame.MOUSEBUTTONDOWN:
                collide = event.pos
                result = check_button(button1,button2,collide)
                if result == 1:
                    help_menu(screen)
                elif result == 2:
                    pause_flag = -pause_flag
        
        if pause_flag > 0:
        # ramdonly control the ghosts' movement
            if ghost_level[level] == 2:
                character.ghost1_movement(ghost1, fps_counter, g)
                character.ghost2_movement(ghost2, fps_counter, g)
            elif ghost_level[level] == 3:
                character.ghost1_movement(ghost1, fps_counter, g)
                character.ghost2_movement(ghost2, fps_counter, g)
                character.ghost4_movement(ghost4, fps_counter, g, pacman)
            else:
                character.ghost1_movement(ghost1, fps_counter, g)
                character.ghost2_movement(ghost2, fps_counter, g)
                character.ghost3_movement(ghost3, fps_counter, g, pacman)
                character.ghost4_movement(ghost4, fps_counter, g, pacman)       
        
            character.pacman_movement(pacman, fps_counter, g, change_direction)
        
        # each second check all 200 fp
        if fps_counter == 199:
            fps_counter = 0
        else:
            fps_counter += 1
        # each fp check if there are any colisions, pac-man eat food and ghost kill pac-man
        eat = pygame.sprite.spritecollide(pacman, food_sprites,dokill=1)
        if len(eat) != 0:
            sound_effect1.play()
        collide1 = pygame.sprite.spritecollide(pacman, super_food_sprites,dokill=1)
        if len(collide1) != 0:
            sound_effect3.play()
            pacman.super = 400
        if pacman.super != 0:
            collide2 = pygame.sprite.groupcollide(pacman_sprites, ghost_sprites,dokilla=0,dokillb=1)
        else:
            collide2 = pygame.sprite.groupcollide(pacman_sprites, ghost_sprites,dokilla=0,dokillb=0)
            if len(collide2) != 0:
                sound_effect2.play()
                pacman.life -= 1
                pacman.update(org_x[level],org_y[level])
                if pacman.life == 0:
                    running = False
        if(pacman.super != 0):
            pacman.super -= 1
        #if there is no food, pac-man wins 
        if len(food_sprites) == 0:
            running = False
            WIN = True
        # if there is no pac-man, it was killed and so lose 
        
        # show the score on the status bar
        max_food = (org_x[level] + 1) * (org_y[level] + 1)-1
        score = max_food - len(food_sprites)-len(super_food_sprites)
        # show the maze with the result
        display_grid(g, screen, pacman, pacman_sprites, food_sprites, ghost_sprites, super_food_sprites, bcollide1, bcollide2)
        show_score(screen, score, level)
        show_life(screen, pacman.life)
        pygame.display.flip()
        clock.tick(200)
    if WIN == True:
        return True
    else:
        return False



def game_over(screen, clock, WIN):       
    
    # final result image, be killed will lose, quit while playing will lose, eat all foods will win
    end = True
    # font variables
    fontobj3 = fonts.setup_fonts(150,True)
    TEXT3 = 'YOU LOSE!'
    upper_left3 = (120, 380)
    length_height3 = (1000, 500)
    wrapped_rect3= pygame.Rect(upper_left3, length_height3)
    wrapped_surface3 = fonts.word_wrap(wrapped_rect3, fontobj3, (255, 255, 255), TEXT3)
    TEXT4 = 'YOU WIN!'
    upper_left4 = (170, 280)
    length_height4 = (1000, 500)
    wrapped_rect4= pygame.Rect(upper_left4, length_height4)
    wrapped_surface4 = fonts.word_wrap(wrapped_rect4, fontobj3, (255, 255, 255), TEXT4)          
    
    while end:
        clock.tick(12)
        black = (0, 0, 0)
        screen.fill(black) 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    end = False
                elif event.key == pygame.K_ESCAPE: 
                    end = False
        if WIN == True:
            img = pygame.image.load(r"image\Win.jpg").convert_alpha()
            img = pygame.transform.scale(img, (1034,778))
            screen.blit(img,(0, 0))
            screen.blit(wrapped_surface4, wrapped_rect4)
        else: 
            img = pygame.image.load(r"image\Lose.jpg").convert_alpha()
            img = pygame.transform.scale(img, (1034,778))
            screen.blit(img,(0, 0))
            screen.blit(wrapped_surface3, wrapped_rect3)
        pygame.display.flip() 


def display_grid(g, screen, pacman, pac_man, food, ghost, super_food, bcollide1, bcollide2):
    screen.fill((255, 255, 255))
    img = pygame.image.load(r"image\sky3.jpg")
    img = pygame.transform.scale(img, (1034,778))
    screen.blit(img,(0,0))
    
    bcollide1.draw(screen)
    bcollide2.draw(screen)
    food.draw(screen)
    super_food.draw(screen)
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            c = g.cell_at(row, col)
            cell_x = col * 32 + 5
            cell_y = row * 32 + 5
            if not c.north or not c.is_linked(c.north):
                pygame.gfxdraw.hline(screen, 
                                     cell_x, cell_x+31, cell_y, 
                                     (0,0,0))
            if not c.south or not c.is_linked(c.south):
                pygame.gfxdraw.hline(screen, 
                                     cell_x, cell_x+31, cell_y+31, 
                                     (0,0,0))
            if not c.east or not c.is_linked(c.east):
                pygame.gfxdraw.vline(screen, 
                                     cell_x+31, cell_y, cell_y+31, 
                                     (0,0,0))
            if not c.west or not c.is_linked(c.west):
                pygame.gfxdraw.vline(screen, 
                                     cell_x, cell_y, cell_y+31, 
                                     (0,0,0))
    if pacman.super == 0:
            img =  pygame.image.load(r"image\daxiong.png").convert_alpha()
            pacman.image = pygame.transform.scale(img, (31, 31))
            pac_man.draw(screen)
    else:
            img =  pygame.image.load(r"image\duola.png").convert_alpha()
            pacman.image = pygame.transform.scale(img, (31, 31))
            pac_man.draw(screen)
    ghost.draw(screen)

def show_score(screen, score, level):
    str2 = str(level+1)
    text_color = (30, 30, 30)
    font1 = pygame.font.SysFont(None, 45)
    score_img1 = pygame.font.Font.render(font1, str2, True, text_color)
    screen.blit(score_img1, (920,12)) 
    
    
    str_score = str(score)
    text_color = (30, 30, 30)
    font1 = pygame.font.SysFont(None, 60)
    score_img1 = pygame.font.Font.render(font1, str_score, True, text_color)
    screen.blit(score_img1, (830,150))

def show_life(screen, life):
    if life == 3:
        img =  pygame.image.load(r"image\daxiong.png").convert_alpha()
        image = pygame.transform.scale(img, (31, 31))
        screen.blit(image,(840,495))
        screen.blit(image,(880,495))
        screen.blit(image,(920,495))
    elif life == 2:
        img =  pygame.image.load(r"image\daxiong.png").convert_alpha()
        image = pygame.transform.scale(img, (31, 31))
        screen.blit(image,(840,495))
        screen.blit(image,(880,495))
    elif life == 1:
        img =  pygame.image.load(r"image\daxiong.png").convert_alpha()
        image = pygame.transform.scale(img, (31, 31))
        screen.blit(image,(840,495))


def show_screen(screen,corner):
    img = pygame.image.load(r"image\sky.png")
    img = pygame.transform.scale(img, (1034,778))
    screen.blit(img,(0,0))
    img = pygame.image.load(r"image\bg.png")
    img = pygame.transform.scale(img, (200,200))
    screen.blit(img,corner)
        
 
    
def check_button(button1, button2, collide):
    if button1.rect.collidepoint(collide):
        return 1
    elif button2.rect.collidepoint(collide):
        return 2
    else:
        return 0

def help_menu(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
        img = pygame.image.load(r"image\help_menu.png")
        img = pygame.transform.scale(img, (1034,778))
        screen.blit(img,(0,0))
        pygame.display.flip() 




