import pygame
from pygame.locals import *
import numpy as np
import math
import time
import sys

## to do list
# can move pieces but if you drop a piece you can't pick it up again without picking up whatever is behind it too
# pieces need to snap to squares after you have dragged them and stopped pressing the mouse button
# shouldn't be able to place black pieces on the same square
# make it so you press the mouse button then you can drag it till you press it again instead of constantly holding it down
# add timers for each player
# add checkmate screen
# change .update() to make selective screen updates (more efficient i think)


''' 
coding chess game using pygame following this tutorial:https://levelup.gitconnected.com/chess-python-ca4532c7f5a4
'''
## defining the board
# defines the square as a surface with a rectangle for position detection later, 
# might just use the actual position of the piece if thats more efficient down the line
class Square(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(Square, self).__init__()
        
        self.image = pygame.Surface((64, 64))
        self.position = position
        if colour == "white":
            self.image.fill((180, 180, 180))
        elif colour == "black":
            self.image.fill((50, 50, 50))
        # position of rectangle is defined in the top left corner same as for surface
        self.rect = self.image.get_rect(topleft = self.position)
                
    def update(self, mouse_pos, event):
        pass

# defines the board which is currently not a sprite but will be maybe if the squares class can work with a drawn board (should do) later on
class Board():
    def __init__(self):
        board_positions  = np.zeros((8,8), dtype = object)
        for i in range(8):
            for j in range(8):
                board_positions[i][j] = ((i+1)*64, (j+1)*64)
        self.positions = board_positions
        # self.surface = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\board.png").convert_alpha()


## defining the pieces

# defines each piece by type, for later rule implementation per class
class pawn(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(pawn, self).__init__()
        
        self.position = position
        self.colour = colour
        self.gotten = False
        if self.colour == "white":
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\pawn_no_bg.png").convert_alpha()
        else:
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_pawn_no_bg.png").convert_alpha()
        
        self.rect = self.image.get_rect(topleft = self.position)
        self.init_sqr = self.rect.topleft
    
    # allows the player to move the pieces
    def drag(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.rect.center = (mouse_pos[0],mouse_pos[1])
            self.position = (mouse_pos[0]-32,mouse_pos[1]-32)
            self.gotten = True
            

    # updates the sprite
    def update(self, got_piece, mouse_pos, event, squares):
        if got_piece == False:
            self.init_sqr = self.rect.topleft
            self.drag(mouse_pos, event)
        elif self.gotten:
            self.drag(mouse_pos, event)
        self.drop(mouse_pos, event)
        
    def drop(self, mouse_pos, event):
        if event.type == MOUSEBUTTONUP and self.gotten:
            self.rect.topleft = (math.floor(mouse_pos[0]/64)*64,math.floor(mouse_pos[1]/64)*64) # dont need to add 64, 64 because division does not define 1 as 0
            self.gotten = False
    
    def get_curr_sqr(self, mouse_pos, event, squares):
        self.current_sqr = 


# rest of the pieces same structure as the pawn with their own seperate functions later down the line
class bishop(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(bishop, self).__init__()
        
        self.position = position
        self.colour = colour
        self.gotten = False
        if self.colour == "white":
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\bishop_no_bg.png").convert_alpha()
        else:
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_bishop_no_bg.png").convert_alpha()
        
        self.rect = self.image.get_rect(topleft = self.position)
        self.init_sqr = self.rect.topleft
    
    # allows the player to move the pieces
    def drag(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.rect.center = (mouse_pos[0],mouse_pos[1])
            self.position = (mouse_pos[0]-32,mouse_pos[1]-32)
            self.gotten = True
            

    # updates the sprite
    def update(self, got_piece, mouse_pos, event):
        if got_piece == False:
            self.init_sqr = self.rect.topleft
            self.drag(mouse_pos, event)
        elif self.gotten:
            self.drag(mouse_pos, event)
        self.drop(mouse_pos, event)
        
    def drop(self, mouse_pos, event):
        if event.type == MOUSEBUTTONUP and self.gotten:
            self.rect.topleft = (math.floor(mouse_pos[0]/64)*64,math.floor(mouse_pos[1]/64)*64) # dont need to add 64, 64 because division does not define 1 as 0
            self.gotten = False

class knight(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(knight, self).__init__()
        
        self.position = position
        self.colour = colour
        self.gotten = False
        if self.colour == "white":
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\knight_no_bg.png").convert_alpha()
        else:
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_knight_no_bg.png").convert_alpha()
        
        self.rect = self.image.get_rect(topleft = self.position)
        self.init_sqr = self.rect.topleft
    
    # allows the player to move the pieces
    def drag(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.rect.center = (mouse_pos[0],mouse_pos[1])
            self.position = (mouse_pos[0]-32,mouse_pos[1]-32)
            self.gotten = True
            

    # updates the sprite
    def update(self, got_piece, mouse_pos, event):
        if got_piece == False:
            self.init_sqr = self.rect.topleft
            self.drag(mouse_pos, event)
        elif self.gotten:
            self.drag(mouse_pos, event)
        self.drop(mouse_pos, event)
        
    def drop(self, mouse_pos, event):
        if event.type == MOUSEBUTTONUP and self.gotten:
            self.rect.topleft = (math.floor(mouse_pos[0]/64)*64,math.floor(mouse_pos[1]/64)*64) # dont need to add 64, 64 because division does not define 1 as 0
            self.gotten = False
        
class rook(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(rook, self).__init__()
        
        self.position = position
        self.colour = colour
        self.gotten = False
        if self.colour == "white":
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\rook_no_bg.png").convert_alpha()
        else:
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_rook_no_bg.png").convert_alpha()
        
        self.rect = self.image.get_rect(topleft = self.position)
        self.init_sqr = self.rect.topleft
    
    # allows the player to move the pieces
    def drag(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.rect.center = (mouse_pos[0],mouse_pos[1])
            self.position = (mouse_pos[0]-32,mouse_pos[1]-32)
            self.gotten = True
            

    # updates the sprite
    def update(self, got_piece, mouse_pos, event):
        if got_piece == False:
            self.init_sqr = self.rect.topleft
            self.drag(mouse_pos, event)
        elif self.gotten:
            self.drag(mouse_pos, event)
        self.drop(mouse_pos, event)
        
    def drop(self, mouse_pos, event):
        if event.type == MOUSEBUTTONUP and self.gotten:
            self.rect.topleft = (math.floor(mouse_pos[0]/64)*64,math.floor(mouse_pos[1]/64)*64) # dont need to add 64, 64 because division does not define 1 as 0
            self.gotten = False

class queen(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(queen, self).__init__()
        
        self.position = position
        self.colour = colour
        self.gotten = False
        if self.colour == "white":
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\queen_no_bg.png").convert_alpha()
        else:
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_queen_no_bg.png").convert_alpha()
        
        self.rect = self.image.get_rect(topleft = self.position)
        self.init_sqr = self.rect.topleft
    
    # allows the player to move the pieces
    def drag(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.rect.center = (mouse_pos[0],mouse_pos[1])
            self.position = (mouse_pos[0]-32,mouse_pos[1]-32)
            self.gotten = True
            

    # updates the sprite
    def update(self, got_piece, mouse_pos, event):
        if got_piece == False:
            self.init_sqr = self.rect.topleft
            self.drag(mouse_pos, event)
        elif self.gotten:
            self.drag(mouse_pos, event)
        self.drop(mouse_pos, event)
        
    def drop(self, mouse_pos, event):
        if event.type == MOUSEBUTTONUP and self.gotten:
            self.rect.topleft = (math.floor(mouse_pos[0]/64)*64,math.floor(mouse_pos[1]/64)*64) # dont need to add 64, 64 because division does not define 1 as 0
            self.gotten = False
        
class king(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple):
        super(king, self).__init__()
        
        self.position = position
        self.colour = colour
        self.gotten = False
        if self.colour == "white":
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\king_no_bg.png").convert_alpha()
        else:
            self.image = pygame.image.load(r"C:\Users\User\Documents\GitHub\firstrepo\project_work\sprites\no_backgrounds\b_king_no_bg.png").convert_alpha()
        
        self.rect = self.image.get_rect(topleft = self.position)
        self.init_sqr = self.rect.topleft
    
    # allows the player to move the pieces
    def drag(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.rect.center = (mouse_pos[0],mouse_pos[1])
            self.position = (mouse_pos[0]-32,mouse_pos[1]-32)
            self.gotten = True
            

    # updates the sprite
    def update(self, got_piece, mouse_pos, event):
        if got_piece == False:
            self.init_sqr = self.rect.topleft
            self.drag(mouse_pos, event)
        elif self.gotten:
            self.drag(mouse_pos, event)
        self.drop(mouse_pos, event)
        
    def drop(self, mouse_pos, event):
        if event.type == MOUSEBUTTONUP and self.gotten:
            self.rect.topleft = (math.floor(mouse_pos[0]/64)*64,math.floor(mouse_pos[1]/64)*64) # dont need to add 64, 64 because division does not define 1 as 0
            self.gotten = False

## main code loop 

def main():
    # sets up screen and moving time
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()
    pygame.display.set_caption("The Board") 
    
    # defines the board
    board = Board()
    board_positions = board.positions
    squares = pygame.sprite.Group()
    for x in range(8):
        for y in range(8):
            colour = "black" if (x + y) % 2 else "white"
            squares.add(Square(colour, board_positions[x][y]))
    
    # places pieces initially
    pieces =  pygame.sprite.Group()
    for x in range(8):
        pieces.add(pawn("white", board_positions[x][1]))
        pieces.add(pawn("black", board_positions[x][6]))
    pieces.add(rook("white", board_positions[0][0]))
    pieces.add(rook("white", board_positions[7][0]))
    pieces.add(rook("black", board_positions[0][7]))
    pieces.add(rook("black", board_positions[7][7]))
    pieces.add(knight("white", board_positions[1][0]))
    pieces.add(knight("white", board_positions[6][0]))
    pieces.add(knight("black", board_positions[1][7]))
    pieces.add(knight("black", board_positions[6][7]))
    pieces.add(queen("white", board_positions[3][0]))
    pieces.add(queen("black", board_positions[3][7]))
    pieces.add(king("white", board_positions[4][0]))
    pieces.add(king("black", board_positions[4][7]))
    pieces.add(bishop("white", board_positions[2][0]))
    pieces.add(bishop("white", board_positions[5][0]))
    pieces.add(bishop("black", board_positions[2][7]))
    pieces.add(bishop("black", board_positions[5][7]))
    
    # initialises used params in loop
    got_piece = False
    exit = False
    game_active = True
    ## running the game
    while not exit: 
        if game_active:
            # draw all elements
            screen.fill((100,100,100))
            squares.draw(screen)
            pieces.draw(screen)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True
            
            if game_active:
                squares.update(mouse_pos, event)
                pieces.update(got_piece, mouse_pos, event, squares)
                got_piece = pygame.mouse.get_pressed()[0]
                
        pygame.display.update() 
        clock.tick(60)

## running main code loop
if __name__ == "__main__":
    main()
    
    
