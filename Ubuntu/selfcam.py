#/usr/bin/env python
#        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#                  Version 2, December 2004 

# Copyright (C) 2013 Naing Ye` Minn <naingyeminn@gmail.com> 

# Everyone is permitted to copy and distribute verbatim or modified 
# copies of this license document, and changing it is allowed as long 
# as the name is changed. 

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

#  0. You just DO WHAT THE FUCK YOU WANT TO.

import sys, os, pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst


class SelfCam_Main():

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_decorated(False)
        window.set_title("SelfCam")
        # You can change Width and Height below
        window.set_default_size(400, 300)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        vbox = gtk.VBox()
        window.add(vbox)
        self.cam_view = gtk.DrawingArea()
        vbox.add(self.cam_view)

        window.show_all()

        self.player = gst.parse_launch("v4l2src ! autovideosink")

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('message', self.on_message)
        bus.connect('sync-message::element', self.on_sync_message)

        self.player.set_state(gst.STATE_PLAYING)


    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == 'prepare-xwindow-id':
            imagesink = message.src
            imagesink.set_property('force-aspect-ratio', True)
            imagesink.set_xwindow_id(self.cam_view.window.xid)


SelfCam_Main()
gtk.gdk.threads_init()
gtk.main()
