import tkinter as tk
from .base_plugin import BasePlugin
from typing import Dict, List, Optional, Union
import types

class EditPlugin(BasePlugin):
    def __init__(self, editable_columns: Optional[Union[List[str], Dict[str, bool]]] = None):
        super().__init__()
        self.editable_columns = editable_columns
        self.entry = None
        self.current_cell = None
        self._entry_update_scheduled = False
        
    def run(self):
        self.tree.bind("<Double-1>", self.edit_cell)
        self.tree.bind("<<TreeviewSelect>>", self._on_scroll)
        self.tree.bind("<MouseWheel>", self._on_scroll)
        self.tree.bind("<Button-4>", self._on_scroll)
        self.tree.bind("<Button-5>", self._on_scroll)
        self.tree.bind("<Configure>", self._on_scroll)
        
        vsb = self.tree.master.winfo_children()
        for child in vsb:
            if isinstance(child, tk.Scrollbar):
                child.bind("<B1-Motion>", self._on_scroll)
                child.bind("<ButtonRelease-1>", self._on_scroll)

    def is_column_editable(self, column_key: str, column_index: int) -> bool:
        if self.editable_columns is None:
            return True
        
        if isinstance(self.editable_columns, list):
            return column_key in self.editable_columns
        
        if isinstance(self.editable_columns, dict):
            return self.editable_columns.get(column_key, False)

        return False

    def _on_scroll(self, *args):
        self._schedule_entry_update()

    def _schedule_entry_update(self):
        if not self._entry_update_scheduled:
            self._entry_update_scheduled = True
            self.table.after(10, self._update_entry_position)

    def _update_entry_position(self):
        self._entry_update_scheduled = False
        if self.entry and self.entry.winfo_exists() and self.current_cell:
            row_id, col_index = self.current_cell
            bbox = self.tree.bbox(row_id, f"#{col_index + 1}")
            if bbox:
                x, y, width, height = bbox
                tree_bbox = self.tree.bbox(row_id)
                if tree_bbox:
                    self.tree.see(row_id)
                    bbox = self.tree.bbox(row_id, f"#{col_index + 1}")
                    if bbox:
                        x, y, width, height = bbox
                        self.entry.place_configure(x=x, y=y, width=width, height=height)
                        self.entry.focus_set()
            else:
                self.entry.place_forget()

    def edit_cell(self, event=None, item_id=None, column_index=None):
        if event:
            region = self.tree.identify("region", event.x, event.y)
            if region != "cell":
                return
            column = self.tree.identify_column(event.x)
            item_id = self.tree.identify_row(event.y)
            if not item_id:
                return
            column_index = int(column.replace("#", "")) - 1

        if item_id is None or column_index is None:
            return

        column_key = self.columns[column_index]
        if not self.is_column_editable(column_key, column_index):
            return

        self.current_cell = (item_id, column_index)
        bbox = self.tree.bbox(item_id, f"#{column_index + 1}")
        if not bbox:
            return

        x, y, width, height = bbox
        value = self.tree.item(item_id)['values'][column_index]

        if self.entry:
            self.entry.destroy()
            self.entry = None

        self.entry = tk.Entry(self.tree)
        self.entry.place(x=x, y=y, width=width, height=height)
        self.entry.insert(0, value)
        self.entry.focus()
        self.entry.select_range(0, tk.END)

        def save_edit(event=None):
            if self.entry and self.table:
                new_value = self.entry.get()
                self.entry.destroy()
                self.entry = None            
                self.table.edit_cell(item_id, column_key, new_value)
                
        def cancel_edit(event=None):
            if self.entry:
                self.entry.destroy()
                self.entry = None

        def move_cell(event):
            save_edit()

            if not self.current_cell or not self.table:
                return

            children = self.tree.get_children()

            item_index = children.index(item_id)
            num_cols = len(self.table.columns)
            row = item_index
            col = column_index

            def find_next_editable_cell(start_row, start_col, direction):
                children = self.tree.get_children()

                if direction == "down":
                    for r in range(start_row + 1, len(children)):
                        col_key = self.columns[start_col]
                        if self.is_column_editable(col_key, start_col):
                            return r, start_col
                        
                    for r in range(start_row + 1, len(children)):
                        for c in range(num_cols):
                            col_key = self.columns[c]
                            if self.is_column_editable(col_key, c):
                                return r, c
                            
                    self.table.add_row()
                    children = self.tree.get_children()
                    col_key = self.columns[start_col]

                    if self.is_column_editable(col_key, start_col):
                        return len(children) - 1, start_col
                    
                    for c in range(num_cols):
                        col_key = self.columns[c]
                        if self.is_column_editable(col_key, c):
                            return len(children) - 1, c
                        
                    return start_row, start_col

                elif direction == "up":
                    for r in range(start_row - 1, -1, -1):
                        col_key = self.columns[start_col]
                        if self.is_column_editable(col_key, start_col):
                            return r, start_col
                        
                    for r in range(start_row - 1, -1, -1):
                        for c in range(num_cols):
                            col_key = self.columns[c]
                            if self.is_column_editable(col_key, c):
                                return r, c
                            
                    return start_row, start_col

                elif direction == "right":
                    for c in range(start_col + 1, num_cols):
                        col_key = self.columns[c]
                        if self.is_column_editable(col_key, c):
                            return start_row, c
                        
                    for r in range(start_row + 1, len(children)):
                        for c in range(num_cols):
                            col_key = self.columns[c]
                            if self.is_column_editable(col_key, c):
                                return r, c
                            
                    self.table.add_row()
                    children = self.tree.get_children()
                    col_key = self.columns[start_col]

                    for c in range(num_cols):
                        col_key = self.columns[c]
                        if self.is_column_editable(col_key, c):
                            return len(children) - 1, c
                        
                    return start_row, start_col

                elif direction == "left":
                    for c in range(start_col - 1, -1, -1):
                        col_key = self.columns[c]
                        if self.is_column_editable(col_key, c):
                            return start_row, c
                        
                    for r in range(start_row - 1, -1, -1):
                        for c in range(num_cols - 1, -1, -1):
                            col_key = self.columns[c]
                            if self.is_column_editable(col_key, c):
                                return r, c
                            
                    return start_row, start_col

                return start_row, start_col

            if event.keysym == "Down":
                row, col = find_next_editable_cell(row, col, "down")
            elif event.keysym == "Up":
                row, col = find_next_editable_cell(row, col, "up")
            elif event.keysym == "Right":
                row, col = find_next_editable_cell(row, col, "right")
            elif event.keysym == "Left":
                row, col = find_next_editable_cell(row, col, "left")

            current_children = self.tree.get_children()

            if row < len(current_children):
                new_item_id = current_children[row]
                self.tree.see(new_item_id)
                self.edit_cell(item_id=new_item_id, column_index=col)     

        self.entry.bind("<Return>", save_edit)
        self.entry.bind("<FocusOut>", save_edit)
        self.entry.bind("<Escape>", cancel_edit)

        self.entry.bind("<Up>", move_cell)
        self.entry.bind("<Down>", move_cell)
        self.entry.bind("<Left>", move_cell)
        self.entry.bind("<Right>", move_cell)

        self.entry.bind("<Tab>", lambda e: move_cell(type('Event', (), {'keysym': 'Right'})()))
        self.entry.bind("<Shift-Tab>", lambda e: move_cell(type('Event', (), {'keysym': 'Left'})()))

    def on_refresh(self, *args):
        if self.entry:
            self.entry.destroy()
            self.entry = None
            self.current_cell = None

    def set_editable_columns(self, editable_columns: Union[List[str], Dict[str, bool]]):
        self.editable_columns = editable_columns
