import pygame
from pygame.locals import *
import time
import sys

''' 
coding chess game using pygame following this tutorial:https://levelup.gitconnected.com/chess-python-ca4532c7f5a4
'''

w_pawn, b_pawn = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\pawn_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png")
w_bishop, b_bishop = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\pawn_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png")
w_knight, b_knight = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png")
w_rook, b_rook = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png")
w_queen, b_queen = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png")
w_king, b_king = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png")



class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        
        self.surf = pygame.Surface((25, 25))
         
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect()
        

class board():
    def __init__(self):
        self.positions = [(i*64, j*64) for i in range(1,9) for j in range(1,9)]
        for i in self.positions:
            if i[0] == 128:
                break
        return


    
if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    i = 0
    
    colour = (100,100,100) 
    board_positions = [((i*64), (j*64)) for i in range(1,9) for j in range(1,9)]
    
    w_pawn_img = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\pawn_no_bg.png")
    b_pawn_img = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png")
    
    # Define the dimensions of screen object
    screen = pygame.display.set_mode((640, 640))
    # TITLE OF CANVAS 
    pygame.display.set_caption("The Board") 
    
    clock = pygame.time.Clock()
    test_surface = pygame.Surface((100, 200))
    test_surface.fill((250, 50, 50))
    exit = False
    
    ## running the game
    while not exit: 
        
        # draw all elements
        screen.fill(colour)

        screen.blit(test_surface, (64, 64))
        
        # update everything
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True
            if event.type == pygame.KEYDOWN:
                screen.blit(b_pawn_img, board_positions[i])
                i += 1
        pygame.display.update() 
        clock.tick(60)
    
    
