"""This provides several methods to help drawing on a surface
"""

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

