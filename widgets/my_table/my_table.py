from .plugin_table import PluginTable
from .plugins.filter_plugin import FilterPlugin
from .plugins.sort_plugin import SortPlugin
from .plugins.style_plugin import StylePlugin
from .plugins.edit_plugin import EditPlugin
from .plugins.cell_plugin import CellPlugin

class Mytable(PluginTable):
    def __init__(self, parent, initial_data=[], *args, **kwargs): 
        super().__init__(parent, initial_data, *args, **kwargs)
        self.register_plugin(FilterPlugin())
        self.register_plugin(SortPlugin())
        self.register_plugin(StylePlugin())
        self.edit_plugin = self.register_plugin(EditPlugin())
        self.register_plugin(CellPlugin())

    def set_editable_columns(self, editable_columns):
        self.edit_plugin.set_editable_columns(editable_columns)