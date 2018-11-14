"""Provides some utility methods
"""

from collections import namedtuple
import pygame

def wait_until_event(*events):
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

    #--------------------------------------Classes---------------------------------------
    class CodexException(Exception):
        """Custom exception for this class so its easier to catch errors from here
        Works as a normal exception
        """
        pass

    class SurfaceHolder(object):
        """Helper class to store more information about a surface
        """

        #-----------------------Variables----------------------
        _dimensioned = {} 
        
        #-----------------------Methods----------------------------------
        def __init__(self, surface, *names, origin=None):
            surface_size = surface.get_size()
            self._original = pygame.Surface(surface_size) #save the original separated, this will be what we use to generate dimension variation and we dont want it to change
            self._original.blit(surface, (0, 0)) #gotta blit this so it gets the surface info
            self.add_dimension(surface_size) #add the original size to dimensioned

            self._names = names
            self._origin = origin

        def add_name(self, *names):
            """Adds a new name, after that this surface collection can be acessed
            from the SurfaceCodex with this name as well as with all the ones before

            Input: 
                names - the various names to add

            Output: None
            """
            self._names += names
        
        def get_names(self):
            """return the list of names with which this surface can be referenced
            
            Input: None

            Output:
                A tuple of strings
            """

            return tuple(self._names)

        def add_dimension(self, dimension):
            """Adds a new dimension to the array of dimensioned images

            Input:
                dimension - the new dimension to add

            Output: None
            """
            if dimension not in self.get_added_dimensions(): #If this dimension exists already dont add it
                new_surface = pygame.transform.scale(self._original, dimension)
                self._dimensioned[dimension] = new_surface

        def get_surface_dimensioned(self, dimension):
            """Returns a surface with the dimensions passed in, adding it to the dimensioned images dict if necessary

            Input:
                dimension - the dimension to return the image

            Output:
                the image dimensioned
            """
            if dimension not in self.get_added_dimensions(): #If dimension is not added yet, add it
                self.add_dimension(dimension)

            return self._dimensioned[dimension]

        def get_original(self):
            """Returns the original surface
            
            Input: None

            Output:
                The original surface with which this was created
            """
            return self._dimensioned[self._original.get_size()]

        def get_added_dimensions(self):
            """Returns the dimensions actually added
            
            Input: None

            Output: 
                a tuple of tuples, each subtuple being a dimension in the form (width, height)
            """
            return tuple(self._dimensioned.keys())

        def __eq__(self, other):
            #an empty origin is considered as diferent from another empty one (Im gonna have problems with this but gotta keep this like this for now
            return self._origin and other._origin and self._origin == other._origin


        def __repr__(self):
            return f"StoredSurface(\n\tnames: {self.get_names()}\n\torigin: {self._origin}\n)"

    #-----------------------------Variables-----------------------------------
    _holders = []
    
    #-----------------------------Methods------------------------------------
    @staticmethod
    def _add_surface(surface, *names, origin=None):
        """Adds a new surface to the codex
        WARNING: private method, should not use this unless you know what you are doing

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
                raise SurfaceCodex.CodexException(f"There is already a surface named {name}") 

        to_store = SurfaceCodex.SurfaceHolder(surface, *names, origin=origin)
        if to_store in SurfaceCodex._holders:
            store_index = SurfaceCodex._holders.index(to_store)
            SurfaceCodex._holders[store_index].add_name(*names) #if already exists, add names
        else:
            SurfaceCodex._holders.append(to_store) #if not, create new

    @staticmethod
    def load_surface(file_name, *names):
        """Loads a image from a file and adds it to the codex

        Input:
            file_name - the name of the file to load
            name(s) - the the name used to store it (can be more than one adding this argument various times)

        Output: None

        Raises:
            CodexException - if name is already in the codex

        """
        image = pygame.image.load(file_name)
        SurfaceCodex._add_surface(image, *names, origin=file_name)
            
    @staticmethod
    def get_surface(name, dimensions=None):
        """Returns the surface referenced by that name, redimensioned if necessary

        Input:
            name - the name of the surface
            dimensions[optional] - the dimension in which this surface will be returned, a (width, height) tuple

        Output:
            the surface requested

        Raises:
            CodexException - if name is not in the codex
        """
        if name not in SurfaceCodex.get_name_list():
            raise SurfaceCodex.CodexException(f"No surface named {name}")
        
        holder = SurfaceCodex._get_holder(name)
        print(holder)
        if dimensions is None: 
            return holder.get_original()
        else: 
            return holder.get_surface_dimensioned(dimensions)

    @staticmethod
    def _get_holder(name):
        """Get a SurfaceHolder from the codex
        WARNING: PRIVATE METHOD, TO GET THE ACTUAL SURFACE USE get_surface

        Input:
            name - the name of the surface

        Output:
            The surface

        Raises:
            CodexException - if name is not in the codex
        """
        if name not in SurfaceCodex.get_name_list():
            raise SurfaceCodex.CodexException(f"No surface named {name}")

        for holder in SurfaceCodex._holders:
            if name in holder.get_names():
                return holder

    @staticmethod
    def get_name_list():
        names = []
        for surf in SurfaceCodex._holders: #Loop through every surface and append the names
            names += list(surf.get_names())

        return tuple(names)

