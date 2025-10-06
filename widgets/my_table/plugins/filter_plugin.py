import tkinter as tk
from .base_plugin import BasePlugin

class FilterPlugin(BasePlugin):
    def __init__(self):
        self.filters = {}
        self.menu_vars = {}

    def run(self):
        self.tree.bind("<Button-3>", self.open_menu, add=True)
        self.filters = self._generate_filters()
        self.table.on("table_refreshed", self.refresh_filters)

        self.table.on("data_setted", self._on_data_change)
        self.table.on("row_added", self._on_data_change)
        self.table.on("row_removed", self._on_data_change)
        self.table.on("cell_edited", self._on_data_change)

    def _on_data_change(self, **kwargs):
        # Quando os dados mudarem, remova todos os filtros
        self.clear_all_filters()
        self.regenerate_filters()

    def regenerate_filters(self):
        new_filters = self._generate_filters()
        merged_filters = {}

        for column, values in new_filters.items():
            merged_filters[column] = {}
            for value in values:
                if column in self.filters and value in self.filters[column]:
                    merged_filters[column][value] = self.filters[column][value]
                else:
                    merged_filters[column][value] = True

        self.filters = merged_filters
        self.menu_vars = {}

    def clear_all_filters(self):
        # Limpar todos os filtros
        self.filters = {}
        self.menu_vars = {}
        
        # Atualizar cabeçalhos de colunas para remover qualquer emoji de filtro
        for col in self.tree["columns"]:
            self.update_column_header(col)

    def open_menu(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            col_id = self.tree.identify_column(event.x)
            col_index = int(col_id.replace("#", "")) - 1

            column_names = self.tree["columns"]
            if col_index >= len(column_names):
                print("Índice de coluna inválido.")
                return

            col = column_names[col_index]

            popup_menu = tk.Menu(self.table, tearoff=0)

            if col not in self.menu_vars:
                self.menu_vars[col] = {}

            popup_menu.add_command(label="全选", command=lambda c=col: self.activate_all(c))
            popup_menu.add_command(label="清除所有", command=lambda c=col: self.deactivate_all(c))

            popup_menu.add_separator()

            for key, value in self.filters.get(col, {}).items():
                if key not in self.menu_vars[col]:
                    self.menu_vars[col][key] = tk.BooleanVar(value=value)

                popup_menu.add_checkbutton(
                    label=str(key),
                    variable=self.menu_vars[col][key],
                    command=self._make_toggle_callback(col, key)
                )

            popup_menu.tk_popup(event.x_root, event.y_root)

            # Adicionando o emoji ao cabeçalho da coluna, se houver filtro aplicado
            self.update_column_header(col)

    def update_column_header(self, col):
        column_name = self.tree.heading(col, "text")
        # Verifica se há algum filtro ativo para a coluna
        if any(not state for state in self.filters.get(col, {}).values()):
            # Adiciona o emoji ao nome da coluna, se não estiver já presente
            emoji = "🔍"  # Emoji indicando filtro aplicado
            if emoji not in column_name:
                new_title = f"{column_name} {emoji}"
                self.tree.heading(col, text=new_title)
        else:
            # Remove o emoji se não houver filtro ativo
            emoji = "🔍"
            new_title = f"{column_name.replace(f' {emoji}', '')}"
            self.tree.heading(col, text=new_title)

    def _make_toggle_callback(self, col, key):
        return lambda: self.on_toggle(col, key)

    def on_toggle(self, col, key):
        value = self.menu_vars[col][key].get()
        self.filters[col][key] = value
        self.update_column_header(col)  # Atualiza o título com o emoji
        self.update_visibility()

    def _generate_filters(self):
        filters = {}
        for row in self.data:
            for column, value in row.items():
                if column not in filters:
                    filters[column] = {}
                if value not in filters[column]:
                    filters[column][value] = True

        return filters

    def toggle_value(self, column, value):
        if column in self.filters:
            if value in self.filters[column]:
                self.filters[column][value] = not self.filters[column][value]
            else:
                self.filters[column][value] = False
        else:
            self.filters[column] = {value: False}
        self.update_visibility()

    def activate_all(self, column):
        if column in self.filters:
            # Ativa todos os valores da coluna
            for value in self.filters[column]:
                self.filters[column][value] = True
                if column in self.menu_vars and value in self.menu_vars[column]:
                    self.menu_vars[column][value].set(True)

            # Remover o emoji, pois todos os filtros estão ativados (sem filtro específico)
            self.update_column_header(column)
            self.update_visibility()
        else:
            print(f"Column '{column}' does not exist in filters.")

    def deactivate_all(self, column):
        if column in self.filters:
            for value in self.filters[column]:
                self.filters[column][value] = False
                if column in self.menu_vars and value in self.menu_vars[column]:
                    self.menu_vars[column][value].set(False)
            self.update_visibility()
        else:
            print(f"Column '{column}' does not exist in filters.")

    def reset_filters(self):
        for column in self.filters:
            for value in self.filters[column]:
                self.filters[column][value] = True
                if column in self.menu_vars and value in self.menu_vars[column]:
                    self.menu_vars[column][value].set(True)

        # Adiciona emoji ao cabeçalho das colunas ao resetar
        for col in self.tree["columns"]:
            self.update_column_header(col)

        self.update_visibility()

    def update_visibility(self):
        for row in self.data:
            visible = True
            for column, filter_values in self.filters.items():
                row_value = row.get(column)
                if row_value is not None:
                    if row_value in filter_values:
                        if not filter_values[row_value]:
                            visible = False
                            break
            row['visible'] = visible
        
        self.table.refresh()

    def refresh_filters(self):
        self.tree.delete(*self.tree.get_children())

        for item in self.data:
            item.pop('row_id', None)

        for item in self.data:
            if 'visible' in item and not item['visible']:
                continue
            
            if 'row_id' not in item:
                row_id = self.tree.insert('', 'end', values=[item.get(col, '') for col in self.columns])
                item['row_id'] = row_id

"""
import tkinter as tk
from .base_plugin import BasePlugin

class FilterPlugin(BasePlugin):
    def __init__(self):
        self.filters = {}
        self.menu_vars = {}

    def run(self):
        self.tree.bind("<Button-3>", self.open_menu, add=True)
        self.filters = self._generate_filters()
        self.table.on("table_refreshed", self.refresh_filters)
        
        self.table.on("data_setted", self._on_data_change)
        self.table.on("row_added", self._on_data_change)
        self.table.on("row_removed", self._on_data_change)
        self.table.on("cell_edited", self._on_data_change)

    def _on_data_change(self, **kwargs):
        self.regenerate_filters()

    def regenerate_filters(self):
        new_filters = self._generate_filters()
        merged_filters = {}

        for column, values in new_filters.items():
            merged_filters[column] = {}
            for value in values:
                if column in self.filters and value in self.filters[column]:
                    merged_filters[column][value] = self.filters[column][value]
                else:
                    merged_filters[column][value] = True

        self.filters = merged_filters
        self.menu_vars = {}

    
    def open_menu(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            col_id = self.tree.identify_column(event.x)
            col_index = int(col_id.replace("#", "")) - 1

            column_names = self.tree["columns"]
            if col_index >= len(column_names):
                print("Índice de coluna inválido.")
                return

            col = column_names[col_index]

            popup_menu = tk.Menu(self.table, tearoff=0)

            if col not in self.menu_vars:
                self.menu_vars[col] = {}

            popup_menu.add_command(label="全选", command=lambda c=col: self.activate_all(c))
            popup_menu.add_command(label="清除所有", command=lambda c=col: self.deactivate_all(c))

            popup_menu.add_separator()

            for key, value in self.filters[col].items():
                if key not in self.menu_vars[col]:
                    self.menu_vars[col][key] = tk.BooleanVar(value=value)

                popup_menu.add_checkbutton(
                    label=str(key),
                    variable=self.menu_vars[col][key],
                    command=self._make_toggle_callback(col, key)
                )

            popup_menu.tk_popup(event.x_root, event.y_root)

    def _make_toggle_callback(self, col, key):
        return lambda: self.on_toggle(col, key)

    def on_toggle(self, col, key):
        value = self.menu_vars[col][key].get()
        self.filters[col][key] = value
        self.update_visibility()

    def _generate_filters(self):
        filters = {}
        for row in self.data:
            for column, value in row.items():
                if column not in filters:
                    filters[column] = {}
                if value not in filters[column]:
                    filters[column][value] = True

        return filters

    def toggle_value(self, column, value):
        if column in self.filters:
            if value in self.filters[column]:
                self.filters[column][value] = not self.filters[column][value]
            else:
                self.filters[column][value] = False
        else:
            self.filters[column] = {value: False}
        self.update_visibility()

    def activate_all(self, column):
        if column in self.filters:
            for value in self.filters[column]:
                self.filters[column][value] = True
                if column in self.menu_vars and value in self.menu_vars[column]:
                    self.menu_vars[column][value].set(True)
            self.update_visibility()
        else:
            print(f"Column '{column}' does not exist in filters.")

    def deactivate_all(self, column):
        if column in self.filters:
            for value in self.filters[column]:
                self.filters[column][value] = False
                if column in self.menu_vars and value in self.menu_vars[column]:
                    self.menu_vars[column][value].set(False)
            self.update_visibility()
        else:
            print(f"Column '{column}' does not exist in filters.")

    def reset_filters(self):
        for column in self.filters:
            for value in self.filters[column]:
                self.filters[column][value] = True
                if column in self.menu_vars and value in self.menu_vars[column]:
                    self.menu_vars[column][value].set(True)
        self.update_visibility()

    def update_visibility(self):
        for row in self.data:
            visible = True
            for column, filter_values in self.filters.items():
                row_value = row.get(column)
                if row_value is not None:
                    if row_value in filter_values:
                        if not filter_values[row_value]:
                            visible = False
                            break
            row['visible'] = visible
        
        self.table.refresh()

    def refresh_filters(self):
        self.tree.delete(*self.tree.get_children())

        for item in self.data:
            item.pop('row_id', None)

        for item in self.data:
            if 'visible' in item and not item['visible']:
                continue
            
            if 'row_id' not in item:
                row_id = self.tree.insert('', 'end', values=[item.get(col, '') for col in self.columns])
                item['row_id'] = row_id

"""