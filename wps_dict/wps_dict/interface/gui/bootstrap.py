import gi

from os.path import dirname, abspath

from .SignalHandler import *
from ...providers.online.downloadable.list import online_downloadable_providers
from ...providers.online.queryable.list import online_queryable_providers
from ...providers.offline.list import offline_providers
from ...tools.list import tools

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def _set_treeview_row(_, cell, *__):
    inconsistent = cell.get_property('inconsistent')
    enabled = cell.get_property('active')
    cell.set_property('inconsistent', inconsistent)
    cell.set_active(enabled)


def _get_column(builder, are_tools=False):
    column = Gtk.TreeViewColumn()

    name = Gtk.CellRendererText()
    enabled = Gtk.CellRendererToggle()

    if are_tools:
        enabled.connect("toggled", SignalHandler(builder).on_cell_toggled_tools)
    else:
        enabled.connect("toggled", SignalHandler(builder).on_cell_toggled_providers)

    column.pack_start(name, True)
    column.pack_start(enabled, True)

    column.add_attribute(name, "text", 0)
    column.add_attribute(enabled, "active", 1)

    if not are_tools:
        column.add_attribute(enabled, "inconsistent", 2)
        column.set_cell_data_func(enabled, _set_treeview_row)

    return column


def generate_provider_tree(builder):
    providers_list = builder.get_object("providers_list")

    item_offline_providers = providers_list.append(None, ['Offline providers', True, False])
    item_online_providers = providers_list.append(None, ['Online providers', True, False])
    item_online_downloadable_providers = providers_list.append(item_online_providers,
                                                               ['Downloadable providers', True, False])
    item_online_queryable_providers = providers_list.append(item_online_providers, ['Queryable providers', True, False])
    for offline_provider in offline_providers.keys():
        providers_list.append(item_offline_providers, [offline_provider, True, False])
    for online_provider in online_queryable_providers.keys():
        providers_list.append(item_online_queryable_providers, [online_provider, True, False])
    for online_downloadable_provider in online_downloadable_providers.keys():
        providers_list.append(item_online_downloadable_providers, [online_downloadable_provider, True, False])

    builder.get_object("providers_tree_view").get_selection().set_mode(Gtk.SelectionMode.NONE)
    builder.get_object("providers_tree_view").append_column(_get_column(builder))


def generate_tool_tree(builder):
    tools_list = builder.get_object("tools_list")
    for tool in tools.keys():
        tools_list.append([tool, True, False])

    builder.get_object("tools_tree_view").append_column(_get_column(builder, True))
    builder.get_object("tools_tree_view").get_selection().set_mode(Gtk.SelectionMode.NONE)


def init():
    builder = Gtk.Builder()
    builder.add_from_file(dirname(abspath(__file__)) + "/ui.glade")
    builder.connect_signals(SignalHandler(builder))
    window = builder.get_object("main_window")
    generate_provider_tree(builder)
    generate_tool_tree(builder)
    window.show_all()
    Gtk.main()
