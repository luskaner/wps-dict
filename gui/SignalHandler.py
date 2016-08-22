import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SignalHandler:
    def __init__(self, builder):
        self.builder = builder

    def delete_window(self, *args):
        Gtk.main_quit(*args)

    def update_db(self, *args):
        from actions import update_db
        update_db.go([], [])

    def tools_auto_switch_change(self, _, activated):
        self.builder.get_object('tools_revealer').set_reveal_child(not activated)

    def update_task_switcher_buttons(self, *args):
        stack_page = args[0].get_visible_child_name()

        if stack_page == 'dictionary_page':
            self.builder.get_object('generate_button').set_visible(True)
        else:
            self.builder.get_object('generate_button').set_visible(False)

        if stack_page == 'providers_page':
            self.builder.get_object('update_button').set_visible(True)
        else:
            self.builder.get_object('update_button').set_visible(False)

    def generate(self, _):
        bssid = self.builder.get_object('bssid').get_text()
        essid = self.builder.get_object('essid').get_text()
        serial = self.builder.get_object('serial').get_text()

        if not bssid:
            self.builder.get_object("bssid_format_error_popover").hide()
            self.builder.get_object("bssid_required_error_popover").show_all()
        else:
            self.builder.get_object("bssid_required_error_popover").hide()
            from helpers.mac import mac
            bssid_mac = mac(bssid)
            if bssid_mac:
                self.builder.get_object("bssid_format_error_popover").hide()
                pins_buffer = self.builder.get_object("pins_buffer")
                from actions import generate
                pins, error_code = generate.go(bssid_mac, essid, serial, [], [], [], [])
                pins_buffer.set_text(', '.join(pins))
                self.builder.get_object("pins_revealer").set_reveal_child(True)
            else:
                self.builder.get_object("bssid_format_error_popover").show_all()
