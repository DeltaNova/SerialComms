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
from gi.repository import Gtk, Gio, Pango, Gdk, GObject
import re
import serial
from serial.tools import list_ports
import sys

"""
TODO:
    - Need to limit the textbuffer. Overtime this will get very long with a
      significant ammount of text input/output. Although the theoretical limit
      is the available system RAM, the program should not be allowed to use too
      much. A MB or a few thousand lines should be more than enough.
"""

class MyWindow(Gtk.Window):
    """Application Window"""
    def __init__(self):
        Gtk.Window.__init__(self, title="Sercom_Gtk")
        self.set_border_width(0)
        self.set_default_size(600, 400)
        self.textmode = 1 # 0 = HEX, 1 = ASCII

        self.hex_regex = re.compile(r'[a-fA-F0-9]', re.I | re.S)

        header,button,self.set_menu = self.header()
        self.button2, self.button3, self.button4, self.button5 = self.buttons()

        baud_label = Gtk.Label("baud")
        port_label = Gtk.Label("port")

        self.entry = Gtk.Entry()
        #DEBUG - self.entry_change
        self.entry.connect("changed", self.on_entry_change)

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


        style_provider = Gtk.CssProvider()
        css = """
        GtkEntry.invalid {
            color: white;
            background: red;
        }
        """
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
        style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        """
        Get a list of available ports and select the first one. This is to
        prevent an Exception Error when a hardcoded USB port doesnt exist.
        """
        # TODO: Tidy this up into a function with exception handling.
        ports = self.get_ports()
        default_port = ports[0]
        default_baud = 9600
        sport = SerialPort(default_port, default_baud)
        self.ser = sport.ser
        port_label.set_text(default_port)
        baud_label.set_text(str(default_baud))

        # Auto Update
        # self.update_terminal needs to return True else it only executes once.
        GObject.timeout_add(100, self.update_terminal)

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

        button = Gtk.MenuButton()
        icon = Gio.ThemedIcon(name="emblem-system-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)

        button.connect("clicked", self.on_click_settings_menu)
        set_menu = Gtk.Menu()
        set_menu.popup(None, button, None, None, 0, Gtk.get_current_event_time())

        # Get a list of the ports on the system. Use to create toggle buttons.
        ports = self.get_ports()
        number_ports = len(ports)
        """
        # Attempt 1
        count = 0
        while count < number_ports:
            for port in ports:
                print("Print port: " + port)
                print("Print number_ports: " + str(number_ports))
                if count == 0:
                    btn = Gtk.RadioMenuItem.new_with_label(None, port)
                    btn.connect("toggled", self.on_port_toggled, number_ports)
                    set_menu.append(btn)
                else:
                    btn2 = Gtk.RadioMenuItem.new_with_label_from_widget(btn, port)
                    btn2.connect("toggled", self.on_port_toggled, number_ports)
                    set_menu.append(btn2)
                number_ports = number_ports + 1
        """
        # Attempt 2

        group = None
        # Create a list to hold the button references
        item_list = []
        # Create several buttons and store them in the list
        for number in range(0,number_ports):
            #item = Gtk.MenuItem("Test: " + str(number))
            #item = Gtk.RadioMenuItem(label ="This is an example")
            #group = Gtk.RadioMenuItem.get_group(Gtk.RadioMenuItem(item))
            #if (number == 0):
            #    Gtk.CheckMenuItem.set_active(Gtk.CheckMenuItem(item))

            if (number == 0):
                #item = Gtk.RadioMenuItem(label = ("Port: " + str(number)))
                item = Gtk.RadioMenuItem(label = (ports[number]))

            else:
                group = item_list[0]
                #item = Gtk.RadioMenuItem(group = group, label = "Example")
                #item = Gtk.RadioMenuItem.new_with_label_from_widget(item_list[0], ("Port: " + str(number)))
                item = Gtk.RadioMenuItem.new_with_label_from_widget(item_list[0], (ports[number]))

            item_list.append(item)
            #Gtk.CheckMenuItem.set_active(Gtk.CheckMenuItem(item_list[0]))

        # DEBUG - Calculate and Print number of items
        #num_items = len(item_list)
        #print("Number of Items: " + str(num_items))

        # Add the buttons to the existing menu
        x = 0
        for the_item in item_list:
            the_item.connect("toggled", self.on_port_toggled, x)
            set_menu.append(the_item)
            x = x + 1
        item_list[0].set_active(1)

        # Reference on the the new buttons and change the label
        #item_list[3].set_label("Something New")
        # End Attempt 2

        # Hardcoded Reference
        """
        i1 = Gtk.MenuItem("First")
        i2 = Gtk.MenuItem("Second")
        i3 = Gtk.MenuItem("Third")
        i4 = Gtk.MenuItem("This is a longer string")
        i5 = Gtk.MenuItem("This is a much much longer string of text")
        set_menu.append(i1)
        set_menu.append(i2)
        set_menu.append(i3)
        set_menu.append(i4)
        set_menu.append(i5)
        """
        button.set_popup(set_menu)
        headerbar.pack_end(button)
        return headerbar,button,set_menu

    def on_port_toggled(self, button, data):
        print("Port Toggled: " + str(data))
        if button.get_active() == 1:
            print("Active Button: " + str(data))

        return

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

    def on_click_settings_menu(self, button):
        """Access Settings Options"""
        self.set_menu.show_all()
        #DEBUG - Settings Menu Button Clicked
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


    def on_textview_change(self, *args):
        """
        Processes Changes in the TextEntry Box
        Scrolls the window vertically
        """
        adj = self.scrolledwindow.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
        #DEBUG - TextEntry Change
        #print(args)
        print("TextView Change ")

    def on_button_toggled(self, button, name):
        """Indicates Text Entry Type"""
        if name == 4:
            if button.get_active() == 1:
                print("ASCII Mode")
                self.textmode = 1
                #DEBUG - Print textmode
                print(self.textmode)
        elif name == 5:
            if button.get_active() == 1:
                print("HEX Mode")
                self.textmode = 0
                #DEBUG - Print textmode
                print(self.textmode)
        else:
            print("ERROR: This mode should not be selectable")
            print(name)
            print(button.get_active())

    def on_entry_change(self, entry):
        """
        Process Changes In Entry Field
        - Check for valid HEX or ASCII Chars
        """
        #TODO - Validate Entered Text
        #self.textmode indicates HEX/ASCII to validate
        if self.textmode == 1:
            # ASCII Mode
            self.validate_ascii()
        elif self.textmode == 0:
            # Hex Mode
            self.validate_hex(entry)
        else:
            print("Invalid Mode Selected")

        #DEBUG - TextEntry Change
        print("Text Entry Change")

    def validate_ascii(self):
        """
        Check to see if text is valid ASCII
        """
        print("Validating ASCII")

    def validate_hex(self, entry):
        """
        Check to see if text is valid HEX
        """
        print("Validating HEX")
        valid = 0 #Set to 1 for invalid text
        ctx = entry.get_style_context()
        ctx.remove_class('invalid')

        text = self.entry.get_text()
        for txt in text:
            if bool(self.hex_regex.match(txt)):
                print(txt + " is valid")
            else:
                print(txt + " is invalid")
                valid = 1

        if valid == 1:
            ctx.add_class('invalid')
            #TDOD - Disable Send Button

    def update_terminal(self):
        """
        Update the textview showing terminal data
        """
        while self.ser.inWaiting() > 0:
            #DEBUG - Print Serial Readline
            data = self.ser.readline().rstrip()
            print(data)
            textdata = (data + '\r')
            self.textview.get_buffer().insert_at_cursor(textdata)
        #print("Updating")
        # Needs to return True else GObject.timeout handler only calls once.
        return True

    def get_ports(self):
        """Obtain a list of the available Serial Ports"""
        port_list_data = serial.tools.list_ports.comports()
        port_list = []
        for port in port_list_data:
            """
            port information is a list [portname, description, hardwareID]
            If hardwareID = 'n/a' then class it as unusable.
            """
            if port[2] != 'n/a':
                port_list.append(port[0])
        if len(port_list) == 0:
            sys.exit("No Available Serial Ports - Application Exiting")

        # DEBUG - Print port_list
        print(str(port_list))
        return port_list

class SerialPort():
    """The Serial Communications Port"""
    def __init__(self, port, baud=9600):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(self.port, self.baud)



if __name__ == "__main__":
    WIN = MyWindow()
    WIN.set_name('MyWindow')
    WIN.connect("delete-event", Gtk.main_quit)
    WIN.show_all()

    Gtk.main()
