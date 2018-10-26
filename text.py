"""This module provides useful methods to print to surface various types of data
"""

from pygame_helpers.util import separate_in_lines
from pygame_helpers.draw import blit_centered
from math import floor, ceil
import pygame

if pygame.font.get_init(): pygame.font.init() #Ensure init

#TODO add this method but works with multiple lines
def print_bounded(surface, text, rect, color=(0, 0, 0), font_name=None):
    """Prints the text in such manner it does not exit the rect passed in
    
    This takes the maximum height possible, will reduce height
    when text has too much width and will create a new line when
    the text has less than half the rect's height.
    Text will be centered.
    Does not accept newline characters

    Input:
        surface   - a pygame surface in which to draw
        text      - the text to be printed
        rect      - the bounds of the text
        color     - the color of the text (optional)
        font_name - the name of the font (optional)
    Output: None
    """
    if not text: return
    #With a little bit of luck I will modify all this fucking shit so Imma let this here totally uncommented, im sorry little guy from the future
    lines = [text]
    test_char_width, test_char_height = pygame.font.SysFont(font_name, 10).size("0")
    rate = test_char_height / test_char_width   

    #Calculate char height
    char_height = 0
    while True:
        proposed_height = min(
                    rect.height / len(lines),
                    rate * rect.width / (len(text) / len(lines))
                ) #chose the largest viable height

        next_proposed_height = min(
                    rect.height / (len(lines) + 1), 
                    rate * rect.width / (len(text) / (len(lines) + 1))
                ) #chose the largest viable height with one more line

        if proposed_height < next_proposed_height: #In next is bigger then chose that
            n_char_per_line = int(len(text) / (len(lines) + 1))
            lines = separate_in_lines(text, n_char_per_line)
        else:
            char_height = int(proposed_height)
            break

    #Print in surface
    for i, line in enumerate(lines):
        rendered = pygame.font.SysFont(font_name, char_height).render(line, 0, color)
        blit_centered(surface, rendered, (rect.width/2, rect.y + char_height * (i + 1/2)))
        
