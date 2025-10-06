from .base_table import BaseTable
from .event_emitter import EventEmitter

class PluginTable(BaseTable, EventEmitter):
    def __init__(self, parent, initial_data=[], *args, **kwargs):
        EventEmitter.__init__(self)        
        BaseTable.__init__(self, parent, initial_data, *args, **kwargs)
        self.plugins = []
        self.refresh()

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
        plugin.set_table(self)
        plugin.run()
        return plugin
    
    def create_widgets(self):
        super().create_widgets()
        self.emit("widgets_created")

    def refresh(self):
        super().refresh()
        self.emit("table_refreshed")

    def add_row(self, index=None, new_row=None):
        super().add_row(index, new_row)
        self.emit("row_added", index=index, row=new_row)

    def remove_row(self, index):
        super().remove_row(index)
        self.emit("row_removed", index=index)

    def edit_cell(self, row_id, column_name, new_value):
        super().edit_cell(row_id, column_name, new_value)
        self.emit("cell_edited", row_id=row_id, column=column_name, new_value=new_value)

    def set_columns(self, new_columns):
        super().set_columns(new_columns)
        self.emit("columns_updated", columns=new_columns)

    def set_data(self, data):
        super().set_data(data)
        self.emit("data_setted", data=data)