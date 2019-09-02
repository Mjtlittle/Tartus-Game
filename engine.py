import pygame
import types
import sys

# I am modeled the Scene api after the scene library present in 
# the IOS app Pythonista, as I am familiar with how it can be used 
# and it is very fexible
# (http://omz-software.com/pythonista/docs/ios/scene.html#overview)

class SceneManager:
    def __init__(self):
        self.globals = types.SimpleNamespace()
    
    def set_scene(self, scene):
        self.background_scene = None
        self.active_scene = scene(self)
        return self.active_scene

    def set_overlay_scene(self, scene):
        self.background_scene = self.active_scene
        self.active_scene = scene(self)

    def close_overlay_scene(self):
        self.active_scene = self.background_scene
        self.background_scene = None

    def set_size(self, window_size):
        self.window = pygame.display.set_mode(window_size)

    def start(self, scene, window_size, **flags):

        # initialize pygame
        pygame.init()
        
        # window settings
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(flags.get('caption','no-caption-set'))
        
        # clock settings
        self.clock = pygame.time.Clock()
        self.fps = flags.get('fps',60)

        # set starting scene        
        self.set_scene(scene)

        # start loop
        while True:

            self.clock.tick(self.fps)

            # pass each event to the handler
            for event in pygame.event.get():
                
                # when quit from window, quit
                if event.type == pygame.QUIT:
                    self.stop()

                # on window resize
                elif event.type == pygame.VIDEORESIZE:
                    self.window = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    self.active_scene.width, self.active_scene.height = self.window.get_size()
                    self.active_scene.on_resize()
                
                # pass through event to scene
                else:
                    self.active_scene.on_event(event)
        
            self.active_scene.update()

            # black background behind all rendered scenes
            self.window.fill((0,0,0))

            # draw the background scene behind the active scene if its set
            # if self.background_scene:
            #    self.background_scene.render()

            # render active primary scene
            self.active_scene.render()

            # push the framebuffer to the scene
            pygame.display.update()

    def stop(self):

        # allow the scene to cleanup for the stop
        self.active_scene.on_stop()

        # quit pygame and the process running
        pygame.quit()
        sys.exit()

class Scene:
    def __init__(self, manager):
        self.manager = manager

        self.clock = self.manager.clock
        self.window = self.manager.window
        self.globals = self.manager.globals

        self.width, self.height = self.window.get_size()

        self.setup()

    #
    #  Interface for Other Scenes
    #

    def setup(self):
        pass

    def on_stop(self):
        pass

    def update(self):
        pass

    def render(self):
        pass
    
    def on_resize(self):
        pass

    def on_event(self, event):
        pass

