# pylint: disable=E1101

import pygame
import numpy as np

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

SCREEN_WIDTH = (CARD_WIDTH * HAND_SIZE) + (CARD_SPACING * HAND_SIZE) + 100
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

def generate_hand(pos_x: int, pos_y: int, hand_size: int, spacing: int)-> list[pygame.Rect]: 
    """
    Generate hand of card rectangles positioned horizontally
    Args: 
        pos_x (int): x position of first card
        pos_y (int): y position of first card
        hand_size (int): number of cards in hand
        spacing (int): horizontal space between cards
    Returns: 
        list[pygame.rect]: list of card rectangles
    """
    return [pygame.Rect(pos_x + i * (CARD_WIDTH + spacing), pos_y, CARD_WIDTH, CARD_HEIGHT) for i in range(hand_size)]

def draw_button(pos_x: int, pos_y: int, color: tuple[int, int, int], text: str) -> pygame.Rect:
    """
    Draws a button on the screen.

    Args: 
        screen (pygame.Surface): Surface to draw on.
        rect (pygame.Rect): Rectangle of the button.
        color (tuple[int, int, int]): Color of the button.
        text (str): Text to display on the button.
    """
    buttonrect = pygame.Rect(pos_x, pos_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, color, buttonrect, border_radius=BORDER_RADII)
    render_text(screen, font, text, BLACK, (pos_x + BUTTON_WIDTH // 2, pos_y + BUTTON_HEIGHT // 2))

    
    return buttonrect

def draw_hand(screen: pygame.Surface, cards: list[pygame.Rect], colors: list[tuple[int, int, int]]) -> None:
    """
    Draws the hand of cards on the screen.

    Args: 
        screen (pygame.Surface): Surface to draw on.
        cards: list[pygame.Rect]: list of card rectangles
        colors: list[tuple[int, int, int]]: list of card colors
    """
    for rect, color in zip(cards, card_colors):
        pygame.draw.rect(screen, color, rect, border_radius=BORDER_RADII)

def render_text(screen: pygame.Surface, font: pygame.font.Font, text: str, color: tuple[int, int, int], pos: tuple[int, int]) -> None:
    """
    Renders text on the screen at the specified position.
    
    Args: 
        screen (pygame.Surface): Surface to draw on.
        font (pygame.font.Font): Font to use.
        text (str): Text to render.
        color (tuple[int, int, int]): Color of the text.
        pos (tuple[int, int]): Position of the text.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)

# Generate initial hand
CURRENT_HAND = generate_hand(100, 300, HAND_SIZE, CARD_SPACING)
RESET_BUTTON = draw_button(SCREEN_WIDTH // 2, 100, BUTTON_COLOR, "Reset Hand")
SELECTED_CARD = None
CARD_CLICKED = False
RUNNING = True

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
                if CURRENT_HAND[i].collidepoint(event.pos):
                    SELECTED_CARD = CURRENT_HAND[i]
                    CARD_CLICKED = True

                    # calculate offset between mouse pos and top left corner of card
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_offset_x =mouse_x - SELECTED_CARD.topleft[0]
                    mouse_offset_y = mouse_y - SELECTED_CARD.topleft[1]

                    card_rect = CURRENT_HAND.pop(i)
                    card_color = card_colors.pop(i)
                    CURRENT_HAND.append(card_rect)
                    card_colors.append(card_color)
                    break

            if RESET_BUTTON.collidepoint(event.pos):
                CURRENT_HAND = generate_hand(100, 300, HAND_SIZE, CARD_SPACING)
                # card_colors = [(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)) for _ in range(HAND_SIZE)]
        elif event.type == pygame.MOUSEBUTTONUP:
            CARD_CLICKED = False

# UPDATE CARD POS
    if CARD_CLICKED and SELECTED_CARD:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        SELECTED_CARD.topleft = (mouse_x - mouse_offset_x, mouse_y - mouse_offset_y)

# DRAWING 

    screen.fill(WHITE)
    
    # draw cards except for the selected card. 
    draw_hand(screen, CURRENT_HAND, card_colors)

    RESET_BUTTON = draw_button(SCREEN_WIDTH // 2, 100, BUTTON_COLOR, "Reset Hand")
    
    render_text(screen, font, "Click and Drag the cards!", (0, 0, 0), (SCREEN_WIDTH // 2, 50))
    pygame.display.flip()
    clock.tick(TICKRATE)
pygame.quit()
