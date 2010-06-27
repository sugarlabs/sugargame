== Sugargame ==

Sugargame is a Python package which allows [http://www.pygame.org/ Pygame] 
programs to run well under Sugar. 
It is fork of the olcpgames framework, which is no longer maintained.

http://git.sugarlabs.org/projects/sugargame

What it does:

* Wraps a Sugar activity around an existing Pygame program with few changes
* Allows Sugar toolbars and other widgets to be added to the activity UI
* Provides hooks for saving to and restoring from the Journal

==== Differences between Sugargame and olpcgames ====

The olpcgames framework provides a wrapper around Pygame which attempts to 
allow a Pygame program to run mostly unmodified under Sugar.  To this end, 
the Pygame program is run in a separate thread with its own Pygame message 
loop while the main thread runs the GTK message loop.  Also, olpcgames wraps 
Sugar APIs such as the journal and mesh into a Pygame-like API.

Sugargame takes a simpler approach; it provides a way to embed Pygame into a 
GTK widget.  The Sugar APIs are used to interact with Sugar, the Pygame APIs 
are used for the game.  

Sugargame advantages:

* Simpler code
* More elegant interface between Pygame and GTK
* Runs as a single thread: no thread related segfaults
* Possible to use Sugar widgets with Pygame

Sugargame limitations:

* No support for Pango or SVG sprites (yet)

== Using Sugargame ==

See also [[Development Team/Sugargame/Examples]].

==== Wrapping a Pygame program ====

To use Sugargame to Sugarize a Pygame program, set up an activity directory and 
copy the Sugargame package to it.

The activity directory should look something like this:
 
   activity/            - Activity directory: activity.info, SVG icon, etc.
   sugargame/           - Sugargame package
   MyActivity.py        - Activity class
   mygame.py            - Pygame code
   setup.py             - Install script

To make the Activity class, start with test/TestActivity.py from the Sugargame 
distribution.  

The activity should create a single PygameCanvas widget and call run_pygame on it.  
Pass the main loop function of the Pygame program.

 self._canvas = sugargame.canvas.PygameCanvas(self)
 self.set_canvas(self._canvas)
        
 # Start the game running.
 self._canvas.run_pygame(self.game.run)

In your Pygame main loop, pump the GTK message loop:

   while gtk.events_pending():
       gtk.main_iteration()

==== Adding Pygame to a PyGTK activity ====

To add Pygame to an existing Sugar activity, create a PygameCanvas widget and call 
run_pygame on it.  

 widget = sugargame.canvas.PygameCanvas(self)
 vbox.pack_start(widget)
 
 widget.run_pygame(self.game.run)

Due to limitations of Pygame and SDL, there can only be one PygameCanvas in the 
entire activity.

The argument to run_pygame is a function structured like a Pygame program.  In the 
main loop, remember to dispatch GTK messages using gtk.main_iteration().

 def main_loop():
        clock = pygame.time.Clock()
        screen = pygame.display.get_surface()
 
        while self.running:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()
 
            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
 
            # Check the mouse position
            x, y = pygame.mouse.get_pos()
  
            # Clear Display
            screen.fill((255,255,255)) #255 for white
 
            # Draw stuff here
            .................
 
            # Flip Display
            pygame.display.flip()  
             
            # Try to stay at 30 FPS
            self.clock.tick(30)

== Support ==

For help with Sugargame, please email the Sugar Labs development list:

: sugar-devel@lists.sugarlabs.org

Sugargame is developed by Wade Brainerd <wadetb@gmail.com>.  

It is loosely based on the source code to the olpcgames framework, developed by 
the One Laptop Per Child project.

=== Changelog ===

====v1.1====
* Fix bugs in event handling.  (Pablo Moleri)
* Remove reference to gtk.Socket.get_window() method, which is missing in older versions of PyGTK.

====v1.0====
* Initial version of Sugargame
