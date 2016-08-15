import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file("ui.glade")
window = builder.get_object("main_window")
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
