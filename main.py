from engine import Scene, SceneManager
from piece import Piece
from board import Board
import data

import pygame
import random

#
# game
#

class Game(Scene):
    def setup(self):

        # debug flag
        self.debug = True

        # controls
        self.controls = {
            pygame.K_r:      self.setup,
            pygame.K_ESCAPE: self.pause,
            pygame.K_DOWN:   self.slow_drop,
            pygame.K_RIGHT:  self.move_right,
            pygame.K_LEFT:   self.move_left,
            pygame.K_c:      self.hold_piece,
            pygame.K_UP:     self.rotate_clockwise,
            pygame.K_z:      self.rotate_counterclockwise,
            pygame.K_SPACE:  self.quick_drop
        }

        # score variables
        self.score = 0
        self.starting_level = 1
        self.lines_cleared = 0

        self.levelup_threshold = 10

        # game functionality
        self.board = Board(data.board_dimensions)
        self.piece_origin = (self.board.width//2-1, 2) # where the piece will spawn in
        self.rng_bag = []
        self.piece = self.get_random_piece()
        self.next_piece = self.get_random_piece()

        # holding
        self.piece_hold = None
        self.recent_hold = False
        
        self.setup_engine()

    #
    #  Game Controls
    #

    @property
    def level(self):
        return self.lines_cleared // self.levelup_threshold + self.starting_level

    def get_random_piece(self):

        # fill the bag if empty
        if len(self.rng_bag) == 0:
            
            # populate with 2 of every piece
            for piece_data in data.pieces + data.pieces:
                self.rng_bag.append(Piece(
                    *self.piece_origin,
                    piece_data['color'],
                    piece_data['stages'],
                    piece_data['centers'],
                ))
            
            # scramble bag
            random.shuffle(self.rng_bag)
        
        # get random piece
        return self.rng_bag.pop()
        
    def new_piece(self):

        self.piece = self.next_piece
        self.next_piece = self.get_random_piece()
        
        # check to see if the game should be over
        # due to piece spawning inside existing ones
        if self.board.does_hitbox_collide(self.piece.get_hitbox()):
            self.gameover()
    
    def move_left(self):
        self.piece.move(self.board, (-1, 0))
    
    def move_right(self):
        self.piece.move(self.board, (1, 0))
    
    def move_down(self):

        # check to see if piece should be locked
        hitbox = self.piece.get_hitbox(position_delta=(0, 1))
        if self.board.does_hitbox_collide(hitbox):
            self.board.lock_piece(self.piece)
            self.check_for_clears()
            self.new_piece()
            self.recent_hold = False
            return False
        
        # other wise move the piece
        self.piece.move(self.board, (0, 1))
        return True

    def slow_drop(self):
        self.move_down()
        self.reset_drop_timer()

    def quick_drop(self):
        while self.move_down():
            pass

    def rotate_clockwise(self):
        self.piece.rotate(self.board, 1)

    def rotate_counterclockwise(self):
        self.piece.rotate(self.board, -1)

    def hold_piece(self):
        
        # prevent holding if recent hold
        if self.recent_hold:
            return False
        
        # turn on recent hold to prevent holding
        self.recent_hold = True

        # if the hold is empty
        if self.piece_hold == None:
            
            # set hold to current piece
            self.piece_hold = self.piece

            # get new piece
            self.new_piece()

        # if hold has a piece in it
        else:

            # swap hold with piece
            self.piece_hold, self.piece = self.piece, self.piece_hold
        
            # set piece location to piece origin
            ox, oy = self.piece_origin
            self.piece.x = ox
            self.piece.y = oy

    def check_for_clears(self):
        clears = self.board.clear_complete()
        if clears > 0:
            self.lines_cleared += clears
            self.score += clears ** 2 * 100

    def get_drop_speed(self):
        return 1000 - self.level * 30

    def reset_drop_timer(self):
        pygame.time.set_timer(Game.PIECE_FALL, self.get_drop_speed())

    def gameover(self):
        g = self.manager.globals

        # set this game as the last game
        g.last_game = self

        # calculate highscore
        if self.score > g.highscore:
            g.highscore = self.score
        
        # switch to gameover scene
        self.manager.set_scene(Gameover)

    def pause(self):
        self.manager.set_overlay_scene(PauseMenu)

    #
    #  Engine Interface
    #

    # get user event enum for piece falling
    PIECE_FALL = pygame.USEREVENT + 1

    def setup_engine(self):

        # enable joystick
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joy = pygame.joystick.Joystick(0)
            self.joy.init()

        # repeat key if sustained for 100 ms (every 50 ms)
        pygame.key.set_repeat(100, 50)

        # register the fall tick event
        self.reset_drop_timer()
        
        # load fonts
        self.load_fonts()

    def load_fonts(self):
        self.small_font = pygame.font.Font(data.font, int(self.height*0.035))
        self.big_font = pygame.font.Font(data.font, int(self.height*0.05))

    def on_resize(self):
        self.load_fonts()

    def render(self):
        
        #
        # set correct background color
        #
        
        self.window.fill(data.background_color)

        #
        # draw the game board 
        # (grid, border, active piece, and locked pieces)
        #

        bh = self.height - 100
        bw = bh/self.board.height*self.board.width
        bx = (self.width/2) - (bw/2)
        by = (self.height/2) - (bh/2)
        draw_packet = (self.window, (bx, by), (bw, bh))

        self.board.draw(*draw_packet)
        self.piece.draw(self.board, *draw_packet)
        self.board.draw_grid(*draw_packet)
        self.board.draw_border(*draw_packet)
        
        #
        # draw hold piece
        #

        text_surface = self.small_font.render('Hold', True, data.primary_color)
        text_height = text_surface.get_rect().height

        size = self.height * 0.1
        x = bx - size - data.padding
        y = by + text_height

        pygame.draw.rect(self.window, data.foreground_color, pygame.Rect(x, y, size, size), data.border_width)
        if self.piece_hold:
            self.piece_hold.draw_preview(self.window, (x, y),(size, size))

        self.window.blit(text_surface, (x, y-text_height))

        #
        # draw next piece
        #

        size = self.height * 0.15
        x = bx + bw + data.padding
        y = by + bh - size
        pygame.draw.rect(self.window, data.foreground_color, pygame.Rect(x, y, size, size), data.border_width)
        self.next_piece.draw_preview(self.window, (x, y),(size, size))

        text_surface = self.small_font.render('Next', True, data.primary_color)
        text_height = text_surface.get_rect().height
        self.window.blit(text_surface, (x, y-text_height))
        
        #
        # draw current score
        #

        text_surface = self.big_font.render(f'Score: {self.score:05.0f}', True, data.primary_color)
        text_height = text_surface.get_rect().height
        self.window.blit(text_surface, (x+data.padding, by))
        
        #
        # draw current level
        #
        
        text_surface = self.big_font.render(f'Level: {self.level}', True, data.primary_color)
        self.window.blit(text_surface, (x+data.padding, by+text_height))
        
        #
        # draw lines completed
        #
        
        text_surface = self.big_font.render(f'Lines: {self.lines_cleared}', True, data.primary_color)
        self.window.blit(text_surface, (x+data.padding, by+text_height*2))

    def on_event(self, event):

        # fall piece at the level speed automatically
        if event.type == Game.PIECE_FALL:
            self.move_down()

        # keyboard controls
        elif event.type == pygame.KEYDOWN:
            key = event.key

            for control in self.controls:
                if key == control:
                    self.controls[control]()
                    break
                    
#
# menus
#

class GameMenuScene(Scene):
    def __init__(self, manager):

        self.title = data.game_name
        self.subtitle = ''

        self.options = []
        self._option_rects = []

        super().__init__(manager)

        self._compile_menu_data()

    def add_option(self, label, function=None):
        self.options.append((label, function))

    def on_resize(self):
        self._compile_menu_data()

    def _compile_menu_data(self):
        
        #
        # compile rectangles
        #

        # clear the previously compiled rects
        self._option_rects = []

        ow = self.width/2*0.7
        oh = self.height*0.1

        options_height = (oh + data.padding) * len(self.options)

        # make a rect for each button
        for i, option in enumerate(self.options):
            
            x = self.width * 0.75 - ow / 2
            y = self.height / 2 + (oh + data.padding) * i - options_height / 2

            self._option_rects.append(pygame.Rect(x,y, ow, oh))

        #
        # load fonts
        #
        self.title_font = pygame.font.Font(data.font, int(self.height*0.1))
        self.label_font = pygame.font.Font(data.font, int(oh*0.4))

    def render(self):

        # fill the background
        self.window.fill(data.background_color)

        super().render()
        
        #
        # draw titles
        #

        # get surfaces with text from fonts
        title_surface = self.title_font.render(self.title, True, data.primary_color)
        subtitle_surface = self.label_font.render(self.subtitle, True, data.secondary_color)

        # get bounding/positioning rectangles
        title_rect = title_surface.get_rect()
        subtitle_rect = subtitle_surface.get_rect()

        # get total height
        total_height = title_rect.height + data.padding + subtitle_rect.height

        # set the centers in the center of the half
        center_point = (self.width//4, 0)
        title_rect.center = center_point
        subtitle_rect.center = center_point

        # center the group of objects

        title_rect.y = self.height//2 - total_height + title_rect.height//2

        subtitle_rect.y = title_rect.bottom + data.padding
        
        # draw the text
        self.window.blit(title_surface, title_rect)
        self.window.blit(subtitle_surface, subtitle_rect)

        #
        # draw buttons
        #

        # get mouse position for hover highlight
        mx, my = pygame.mouse.get_pos()

        # draw each option
        for option, rect in zip(self.options, self._option_rects):

            label, _ = option

            # set color for items
            color = data.primary_color

            # if the option is a button
            if option[1]:
                
                # color change on hover
                if rect.collidepoint(mx, my):
                    color = data.secondary_color

                # draw border to indicate button
                pygame.draw.rect(self.window, color, rect, 3)

            # draw the button label
            text_surface = self.label_font.render(label, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = rect.center
            self.window.blit(text_surface, text_rect)
        
    def on_event(self, event):

        # check to see if the user clicks a button
        if event.type == pygame.MOUSEBUTTONUP:

            # iterate through all buttons
            for option, rect in zip(self.options, self._option_rects):

                # check whether mouse clicked one
                if rect.collidepoint(event.pos) and callable(option[1]):
                    
                    # evoke its action
                    option[1]()

                    break

class MainMenu(GameMenuScene):
    def setup(self):
        self.title = data.game_name
        self.subtitle = 'Tetris... but not'

        self.add_option('Start', lambda: self.manager.set_scene(Game))
        self.add_option('Controls', lambda: self.manager.set_scene(Controls))
        self.add_option('Quit', self.manager.stop)

class PauseMenu(GameMenuScene):
    def setup(self):
        self.title = 'Paused'
        self.subtitle = 'Take your time!'

        self.add_option('Continue', self.manager.close_overlay_scene)
        self.add_option('Main Menu', lambda: self.manager.set_scene(MainMenu))
        self.add_option('Quit', self.manager.stop)

class Controls(GameMenuScene):
    def setup(self):
        self.title = 'Controls'
        self.subtitle = 'Study These :)'
        
        self.add_option('Move: Left and Right')
        self.add_option('Rotate: Up and Z')
        self.add_option('Fall: Down')
        self.add_option('Fastfall: Spacebar')
        self.add_option('Pause: Escape or Backspace')
        self.add_option('Hold: C')
        self.add_option('')
        self.add_option('Back', lambda: self.manager.set_scene(MainMenu))

class Gameover(GameMenuScene):
    def setup(self):
        self.title = 'Gameover'
        self.subtitle = 'Thanks for Playing!'

        g = self.manager.globals

        self.add_option(f'Score: {g.last_game.score:05.0f}')
        self.add_option(f'Highscore: {g.highscore:05.0f}')
        self.add_option('')

        self.add_option('Play Again', lambda: self.manager.set_scene(Game))
        self.add_option('Main Menu', lambda: self.manager.set_scene(MainMenu))
        self.add_option('Quit', self.manager.stop)

if __name__ == '__main__':
    sm = SceneManager()
    sm.globals.highscore = 0
    sm.start(MainMenu, (1920//2,1080//2), caption=data.game_name)