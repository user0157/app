import tkinter as tk
from tkinter import ttk
import uuid
from .dict_processor import DictProcessor

class BaseTable(ttk.Frame):
    def __init__(self, parent, initial_data=None, columns=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Define colunas visíveis, removendo 'row_id' caso esteja presente
        if columns is not None:
            self.columns = list(columns)
        elif initial_data:
            self.columns = list(set().union(*(row.keys() for row in initial_data)))
        else:
            self.columns = []

        # Remove 'row_id' das colunas visíveis (para não aparecer na tabela)
        if "row_id" in self.columns:
            self.columns.remove("row_id")

        self.create_widgets()
        self.set_data(initial_data or [])
        
        # Forçar o redimensionamento inicial após a criação
        self.after(100, self.adjust_columns)

    def create_widgets(self):
        if hasattr(self, 'tree'):
            self.tree.destroy()

        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')

        for col in self.columns:
            self.tree.heading(col, text=col)
            # Configura stretch=True para que as colunas se expandam
            self.tree.column(col, anchor='center', stretch=True, width=1)  # Width mínimo inicial

        # Layout simples sem scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Configurar pesos para redimensionamento
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Bind para redimensionar quando o widget for redimensionado
        self.bind("<Configure>", self.on_resize)
        self.tree.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        """Redimensiona as colunas quando o widget é redimensionado"""
        self.adjust_columns()

    def adjust_columns(self):
        """Ajusta o tamanho das colunas para preencher o espaço disponível"""
        if not self.columns:
            return
            
        # Atualiza a interface para garantir que as medidas estejam corretas
        self.update_idletasks()
        
        # Obtém a largura total do Treeview
        tree_width = self.tree.winfo_width()
        
        if tree_width > 10:  # Só ajusta se o Treeview já tiver um tamanho significativo
            # Divide igualmente a largura entre as colunas
            col_width = max(50, tree_width // len(self.columns))
            
            for col in self.columns:
                self.tree.column(col, width=col_width, stretch=True)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())

        for item in self.data:
            values = [item.get(col, '') for col in self.columns]
            row_id = item.get("row_id")
            self.tree.insert('', 'end', iid=row_id, values=values)
        
        # Ajustar colunas após refresh
        self.after(100, self.adjust_columns)

    def add_row(self, index=None, new_row=None):
        if new_row is None:
            new_row = {col: '' for col in self.columns}
        else:
            for col in self.columns:
                if col not in new_row:
                    new_row[col] = ''

        # Gera row_id único caso não tenha
        if not new_row.get("row_id"):
            new_row["row_id"] = str(uuid.uuid4())

        if index is None:
            self.data.append(new_row)
        else:
            index = max(0, min(index, len(self.data)))
            self.data.insert(index, new_row)

        self.refresh()

    def remove_row(self, index):
        if 0 <= index < len(self.data):
            self.data.pop(index)
        else:
            print(f"Invalid index for removal: {index}")

        self.refresh()

    def edit_cell(self, row_id, column_name, new_value):
        for index, row in enumerate(self.data):
            if row.get("row_id") == row_id:
                if column_name in self.columns:
                    self.data[index][column_name] = new_value
                    values = [self.data[index].get(col, '') for col in self.columns]
                    self.tree.item(row_id, values=values)
                break

    def set_columns(self, new_columns):
        # Remove 'row_id' das colunas visíveis
        if "row_id" in new_columns:
            new_columns = [col for col in new_columns if col != "row_id"]
        self.columns = list(new_columns)
        self.create_widgets()
        self.set_data(self.data)
        self.after(100, self.adjust_columns)

    def set_data(self, new_data):
        # Garante row_id em todas as linhas
        processed_data = []
        for row in new_data:
            row = dict(row)
            if "row_id" not in row:
                row["row_id"] = str(uuid.uuid4())
            processed_data.append(row)

        processor = DictProcessor(
            order=self.columns,
            default_value=""
        )
        self.data = processor(processed_data)
        self.refresh()
        self.after(100, self.adjust_columns)

    def get_data(self):
        # Retorna dados sem 'row_id' (apenas colunas visíveis)
        return [{k: v for k, v in row.items() if k != "row_id"} for row in self.data]