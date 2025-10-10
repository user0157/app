import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pages.page import Page
from widgets import Mytable, MyText, ToastMessage
from pages.utils import wrap_number_to_lines, generate_product_map, load_cache, generate_aliases
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
import datetime
import pyperclip

class MainPage(Page):
    def __init__(self, parent, page_id):
        super().__init__(parent, page_id)

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ttk.Frame(self, width=150)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        self.sidebar.grid_propagate(False)
        
        self.sidebar.grid_columnconfigure(0, weight=1)

        buttons = [
            ("文本标记", None),
            ("标记数量-前面", lambda: self.run_algorithm("quantity", "forward")),
            ("标记数量-后面", lambda: self.run_algorithm("quantity", "backward")),
            ("标记价格-前面", lambda: self.run_algorithm("price", "forward")),
            ("标记价格-后面", lambda: self.run_algorithm("price", "backward")),
            ("文本处理", None),
            ("提取表格", self.process_text),
            ("复制表格数据", self.copy_to_clipboard),
            ("表格处理", None),
            ("匹配SKU", self.get_sku),
            ("添加行", lambda: self.table.add_row()),
            ("清理表格数据", lambda: self.table.set_data([])),
            ("Excel", None),
            ("导入Excel", self.upload_excel),
            ("导出Excel", self.export_excel),
            ("创建缓存", self.create_cache),
        ]
        
        for i, (text, command) in enumerate(buttons):
            if command is None:
                label = ttk.Label(self.sidebar, text=text, anchor="center", font=("Arial", 10, "bold"))
                label.grid(row=i, column=0, sticky="ew", pady=(10, 2))
            else:
                btn = ttk.Button(self.sidebar, text=text, command=command)
                btn.grid(row=i, column=0, sticky="ew", pady=2)

        self.sidebar.grid_rowconfigure(len(buttons), weight=1)

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=2, uniform="equal")
        self.container.grid_columnconfigure(1, weight=3, uniform="equal")

        self.editor = MyText(self.container)
        self.editor.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.table = Mytable(self.container)
        self.table.grid(row=0, column=1, sticky="nsew")

        self.table.set_columns(["sku", "name", "quantity", "price"])

    def copy_to_clipboard(self):
        item_ids = self.table.tree.get_children()
        col_names = self.table.columns

        lines = []

        for item_id in item_ids:
            values = self.table.tree.item(item_id)['values']
            row_dict = dict(zip(col_names, values))

            quantity = row_dict.get('quantity', '')
            name = row_dict.get('name', '')
            price = row_dict.get('price', '')

            line = f"{quantity} {name} {price}".strip()
            lines.append(line)

        text = "\n".join(lines)
        pyperclip.copy(text)
        ToastMessage(self, "成功复制到粘贴面板")

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.emit("page/logout", self.page_id)

    def run_algorithm(self, key, direction):
        text = self.editor.get("1.0", tk.END)
        new_text = wrap_number_to_lines(text, key, direction)
        self.editor.overwrite(new_text)

    def get_sku(self):
        items = [item["name"] for item in self.table.get_data() if item.get("name")]
        text = "\n".join(items)
        self.emit("page/process", text, self.page_id)

    def process_text(self):
        text = self.editor.get("1.0", tk.END)
        self.emit("page/process", text, self.page_id)

    def handle_text_processed(self, data):
        desired_keys = ["sku", "name", "quantity", "price"]
        filtered = [
            {key: d[key] for key in desired_keys}
            for d in data
        ]

        result = self.match(filtered, mode="both")
        if not result:
            return

        self.table.set_data(result)
        self.table.set_columns(["sku", "name", "quantity", "price"])
        self.table.set_editable_columns(["sku", "name", "quantity", "price"])

    def match(self, data, mode="both"):
        cache = load_cache()
        if not cache:
            return

        price_map = generate_product_map(cache)

        for item in data:
            original_sku = item.get("sku")
            aliases = generate_aliases(original_sku)

            matched_price = 0
            matched_product = None

            for alias in aliases:
                product = price_map.get(alias)
                if product:
                    price = product.get("price", 0)
                    if price > matched_price:
                        matched_price = price
                        matched_product = product

            if mode in ("price", "both"):
                item["price"] = "" if matched_price == 0 else matched_price

            if mode in ("sku", "both"):
                if matched_product:
                    item["sku"] = matched_product.get("sku", "")
                else:
                    item["sku"] = ""

        return data
    
    def get_price(self):
        data = self.table.get_data()
        result = self.match(data, mode="price")
        if not result:
            return

        self.table.set_data(result)

    def create_cache(self):
        self.emit("page/create_cache", self.page_id)

    def upload_excel(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")],
            title="选择要导入的Excel文件"
        )
        if not file_path:
            return

        try:
            wb = load_workbook(file_path)
            ws = wb.active

            headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
            expected_columns = ["sku", "name", "quantity", "price"]
            existing_columns = [col for col in expected_columns if col in headers]

            if not existing_columns:
                messagebox.showerror("错误", "Excel 文件中没有找到可导入的列。")
                return

            col_indices = {col: headers.index(col) for col in existing_columns}

            data = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if all(cell is None for cell in row):
                    continue

                item = {}
                for col in existing_columns:
                    value = row[col_indices[col]]

                    if col == "quantity":
                        try:
                            value = int(float(value))
                        except (TypeError, ValueError):
                            value = 0

                    elif col == "price":
                        try:
                            price_val = float(value)
                            if price_val.is_integer():
                                value = str(int(price_val))
                            else:
                                value = f"{price_val:.2f}"
                        except (TypeError, ValueError):
                            value = "0"

                    if value is None:
                        value = "" if col != "quantity" else 0

                    item[col] = value

                for col in expected_columns:
                    if col not in existing_columns:
                        item[col] = 0 if col == "quantity" else ""

                data.append(item)

            self.table.set_columns(expected_columns)
            self.table.set_data(data)
            self.table.set_editable_columns(expected_columns)
            messagebox.showinfo("成功", "Excel 文件导入成功。")

        except Exception as e:
            messagebox.showerror("错误", f"导入 Excel 文件失败: {str(e)}")
                    
    def export_excel(self):
        default_filename = f"data_{datetime.date.today()}.xlsx"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx *.xls")],
            initialfile=default_filename
        )
        
        if not file_path:
            return

        try:
            treeview = self.table.tree
            wb = Workbook()
            ws = wb.active

            columns = self.table.columns
            header_font = Font(name='Calibri', size=11, bold=True)
            default_font = Font(name='Calibri', size=11)

            for col_idx, col_name in enumerate(columns, start=1):
                cell = ws.cell(row=1, column=col_idx, value=col_name)
                cell.font = header_font

            for row_idx, row_id in enumerate(treeview.get_children(), start=2):
                row_values = treeview.item(row_id)["values"]
                for col_idx, value in enumerate(row_values, start=1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=value)
                    cell.font = default_font

            for col_idx, col_name in enumerate(columns, start=1):
                max_length = len(str(col_name))
                for row in ws.iter_rows(min_row=2, min_col=col_idx, max_col=col_idx):
                    for cell in row:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                adjusted_width = (max_length + 2)
                col_letter = get_column_letter(col_idx)
                ws.column_dimensions[col_letter].width = adjusted_width

            max_row = ws.max_row
            max_col = ws.max_column
            for row in ws.iter_rows(min_row=1, max_row=max_row, min_col=1, max_col=max_col):
                for cell in row:
                    if cell.font != header_font:
                        cell.font = default_font

            wb.save(file_path)
            messagebox.showinfo("成功", "数据导出成功。")
        except Exception as e:
            messagebox.showerror("错误", f"保存 Excel 文件失败: {str(e)}")