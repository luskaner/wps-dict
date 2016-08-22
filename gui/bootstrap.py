import gi
from os.path import dirname, abspath
from .SignalHandler import *
from providers.offline.core.helper import *
from providers.online.core.helper import *
from providers.online.downloadable.core.helper import *
from tools.core.helper import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def _get_column(builder, tools=False):
    column = Gtk.TreeViewColumn()

    name = Gtk.CellRendererText()
    enabled = Gtk.CellRendererToggle()
    if tools:
        enabled.connect("toggled", SignalHandler(builder).on_cell_toggled_tools)
    else:
        enabled.connect("toggled", SignalHandler(builder).on_cell_toggled_providers)

    column.pack_start(name, True)
    column.pack_start(enabled, True)

    column.add_attribute(name, "text", 0)
    column.add_attribute(enabled, "active", 1)


    return column


def generate_provider_tree(builder):
    providers_list = builder.get_object("providers_list")

    item_offline_providers = providers_list.append(None, ['Offline providers', True])
    item_online_providers = providers_list.append(None, ['Online providers', True])
    item_online_downloadable_providers = providers_list.append(item_online_providers, ['Downloadable providers', True])
    item_online_queryable_providers = providers_list.append(item_online_providers, ['Queryable providers', True])
    for offline_provider in offline_providers.keys():
        providers_list.append(item_offline_providers, [offline_provider, True])
    for online_provider in online_providers.keys():
        providers_list.append(item_online_queryable_providers, [online_provider, True])
    for online_downloadable_provider in online_downloadable_providers.keys():
        providers_list.append(item_online_downloadable_providers, [online_downloadable_provider, True])

    builder.get_object("providers_tree_view").get_selection().set_mode(Gtk.SelectionMode.NONE)
    builder.get_object("providers_tree_view").append_column(_get_column(builder))


def generate_tool_tree(builder):
    tools_list = builder.get_object("tools_list")
    for tool in tools.keys():
        tools_list.append([tool, True])

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
