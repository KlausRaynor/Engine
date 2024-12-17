import pygame

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


def draw_button(screen: pygame.Surface, pos_x: int, pos_y: int, 
                button_width: int, button_height: int,color: tuple[int, int, int],
                border_radii: int, text: str, font: pygame.font.Font, text_color: tuple[int, int, int]) -> pygame.Rect:
    """
    Draws a button on the screen.

    Args: 
        screen (pygame.Surface): Surface to draw on.
        rect (pygame.Rect): Rectangle of the button.
        color (tuple[int, int, int]): Color of the button.
        text (str): Text to display on the button.
    """
    buttonrect = pygame.Rect(pos_x, pos_y, button_width, button_height)
    pygame.draw.rect(screen, color, buttonrect, border_radius=border_radii)
    render_text(screen, font, text, text_color, (pos_x + button_width // 2, pos_y + button_height // 2))

    
    return buttonrect

def draw_hand(screen: pygame.Surface, hand: list[dict], border_radii: int) -> None:
    """
    Draws the hand of cards on the screen.

    Args: 
        screen (pygame.Surface): Surface to draw on.
        cards: list[pygame.Rect]: list of card rectangles
        colors: list[tuple[int, int, int]]: list of card colors
    """
    for card in hand:
        pygame.draw.rect(screen, card["color"], card["rect"], border_radius=border_radii)