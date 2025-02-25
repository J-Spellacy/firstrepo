import pygame
from pygame.locals import *
import numpy as np
import time
import sys

''' 
coding chess game using pygame following this tutorial:https://levelup.gitconnected.com/chess-python-ca4532c7f5a4
'''

w_pawn, b_pawn = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\pawn_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png")
w_bishop, b_bishop = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\bishop_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_bishop_no_bg.png")
w_knight, b_knight = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\knight_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_knight_no_bg.png")
w_rook, b_rook = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\rook_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_rook_no_bg.png")
w_queen, b_queen = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\queen_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_queen_no_bg.png")
w_king, b_king = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\king_no_bg.png"), pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_king_no_bg.png")


# defines the square as a surface with a rectangle for position detection later, 
# might just use the actual position of the piece if thats more efficient down the line
class Square(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(Square, self).__init__()
        
        self.surf = pygame.Surface((64, 64))
        self.position = position
        if colour == "white":
            self.surf.fill((180, 180, 180))
        elif colour == "black":
            self.surf.fill((50, 50, 50))
        # position of rectangle is defined in the top left corner same as for surface
        self.rect = self.surf.get_rect()
        

class board():
    def __init__(self):
        board_positions  = np.zeros((8,8), dtype = object)
        for i in range(8):
            for j in range(8):
                board_positions[i][j] = ((i+1)*64, (j+1)*64)
        self.positions = board_positions
        self.surface = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\board.png").convert_alpha()


## defining the pieces

# current bug rect for pieces is not updating with position
class pawn(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(pawn, self).__init__()
        
        self.position = position
        self.colour = colour
        if self.colour == "white":
            self.surface = w_pawn
        else:
            self.surface = b_pawn
        
        self.rect = self.surface.get_rect()

class bishop(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(bishop, self).__init__()
        
        self.position = position
        self.colour = colour
        if self.colour == "white":
            self.surface = w_bishop
        else:
            self.surface = b_bishop
        
        self.rect = self.surface.get_rect()

class knight(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(knight, self).__init__()
        
        self.position = position
        self.colour = colour
        if self.colour == "white":
            self.surface = w_knight
        else:
            self.surface = b_knight
        
        self.rect = self.surface.get_rect()
        
class rook(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(rook, self).__init__()
        
        self.position = position
        self.colour = colour
        if self.colour == "white":
            self.surface = w_rook
        else:
            self.surface = b_rook
        
        self.rect = self.surface.get_rect()

class queen(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(queen, self).__init__()
        
        self.position = position
        self.colour = colour
        if self.colour == "white":
            self.surface = w_queen
        else:
            self.surface = b_queen
        
        self.rect = self.surface.get_rect()
        
class king(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(king, self).__init__()
        
        self.position = position
        self.colour = colour
        if self.colour == "white":
            self.surface = w_king
        else:
            self.surface = b_king
        
        self.rect = self.surface.get_rect()

## main code loop 

if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    
    
    colour = (100,100,100) 
    
    
    board_positions  = np.zeros((8,8), dtype = object)
    for i in range(8):
        for j in range(8):
            board_positions[i][j] = ((i+1)*64, (j+1)*64)
            
            
    # Define the dimensions of screen object
    screen = pygame.display.set_mode((640, 640))
    w_pawn_img = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\pawn_no_bg.png").convert_alpha()
    b_pawn_img = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png").convert_alpha()
    
    squares=[]
    for x in range(8):
        for y in range(8):
            colour = "black" if (x + y) % 2 else "white"
            squares.append(Square(colour, board_positions[x][y]))

    # places pieces initially
    pawns = []
    for x in range(8):
        pawns.append(pawn("white", board_positions[x][1]))
        pawns.append(pawn("black", board_positions[x][6]))
    
    w_rook_1 = rook("white", board_positions[0][0])
    w_rook_2 = rook("white", board_positions[7][0])
    b_rook_1 = rook("black", board_positions[0][7])
    b_rook_2 = rook("black", board_positions[7][7])
    w_knight_1 = knight("white", board_positions[1][0])
    w_knight_2 = knight("white", board_positions[6][0])
    b_knight_1 = knight("black", board_positions[1][7])
    b_knight_2 = knight("black", board_positions[6][7])
    w_queen_sprite = queen("white", board_positions[3][0])
    b_queen_sprite = queen("black", board_positions[3][7])
    w_king_sprite = king("white", board_positions[4][0])
    b_king_sprite = king("black", board_positions[4][7])
    w_bishop_1 = bishop("white", board_positions[2][0])
    w_bishop_2 = bishop("white", board_positions[5][0])
    b_bishop_1 = bishop("black", board_positions[2][7])
    b_bishop_2 = bishop("black", board_positions[5][7])
    
    w_pieces = [w_rook_1, w_knight_1, w_bishop_1, w_queen_sprite, w_king_sprite, w_bishop_2, w_knight_2, w_rook_2]
    b_pieces = [b_rook_1, b_knight_1, b_bishop_1, b_queen_sprite, b_king_sprite, b_bishop_2, b_knight_2, b_rook_2]
    
    # TITLE OF CANVAS 
    pygame.display.set_caption("The Board") 
    
    clock = pygame.time.Clock()
    test_surface = pygame.Surface((100, 200))
    test_surface.fill((250, 50, 50))
    
    
    i = 0
    exit = False
    
    ## running the game
    while not exit: 
        
        # draw all elements
        screen.fill(colour)

        # screen.blit(test_surface, (64, 64))
        
        for s in squares:
            screen.blit(s.surf, s.position)
        for p in pawns:
            screen.blit(p.surface, p.position)
        for p in w_pieces:
            screen.blit(p.surface, p.position)
        for p in b_pieces:
            screen.blit(p.surface, p.position) 
        
        pieces =  pawns + w_pieces + b_pieces
        
        mouse_pos = pygame.mouse.get_pos()
        # update everything in main run loop
        
        for p in pieces:    
                if p.rect.collidepoint(mouse_pos):
                    print(pygame.mouse.get_pressed())
        
        # print(pygame.mouse.get_pressed())
               
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True
            # for p in pieces:    
            #     if p.rect.collidepoint(mouse_pos):
            
                    # p.position = mouse_pos
        
        pygame.display.update() 
        clock.tick(60)
    
    
