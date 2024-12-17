# pylint: disable=E1101

import pygame
import numpy as np
from graphics import render_text, draw_button, draw_hand
from generators import generate_hand
from utils import check_collision

pygame.init()

CARD_WIDTH = 200
CARD_HEIGHT = int(CARD_WIDTH * 1.4)
CARD_SPACING = 25
HAND_SIZE = 5
BORDER_RADII = 15
SPEED = [2, 2]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
TICKRATE = 60

SCREEN_WIDTH = (CARD_WIDTH * HAND_SIZE) + (CARD_SPACING * HAND_SIZE) + CARD_SPACING
SCREEN_HEIGHT = 1000
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (0, 255, 0)
BUTTON_HIGHLIGHT_COLOR = (0, 200, 0)


# Initialize Screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Physics Playground")
font = pygame.font.Font(None, 30)

# card setup
card_colors = [(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)) for _ in range(HAND_SIZE)]

# Generate initial hand
STARTING_HAND = generate_hand(CARD_SPACING, 300, HAND_SIZE, CARD_SPACING, CARD_WIDTH, CARD_HEIGHT)
CURRENT_HAND = [
    {"rect": pygame.Rect(*rect_data), "color": color, "velocity": [0,0]}
    for rect_data, color in STARTING_HAND
]

RESET_BUTTON = draw_button(screen, SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BORDER_RADII, "Reset Hand", font, BLACK)
SELECTED_CARD = None
CARD_CLICKED = False
mouse_offset_x, mouse_offset_y = 0, 0
RUNNING = True

check_collision()

GRAVITY = 0.5
GROUND_HEIGHT = SCREEN_HEIGHT

# frame rate
clock = pygame.time.Clock()

#                #
# MAIN GAME LOOP #
#                #
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    # MOUSE BUTTON DOWN
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(CURRENT_HAND) - 1, -1, -1):
                card = CURRENT_HAND[i]
                rect = card["rect"]
                color = card["color"]

                if rect.collidepoint(event.pos):
                    SELECTED_CARD = card
                    CARD_CLICKED = True

                    # calculate offset between mouse pos and top left corner of card
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_offset_x = mouse_x - rect.topleft[0]
                    mouse_offset_y = mouse_y - rect.topleft[1]

                    CURRENT_HAND.append(CURRENT_HAND.pop(i))
                    break

            if RESET_BUTTON.collidepoint(event.pos):
                CURRENT_HAND = [
                    {"rect": pygame.Rect(*rect_data), "color": color, "velocity": [0, 0]}
                    for rect_data, color in STARTING_HAND
                ]
        elif event.type == pygame.MOUSEBUTTONUP:
            CARD_CLICKED = False
            SELECTED_CARD = None
    
    # UPDATE FOR PHYSICS
    for card in CURRENT_HAND:
        if not CARD_CLICKED or SELECTED_CARD != card:
            card["velocity"][1] += GRAVITY
            card["rect"].y += card["velocity"][1]

            # STOP CARD WHEN GROUND IS HIT
            if card["rect"].y + card["rect"].height >= GROUND_HEIGHT:
                card["rect"].y = GROUND_HEIGHT - card["rect"].height
                card["velocity"][1] = 0

# UPDATE CARD POS
    if CARD_CLICKED and SELECTED_CARD:
        
        if "rect" in SELECTED_CARD: 
            mouse_x, mouse_y = pygame.mouse.get_pos()
            SELECTED_CARD["rect"].topleft = (mouse_x - mouse_offset_x, mouse_y - mouse_offset_y)
        SELECTED_CARD["velocity"] = [0, 0]

# DRAWING 
    screen.fill(WHITE)
    
    # draw cards except for the selected card. 
    draw_hand(screen, CURRENT_HAND, BORDER_RADII)

    RESET_BUTTON = draw_button(screen, SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BORDER_RADII, "Reset Hand", font, BLACK)
    
    render_text(screen, font, "Click and Drag the cards!", (0, 0, 0), (SCREEN_WIDTH // 2, 50))
    pygame.display.flip()
    clock.tick(TICKRATE)
pygame.quit()
