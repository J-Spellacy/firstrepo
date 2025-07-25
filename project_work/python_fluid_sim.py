import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pygame
import math


def derivative(y, x): # scalar derivative: Scalar -> Scalar
    pass

def partial_derivative(y, x): # partial derivative: Vector -> Scalar
    pass    

def gradient(Y, x): # Gradient of a vector field: Vector -> Scalar
    pass

def Curl(Y, x): # Curl of a vector field: Vector -> Vector
    pass

def Divergence(Y, x): # Divergence of a vector field: Vector -> scalar
    pass

def Laplacian(Y, X): # Laplacian of a vector field: Vector -> Vector
    pass


# time stepping function for each position in the field
def time_step(pos, t):
    pass

# Draws each arrow from fixed position to end which is itself a vector determined in the main loop.
'''
This function needs changing to work with appropriate vector inputs.
'''
def draw_arrow(surface, start, end, color=(255, 0, 0), width=1):
    pygame.draw.line(surface, color, start, end, width)
    
    # end position is input as a vector
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)

    # arrowhead shape parameters
    length = 10  
    arrow_angle = math.radians(30)

    left = (end[0] - length * math.cos(angle - arrow_angle),
            end[1] - length * math.sin(angle - arrow_angle))
    right = (end[0] - length * math.cos(angle + arrow_angle),
             end[1] - length * math.sin(angle + arrow_angle))

    pygame.draw.polygon(surface, color, [end, left, right])



'''
Main loop needs to be adapted to work on the vector field, by adapting the vector per position.
Apply the appropriate equations to a finite difference or shape method to compute the vector field at each position.
'''
def main():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    
    pygame.display.set_caption("Vector Field Visualization")
    
    # Define fixed arrow positions and defines the number of vectors per x row and y column and their spacing
    n_vectors = 30
    vector_spacing_x, vector_spacing_y = screen_width // n_vectors, screen_height // n_vectors
    arrow_positions = [(i, j) for i in range(0, screen_width+vector_spacing_x, vector_spacing_x) for j in range(0, screen_height+vector_spacing_y, vector_spacing_y)]
    
    # main loop of pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        # following the mouse (demo)
        for pos in arrow_positions:
            dx = mouse_pos[0] - pos[0]
            dy = mouse_pos[1] - pos[1]
            distance = math.hypot(dx, dy)

            # Scale arrow length
            scale = min(distance ** 2, 50) # second number is the maximum length of the arrow
            angle = math.atan2(dy, dx)

            # Final vector positions
            end_x = pos[0] + scale * math.cos(angle)
            end_y = pos[1] + scale * math.sin(angle)
            draw_arrow(screen, pos, (end_x, end_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
    
