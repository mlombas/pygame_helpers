"""Provides some utility methods
"""

from collections import namedtuple
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


class SurfaceCodex(object):
    """This class serves the purpose of loading and storing surfaces without repeating them
    """
    class StoredSurface(pygame.Surface):
        """Helper class to store more information about a surface
        """
        def __init__(self, surface, *names, file_origin=None):
            super().__init__(surface.get_size())
            self.blit(surface, (0, 0)) #gotta blit this so it gets the surface info
            self.names = names
            self.file_origin = file_origin

        def __eq__(self, other):
            #if the origin is not the same or the dimensions are not equal, then its a new surface
            #an empty origin is considered as diferent from another empty one (Im gonna have problems with this but gotta keep this like this for now
            file_equal = self.file_origin and other.file_origin and self.file_origin == other.file_origin
            dimensions_equal = self.get_size() == other.get_size()
            return file_equal and dimensions_equal
        
        def __repr__(self):
            return "StoredSurface(\n\tnames: {}\n\torigin: {}\n)".format(self.names, self.file_origin)


    _surfaces = []
    
    @staticmethod
    def add_surface(surface, *names, file_origin=None):
        """Adds a new surface to the codex

        Input:
            surface - the surface to add
            *names - the name(s) used to store surface
            file_origin[optional] - the file origin for this surface

        Output: None

        Raises:
            NameError - if name is already in the codex
        """
        #check if any of the names is already in list
        name_list = SurfaceCodex.get_name_list()
        for name in names: #could do this with an any() but this way I can actually include the exact name that is provoking the NameError with it
            if name in name_list:
                raise NameError("There is already a surface named {}".format(name)) #TODO make a custom error class for the whole framework

        to_store = SurfaceCodex.StoredSurface(surface, *names, file_origin=file_origin)
        if to_store in SurfaceCodex._surfaces:
            store_index = SurfaceCodex._surfaces.index(to_store)
            SurfaceCodex._surfaces[store_index].names += names #if already exists, add names
        else:
            SurfaceCodex._surfaces.append(to_store) #if not, create new

    @staticmethod
    def load_surface(file_name, name, dimensions=None):
        """Loads a image from a file and adds it to the codex

        Input:
            file_name - the name of the file to load
            name - the the name used to store it
            dimensions[optional] - the dimensions of the surface, it will be scaled if necessary

        Output: None

        Raises:
            NameError - if name is already in the codex
        """
        image = pygame.image.load(file_name)
        if dimensions is not None: #Transform if requested
            image = pygame.transform.scale(image, dimensions)

        SurfaceCodex.add_surface(image, names, file_origin=file_name)

    @staticmethod
    def get_surface(name):
        """Get a surface from the codex

        Input:
            name - the name of the surface

        Output:
            The surface

        Raises:
            NameError - if name is not in the codex
        """
        if name not in SurfaceCodex.get_name_list():
            raise NameError("No surface named {}".format(name))

        for surf in SurfaceCodex._surfaces:
            if name in surf.names:
                return surf

    @staticmethod
    def get_name_list():
        names = []
        for surf in SurfaceCodex._surfaces: #Loop through every surface and append the names
            names += surf.names

        return names

