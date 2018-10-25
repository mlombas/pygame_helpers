"""This module provides useful methods to print to surface various types of data
"""

from util import separate_in_lines
from draw import blit_centered
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
    #Calculate char height
    lines = [text]
    ch_height = rect.height
    while any(pygame.font.SysFont(font_name, ch_height).size(line)[0] > rect.width for line in lines): #If any line is wider than the rect, add a new line and retry
        n_lines = len(lines) + 1
        print(len(text) / n_lines)
        lines = separate_in_lines(text, int(len(text) / n_lines))
        ch_height = int(rect.height / len(lines))

    #Print in surface
    for i, line in enumerate(lines):
        rendered = pygame.font.SysFont(font_name, ch_height).render(line, 0, color)
        blit_centered(surface, rendered, (rect.width/2, rect.y + ch_height * (i + 1/2)))
        
