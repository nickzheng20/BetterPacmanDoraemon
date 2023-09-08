import pygame

def setup_fonts(font_size, bold=False, italic=False):
    ''' Load a font, given a list of preferences

        The preference list is a sorted list of strings (should probably be a parameter),
        provided in a form from the FontBook list. 
        Any available font that starts with the same letters (lowercased, spaces removed) 
        as a font in the font_preferences list will be loaded.
        If no font can be found from the preferences list, the pygame default will be returned.

        returns -- A Font object
    '''
    font_preferences = ['Helvetica Neue', 'Iosevka Regular', 'Comic Sans', 'Courier New']
    available = pygame.font.get_fonts()
    prefs = [x.lower().replace(' ', '') for x in font_preferences]
    for pref in prefs:
        a = [x
             for x in available
             if x.startswith(pref)
            ]
    if a:
        fonts = ','.join(a) #SysFont expects a string with font names in it
        return pygame.font.SysFont(fonts, font_size, bold, italic)
    return pygame.font.SysFont(None, font_size, bold, italic)

def word_wrap(rect, font, color, text):
    ''' Wrap the text into the space of the rect, using the font object provided.
        Returns a surface of rect size with the text rendered in it.
    '''
    paragraph = {} # the container of each paragraph of the text
    row = {} # the container of each row of the text which will be shown on the rect
    p_counter = 0 # paragraph's index
    r_counter = 0 # row's index
    str = "" # the strings in each paragraph
    start_point = 0 # the start point of paragraph[:]
    end_point = 0 # the end point of last row, which can also be the start point of the next row 
    
    surface1 = pygame.Surface(rect.size) # the surface with the same size as rect, which we will finally return
    surface1.fill((0,0,0))
    # set the white background become transparent
    surface1.convert_alpha()
    surface1.set_colorkey((0,0,0)) 
    surface1_width = 0 # the y position of the first row of text will be render on the rect
    # use for loop to find each paragraph of the text
    for i in range(len(text)):
        if text[i] != "\n":
            str += text[i]
        else:
            paragraph[p_counter] = str + "\n"
            str = ""
            p_counter += 1 # fill next paragraph
    paragraph[p_counter] = str + "\n"
    # use for loop to find each row of the text will be shown on the rect
    for i in range(p_counter+1):
        for j in range(len(paragraph[i])):
            surface = pygame.font.Font.render(font, paragraph[i][start_point:j], True, color)
            size = pygame.Surface.get_size(surface) # get the size of the fonted text
            if (size[0] <= rect.width and paragraph[i][j] == " "): # check if every word in the sentence is completed and the length of rendered text is below the length boundary
                row[r_counter] = paragraph[i][start_point:j] # the row should contain start point to this word
                end_point = j # record this turn's end point
            elif size[0] >= rect.width : # if next add word to current row will over the boundary, we should let the word be the start of next row
                start_point = end_point # let the end point of last turn become the start point of next turn
                r_counter += 1 # fill next row
            elif paragraph[i][j] == "\n": # if we need to get to next paragraph, we should go to a new row
                row[r_counter] = paragraph[i][start_point:j]
                start_point = j
                r_counter += 1
        start_point = 0 # after check each paragraph, we should let the start point become 0 
    # bill each row on the rect
    for i in range(len(row)):
        surface = surface = pygame.font.Font.render(font, row[i], True, color)
        size = pygame.Surface.get_size(surface)
        surface1.blit(surface, (0,surface1_width))
        surface1_width += size[1]+10
    # set the alpha value of the whole surface to ensure the transparent
    surface1.set_alpha(200)

    return surface1