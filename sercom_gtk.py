#!/usr/bin/env python
# sercom_gtk.py - GTK Application for serial communications

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function
from gi.repository import Gtk, Gio, Pango

class MyWindow(Gtk.Window):
    """Application Window"""
    def __init__(self):
        Gtk.Window.__init__(self, title="Sercom_Gtk")
        self.set_border_width(0)
        self.set_default_size(500, 400)

        headerbar = Gtk.HeaderBar()
        headerbar.props.show_close_button = True
        headerbar.props.title = "Sercom_Gtk"
        self.set_titlebar(headerbar)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="emblem-system-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.connect("clicked", self.on_click_settings)
        headerbar.pack_end(button)

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
        button4.connect("toggled", self.on_button_toggled, 4)
        button5.connect("toggled", self.on_button_toggled, 5)

        self.entry = Gtk.Entry()
        self.entry.connect("changed", self.on_entry_change)

        self.vbox = Gtk.VBox(0, 1)
        self.add(self.vbox)

        hbox = Gtk.HBox(0, 1)
        hbox2 = Gtk.HBox(0, 1)

        textview = self.textview()

        self.vbox.pack_start(textview, 1, 1, 0)
        self.vbox.pack_start(hbox2, 0, 0, 0)
        self.vbox.pack_start(hbox, 0, 0, 1)

        hbox2.pack_start(self.entry, 1, 1, 0)

        hbox.pack_start(button4, 0, 0, 0)
        hbox.pack_start(button5, 0, 0, 0)
        hbox.pack_start(baud_label, 1, 1, 0)
        hbox.pack_start(port_label, 1, 1, 0)
        hbox.pack_start(button3, 0, 0, 10)
        hbox.pack_start(button2, 0, 0, 0)

    def textview(self):
        """Setup the textview area"""
        textview = Gtk.TextView()
        fontdesc = Pango.FontDescription("monospace")
        textview.modify_font(fontdesc)
        return textview

    def on_click_settings(self, button):
        """Access Settings Options"""
        print("Settings Button Clicked " + str(button))

    def on_click_send(self, button):
        """Send TextEntry Contents by toggled type"""
        print("Send Button Clicked " + str(button))

    def on_click_clear(self, button):
        """Clears Contents of TextEntry"""
        self.entry.set_text("")
        print("Clear Button Clicked " + str(button))

    def on_entry_change(self, entry):
        """Process Changes in the TextEntry Box"""
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.get_insert()
        self.textbuffer.insert("Change Text ")
        print("Text Entry Change " + str(entry))

    def on_button_toggled(self, button, name):
        """Indicates Text Entry Type"""
        if name == 4:
            if button.get_active() == 1:
                print("ASCII Mode")
        elif name == 5:
            if button.get_active() == 1:
                print("HEX Mode")
        else:
            print("ERROR: This mode should not be selectable")
            print(name)
            print(button.get_active())



WIN = MyWindow()
WIN.connect("delete-event", Gtk.main_quit)
WIN.show_all()
Gtk.main()
