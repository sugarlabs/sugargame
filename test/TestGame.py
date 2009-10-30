#!/usr/bin/python
import pygame
import gtk

class TestGame:
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.x = -100
        self.y = 100

        self.vx = 10
        self.vy = 0

        self.paused = False
        
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

            # Move the ball
            if not self.paused:
                self.x += self.vx
                if self.x > screen.get_width() + 100:
                    self.x = -100
                
                self.y += self.vy
                if self.y > screen.get_height() - 100:
                    self.y = screen.get_height() - 100
                    self.vy = -self.vy
                
                self.vy += 5;
            
            # Clear Display
            screen.fill((255,255,255)) #255 for white

            # Draw the ball
            pygame.draw.circle(screen, (255,0,0), (self.x, self.y), 100)
                    
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

