import pygame
from pygame.locals import *
import time
import sys

''' 
coding chess game using pygame following this tutorial:https://levelup.gitconnected.com/chess-python-ca4532c7f5a4
'''

class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        
        self.surf = pygame.Surface((25, 25))
         
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect()
        

    
if __name__ == "__main__":
    

    
    
    # initialize pygame
    pygame.init()
    
    colour = (0,0,255) 
    w_p_positions = [((i*64)+64, (512-j*64)+64) for i in range(8) for j in range(1,3)]
    b_p_positions = [((i*64)+64, (512-j*64)) for i in range(8) for j in range(6,8)]
    
        
    print(len(w_p_positions))
    
    w_pawn_img = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\queen_no_bg.png")
    b_pawn_img = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\b_queen_no_bg.png")
    
    # Define the dimensions of screen object
    screen = pygame.display.set_mode((640, 640))
    # TITLE OF CANVAS 
    pygame.display.set_caption("The Board") 
    exit = False
    
    ## running the game
    while not exit: 
        screen.fill(colour)
        for p in w_p_positions[::2]:
            screen.blit(w_pawn_img, p)
        for p in b_p_positions[9:16]:
            screen.blit(b_pawn_img, p)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True
        pygame.display.update() 
    
    
