import pygame
from pygame.locals import *
import numpy as np
import math
import time
import sys

## to do list

# game is fully playable as white or black but no board flipping
# board flipping

# optional:

# read board game state notation and set up board in said position, potentially even move forward one move based on new line of notation, also return current board state as notation
# layer sprites so that the available squares is drawn beneath pieces
# make it so you press the mouse button then you can drag it till you press it again instead of constantly holding it down (configurable)
# change .update() to make selective screen updates (more efficient i think)

## bugs

# piece lags behind mouse and stops drag()  till  mouse rejoins it


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
                
    def update(self, mouse_pos):
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
    
    def chk_mate_screen(self, screen, white_pieces, black_pieces, font, font2):
        if white_pieces.game_active:
            win_str = 'white'
        elif black_pieces.game_active:
            win_str = 'black'
        check_mate_text = font.render(f'checkmate!!  {win_str} wins!!  well done!!', False, (0,0,0))
        win_text_rect = check_mate_text.get_rect(center = (640, 180))
        screen.blit(check_mate_text, win_text_rect)
        rst_button_surf = pygame.image.load('project_work/sprites/button.png').convert_alpha()
        self.rst_button_rect = rst_button_surf.get_rect(center = (640, 320))
        screen.blit(rst_button_surf, self.rst_button_rect)
        rst_txt_surf = font2.render('restart?', False, (64,64,64))
        rst_txt_rect = rst_txt_surf.get_rect(center = (640, 320))
        screen.blit(rst_txt_surf, rst_txt_rect)
    
    def restart_game(self, mouse_pos):
        if self.rst_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True

# not working hurumph
class Timer(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, pieces, time_between_turns):
        super(Timer, self).__init__()
        self.pos = pos
        self.base_image = pygame.image.load('project_work/sprites/button.png').convert_alpha()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center = self.pos)
        self.total_time = 600
        self.current_time = 0
        self.end_time = time_between_turns
        self.in_turn = pieces.my_turn

    def update(self, font, pieces, screen, time_passed):
        if pieces.my_turn:
            self.current_time = self.total_time - (time_passed - self.end_time)
            self.current_min = int(np.floor(self.current_time/60))
            self.current_sec = self.current_time - self.current_min*60
            if self.current_sec < 10:
                self.timer_txt = font.render(f'{self.current_min}:0{self.current_sec}', False, (64,64,64))
            else:
                self.timer_txt = font.render(f'{self.current_min}:{self.current_sec}', False, (64,64,64))
            self.timer_txt_rect = self.timer_txt.get_rect(center = self.rect.center)
            screen.blit(self.timer_txt, self.timer_txt_rect)
            self.in_turn = True
            if self.current_time == 0:
                pieces.game_active = False
        else:
            if self.in_turn:
                self.total_time = self.current_time
                self.in_turn = False
            self.end_time = time_passed

class Graveyard():
    def __init__(self):
        graveyard_pos = []
        for i in range(8):
            for j in range(8):
                graveyard_pos.append(((j+1)*64 +640, (i+1)*64))
        self.positions = graveyard_pos
        self.counter = 0
        self.bone_list = []
    
    def die(self, piece: pygame.sprite.Sprite):
        piece.rect.topleft = self.positions[self.counter]
        piece.init_sqr = piece.rect.topleft
        self.add_to(piece)
        piece.on_board = False
        self.counter += 1
    
    def add_to(self, piece):
        self.bone_list.append(piece)


## defining the pieces

class Piece(pygame.sprite.Sprite):
    def __init__(self, colour: str, position: tuple, w_image_address: str, b_image_address: str):
        super(Piece, self).__init__()
        self.on_board = True
        self.has_moved = False
        self.position = position
        self.init_pos = position
        self.colour = colour
        self.gotten = False
        if self.colour == "white":
            self.image = pygame.image.load(w_image_address).convert_alpha()
        else:
            self.image = pygame.image.load(b_image_address).convert_alpha()
        
        self.rect = self.image.get_rect(topleft = self.position)
        self.init_sqr = self.rect.topleft
        self.passantable = False
    
    # allows the player to move the pieces
    def drag(self, mouse_pos, screen, other_pieces):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.allowable_squares(screen, other_pieces)
            pygame.draw.rect(screen, (255, 100, 100), (self.init_sqr[0],self.init_sqr[1], 64, 64), 3)
            self.rect.center = mouse_pos
            self.gotten = True
    
    # updates the sprite
    def update(self, got_piece, mouse_pos, squares, other_pieces, screen, grave_pos):
        self.p_update()
        if self.on_board and self.groups()[0].my_turn:
            if not got_piece or self.gotten:
                self.drag(mouse_pos, screen, other_pieces)
            self.drop(mouse_pos, other_pieces, screen, grave_pos)
            
        
    def drop(self, mouse_pos, other_pieces, screen, graveyard):
        if not pygame.mouse.get_pressed()[0] and self.gotten:
            self.rect.topleft = (math.floor(mouse_pos[0]/64)*64,math.floor(mouse_pos[1]/64)*64)
            for p in self.groups()[0].sprites(): # checking move prevention loop
                if p.type == 'king':
                    if self.type == 'king': # moving the king out of check
                        check_from_move = p.check_check(p.rect.topleft, other_pieces)
                        
                    elif square_occupation(self.rect.topleft, other_pieces): # taking checking piece
                        for piece in other_pieces.sprites():
                            if piece.rect.collidepoint(self.rect.topleft):
                                checking_candidates = other_pieces.sprites().copy()
                                checking_candidates.remove(piece)
                                check_from_move = p.check_check(p.init_sqr, checking_candidates, is_list = True)
                        
                    else: # blocking checking piece
                        check_from_move = p.check_check(p.init_sqr, other_pieces)
            if check_from_move:
                self.urine_check(screen)
            if not self.collision(screen) and not check_from_move:
                if self.type == 'king' and not self.has_moved:
                    if self.rect.topleft[0] - self.init_sqr[0]<64 and abs(self.rect.topleft[0] - self.init_sqr[0]) > 64:
                        for p in self.groups()[0].sprites():
                            if p.type == 'rook' and not p.has_moved and p.init_sqr[0] < self.init_sqr[0]:
                                p.rect.topleft = (self.rect.topleft[0]+64, self.init_sqr[1])
                    if self.rect.topleft[0] - self.init_sqr[0]>64 and abs(self.rect.topleft[0] - self.init_sqr[0]) > 64:
                        for p in self.groups()[0].sprites():
                            if p.type == 'rook' and not p.has_moved and p.init_sqr[0] > self.init_sqr[0]:
                                p.rect.topleft = (self.rect.topleft[0]-64, self.init_sqr[1])
                            p.init_sqr = p.rect.topleft
                            p.has_moved = True
                if self.type == 'pawn' and abs(self.rect.topleft[1] - self.init_sqr[1]) > 64: # for double move leading to en passant
                    self.passantable = True
                    for piece in self.groups()[0].sprites():
                        if piece != self:
                            piece.passantable = False
                else:
                    for pieces in self.groups()[0].sprites():
                        pieces.passantable = False
                if self.type == 'pawn' and abs(self.rect.topleft[0]-self.init_sqr[0]) == 64 and abs(self.rect.topleft[1]-self.init_sqr[1]) == 64: # en passant
                    if not square_occupation(self.rect.topleft, other_pieces):
                        if self.colour == 'white':
                            for p in other_pieces.sprites():
                                if p.rect.topleft == (self.rect.topleft[0], self.rect.topleft[1]+64):
                                    graveyard.die(p)
                        elif self.colour == 'black':
                            for p in other_pieces.sprites():
                                if p.rect.topleft == (self.rect.topleft[0], self.rect.topleft[1]-64):
                                    graveyard.die(p)
                self.take(other_pieces, graveyard)
                self.init_sqr = self.rect.topleft
                if self.type == 'pawn': # pawn promotion
                    if (self.rect.topleft[1] == 64 and self.colour == 'white') or (self.rect.topleft[1] == 512 and self.colour == 'black'):
                        self.promote(graveyard, screen)
                        self.groups()[0].my_turn = False
                    else:
                        self.groups()[0].my_turn = False
                        other_pieces.my_turn = True
                else:
                    self.groups()[0].my_turn = False
                    other_pieces.my_turn = True
                self.has_moved = True
                self.groups()[0].in_check = False
                print(self.passantable)
                for p in other_pieces.sprites():
                    if p.type == 'king':
                        if p.check_check(p.init_sqr, self.groups()[0]):
                            all_available_squares = []
                            for i in p.move_rules(p.init_sqr, self.groups()[0]):
                                if p.check_check(i, self.groups()[0]):
                                    all_available_squares.append(True)
                                else:
                                    all_available_squares.append(False)
                            if all(all_available_squares):
                                other_pieces.game_active = False
            else:
                self.rect.topleft = self.init_sqr
            
            self.gotten = False
            
    def collision(self, screen): # logic on this fixed by chatgpt lol thanks
        collisions = pygame.sprite.spritecollide(self, self.groups()[0], dokill=False) # assumes 0 th group is its own colour pieces
        collisions = [sprite for sprite in collisions if sprite != self]  
        if self.rect.topleft not in self.available_squares:
            return True
        if collisions:
            pygame.draw.rect(screen, (255, 100, 100), (self.init_sqr[0],self.init_sqr[1], 64, 64), 3)
            return True
        return False
    
    def take(self, other_pieces, graveyard):
        take_col = pygame.sprite.spritecollide(self, other_pieces, dokill=False)
        if take_col:
            graveyard.die(take_col[0])
            return True
        return False

    def allowable_squares(self, screen, other_pieces):
        self.available_squares = self.move_rules(self.init_sqr, other_pieces)
        av_sqr_sur =  pygame.Surface((64,64))
        av_sqr_sur.set_alpha(128)
        av_sqr_sur.fill((150,200,255))
        for sqr in self.available_squares:
            screen.blit(av_sqr_sur, sqr)
    
    def urine_check(self, screen):
        for p in self.groups()[0].sprites():
            if p.type == 'king':
                self.groups()[0].kg_sqr_sur =  pygame.Surface((64,64))
                self.groups()[0].kg_sqr_sur.set_alpha(128)
                self.groups()[0].kg_sqr_sur.fill((255,10,10))
                self.groups()[0].king_sqr = p.init_sqr
                # screen.blit(kg_sqr_sur, p.init_sqr)
                self.groups()[0].in_check = True
                
                
def in_check(group, screen):
    screen.blit(group.kg_sqr_sur, group.king_sqr)

def promotion_choice(group, screen, mouse_pos, graveyard, other_pieces):
    screen.blit(group.selection_surf, group.selection_pos)
    bishop_surf = pygame.image.load(piece_image_address(group.sprites()[0].colour, 'bishop')).convert_alpha()
    bishop_rect = bishop_surf.get_rect(topleft = group.selection_pos)
    knight_surf = pygame.image.load(piece_image_address(group.sprites()[0].colour, 'knight')).convert_alpha()
    knight_rect = knight_surf.get_rect(topleft = (group.selection_pos[0]+64, group.selection_pos[1]))
    rook_surf = pygame.image.load(piece_image_address(group.sprites()[0].colour, 'rook')).convert_alpha()
    rook_rect = rook_surf.get_rect(topleft = (group.selection_pos[0]+128, group.selection_pos[1]))
    queen_surf = pygame.image.load(piece_image_address(group.sprites()[0].colour, 'queen')).convert_alpha()
    queen_rect = queen_surf.get_rect(topleft = (group.selection_pos[0]+192, group.selection_pos[1]))
    screen.blit(bishop_surf, bishop_rect)
    screen.blit(knight_surf, knight_rect)
    screen.blit(rook_surf, rook_rect)
    screen.blit(queen_surf, queen_rect)
        
    selection_rect = group.selection_surf.get_rect(topleft = group.selection_pos)
    if selection_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        for p in group.sprites():
                if p.rect.topleft == group.prom_sqr:
                    graveyard.die(p)
        if bishop_rect.collidepoint(mouse_pos):
            group.add(queen(group.sprites()[0].colour, group.prom_sqr, 'project_work/sprites/no_backgrounds/queen_no_bg.png','project_work/sprites/no_backgrounds/b_queen_no_bg.png'))
        if knight_rect.collidepoint(mouse_pos):
            group.add(queen(group.sprites()[0].colour, group.prom_sqr, 'project_work/sprites/no_backgrounds/knight_no_bg.png','project_work/sprites/no_backgrounds/b_knight_no_bg.png'))
        if rook_rect.collidepoint(mouse_pos):
            group.add(queen(group.sprites()[0].colour, group.prom_sqr, 'project_work/sprites/no_backgrounds/rook_no_bg.png','project_work/sprites/no_backgrounds/b_rook_no_bg.png'))
        if queen_rect.collidepoint(mouse_pos):
            group.add(queen(group.sprites()[0].colour, group.prom_sqr, 'project_work/sprites/no_backgrounds/queen_no_bg.png','project_work/sprites/no_backgrounds/b_queen_no_bg.png'))
        
        group.my_turn = False
        other_pieces.my_turn = True
        group.choose = False
        
def piece_image_address(colour, type):
    base_str = 'project_work/sprites/no_backgrounds/'
    if colour == 'black':
        base_str += 'b_'
    base_str += str(type) + '_no_bg.png'
    return base_str

def board_setup(positions, w_pieces, b_pieces):
    for x in range(8):
        w_pieces.add(pawn("white", positions[x][6], 'project_work/sprites/no_backgrounds/pawn_no_bg.png','project_work/sprites/no_backgrounds/b_pawn_no_bg.png'))
        b_pieces.add(pawn("black", positions[x][1], 'project_work/sprites/no_backgrounds/pawn_no_bg.png','project_work/sprites/no_backgrounds/b_pawn_no_bg.png'))
    
    w_pieces.add(bishop("white", positions[2][7], 'project_work/sprites/no_backgrounds/bishop_no_bg.png','project_work/sprites/no_backgrounds/b_bishop_no_bg.png'))
    w_pieces.add(bishop("white", positions[5][7], 'project_work/sprites/no_backgrounds/bishop_no_bg.png','project_work/sprites/no_backgrounds/b_bishop_no_bg.png'))
    w_pieces.add(knight("white", positions[1][7], 'project_work/sprites/no_backgrounds/knight_no_bg.png','project_work/sprites/no_backgrounds/b_knight_no_bg.png'))
    w_pieces.add(knight("white", positions[6][7], 'project_work/sprites/no_backgrounds/knight_no_bg.png','project_work/sprites/no_backgrounds/b_knight_no_bg.png'))
    w_pieces.add(rook("white", positions[0][7], 'project_work/sprites/no_backgrounds/rook_no_bg.png','project_work/sprites/no_backgrounds/b_rook_no_bg.png'))
    w_pieces.add(rook("white", positions[7][7], 'project_work/sprites/no_backgrounds/rook_no_bg.png','project_work/sprites/no_backgrounds/b_rook_no_bg.png'))
    w_pieces.add(queen("white", positions[3][7], 'project_work/sprites/no_backgrounds/queen_no_bg.png','project_work/sprites/no_backgrounds/b_queen_no_bg.png'))
    w_pieces.add(king("white", positions[4][7], 'project_work/sprites/no_backgrounds/king_no_bg.png','project_work/sprites/no_backgrounds/b_king_no_bg.png'))
    
    b_pieces.add(bishop("black", positions[2][0], 'project_work/sprites/no_backgrounds/bishop_no_bg.png','project_work/sprites/no_backgrounds/b_bishop_no_bg.png'))
    b_pieces.add(bishop("black", positions[5][0], 'project_work/sprites/no_backgrounds/bishop_no_bg.png','project_work/sprites/no_backgrounds/b_bishop_no_bg.png'))
    b_pieces.add(knight("black", positions[1][0], 'project_work/sprites/no_backgrounds/knight_no_bg.png','project_work/sprites/no_backgrounds/b_knight_no_bg.png'))
    b_pieces.add(knight("black", positions[6][0], 'project_work/sprites/no_backgrounds/knight_no_bg.png','project_work/sprites/no_backgrounds/b_knight_no_bg.png'))
    b_pieces.add(rook("black", positions[0][0], 'project_work/sprites/no_backgrounds/rook_no_bg.png','project_work/sprites/no_backgrounds/b_rook_no_bg.png'))
    b_pieces.add(rook("black", positions[7][0], 'project_work/sprites/no_backgrounds/rook_no_bg.png','project_work/sprites/no_backgrounds/b_rook_no_bg.png'))
    b_pieces.add(queen("black", positions[3][0], 'project_work/sprites/no_backgrounds/queen_no_bg.png','project_work/sprites/no_backgrounds/b_queen_no_bg.png'))
    b_pieces.add(king("black", positions[4][0], 'project_work/sprites/no_backgrounds/king_no_bg.png','project_work/sprites/no_backgrounds/b_king_no_bg.png'))

def square_occupation(sqr, pieces, self = None):
        for piece in pieces:
            if piece != self:
                piece_here = piece.rect.collidepoint(sqr)
            if piece_here:
                return True
        return False
    
# defines each piece by type, for later rule implementation per class
class pawn(Piece):
    def __init__(self, colour: str, position: tuple, w_image_address: str, b_image_address: str):
        self.type = 'pawn'
        super(pawn, self).__init__(colour, position, w_image_address, b_image_address)
    
    def move_rules(self, sqr, other_pieces, chk_list = False): # piecewise update function with specific piece rules
        available_sqrs = []
        pieces_list = other_pieces.sprites() + self.groups()[0].sprites()
        if self.colour == 'white':
            if sqr[1]-64 >= 64 and sqr[1]-64 <= 512: # standard forward move with first double move
                if not square_occupation((sqr[0], sqr[1]-64), pieces_list, self):
                    available_sqrs.append((sqr[0], sqr[1]-64))
                    if sqr[1] == 448 and not square_occupation((sqr[0], sqr[1]-128), pieces_list, self):
                        available_sqrs.append((sqr[0], sqr[1]-128))
            if square_occupation((sqr[0]-64, sqr[1]-64), other_pieces.sprites()): # diagonal take
                available_sqrs.append((sqr[0]-64, sqr[1]-64))
            if square_occupation((sqr[0]+64, sqr[1]-64), other_pieces.sprites()): # diagonal take
                available_sqrs.append((sqr[0]+64, sqr[1]-64))
            for piece in other_pieces.sprites(): # en_passant
                if piece.type == 'pawn' and piece.passantable and piece.rect.topleft == (sqr[0]-64, sqr[1]):
                    available_sqrs.append((sqr[0]-64, sqr[1]-64))
                if piece.type == 'pawn' and piece.passantable and piece.rect.topleft == (sqr[0]+64, sqr[1]):
                    available_sqrs.append((sqr[0]+64, sqr[1]-64))
        elif self.colour == 'black':
            if sqr[1]+64 >= 64 and sqr[1]+64 <= 512:
                if not square_occupation((sqr[0], sqr[1]+64), pieces_list, self): # standard forward move with first double move
                    available_sqrs.append((sqr[0], sqr[1]+64))
                    if sqr[1] == 128 and not square_occupation((sqr[0], sqr[1]+128), pieces_list, self):
                        available_sqrs.append((sqr[0], sqr[1]+128))
            if square_occupation((sqr[0]+64, sqr[1]+64), other_pieces.sprites()): # diagonal take
                available_sqrs.append((sqr[0]+64, sqr[1]+64))
            if square_occupation((sqr[0]-64, sqr[1]+64), other_pieces.sprites()): # diagonal take
                available_sqrs.append((sqr[0]-64, sqr[1]+64))
            for piece in other_pieces.sprites(): # en passant
                if piece.type == 'pawn' and piece.passantable and piece.rect.topleft == (sqr[0]-64, sqr[1]):
                    available_sqrs.append((sqr[0]-64, sqr[1]+64))
                if piece.type == 'pawn' and piece.passantable and piece.rect.topleft == (sqr[0]+64, sqr[1]):
                    available_sqrs.append((sqr[0]+64, sqr[1]+64))
        return available_sqrs
    
    def p_update(self): # piecewise update function
        pass
    
    def promote(self, graveyard, screen):
        self.groups()[0].prom_sqr = self.init_sqr
        self.groups()[0].selection_surf = pygame.Surface((256, 64))
        if self.colour == 'white':
            self.groups()[0].selection_surf.fill((255,255,255))
        elif self.colour == 'black':
            self.groups()[0].selection_surf.fill((0,0,0))
        if self.groups()[0].prom_sqr[1] > 320:
            self.groups()[0].selection_pos = (self.groups()[0].prom_sqr[0], self.groups()[0].prom_sqr[1]+64)
        else:
            self.groups()[0].selection_pos = (self.groups()[0].prom_sqr[0], self.groups()[0].prom_sqr[1]-64)
        self.groups()[0].choose = True
    
        
class bishop(Piece):
    def __init__(self, colour: str, position: tuple, w_image_address: str, b_image_address: str):
        self.type = 'bishop'
        super(bishop, self).__init__(colour, position, w_image_address, b_image_address)

    def move_rules(self, sqr, other_pieces, chk_list = False): # piecewise update function with specific piece rules
        if chk_list:
            other_pieces_list = other_pieces
        else:
            other_pieces_list = other_pieces.sprites()
        same_pieces_list = self.groups()[0].sprites()
        available_sqrs = []
        y1, y2, y3, y4 = True, True, True, True
        for j in range(0,9):
            if j:
                if (sqr[0]+64*j <= 512 and sqr[0]+64*j >= 64) and (sqr[1]+64*j <= 512 and sqr[1]+64*j >= 64) and y1: 
                    if square_occupation((sqr[0]+64*j, sqr[1]+64*j), same_pieces_list, self) and not chk_list:
                        y1 = False
                    elif square_occupation((sqr[0]+64*j, sqr[1]+64*j), other_pieces_list):
                        available_sqrs.append((sqr[0]+64*j, sqr[1]+64*j))
                        y1 = False
                    else: 
                        available_sqrs.append((sqr[0]+64*j, sqr[1]+64*j))
                if (sqr[0]+64*j <= 512 and sqr[0]+64*j >= 64) and (sqr[1]-64*j <= 512 and sqr[1]-64*j >= 64) and y2:
                    if square_occupation((sqr[0]+64*j, sqr[1]-64*j), same_pieces_list, self) and not chk_list:
                        y2 = False
                    elif square_occupation((sqr[0]+64*j, sqr[1]-64*j), other_pieces_list):
                        available_sqrs.append((sqr[0]+64*j, sqr[1]-64*j))
                        y2 = False
                    else: 
                        available_sqrs.append((sqr[0]+64*j, sqr[1]-64*j))
                if (sqr[0]-64*j <= 512 and sqr[0]-64*j >= 64) and (sqr[1]-64*j <= 512 and sqr[1]-64*j >= 64) and y3:
                    if square_occupation((sqr[0]-64*j, sqr[1]-64*j), same_pieces_list, self) and not chk_list:
                        y3 = False
                    elif square_occupation((sqr[0]-64*j, sqr[1]-64*j), other_pieces_list):
                        available_sqrs.append((sqr[0]-64*j, sqr[1]-64*j))
                        y3 = False
                    else:
                        available_sqrs.append((sqr[0]-64*j, sqr[1]-64*j))
                if (sqr[0]-64*j <= 512 and sqr[0]-64*j >= 64) and (sqr[1]+64*j <= 512 and sqr[1]+64*j >= 64) and y4:
                    if square_occupation((sqr[0]-64*j, sqr[1]+64*j), same_pieces_list, self) and not chk_list:
                        y4 = False
                    elif square_occupation((sqr[0]-64*j, sqr[1]+64*j), other_pieces_list):
                        available_sqrs.append((sqr[0]-64*j, sqr[1]+64*j))
                        y4 = False
                    else: 
                        available_sqrs.append((sqr[0]-64*j, sqr[1]+64*j))
                
        return available_sqrs
    
    def p_update(self): # piecewise update function
        pass

class knight(Piece):
    def __init__(self, colour: str, position: tuple, w_image_address: str, b_image_address: str):
        self.type = 'knight'
        super(knight, self).__init__(colour, position, w_image_address, b_image_address)
        
    def move_rules(self, sqr, other_pieces, chk_list = False): # piecewise update function with specific piece rules
        available_sqrs = []
        for i in range(-1,2):
            for j in range(-1,2):
                if i and j:
                    if (sqr[0]+j*128 >= 64 and sqr[0]+j*128 <= 512) and (sqr[1]+i*64 >= 64 and sqr[1]+i*64 <= 512) and not square_occupation((sqr[0]+j*128, sqr[1]+i*64), self.groups()[0].sprites(), self):
                        available_sqrs.append((sqr[0]+j*128, sqr[1]+i*64))
                    if (sqr[0]+j*64 >= 64 and sqr[0]+j*64 <= 512) and (sqr[1]+i*128 >= 64 and sqr[1]+i*128 <= 512) and not square_occupation((sqr[0]+j*64, sqr[1]+i*128), self.groups()[0].sprites(), self):
                        available_sqrs.append((sqr[0]+j*64, sqr[1]+i*128))
        return available_sqrs
    
    def p_update(self): # piecewise update function
        pass

class rook(Piece):
    def __init__(self, colour: str, position: tuple, w_image_address: str, b_image_address: str):
        self.type = 'rook'
        super(rook, self).__init__(colour, position, w_image_address, b_image_address)

    def move_rules(self, sqr, other_pieces, chk_list = False): # piecewise update function with specific piece rules
        if chk_list:
            other_pieces_list = other_pieces
        else:
            other_pieces_list = other_pieces.sprites()
        same_pieces_list = self.groups()[0].sprites()
        available_sqrs = []
        y1, y2, y3, y4 = True, True, True, True
        for j in range(0,9):
            if j:
                if sqr[0]+64*j <= 512 and sqr[0]+64*j >= 64 and y1:
                    if square_occupation((sqr[0]+64*j, sqr[1]), same_pieces_list, self) and not chk_list:
                        y1=False
                    elif square_occupation((sqr[0]+64*j, sqr[1]), other_pieces_list):
                        available_sqrs.append((sqr[0]+64*j, sqr[1]))
                        y1=False
                    else:
                        available_sqrs.append((sqr[0]+64*j, sqr[1]))
                if sqr[1]+64*j <= 512 and sqr[1]+64*j >= 64 and y2:
                    if square_occupation((sqr[0], sqr[1]+64*j), same_pieces_list, self) and not chk_list:
                        y2=False
                    elif square_occupation((sqr[0], sqr[1]+64*j), other_pieces_list):
                        available_sqrs.append((sqr[0], sqr[1]+64*j))
                        y2=False
                    else:
                        available_sqrs.append((sqr[0], sqr[1]+64*j))
                if sqr[0]-64*j <= 512 and sqr[0]-64*j >= 64 and y3:
                    if square_occupation((sqr[0]-64*j, sqr[1]), same_pieces_list, self) and not chk_list:
                        y3=False
                    elif square_occupation((sqr[0]-64*j, sqr[1]), other_pieces_list):
                        available_sqrs.append((sqr[0]-64*j, sqr[1]))
                        y3=False
                    else:
                        available_sqrs.append((sqr[0]-64*j, sqr[1]))
                if sqr[1]-64*j <= 512 and sqr[1]-64*j >= 64 and y4:
                    if square_occupation((sqr[0], sqr[1]-64*j), same_pieces_list, self) and not chk_list:
                        y4=False
                    elif square_occupation((sqr[0], sqr[1]-64*j), other_pieces_list):
                        available_sqrs.append((sqr[0], sqr[1]-64*j))
                        y4=False
                    else:    
                        available_sqrs.append((sqr[0], sqr[1]-64*j))
        return available_sqrs
    
    def p_update(self): # piecewise update function
        pass
    
class queen(Piece):
    def __init__(self, colour: str, position: tuple, w_image_address: str, b_image_address: str):
        self.type = 'queen'
        super(queen, self).__init__(colour, position, w_image_address, b_image_address)
        
    def move_rules(self, sqr, other_pieces, chk_list = False): # piecewise update function with specific piece rules
        if chk_list:
            other_pieces_list = other_pieces
        else:
            other_pieces_list = other_pieces.sprites()
        same_pieces_list = self.groups()[0].sprites()
        available_sqrs = []
        y1, y2, y3, y4, y5, y6, y7, y8 = True, True, True, True, True, True, True, True
        for j in range(0,9):
            if j:
                if sqr[0]+64*j <= 512 and sqr[0]+64*j >= 64 and y1:
                    if square_occupation((sqr[0]+64*j, sqr[1]), same_pieces_list, self) and not chk_list:
                        y1=False
                    elif square_occupation((sqr[0]+64*j, sqr[1]), other_pieces_list):
                        available_sqrs.append((sqr[0]+64*j, sqr[1]))
                        y1=False
                    else:
                        available_sqrs.append((sqr[0]+64*j, sqr[1]))
                if sqr[1]+64*j <= 512 and sqr[1]+64*j >= 64 and y2:
                    if square_occupation((sqr[0], sqr[1]+64*j), same_pieces_list, self) and not chk_list:
                        y2=False
                    elif square_occupation((sqr[0], sqr[1]+64*j), other_pieces_list):
                        available_sqrs.append((sqr[0], sqr[1]+64*j))
                        y2=False
                    else:
                        available_sqrs.append((sqr[0], sqr[1]+64*j))
                if sqr[0]-64*j <= 512 and sqr[0]-64*j >= 64 and y3:
                    if square_occupation((sqr[0]-64*j, sqr[1]), same_pieces_list, self) and not chk_list:
                        y3=False
                    elif square_occupation((sqr[0]-64*j, sqr[1]), other_pieces_list):
                        available_sqrs.append((sqr[0]-64*j, sqr[1]))
                        y3=False
                    else:
                        available_sqrs.append((sqr[0]-64*j, sqr[1]))
                if sqr[1]-64*j <= 512 and sqr[1]-64*j >= 64 and y4:
                    if square_occupation((sqr[0], sqr[1]-64*j), same_pieces_list, self) and not chk_list:
                        y4=False
                    elif square_occupation((sqr[0], sqr[1]-64*j), other_pieces_list):
                        available_sqrs.append((sqr[0], sqr[1]-64*j))
                        y4=False
                    else:    
                        available_sqrs.append((sqr[0], sqr[1]-64*j))  
                    
                    
                if (sqr[0]+64*j <= 512 and sqr[0]+64*j >= 64) and (sqr[1]+64*j <= 512 and sqr[1]+64*j >= 64) and y5: 
                    if square_occupation((sqr[0]+64*j, sqr[1]+64*j), same_pieces_list, self) and not chk_list:
                        y5 = False
                    elif square_occupation((sqr[0]+64*j, sqr[1]+64*j), other_pieces_list):
                        available_sqrs.append((sqr[0]+64*j, sqr[1]+64*j))
                        y5 = False
                    else: 
                        available_sqrs.append((sqr[0]+64*j, sqr[1]+64*j))
                if (sqr[0]+64*j <= 512 and sqr[0]+64*j >= 64) and (sqr[1]-64*j <= 512 and sqr[1]-64*j >= 64) and y6:
                    if square_occupation((sqr[0]+64*j, sqr[1]-64*j), same_pieces_list, self) and not chk_list:
                        y6 = False
                    elif square_occupation((sqr[0]+64*j, sqr[1]-64*j), other_pieces_list):
                        available_sqrs.append((sqr[0]+64*j, sqr[1]-64*j))
                        y6 = False
                    else: 
                        available_sqrs.append((sqr[0]+64*j, sqr[1]-64*j))
                if (sqr[0]-64*j <= 512 and sqr[0]-64*j >= 64) and (sqr[1]-64*j <= 512 and sqr[1]-64*j >= 64) and y7:
                    if square_occupation((sqr[0]-64*j, sqr[1]-64*j), same_pieces_list, self) and not chk_list:
                        y7 = False
                    elif square_occupation((sqr[0]-64*j, sqr[1]-64*j), other_pieces_list):
                        available_sqrs.append((sqr[0]-64*j, sqr[1]-64*j))
                        y7 = False
                    else:
                        available_sqrs.append((sqr[0]-64*j, sqr[1]-64*j))
                if (sqr[0]-64*j <= 512 and sqr[0]-64*j >= 64) and (sqr[1]+64*j <= 512 and sqr[1]+64*j >= 64) and y8:
                    if square_occupation((sqr[0]-64*j, sqr[1]+64*j), same_pieces_list, self) and not chk_list:
                        y8 = False
                    elif square_occupation((sqr[0]-64*j, sqr[1]+64*j), other_pieces_list):
                        available_sqrs.append((sqr[0]-64*j, sqr[1]+64*j))
                        y8 = False
                    else: 
                        available_sqrs.append((sqr[0]-64*j, sqr[1]+64*j))
        return available_sqrs

    def p_update(self): # piecewise update function
        pass

class king(Piece):
    def __init__(self, colour: str, position: tuple, w_image_address: str, b_image_address: str):
        self.type = 'king'
        super(king, self).__init__(colour, position, w_image_address, b_image_address)

    def move_rules(self, sqr, other_pieces, chk_list = False): # specific piece rules
        available_sqrs = []
        for i in range(-1,2):
            for j in range(-1,2):
                if not i and not j:
                    pass
                elif (sqr[0]+j*64 >= 64 and sqr[0]+j*64 <= 512) and (sqr[1]+i*64 >= 64 and sqr[1]+i*64 <= 512):
                    if not square_occupation((sqr[0]+j*64, sqr[1]+i*64), self.groups()[0].sprites(), self):
                        if not self.check_check((sqr[0]+j*64, sqr[1]+i*64), other_pieces):
                            available_sqrs.append((sqr[0]+j*64, sqr[1]+i*64))
        for p in self.groups()[0].sprites(): # castling
            if p.type == 'rook' and not p.has_moved and not self.has_moved:
                if p.init_sqr[0] < self.init_sqr[0]:
                    if not square_occupation((self.init_sqr[0]-64, self.init_sqr[1]), self.groups()[0].sprites(), self) and not square_occupation((self.init_sqr[0]-64, self.init_sqr[1]), other_pieces):
                        if not square_occupation((self.init_sqr[0]-128, self.init_sqr[1]), self.groups()[0].sprites(), self) and not square_occupation((self.init_sqr[0]-128, self.init_sqr[1]), other_pieces):
                            if not square_occupation((self.init_sqr[0]-192, self.init_sqr[1]), self.groups()[0].sprites(), self) and not square_occupation((self.init_sqr[0]-192, self.init_sqr[1]), other_pieces):
                                if not self.check_check((self.init_sqr[0]-64, self.init_sqr[1]), other_pieces) and not self.check_check((self.init_sqr[0]-128, self.init_sqr[1]), other_pieces) and not self.check_check((self.init_sqr[0]-192, self.init_sqr[1]), other_pieces):
                                    available_sqrs.append((self.init_sqr[0]-128, self.init_sqr[1]))
                if p.init_sqr[0] > self.init_sqr[0]:
                    if not square_occupation((self.init_sqr[0]+64, self.init_sqr[1]), self.groups()[0].sprites(), self) and not square_occupation((self.init_sqr[0]+64, self.init_sqr[1]), other_pieces):
                        if not square_occupation((self.init_sqr[0]+128, self.init_sqr[1]), self.groups()[0].sprites(), self) and not square_occupation((self.init_sqr[0]+128, self.init_sqr[1]), other_pieces):
                            if not self.check_check((self.init_sqr[0]+64, self.init_sqr[1]), other_pieces) and not self.check_check((self.init_sqr[0]+128, self.init_sqr[1]), other_pieces):
                                available_sqrs.append((self.init_sqr[0]+128, self.init_sqr[1]))
        return available_sqrs
    
    def p_update(self): # piecewise update function
        if self.on_board == False:
            self.groups()[0].game_active = False
    
    def check_check(self, sqr, other_pieces, is_list =  False):
        if is_list:
            checking_candidates = other_pieces
            all_pieces = other_pieces + self.groups()[0].sprites()
        else:
            checking_candidates = other_pieces.sprites()
            all_pieces = other_pieces.sprites() + self.groups()[0].sprites()
        for i in checking_candidates: # stops you from checking yourself in your own turn
            if i.type == 'king': 
                for m in range(-1,2):
                    for n in range(-1,2):
                        if m and n:
                            if (i.rect.topleft[0]+m*64, i.rect.topleft[1]+n*64) == sqr:
                                return True
                i.rect.topleft
            elif i.type == 'pawn' and i.colour == 'black':
                if (i.rect.topleft[0]+64, i.rect.topleft[1]+64) == sqr or (i.rect.topleft[0]-64, i.rect.topleft[1]+64) == sqr:
                    return True
            elif i.type == 'pawn' and i.colour == 'white':
                if (i.rect.topleft[0]+64, i.rect.topleft[1]-64) == sqr or (i.rect.topleft[0]-64, i.rect.topleft[1]-64) == sqr:
                    return True
            elif sqr in i.move_rules(i.init_sqr, all_pieces, True):
                return True
                
                

            
## main code loop 

def main(time_between_games = 0):
    pygame.init()
    # sets up screen and moving time
    screen = pygame.display.set_mode((1280, 640))
    clock = pygame.time.Clock()
    pygame.display.set_caption("The Board") 
    chess_font = pygame.font.Font(None, 64)
    chess_font_sml = pygame.font.Font(None, 32)
    
    # defines the board
    board = Board()
    graveyard = Graveyard()
    squares = pygame.sprite.Group()
    for x in range(8):
        for y in range(8):
            colour = "black" if (x + y) % 2 else "white"
            squares.add(Square(colour, board.positions[x][y]))

    # places pieces initially
    w_pieces = pygame.sprite.Group()
    b_pieces = pygame.sprite.Group()
    board_setup(board.positions, w_pieces, b_pieces)
    w_pieces.my_turn = True
    b_pieces.my_turn = False
    
    b_timer_pos = (64,32)
    w_timer_pos = (576,608)
    
    # initialises used params in loop
    got_piece = False
    exit = False
    w_pieces.game_active = True
    b_pieces.game_active = True
    w_pieces.in_check = False
    b_pieces.in_check = False
    w_pieces.choose = False
    b_pieces.choose = False
    w_timer = Timer(w_timer_pos, w_pieces, time_between_games)
    b_timer = Timer(b_timer_pos, b_pieces, time_between_games)
    W_Timers = pygame.sprite.Group()
    B_Timers = pygame.sprite.Group()
    W_Timers.add(w_timer)
    B_Timers.add(b_timer)
    ## running the game
    while not exit: 
        mouse_pos = pygame.mouse.get_pos()
        time_passed = int(round(pygame.time.get_ticks()/1000))
        if w_pieces.game_active and b_pieces.game_active:
            
            # draw all elements
            screen.fill((50,100,50))
            squares.draw(screen)
            w_pieces.draw(screen)
            b_pieces.draw(screen)
            B_Timers.draw(screen)
            W_Timers.draw(screen)
            
            
            
            pygame.draw.rect(screen, (255, 100, 100), (math.floor(mouse_pos[0]/64)*64,math.floor(mouse_pos[1]/64)*64, 64, 64), 3)
            squares.update(mouse_pos)
            w_pieces.update(got_piece, mouse_pos, squares, b_pieces, screen, graveyard)
            b_pieces.update(got_piece, mouse_pos, squares, w_pieces, screen, graveyard)
            if w_pieces.choose:
                promotion_choice(w_pieces, screen, mouse_pos, graveyard, b_pieces)
            if b_pieces.choose:
                promotion_choice(b_pieces, screen, mouse_pos, graveyard, w_pieces)
            if w_pieces.in_check:
                in_check(w_pieces, screen)
            if b_pieces.in_check:
                in_check(b_pieces, screen)
            W_Timers.update(chess_font_sml, w_pieces, screen, time_passed)
            B_Timers.update(chess_font_sml, b_pieces, screen, time_passed)
            got_piece = pygame.mouse.get_pressed()[0]
        else:
            screen.fill((50,100,50))
            board.chk_mate_screen(screen, w_pieces, b_pieces, chess_font, chess_font_sml)
            if board.restart_game(mouse_pos):
                return True
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                return False
                
        pygame.display.update() 
        clock.tick(60)

## running main code loop
if __name__ == "__main__":
    restart = main()
    while restart:
        restart = main(time_between_games=int(round(pygame.time.get_ticks()/1000)))
    
    
