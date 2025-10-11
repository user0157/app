import tkinter as tk
from tkinter import ttk
import uuid
from .dict_processor import DictProcessor

class BaseTable(ttk.Frame):
    def __init__(self, parent, initial_data=None, columns=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # 设置表格显示的列
        if columns is not None:
            self.columns = list(columns)
        elif initial_data:
            # 从初始数据中提取所有键作为列名（去重合并）
            self.columns = list(set().union(*(row.keys() for row in initial_data)))
        else:
            self.columns = []

        # 不显示内部管理的 'row_id' 列
        if "row_id" in self.columns:
            self.columns.remove("row_id")

        self.create_widgets()              # 创建 Treeview 等组件
        self.set_data(initial_data or [])  # 设定初始数据

        # 延迟调整列宽，确保控件尺寸已初始化
        self.after(100, self.adjust_columns)

    def create_widgets(self):
        # 重新创建 Treeview 控件（先销毁旧的）
        if hasattr(self, 'tree'):
            self.tree.destroy()

        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')

        # 设置每列标题和样式
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', stretch=True, width=1)  # 初始宽度设为 1，后续调整

        # 布局 Treeview
        self.tree.grid(row=0, column=0, sticky="nsew")

        # 配置栅格权重，实现控件自动拉伸
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 绑定大小改变事件，动态调整列宽
        self.bind("<Configure>", self.on_resize)
        self.tree.bind("<Configure>", self.on_resize)

    def on_resize(self, event=None):
        """控件大小变化时调用，调整列宽"""
        self.adjust_columns()

    def adjust_columns(self):
        """均匀分配 Treeview 总宽度给所有列，且设置最小宽度 50"""
        if not self.columns:
            return

        self.update_idletasks()   # 确保界面尺寸最新

        tree_width = self.tree.winfo_width()

        if tree_width > 10:  # 只有控件宽度足够时才调整
            col_width = max(50, tree_width // len(self.columns))

            for col in self.columns:
                self.tree.column(col, width=col_width, stretch=True)

    def refresh(self):
        """刷新表格数据"""
        self.tree.delete(*self.tree.get_children())

        # 逐行插入数据，row_id 作为每行唯一标识符
        for item in self.data:
            values = [item.get(col, '') for col in self.columns]
            row_id = item.get("row_id")
            self.tree.insert('', 'end', iid=row_id, values=values)

        # 延迟调整列宽，保证数据加载后界面美观
        self.after(100, self.adjust_columns)

    def add_row(self, index=None, new_row=None):
        """新增一行数据，支持指定插入位置"""
        if new_row is None:
            new_row = {col: '' for col in self.columns}
        else:
            # 补齐缺失列
            for col in self.columns:
                if col not in new_row:
                    new_row[col] = ''

        # 生成唯一的 row_id 方便管理
        if not new_row.get("row_id"):
            new_row["row_id"] = str(uuid.uuid4())

        if index is None:
            self.data.append(new_row)
        else:
            index = max(0, min(index, len(self.data)))
            self.data.insert(index, new_row)

        self.refresh()

    def remove_row(self, index):
        """删除指定索引的行"""
        if 0 <= index < len(self.data):
            self.data.pop(index)
        else:
            print(f"Invalid index for removal: {index}")

        self.refresh()

    def edit_cell(self, row_id, column_name, new_value):
        """编辑指定单元格的值，更新界面"""
        for index, row in enumerate(self.data):
            if row.get("row_id") == row_id:
                if column_name in self.columns:
                    self.data[index][column_name] = new_value
                    values = [self.data[index].get(col, '') for col in self.columns]
                    self.tree.item(row_id, values=values)
                break

    def set_columns(self, new_columns):
        """重置列名（不包含 'row_id'），重新创建表格和数据"""
        if "row_id" in new_columns:
            new_columns = [col for col in new_columns if col != "row_id"]
        self.columns = list(new_columns)
        self.create_widgets()
        self.set_data(self.data)
        self.after(100, self.adjust_columns)

    def set_data(self, new_data):
        """设置表格数据，自动为缺失的行添加唯一 row_id"""
        processed_data = []
        for row in new_data:
            row = dict(row)
            if "row_id" not in row:
                row["row_id"] = str(uuid.uuid4())
            processed_data.append(row)

        # 用 DictProcessor 按列顺序和默认值处理数据
        processor = DictProcessor(
            order=self.columns,
            default_value=""
        )
        self.data = processor(processed_data)
        self.refresh()
        self.after(100, self.adjust_columns)

    def get_data(self):
        """获取当前数据（不包含内部管理的 row_id）"""
        return [{k: v for k, v in row.items() if k != "row_id"} for row in self.data]
