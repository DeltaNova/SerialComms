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

        self.header()
        self.button2, self.button3, self.button4, self.button5 = self.buttons()

        baud_label = Gtk.Label("baud")
        port_label = Gtk.Label("port")

        self.entry = Gtk.Entry()
        #DEBUG - self.entry_change
        #self.entry.connect("changed", self.on_entry_change)

        hbox = Gtk.HBox(0, 1)
        hbox.pack_start(self.button4, 0, 0, 0)
        hbox.pack_start(self.button5, 0, 0, 0)
        hbox.pack_start(baud_label, 1, 1, 0)
        hbox.pack_start(port_label, 1, 1, 0)
        hbox.pack_start(self.button3, 0, 0, 10)
        hbox.pack_start(self.button2, 0, 0, 0)

        hbox2 = Gtk.HBox(0, 1)
        hbox2.pack_start(self.entry, 1, 1, 0)

        self.textview = self.set_textview()
        self.scrolledwindow = self.scroll_window()
        self.scrolledwindow.add(self.textview)
        self.vbox = Gtk.VBox(0, 1)
        self.add(self.vbox)
        self.vbox.pack_start(self.scrolledwindow, 1, 1, 0)
        self.vbox.pack_start(hbox2, 0, 0, 0)
        self.vbox.pack_start(hbox, 0, 0, 1)

    def buttons(self):
        """Create Window Buttons"""
        button2 = Gtk.Button("Send")
        button2.connect("clicked", self.on_click_send)
        button3 = Gtk.Button("Clear")
        button3.connect("clicked", self.on_click_clear)
        button4 = Gtk.RadioButton.new_from_widget(None)
        button5 = Gtk.RadioButton.new_from_widget(button4)
        button4.set_label("ASCII")
        button5.set_label("HEX")
        button4.connect("toggled", self.on_button_toggled, 4)
        button5.connect("toggled", self.on_button_toggled, 5)
        return button2, button3, button4, button5

    def header(self):
        """Setup the header bar"""
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
        return headerbar

    def scroll_window(self):
        """Create ScrolledWindow"""
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        return scrolledwindow

    def set_textview(self):
        """Setup the textview area"""
        textview = Gtk.TextView()
        textview.connect("size-allocate", self.on_textview_change)
        textview.set_wrap_mode(1)
        fontdesc = Pango.FontDescription("monospace")
        textview.modify_font(fontdesc)
        return textview

    def on_click_settings(self, button):
        """Access Settings Options"""
        print("Settings Button Clicked " + str(button))

    def on_click_send(self, button):
        """Send TextEntry Contents by toggled type"""
        textbuffer = self.textview.get_buffer()
        textbuffer.get_insert()
        entry_text = self.entry.get_text()
        textbuffer.insert_at_cursor(entry_text)
        #DEBUG - Send Button Clicked
        print("Send Button Clicked " + str(button))

    def on_click_clear(self, button):
        """Clears Contents of TextEntry"""
        self.entry.set_text("")
        #DEBUG - Clear Button Clicked
        print("Clear Button Clicked " + str(button))

    def on_textview_change(self, entry, *args):
        """
        Processes Changes in the TextEntry Box
        Scrolls the window vertically
        """
        adj = self.scrolledwindow.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
        #DEBUG - TextEntry Change
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
