"""Provides some helper methods and classes to work with input in pygame"""

import pygame

def prompt(surface, message, x=0, y=0, width=100, height=100):
    """Will prompt the user with a message and return what the user inputs.
    
    Please note that this method is async, it will stop execution until the
    user inputs something.
    This method only calls prompt(surface, message, rect) constructing a new
    rect with the parameters given

    Input:
        surface - the surface to show the prompt box
        message - the message to prompt
        x - the x coordinate of the top left corner
        y - the y coordinate of the top left corner
        width - the width of the box
        height - the height of the box

    Output:
        The string inputed by the user as the answer
    """
    return prompt(surface, message, pygame.Rect(x, y, width, height))

def prompt(surface, message, rect=pygame.Rect(0, 0, 100, 100)):
    """Will prompt the user with a message and return what the user inputs.
    
    Please note that this method is async, it will stop execution until the
    user inputs something.

    Input:
        surface - the surface to show the prompt box
        message - the message to prompt
        x - the x coordinate of the top left corner
        y - the y coordinate of the top left corner
        width - the width of the box
        height - the height of the box

    Output:
        The string inputed by the user as the answer
    """

    box = pygame.Surface((rect.width, rect.height))
    introduced = ""
    if not pygame.font.get_init(): pygame.font.init()
    font = pygame.font.SysFont(None, int(rect.height * 0.9 / 2)) #Leave 10% for margin
    while True: #Wait until next event, if its a keyboard event process it
        #Draw all box
        box.fill((0, 0, 0))
        box.blit(font.render(message, 0, (255, 255, 255)), (0, 0)) #Print message
        box.blit(font.render(introduced, 0, (255, 255, 255)), (0, rect.height * 0.9 / 2)) #Print the input so far
        surface.blit(box, rect)
        pygame.display.update()

        #Wait for input
        evt = pygame.event.wait()
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_BACKSPACE:
                introduced = introduced[:-1]
            elif evt.key == pygame.K_RETURN:
                return introduced #If the user presses enter, return the inputs
            else:
                introduced += evt.unicode            
   
