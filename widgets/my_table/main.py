import tkinter as tk  # 导入 tkinter 库，用于创建图形用户界面 (GUI)
from dict_processor import DictProcessor  # 导入 DictProcessor 类，用于处理字典数据
from my_table import Mytable  # 导入自定义的 Mytable 类，用于显示数据表格
from plugins.filter_plugin import FilterPlugin  # 导入 FilterPlugin 插件，用于数据过滤
from plugins.sort_plugin import SortPlugin  # 导入 SortPlugin 插件，用于数据排序
from plugins.style_plugin import StylePlugin  # 导入 StylePlugin 插件，用于样式应用
from plugins.edit_plugin import EditPlugin  # 导入 EditPlugin 插件，用于数据编辑
from plugins.cell_plugin import CellPlugin  # 导入 CellPlugin 插件，用于单元格操作

if __name__ == "__main__":  # 如果是主程序启动，则执行以下代码
    root = tk.Tk()  # 创建一个 tkinter 窗口实例
    
    # 初始数据：一个包含多个字典的列表，每个字典代表一行数据
    initial_data = [
        {"id": 1, "name": "Item 1", "value": 10},
        {"id": 2, "name": "Item 2", "value": 20},
        {"id": 3, "name": "Item 3", "value": 30}
    ]

    # 创建 DictProcessor 实例，默认值为空字符串
    processor = DictProcessor(default_value='')
    
    # 使用 DictProcessor 处理初始数据，返回处理后的数据
    data = processor(initial_data)
    print("Processed Data:", data)  # 打印处理后的数据
    
    # 创建 Mytable 实例，并将处理后的数据传入
    table = Mytable(root, data)
    
    # 使用 pack 方法将表格添加到窗口中，设置表格可以扩展并填充可用空间
    table.pack(expand=True, fill='both')

    # 注册插件：为表格功能增加额外的操作
    table.register_plugin(FilterPlugin())  # 注册过滤插件
    table.register_plugin(SortPlugin())  # 注册排序插件
    table.register_plugin(StylePlugin())  # 注册样式插件
    table.register_plugin(EditPlugin(["id", "value"]))  # 注册编辑插件，允许编辑 'id' 和 'value' 列
    table.register_plugin(CellPlugin())  # 注册单元格操作插件

    # 定义一个打印数据的函数，用于打印表格中的数据
    def print_data():
        for item in table.data:  # 遍历表格中的每一项数据
            print(item)  # 打印每一项数据
    
    # 创建一个按钮，点击时调用 print_data 函数
    print_button = tk.Button(root, text="Print Data", command=print_data)
    
    # 将按钮添加到窗口中，并设置垂直间距
    print_button.pack(pady=10)
    
    # 启动 tkinter 主事件循环，保持窗口响应用户操作
    root.mainloop()
