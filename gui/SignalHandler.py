import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SignalHandler:
    def __init__(self, builder):
        self.builder = builder

    def delete_window(self, *args):
        Gtk.main_quit(*args)

    def generate(self, _):
        bssid = self.builder.get_object('bssid').get_text()
        essid = self.builder.get_object('essid').get_text()
        serial = self.builder.get_object('serial').get_text()

        if not bssid:
            self.builder.get_object("bssid_error_popover").show_all()
        else:
            self.builder.get_object("bssid_error_popover").hide()
            from netaddr import EUI
            from actions import generate

            pins, error_code = generate.go(EUI(bssid), essid, serial, [], [], [], [])

            pins_expander = self.builder.get_object("pins_expander")
            pins_buffer = self.builder.get_object("pins_buffer")
            pins_buffer.set_text(', '.join(pins))
            pins_expander.set_sensitive(True)
            pins_expander.set_expanded(True)
