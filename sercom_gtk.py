#!/usr/bin/env python
"""
sercom_gtk.py - GTK Application for serial communications

"""
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Sercom_Gtk")

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
