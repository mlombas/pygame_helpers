"""This module provides useful methods to print to surface various types of data
"""

from math import floor, ceil
from pygame import font

if font.get_init(): font.init() #Ensure init

#TODO add this method but works with multiple lines
def print_bounded(surface, text, rect, color=(0, 0, 0), font_name=None):
    """Prints the text in such manner it does not exit the rect passed in
    
    This takes the maximum height possible, will reduce height
    when text has too much width and will create a new line when
    the text has less than half the rect's height.
    Text will be centered.
    Does not accept newline characters

    Input:
        surface - a pygame surface in which to draw
        text - the text to be printed
        rect - the bounds of the text
    Output: None
    """
    if len(text) == 0: return

    #Calculate parameters
    char_test_width, char_test_height = font.SysFont(font_name, rect.height).size("0") #TODO fix this to work better, now it leaves margins at the sides 
    char_rate = char_test_width / char_test_height #Get relationship in a single char
    chars_per_line = ceil((len(text) * rect.width / (char_rate * rect.height))**(1/2)) #Those formulas I created them with my bare hands, hope you like it
    maximum_size = min(rect.height, ceil(rect.width / (chars_per_line * char_rate)))
    
    #Print the text
    lines = [text[i:i+chars_per_line] for i in range(0, len(text), chars_per_line)] #Split the lines
    for i, line in enumerate(lines): 
        rendered_text = font.SysFont(font_name, maximum_size).render(line, 0, color)
        location = (rect.x + rect.width/2, rect.y + rect.height/len(lines) * (i + 0.5)) #set location, the height aligned to fit various lines
        blit_centered(surface, rendered_text, location)


def blit_centered(surface, other_surface, location):
    """Draws other_surface centered on location
    
    Input:
        surface - the surface in which to draw
        other_surface - the surface to draw
        location - the location, as a (x, y) tuple
    Output: None
    """
    width, height = other_surface.get_size()
    surface.blit(other_surface, (location[0] - width/2, location[1] - height/2))

