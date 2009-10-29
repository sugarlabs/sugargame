== Sugargame ==

Sugargame allows Pygame programs to run well under Sugar. It is fork of the 
olcpgames framework, which is no longer maintained.

Sugargame embeds the Pygame window into a GTK window, and translates GTK 
events to Pygame events.

What it does:

 * Wraps a Sugar activity around an existing Pygame program with few changes
 * Allows Sugar toolbars and other widgets to be added to the activity UI
 * Provides hooks for saving to and restoring from the Journal

Advantages vs olpcgames:

 * Simpler code
 * More elegant interface between Pygame and GTK
 * Runs as a single thread: no thread related segfaults

 == Using Sugargame ==
 
To use Sugargame in an activity, copy the sugargame folder into the activity's 
source directory.
 
The activity directory should look something like this:
 
   activity/            - Activity directory: activity.info, SVG icon, etc.
   sugargame/           - Sugargame package
   MyActivity.py        - Activity class
   mygame.py            - Pygame code
   setup.py             - Install script
   
To make the Activity class, start with test/TestActivity.py.  

== Support ==

For help with Sugargame, please email the Sugar Labs development list:

  sugar-devel@lists.sugarlabs.org

== Author ==

Sugargame is developed by Wade Brainerd <wadetb@gmail.com>.  
It is loosely based on the source code to the olpcgames framework, developed by 
the One Laptop Per Child project.
