import tkinter as tk
from dict_processor import DictProcessor
from my_table import Mytable
from plugins.filter_plugin import FilterPlugin
from plugins.sort_plugin import SortPlugin
from plugins.style_plugin import StylePlugin
from plugins.edit_plugin import EditPlugin
from plugins.cell_plugin import CellPlugin

if __name__ == "__main__":
    root = tk.Tk()
    initial_data = [
        {"id": 1, "name": "Item 1", "value": 10},
        {"id": 2, "name": "Item 2", "value": 20},
        {"id": 3, "name": "Item 3", "value": 30}
    ]

    processor = DictProcessor(
        default_value=''
    )

    data = processor(initial_data)
    print("Processed Data:", data)
    
    table = Mytable(root, data)
    table.pack(expand=True, fill='both')

    table.register_plugin(FilterPlugin())
    table.register_plugin(SortPlugin())
    table.register_plugin(StylePlugin())
    table.register_plugin(EditPlugin(["id", "value"]))
    table.register_plugin(CellPlugin())

    def print_data():
        for item in table.data:
            print(item)

    print_button = tk.Button(root, text="Print Data", command=print_data)
    print_button.pack(pady=10)
    root.mainloop()
