import pygame

class Piece:
    def __init__(self, x, y, color, stages, centers):
        self.x = x
        self.y = y
        self.color = color
        
        self.stages = stages
        self.centers = centers
        self.rotation = 0

    def rotate(self, board, delta):

        # if no board is provided then force rotate
        if board:

            # check to see if new hit box colides with anything
            hitbox = self.get_hitbox(rotation_delta=delta)
            if board.does_hitbox_collide(hitbox):
                return False

        # update rotation
        self.rotation += delta
        self.rotation %= len(self.stages)
        return True

    def move(self, board, delta):

        # get delta components
        dx, dy = delta

        hitbox = self.get_hitbox(position_delta=delta)
        if not board.does_hitbox_collide(hitbox):
            self.x += dx
            self.y += dy

    def get_hitbox(self, position_delta=(0,0), rotation_delta=0):
        
        # get the cells for next rotation
        next_rotation = (self.rotation + rotation_delta)
        next_rotation %= len(self.stages)
        cells = self.stages[next_rotation]

        # get position delta components
        dx, dy = position_delta

        # add position delta and current position
        new_cells = []
        for xi, yi in cells:
            x = xi + dx + self.x
            y = yi + dy + self.y
            new_cells.append((x,y))

        return new_cells

    def draw(self, board, window, location, dimensions):
        
        x, y = location
        w, h = dimensions

        # get the size of the cells
        cw = w / board.width
        ch = h / board.height

        # get the offset for how far the piece can go down
        offset = 0
        for i in range(board.height):
            if board.does_hitbox_collide(self.get_hitbox(position_delta=(0, i))):
                offset = i - 1
                break
        
        # draw active pieces
        for xi, yi in self.get_hitbox():
            cx = x + xi * cw
            cy = y + yi * ch

            # actual location
            pygame.draw.rect(window, self.color, pygame.Rect(cx, cy, cw+1, ch+1))

            # where the piece will end up if dropped
            s = pygame.Surface((cw+1, ch+1))
            s.set_alpha(50)
            s.fill(self.color)
            window.blit(s, (cx, cy + offset*ch))
    
    def draw_preview(self, window, location, dimensions):

        x, y = location
        w, h = dimensions

        cw = w * 0.2
        ch = h * 0.2

        rcx, rcy = self.centers[self.rotation]
        for xi, yi in self.stages[self.rotation]:
            cx = x + (xi - rcx) * cw + w/2 - cw/2
            cy = y + (yi - rcy) * ch + h/2 - ch/2

            pygame.draw.rect(window, self.color, pygame.Rect(cx, cy, cw+1, ch+1))
