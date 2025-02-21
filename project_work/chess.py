import pygame
from pygame.locals import *
import time
import sys

''' 
coding chess game using pygame following this tutorial:https://levelup.gitconnected.com/chess-python-ca4532c7f5a4
'''

w_pawn, b_pawn = pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/pawn_no_bg.png"), pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/b_pawn_no_bg.png")
w_bishop, b_bishop = pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/bishop_no_bg.png"), pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/b_bishop_no_bg.png")
w_knight, b_knight = pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/knight_no_bg.png"), pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/b_knight_no_bg.png")
w_rook, b_rook = pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/rook_no_bg.png"), pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/b_rook_no_bg.png")
w_queen, b_queen = pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/queen_no_bg.png"), pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/b_queen_no_bg.png")
w_king, b_king = pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/king_no_bg.png"), pygame.image.load("C:/Users/User/Documents/GitHub/firstrepo/project_work/b_king_no_bg.png")



class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
        
        self.surf = pygame.Surface((25, 25))
         
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect()
        

def board_start(positions):
    for i in positions:
        if i[0] == 128:
            break
    return


    
if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    
    colour = (0,0,255) 
    board_positions = [((i*64)+64, (512-j*64)+64) for i in range(8) for j in range(1,9)]
    
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
        # for p in board_positions[::2]:
        #     screen.blit(w_pawn_img, p)
        # board set up (initial positions)
        for p in board_positions:
            screen.blit(b_pawn_img, p)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True
        pygame.display.update() 
    
    
