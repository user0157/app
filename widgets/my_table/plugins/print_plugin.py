from .base_plugin import BasePlugin

class PrintPlugin(BasePlugin):
    def run(self):
        self.table.on("row_added", self.print_row_added)
        self.table.on("row_removed", self.print_row_removed)
        self.table.on("cell_edited", self.print_cell_edited)

    def print_row_added(self, index, row):
        print(f"Row added at index {index}: {row}")

    def print_row_removed(self, index):
        print(f"Row removed from index {index}")

    def print_cell_edited(self, index, column, new_value):
        print(f"Cell edited at index {index}, column '{column}': {new_value}")
