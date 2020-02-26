#!/usr/bin/python3
#
# Copyright (c) 2020 Wade Brainerd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import pygame
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


RADIUS = 100


class TestGame:

    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.x = -RADIUS
        self.y = RADIUS

        self.vx = RADIUS // 10
        self.vy = 0

        self.paused = False
        self.direction = 1

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
        width = screen.get_width()
        height = screen.get_height()

        dirty = []
        dirty.append(pygame.draw.rect(screen, (255, 255, 255),
                                      pygame.Rect(0, 0, width, height)))
        pygame.display.update(dirty)

        while self.running:
            dirty = []

            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    width = screen.get_width()
                    height = screen.get_height()
                    dirty.append(pygame.draw.rect(screen, (255, 255, 255),
                                                  pygame.Rect(0, 0,
                                                              width, height)))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction = -1
                    elif event.key == pygame.K_RIGHT:
                        self.direction = 1

            # Move the ball
            if not self.paused:

                # Erase the ball
                dirty.append(pygame.draw.circle(screen, (255, 255, 255),
                                                (self.x, self.y), RADIUS))

                self.x += self.vx * self.direction
                if self.direction == 1 and self.x > width - RADIUS:
                    self.x = width - RADIUS
                    self.direction = -1
                elif self.direction == -1 and self.x < RADIUS:
                    self.x = RADIUS
                    self.direction = 1

                self.y += self.vy
                if self.y > height - RADIUS:
                    self.y = height - RADIUS
                    self.vy = -self.vy

                self.vy += 5

                # Draw the ball
                dirty.append(pygame.draw.circle(screen, (192, 0, 0),
                                                (self.x, self.y), RADIUS))

            # Update Display
            pygame.display.update(dirty)

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
