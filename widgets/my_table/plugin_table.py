from .base_table import BaseTable  # 导入 BaseTable 类，Mytable 类继承自它，提供基本的表格功能
from .event_emitter import EventEmitter  # 导入 EventEmitter 类，用于事件通知机制

class PluginTable(BaseTable, EventEmitter):  # PluginTable 类继承了 BaseTable 和 EventEmitter
    def __init__(self, parent, initial_data=[], *args, **kwargs):
        # 初始化父类 EventEmitter
        EventEmitter.__init__(self)
        
        # 初始化父类 BaseTable，设置表格的父组件和初始数据
        BaseTable.__init__(self, parent, initial_data, *args, **kwargs)
        
        # 初始化插件列表，用于存储注册的插件
        self.plugins = []
        
        # 调用 refresh 方法，刷新表格内容
        self.refresh()

    def register_plugin(self, plugin):
        """
        注册插件，并初始化插件与表格的关系
        :param plugin: 插件实例
        :return: 注册的插件实例
        """
        # 将插件添加到插件列表中
        self.plugins.append(plugin)
        
        # 设置插件的表格实例
        plugin.set_table(self)
        
        # 执行插件中的初始化操作
        plugin.run()
        
        # 返回插件实例
        return plugin
    
    def create_widgets(self):
        """
        创建表格的控件，并触发 'widgets_created' 事件
        """
        # 调用父类的 create_widgets 方法创建表格控件
        super().create_widgets()
        
        # 触发 'widgets_created' 事件，通知其他模块控件已创建
        self.emit("widgets_created")

    def refresh(self):
        """
        刷新表格数据，并触发 'table_refreshed' 事件
        """
        # 调用父类的 refresh 方法刷新表格
        super().refresh()
        
        # 触发 'table_refreshed' 事件，通知表格已刷新
        self.emit("table_refreshed")

    def add_row(self, index=None, new_row=None):
        """
        向表格中添加一行数据，并触发 'row_added' 事件
        :param index: 插入行的索引
        :param new_row: 新添加的行数据
        """
        # 调用父类的 add_row 方法添加数据行
        super().add_row(index, new_row)
        
        # 触发 'row_added' 事件，通知表格数据已添加
        self.emit("row_added", index=index, row=new_row)

    def remove_row(self, index):
        """
        从表格中删除一行数据，并触发 'row_removed' 事件
        :param index: 要删除的行的索引
        """
        # 调用父类的 remove_row 方法删除数据行
        super().remove_row(index)
        
        # 触发 'row_removed' 事件，通知表格数据已删除
        self.emit("row_removed", index=index)

    def edit_cell(self, row_id, column_name, new_value):
        """
        编辑表格某个单元格的数据，并触发 'cell_edited' 事件
        :param row_id: 行 ID
        :param column_name: 列名称
        :param new_value: 新的单元格值
        """
        # 调用父类的 edit_cell 方法修改单元格
        super().edit_cell(row_id, column_name, new_value)
        
        # 触发 'cell_edited' 事件，通知表格某个单元格已编辑
        self.emit("cell_edited", row_id=row_id, column=column_name, new_value=new_value)

    def set_columns(self, new_columns):
        """
        更新表格的列定义，并触发 'columns_updated' 事件
        :param new_columns: 新的列定义
        """
        # 调用父类的 set_columns 方法更新列定义
        super().set_columns(new_columns)
        
        # 触发 'columns_updated' 事件，通知表格列已更新
        self.emit("columns_updated", columns=new_columns)

    def set_data(self, data):
        """
        设置表格的数据，并触发 'data_setted' 事件
        :param data: 新的表格数据
        """
        # 调用父类的 set_data 方法设置表格数据
        super().set_data(data)
        
        # 触发 'data_setted' 事件，通知表格数据已设置
        self.emit("data_setted", data=data)
