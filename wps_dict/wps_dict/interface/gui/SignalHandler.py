import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SignalHandler:
    def __init__(self, builder):
        self.builder = builder

    def delete_window(self, *args):
        Gtk.main_quit(*args)

    def update_db(self, *args):
        from ...actions.base import update_db
        included, excluded = self._get_providers_included_excluded()
        update_db.go(included, excluded)

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

    def _get_tools_included_excluded(self):
        if self.builder.get_object("providers_auto").get_active():
            return ['auto'], ['auto']
        else:
            tools_list_str = []
            tools_list = self.builder.get_object("tools_list")
            for tool_row in tools_list:
                if tool_row[1]:
                    tools_list_str.append(tool_row[0])
            return tools_list_str, ['auto']

    def on_cell_toggled_tools(self, _, index):
        tools_list = self.builder.get_object("tools_list")
        tools_list[index][1] = not tools_list[index][1]

    def _update_toggle(self, row):
        children = row.iterchildren()
        if children:
            children_total = 0
            children_on = 0
            for child in children:
                if child[1]:
                    children_on += 1
                children_total += 1
            if children_on == 0:
                row[1] = False
                row[2] = False
            elif children_on == children_total:
                row[1] = True
                row[2] = False
            else:
                row[1] = False
                row[2] = True
        parent = row.parent
        if parent:
            self._update_toggle(parent)

    def _update_toggle_children(self, row):
        children = row.iterchildren()
        active = row[1]

        for child in children:
            child[1] = active
            children_of_child = child.iterchildren()
            if children_of_child:
                self._update_toggle_children(child)

    def on_cell_toggled_providers(self, item, index):
        providers_list = self.builder.get_object("providers_list")
        node_toggled = providers_list[index]
        node_toggled[1] = not node_toggled[1]
        parent = node_toggled.parent
        if parent:
            self._update_toggle(parent)
        children = node_toggled.iterchildren()
        if children:
            self._update_toggle_children(node_toggled)

    def _get_providers(self, store, treeiter):
        orphan_children = []
        while treeiter:
            if not store.iter_has_child(treeiter):
                if store[treeiter][1]:
                    orphan_children.append(store[treeiter][0])
            else:
                orphan_children.extend(self._get_providers(store, store.iter_children(treeiter)))
            treeiter = store.iter_next(treeiter)
        return orphan_children

    def _get_providers_included_excluded(self):
        store = self.builder.get_object("providers_list")
        return self._get_providers(store, store.get_iter_first()), ['none']

    def generate(self, _):
        bssid = self.builder.get_object('bssid').get_text()
        essid = self.builder.get_object('essid').get_text()
        serial = self.builder.get_object('serial').get_text()

        if not bssid:
            self.builder.get_object("bssid_format_error_popover").hide()
            self.builder.get_object("bssid").get_style_context().remove_class('error')
            self.builder.get_object("bssid").get_style_context().add_class('warning')
            self.builder.get_object("bssid_required_error_popover").show_all()
        else:
            self.builder.get_object("bssid").get_style_context().remove_class('warning')
            self.builder.get_object("bssid_required_error_popover").hide()
            from ...helpers.mac import mac
            bssid_mac = mac(bssid)
            if bssid_mac:
                self.builder.get_object("bssid_format_error_popover").hide()
                self.builder.get_object("bssid").get_style_context().remove_class('error')
                tools_list_included_str, tools_list_excluded_str = self._get_tools_included_excluded()
                providers_list_included_str, providers_list_excluded_str = self._get_providers_included_excluded()
                pins_buffer = self.builder.get_object("pins_buffer")
                from ...actions.base import generate
                pins, error_code = generate.go(bssid_mac, essid, serial, tools_list_included_str,
                                               tools_list_excluded_str, providers_list_included_str,
                                               providers_list_excluded_str)
                if not pins:
                    pins_buffer.set_text('No pins')
                else:
                    pins_buffer.set_text(', '.join(pins))
                self.builder.get_object("pins_revealer").set_reveal_child(True)
            else:
                self.builder.get_object("bssid").get_style_context().add_class('error')
                self.builder.get_object("bssid_format_error_popover").show_all()
