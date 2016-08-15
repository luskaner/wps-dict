import gi
from os.path import dirname, abspath
from .SignalHandler import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def init():
    builder = Gtk.Builder()
    builder.add_from_file(dirname(abspath(__file__)) + "/ui.glade")
    builder.connect_signals(SignalHandler(builder))
    window = builder.get_object("main_window")
    window.show_all()
    Gtk.main()
