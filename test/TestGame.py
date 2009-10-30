#!/usr/bin/python
import pygame
import gtk

class TestGame:
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()
        
        # Set up a font for rendering.
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        
    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass
        
    # The main game loop.
    def run(self):
        self.running = True    
            
        screen = pygame.display.get_surface()

        while self.running:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Clear Display
            screen.fill((255,255,255)) #255 for white

            # Flip Display
            pygame.display.flip()  
            
            # Try to stay at 30 FPS
            self.clock.tick(30)

# This function is called when the game is run directly from the command line:
# ./TestGame.py 
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = TestGame() 
    game.run()

if __name__ == '__main__':
    main()

