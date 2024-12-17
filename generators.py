import pygame
import numpy as np

def generate_hand(pos_x: int, pos_y: int, hand_size: int, spacing: int, 
                  card_width: int, card_height: int)-> list[tuple[pygame.Rect, tuple[int, int, int]]]: 
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
    hand = []
    for i in range(hand_size):
        rect = pygame.Rect(pos_x + i * (card_width + spacing), pos_y, card_width, card_height)
        color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        hand.append((rect, color))
    return hand