from gettext import gettext as _

import sys
import gtk

import sugar.activity.activity
import sugar.graphics.toolbutton

sys.path.append('..') # Import sugargame package from top directory.
import sugargame.activity

import TestGame

class TestActivity(sugargame.activity.PygameActivity):
    def __init__(self, handle):
        super(TestActivity, self).__init__(handle)
        
        self.metadata['mime_type'] = 'application/x-physics-activity'
        
        self._resume_path = None
        
        self.build_toolbar()
        self.build_canvas()

        self.paused = False

        # Create the game instance.
        self.game = TestGame.TestGame(self.get_pygame_screen())
        
        # If resuming from the Journal, load the data.
        if self._resume_path:
            self.read_file(self._resume_path)

        # Start the main loop running.
        self.run_pygame(self.game.run)
        
    def build_toolbar(self):        
        stop_play = sugar.graphics.toolbutton.ToolButton('media-playback-stop')
        stop_play.set_tooltip(_("Stop"))
        stop_play.set_accelerator(_('<ctrl>space'))
        stop_play.connect('clicked', self._stop_play_cb)

        toolbar = gtk.Toolbar()
        toolbar.insert(stop_play, 0)
        toolbar.insert(gtk.SeparatorToolItem(), 1)
        
        toolbox = sugar.activity.activity.ActivityToolbox(self)
        toolbox.add_toolbar(_("Pygame"), toolbar)
        
        toolbox.show_all()
        self.set_toolbox(toolbox)

    def _stop_play_cb(self, button):
        # Pause or unpause the game.
        self.paused = not self.paused
        self.game.set_paused(self.paused)
        
        # Update the button to show the next action.
        if self.paused:
            button.set_icon('media-playback-start')
            button.set_tooltip(_("Start"))
        else:
            button.set_icon('media-playback-stop')
            button.set_tooltip(_("Stop"))

    def read_file(self, file_path):
        # Read file is called before the constructor returns when game is not yet valid.
        # Caching the file path seems to work in this specific instance.
        if not self.game:
            self._resume_path = file_path
        else:
            self.game.read_file(file_path)
        
    def write_file(self, file_path):
        self.game.write_file(file_path)
