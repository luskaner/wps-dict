#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def generate(_):
    pins_expander = builder.get_object("pins_expander")
    pins_buffer = builder.get_object("pins_buffer")
    error_popover = builder.get_object("bssid_error_popover")
    pins_buffer.set_text("12345670 12346789")
    pins_expander.set_sensitive(True)
    pins_expander.set_expanded(True)   
    error_popover.show_all()   

builder = Gtk.Builder()
builder.add_from_file("gui/ui.glade")

handlers = {
    "generate": generate
}
builder.connect_signals(handlers)

window = builder.get_object("main_window")
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
