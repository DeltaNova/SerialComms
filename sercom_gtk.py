#!/usr/bin/env python
"""
sercom_gtk.py - GTK Application for serial communications

"""
from gi.repository import Gtk,Gio

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Sercom_Gtk")
        self.set_border_width(0)
        self.set_default_size(500,400)

        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "Sercom_Gtk"
        self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="emblem-system-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.connect("clicked", self.on_click_settings)
        hb.pack_end(button)

        button2 = Gtk.Button("Send")
        button2.connect("clicked", self.on_click_send)
        button3 = Gtk.Button("Clear")
        button3.connect("clicked", self.on_click_clear)

        baud_label = Gtk.Label("baud")
        port_label = Gtk.Label("port")


        button4 = Gtk.RadioButton.new_from_widget(None)
        button5 = Gtk.RadioButton.new_from_widget(button4)
        button4.set_label("ASCII")
        button5.set_label("HEX")
        button4.connect("toggled", self.on_button_toggled, "1")
        button5.connect("toggled", self.on_button_toggled, "2")

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        stack.set_transition_duration(500)
        stack.set_hexpand(True)

        self.entry = Gtk.Entry()
        self.entry.connect("changed", self.on_entry_change)
        #self.entry.set_text("Enter ASCII Text")
        #stack.add_titled(self.entry, "entryA","ASCII")

        #self.entry2 = Gtk.Entry()
        #self.entry2.connect("changed", self.on_hex_change)
        #self.entry2.set_text("Enter HEX String")
        #stack.add_titled(self.entry2, "entryH", "HEX")

        #stack_switcher = Gtk.StackSwitcher()
        #stack_switcher.set_stack(stack)

        self.vbox = Gtk.VBox(0,1)
        self.add(self.vbox)

        hbox = Gtk.HBox(0,1)
        hbox2 = Gtk.HBox(0,1)
        tv = Gtk.TextView()

        self.vbox.pack_start(tv,1,1,0)
        self.vbox.pack_start(hbox2,0,0,0)
        self.vbox.pack_start(hbox,0,0,1)
        #hbox2.pack_start(stack,1,1,0)
        hbox2.pack_start(self.entry,1,1,0)
        #hbox.pack_start(stack_switcher,1,1,0)
        hbox.pack_start(button4,0,0,0)
        hbox.pack_start(button5,0,0,0)
        hbox.pack_start(baud_label,1,1,0)
        hbox.pack_start(port_label,1,1,0)
        hbox.pack_start(button3,0,0,10)
        hbox.pack_start(button2,0,0,0)

    def on_click_settings(self, button):
        print("Settings Button Clicked")
    def on_click_send(self, button):
        print("Send Button Clicked")
    def on_click_clear(self, button):
        print("Clear Button Clicked")
    def on_entry_change(self, entry):
        print("Text Entry Change")
    def on_hex_change(self, entry):
        print("Hex Change")
    def on_button_toggled(self, button, name):
        if button.get_active():
            state="on"
        else:
            state="off"
        print("Button", name, "was turned", state)


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
