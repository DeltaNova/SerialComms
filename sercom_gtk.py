#!/usr/bin/env python
"""
sercom_gtk.py - GTK Application for serial communications

"""
from gi.repository import Gtk,Gio

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Sercom_Gtk")
        self.set_border_width(0)
        self.set_default_size(400,200)

        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "Sercom_Gtk"
        self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="emblem-system-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)

        self.add(Gtk.TextView())

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
