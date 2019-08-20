from gettext import gettext as _

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pygame

from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton


sys.path.append('..')  # Import sugargame package from top directory.
import sugargame.canvas

import TestGame


class TestActivity(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.paused = False

        # Create the game instance.
        self.game = TestGame.TestGame()

        # Build the activity toolbar.
        self.build_toolbar()

        # Build the Pygame canvas and start the game running
        # (self.game.run is called when the activity constructor
        # returns).
        self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display])

        # Note that set_canvas implicitly calls read_file when
        # resuming from the Journal.
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        # Pause/Play button:

        pause_play = ToolButton('media-playback-pause')
        pause_play.set_tooltip(_("Pause"))
        pause_play.set_accelerator(_('<ctrl>space'))
        pause_play.connect('clicked', self._pause_play_cb)
        pause_play.show()

        toolbar_box.toolbar.insert(pause_play, -1)

        # Blank space (separator) and Stop button at the end:

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        stop_button.connect('clicked', self._stop_cb)

    def _pause_play_cb(self, button):
        # Pause or unpause the game.
        self.paused = not self.paused
        self.game.set_paused(self.paused)

        # Update the button to show the next action.
        if self.paused:
            button.set_icon_name('media-playback-start')
            button.set_tooltip(_("Start"))
        else:
            button.set_icon_name('media-playback-pause')
            button.set_tooltip(_("Pause"))

    def _stop_cb(self, button):
        self.game.running = False

    def read_file(self, file_path):
        self.game.read_file(file_path)

    def write_file(self, file_path):
        self.game.write_file(file_path)

    def get_preview(self):
        return self._pygamecanvas.get_preview()
