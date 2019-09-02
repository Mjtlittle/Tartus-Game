import data
import pygame

class Board:
    def __init__(self, dimensions=(10,20)):
        self.width, self.height = dimensions
        
        self.data = None

        self.clear()

    def is_open(self, xi, yi):
        return self.is_within(xi, yi) and (self.get_cell(xi, yi) == None)

    def is_within(self, xi, yi):
        return (0 <= xi < self.width) and (0 <= yi < self.height)

    def does_hitbox_collide(self, hitbox):
        for xi, yi in hitbox:
            if not self.is_open(xi, yi):
                return True
        return False

    def get_cell(self, xi, yi):
        return self.data[yi][xi]
    
    def set_cell(self, xi, yi, value):
        self.data[yi][xi] = value

    def clear_complete(self):

        # remove all rows that are full, 
        # while also keeping track of that count
        replace_count = 0
        for i, row in reversed(list(enumerate(self.data))):
            if all(row):
                self.data.pop(i)
                replace_count += 1
        
        # add the blank rows back to the top
        for _ in range(replace_count):
            self.data.insert(0, [None for _ in range(self.width)])
        
        # return the amount of lines cleared
        return replace_count
    
    def lock_piece(self, piece):
        for xi, yi in piece.get_hitbox():
            self.set_cell(xi, yi, piece.color)
    
    def draw_grid(self, window, location, dimensions):

        x, y = location
        w, h = dimensions

        cw = w / self.width
        ch = h / self.height

        # verticals
        for xi in range(1,self.width):
            cx = x + xi * cw
            pygame.draw.line(window, data.middleground_color, (cx,y), (cx,y+h))

        # horizontals
        for yi in range(1,self.height):
            cy = y + yi * ch
            pygame.draw.line(window, data.middleground_color, (x,cy), (x+w,cy))

    def draw_border(self, window, location, dimensions):
        x, y = location
        w, h = dimensions

        pygame.draw.rect(window, data.foreground_color, pygame.Rect(x,y,w,h), data.border_width)

    def draw(self, window, location, dimensions):

        argument_tuple = (window, location, dimensions)

        x, y = location
        w, h = dimensions

        cw = w / self.width
        ch = h / self.height

        # draw locked pieces
        for xi in range(self.width):
            for yi in range(self.height):
                
                # get cell color
                cell_color = self.get_cell(xi, yi)

                # if the piece exists (ie. there is a color present)
                if cell_color != None:

                    cx = x + xi * cw
                    cy = y + yi * ch

                    pygame.draw.rect(window, cell_color, pygame.Rect(cx, cy, cw+1, ch+1))
        
    def clear(self):
        self.data = [[None for _ in range(self.width)] for _ in range(self.height)]
