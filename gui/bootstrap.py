import gi
from os.path import dirname, abspath
from .SignalHandler import *
from providers.offline.core.helper import *
from providers.online.core.helper import *
from providers.online.downloadable.core.helper import *
from tools.core.helper import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def _get_column():
    column = Gtk.TreeViewColumn()

    name = Gtk.CellRendererText()
    enabled = Gtk.CellRendererToggle()

    column.pack_start(name, True)
    column.pack_start(enabled, True)

    column.add_attribute(name, "text", 0)
    column.add_attribute(enabled, "active", 1)

    return column


def generate_provider_tree(builder):
    lista = builder.get_object("providers_list")

    item_offline_providers = lista.append(None, ['Offline providers', True])
    item_online_providers = lista.append(None, ['Online providers', True])
    item_online_downloadable_providers = lista.append(item_online_providers, ['Downloadable providers', True])
    item_online_queryable_providers = lista.append(item_online_providers, ['Queryable providers', True])
    for offline_provider in offline_providers.keys():
        lista.append(item_offline_providers, [offline_provider, True])
    for online_provider in online_providers.keys():
        lista.append(item_online_queryable_providers, [online_provider, True])
    for online_downloadable_provider in online_downloadable_providers.keys():
        lista.append(item_online_downloadable_providers, [online_downloadable_provider, True])

    builder.get_object("providers_tree_view").append_column(_get_column())


def generate_tool_tree(builder):
    lista = builder.get_object("tools_list")
    for tool in tools.keys():
        lista.append([tool, True])

    builder.get_object("tools_tree_view").append_column(_get_column())


def init():
    builder = Gtk.Builder()
    builder.add_from_file(dirname(abspath(__file__)) + "/ui.glade")
    builder.connect_signals(SignalHandler(builder))
    window = builder.get_object("main_window")
    generate_provider_tree(builder)
    generate_tool_tree(builder)
    window.show_all()
    Gtk.main()
