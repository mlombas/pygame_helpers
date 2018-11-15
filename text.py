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
    if not text: return
    #TODO fix this so it uses all space aviable
    rate = get_font_rate(font_name)
    n_lines = 0
    while True:
        n_lines += 1
        max_viable_chars = int(rect.width / (rect.height / n_lines / rate))
        if max_viable_chars * n_lines >= len(text) and max_viable_chars > max(len(w) for w in text.split(" ")): break
   
    lines = separate_in_lines(text, max_viable_chars)
    char_height = int(rect.height / n_lines)

    #Print in surface
    for i, line in enumerate(lines):
        rendered = pygame.font.SysFont(font_name, char_height).render(line, 0, color)
        blit_centered(surface, rendered, (rect.width/2, rect.y + char_height * (i + 1/2)))
    

def get_font_rate(font_name):
    """Returns the height/width ratio for the font, the font must be monospace
    
    Input:
        font_name - the name of the font
    Output: None
    """
    width, height = pygame.font.SysFont(font_name, 100).size("0")
    return height / width
