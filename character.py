#! /usr/bin/env python3
''' Run cool maze generating algorithms. '''

import pygame
import maze
import random

class pac_man(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)
        self.life = 3
        self.super = 0
        img =  pygame.image.load(r"image\daxiong.png").convert_alpha()
        self.image = pygame.transform.scale(img, (31, 31))
    def update(self, row, column):
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)

class food(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        self.rect = pygame.Rect(self.cell_x,self.cell_y,15,15)
        self.rect.center = (self.cell_x+15,self.cell_y+15)
        self.super = 0
        img =  pygame.image.load(r"image\lingdang.png").convert_alpha()
        self.image = pygame.transform.scale(img, (15, 15))

class super_food(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        self.rect = pygame.Rect(self.cell_x,self.cell_y,20,20)
        self.rect.center = (self.cell_x+15,self.cell_y+15)
        img =  pygame.image.load(r"image\duola2.png").convert_alpha()
        self.image = pygame.transform.scale(img, (20, 20)) 


class ghost1(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        img =  pygame.image.load(r"image\xiaofu.png").convert_alpha()
        self.image = pygame.transform.scale(img, (31, 31))
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)
    def update(self, row, column):
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)

class ghost2(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        img =  pygame.image.load(r"image\mama.png").convert_alpha()
        self.image = pygame.transform.scale(img, (31, 31))
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)
    def update(self, row, column):
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)

class ghost3(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        img =  pygame.image.load(r"image\panghu.png").convert_alpha()
        self.image = pygame.transform.scale(img, (31, 31))
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)
    def update(self, row, column):
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)

class ghost4(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        img =  pygame.image.load(r"image\laoshi.png").convert_alpha()
        self.image = pygame.transform.scale(img, (31, 31))
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)
    def update(self, row, column):
        self.x = row
        self.y = column
        self.cell_x = self.y * 32 + 5
        self.cell_y = self.x * 32 + 5
        self.rect = pygame.Rect(self.cell_x,self.cell_y,31,31)   
         
        

def ghost1_movement(ghost1, fps_counter, g):
    # ghost1 is noob and fast
    if (fps_counter % 50) == 0:
                i = ghost1
                choice1 = random.randint(0,1)
                choice2 = random.randint(0,1)
                if choice1 == 0 and choice2 == 0:
                    x_new = i.x-1
                    y_new = i.y
                    if x_new > -1:
                        if g.grid[i.x][i.y].is_linked(g.grid[x_new][y_new]):
                            i.update(x_new, y_new)
                        else:
                            llist = g.grid[i.x][i.y].all_links()
                            llen = len(llist)-1
                            idx = random.randint(0,llen)
                            x_new = llist[idx].row
                            y_new = llist[idx].column
                            i.update(x_new, y_new)
                    else:
                        llist = g.grid[i.x][i.y].all_links()
                        llen = len(llist)-1
                        idx = random.randint(0,llen)
                        x_new = llist[idx].row
                        y_new = llist[idx].column
                        i.update(x_new, y_new)
                elif choice1 == 0 and choice2 == 1:
                    x_new = i.x+1
                    y_new = i.y
                    if x_new < g.num_rows:
                        if g.grid[i.x][i.y].is_linked(g.grid[x_new][y_new]) :
                            i.update(x_new, y_new)
                        else:
                            llist = g.grid[i.x][i.y].all_links()
                            llen = len(llist)-1
                            idx = random.randint(0,llen)
                            x_new = llist[idx].row
                            y_new = llist[idx].column
                            i.update(x_new, y_new)
                    else:
                        llist = g.grid[i.x][i.y].all_links()
                        llen = len(llist)-1
                        idx = random.randint(0,llen)
                        x_new = llist[idx].row
                        y_new = llist[idx].column
                        i.update(x_new, y_new)
                elif choice1 == 1 and choice2 == 0:
                    x_new = i.x
                    y_new = i.y-1
                    if y_new > -1:
                        if g.grid[i.x][i.y].is_linked(g.grid[x_new][y_new]): 
                            i.update(x_new, y_new)
                        else:
                            llist = g.grid[i.x][i.y].all_links()
                            llen = len(llist)-1
                            idx = random.randint(0,llen)
                            x_new = llist[idx].row
                            y_new = llist[idx].column
                            i.update(x_new, y_new)
                    else:
                        llist = g.grid[i.x][i.y].all_links()
                        llen = len(llist)-1
                        idx = random.randint(0,llen)
                        x_new = llist[idx].row
                        y_new = llist[idx].column
                        i.update(x_new, y_new)
                elif choice1 == 1 and choice2 == 1:
                    x_new = i.x
                    y_new = i.y+1
                    if y_new < g.num_columns:
                        if g.grid[i.x][i.y].is_linked(g.grid[x_new][y_new]):
                            i.update(x_new, y_new)
                        else:
                            llist = g.grid[i.x][i.y].all_links()
                            llen = len(llist)-1
                            idx = random.randint(0,llen)
                            x_new = llist[idx].row
                            y_new = llist[idx].column
                            i.update(x_new, y_new)
                    else:
                        llist = g.grid[i.x][i.y].all_links()
                        llen = len(llist)-1
                        idx = random.randint(0,llen)
                        x_new = llist[idx].row
                        y_new = llist[idx].column
                        i.update(x_new, y_new)

def ghost2_movement(ghost2, fps_counter, g):
    # ghost1 is noob and slow
    if (fps_counter % 100) == 0:
                i = ghost2
                choice1 = random.randint(0,1)
                choice2 = random.randint(0,1)
                if choice1 == 0 and choice2 == 0:
                    x_new = i.x-1
                    y_new = i.y
                    if x_new > -1:
                        if g.grid[i.x][i.y].is_linked(g.grid[x_new][y_new]):
                            i.update(x_new, y_new)
                        else:
                            llist = g.grid[i.x][i.y].all_links()
                            llen = len(llist)-1
                            idx = random.randint(0,llen)
                            x_new = llist[idx].row
                            y_new = llist[idx].column
                            i.update(x_new, y_new)
                    else:
                        llist = g.grid[i.x][i.y].all_links()
                        llen = len(llist)-1
                        idx = random.randint(0,llen)
                        x_new = llist[idx].row
                        y_new = llist[idx].column
                        i.update(x_new, y_new)
                elif choice1 == 0 and choice2 == 1:
                    x_new = i.x+1
                    y_new = i.y
                    if x_new < g.num_rows:
                        if g.grid[i.x][i.y].is_linked(g.grid[x_new][y_new]) :
                            i.update(x_new, y_new)
                        else:
                            llist = g.grid[i.x][i.y].all_links()
                            llen = len(llist)-1
                            idx = random.randint(0,llen)
                            x_new = llist[idx].row
                            y_new = llist[idx].column
                            i.update(x_new, y_new)
                    else:
                        llist = g.grid[i.x][i.y].all_links()
                        llen = len(llist)-1
                        idx = random.randint(0,llen)
                        x_new = llist[idx].row
                        y_new = llist[idx].column
                        i.update(x_new, y_new)
                elif choice1 == 1 and choice2 == 0:
                    x_new = i.x
                    y_new = i.y-1
                    if y_new > -1:
                        if g.grid[i.x][i.y].is_linked(g.grid[x_new][y_new]): 
                            i.update(x_new, y_new)
                        else:
                            llist = g.grid[i.x][i.y].all_links()
                            llen = len(llist)-1
                            idx = random.randint(0,llen)
                            x_new = llist[idx].row
                            y_new = llist[idx].column
                            i.update(x_new, y_new)
                    else:
                        llist = g.grid[i.x][i.y].all_links()
                        llen = len(llist)-1
                        idx = random.randint(0,llen)
                        x_new = llist[idx].row
                        y_new = llist[idx].column
                        i.update(x_new, y_new)
                elif choice1 == 1 and choice2 == 1:
                    x_new = i.x
                    y_new = i.y+1
                    if y_new < g.num_columns:
                        if g.grid[i.x][i.y].is_linked(g.grid[x_new][y_new]):
                            i.update(x_new, y_new)
                        else:
                            llist = g.grid[i.x][i.y].all_links()
                            llen = len(llist)-1
                            idx = random.randint(0,llen)
                            x_new = llist[idx].row
                            y_new = llist[idx].column
                            i.update(x_new, y_new)
                    else:
                        llist = g.grid[i.x][i.y].all_links()
                        llen = len(llist)-1
                        idx = random.randint(0,llen)
                        x_new = llist[idx].row
                        y_new = llist[idx].column
                        i.update(x_new, y_new)

def ghost3_movement(ghost3, fps_counter, g, pacman):
    # ghost3 is clever and fast
    if (fps_counter % 50) == 0:
        i = ghost3
        start_cell = g.grid[i.x][i.y]
        goal_cell = g.grid[pacman.x][pacman.y]
        d = maze.ShortestPathMarkup(g, start_cell, goal_cell)
        cell_new = d.path.pop()
        cell_new = d.path.pop()
        x_new = cell_new.row
        y_new = cell_new.column
        i.update(x_new, y_new)
        
def ghost4_movement(ghost4, fps_counter, g, pacman):
    # ghost3 is clever and slow
    if (fps_counter % 100) == 0:
        i = ghost4
        start_cell = g.grid[i.x][i.y]
        goal_cell = g.grid[pacman.x][pacman.y]
        d = maze.ShortestPathMarkup(g, start_cell, goal_cell)
        cell_new = d.path.pop()
        cell_new = d.path.pop()
        x_new = cell_new.row
        y_new = cell_new.column
        i.update(x_new, y_new)


def pacman_movement(pacman, fps_counter, g, change_direction):
    if (fps_counter % 50) == 0 :
        if change_direction == 0:
            x_new = pacman.x+1
            y_new = pacman.y
            if x_new < g.num_rows:
                if g.grid[pacman.x][pacman.y].is_linked(g.grid[x_new][y_new]) :
                    pacman.update(x_new, y_new)
        elif change_direction == 1:
            x_new = pacman.x
            y_new = pacman.y-1
            y_new = y_new % g.num_columns
            if y_new > -1:
                if g.grid[pacman.x][pacman.y].is_linked(g.grid[x_new][y_new]) :
                    pacman.update(x_new, y_new)
        elif change_direction == 2:
            x_new = pacman.x
            y_new = pacman.y+1
            y_new = y_new % g.num_columns
            if y_new < g.num_columns:
                if g.grid[pacman.x][pacman.y].is_linked(g.grid[x_new][y_new]) :
                    pacman.update(x_new, y_new)
        elif change_direction == 3:
            x_new = pacman.x-1
            y_new = pacman.y
            if x_new > -1:
                if g.grid[pacman.x][pacman.y].is_linked(g.grid[x_new][y_new]) :
                    pacman.update(x_new, y_new)


class button1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cell_x = 20
        self.cell_y = 580
        img =  pygame.image.load(r"image\bot1.jpg").convert_alpha()
        self.image = pygame.transform.scale(img, (180, 180))
        self.rect = pygame.Rect(self.cell_x,self.cell_y,180,180)

class button2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cell_x = 250
        self.cell_y = 580
        img =  pygame.image.load(r"image\bot2.jpg").convert_alpha()
        self.image = pygame.transform.scale(img, (180, 180))
        self.rect = pygame.Rect(self.cell_x,self.cell_y,180,180)


        









    

