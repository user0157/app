import tkinter as tk
from .base_plugin import BasePlugin

class SortPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.sort_order = {}

    def run(self):
        self.tree.bind("<Button-1>", self.on_header_click)

    def reset_sort_order(self, *args):
        self.sort_order = {}

    def on_header_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            col_id = self.tree.identify_column(event.x)
            col_index = int(col_id.replace("#", "")) - 1

            columns = self.tree["columns"]
            if col_index >= len(columns):
                print("Índice de coluna inválido.")
                return

            column = columns[col_index]
            self.toggle_sort(column)

    def toggle_sort(self, column):
        if column in self.sort_order:
            self.sort_order[column] *= -1
        else:
            self.sort_order = {column: 1}

        reverse = self.sort_order[column] < 0

        def convert_for_sort(val):
            raw = val.get(column)
            if raw is None:
                return (2, "")  # Valores ausentes ficam no final
            try:
                return (0, float(raw))  # Tenta converter para número
            except (ValueError, TypeError):
                return (1, str(raw))  # Se falhar, usa como string

        self.data.sort(key=convert_for_sort, reverse=reverse)
        self.table.refresh()

