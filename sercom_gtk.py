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

        button2 = Gtk.Button("Send")



        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        self.entry = Gtk.Entry()
        self.entry.set_text("Enter ASCII Text")
        stack.add_titled(self.entry, "entryA","ASCII")

        self.entry2 = Gtk.Entry()
        self.entry2.set_text("Enter HEX String")
        stack.add_titled(self.entry2, "entryH", "HEX")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        self.vbox = Gtk.VBox(0,1)
        self.add(self.vbox)

        hbox = Gtk.HBox(0,1)
        tv = Gtk.TextView()
        stbr = Gtk.Statusbar()
        self.vbox.pack_start(tv,1,1,0)
        self.vbox.pack_start(hbox,0,0,0)
        self.vbox.pack_start(stbr,0,0,0)

        hbox.pack_start(stack_switcher,1,1,0)
        hbox.pack_start(stack,1,1,0)
        hbox.pack_start(button2,0,0,0)







win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
