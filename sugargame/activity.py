import os
import gobject
import gtk

import sugar.activity.activity
import sugar.graphics.style

import pygame
import event

ACTIVITY = None

def get_activity():
    return ACTIVITY

class PygameActivity(sugar.activity.activity.Activity):
    def __init__(self, handle):
        super(PygameActivity, self).__init__(handle)

        self._socket = None
        self._screen = None
        
        # Fudge the toolbar size.
        TOOLBAR_HEIGHT = 75
        TAB_HEIGHT = 45
        self.width = gtk.gdk.screen_width()
        self.height = gtk.gdk.screen_height() - TOOLBAR_HEIGHT - TAB_HEIGHT
        
        global ACTIVITY
        ACTIVITY = self

    def build_canvas( self ):
        # Build the widget in which to embed Pygame.
        self._socket = gtk.Socket()

        eventbox = gtk.EventBox()
        eventbox.set_flags(gtk.CAN_FOCUS)
        eventbox.set_size_request(self.width, self.height)
        eventbox.add(self._socket)
        eventbox.show_all()

        self.set_canvas(eventbox)

        # Preinitialize Pygame so we can hook its methods.
        os.environ['SDL_WINDOWID'] = str(self._socket.get_id())
        pygame.init()

        # Hook certain Pygame functions with GTK equivalents.
        translator = event.Translator(self, eventbox)
        translator.hook_pygame()

        # Initialize the Pygame window.
        self._screen = pygame.display.set_mode((self.width,self.height))

        # Restore the default cursor.
        self._socket.get_window().set_cursor(None)
        
    def run_pygame(self, main_fn):
        # Run the main loop after a short delay.  The reason for the delay is that the
        # Sugar activity is not properly created until after its constructor returns.
        # If the Pygame main loop is called from the activity constructor, the 
        # constructor never returns and the activity freezes.
        gobject.idle_add(self._run_pygame_cb, main_fn)
        
    def _run_pygame_cb(self, main_fn):
        # Run the Pygame main loop.
        main_fn()
        return False

    def get_pygame_widget(self):
        return self._socket

    def get_pygame_screen(self):
        return self._screen
    