"""Provides some utility methods
"""

import pygame

def wait_until_event(events=[pygame.QUIT]):
    """Waits until some of the passed events happen
    
    Input:
        events - a list with the events to catch
    Output:
        the event catched
    """
    pygame.event.get()
    evt = pygame.event.wait()
    while evt.type not in events: 
        evt = pygame.event.wait()
    
    return evt


def separate_in_lines(text, max_chars_per_line):
    """Separates in lines without separating words
    
    Input:
        text - the text to separate
        max_max_chars_per_line - maximum number of chars per line
    """

    if max(len(w) for w in text.split()) > max_chars_per_line:
        raise ValueError("max_chars_per_line must be greater than the length of any word in text")

    lines = []
    while text:
        i = min(max_chars_per_line, len(text)) #set max length
        while i != len(text) and text[i] != " ": #Go backwards until not in the end of a word
            i -= 1
        
        sub = text[:i] #Extract text
        text = text[i + 1:] #dont add leading space
        lines.append(sub)
    
    return lines
