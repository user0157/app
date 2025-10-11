from .plugin_table import PluginTable  # 导入 PluginTable 类，Mytable 类继承自它
from .plugins.filter_plugin import FilterPlugin  # 导入 FilterPlugin 插件，用于数据过滤
from .plugins.sort_plugin import SortPlugin  # 导入 SortPlugin 插件，用于数据排序
from .plugins.style_plugin import StylePlugin  # 导入 StylePlugin 插件，用于样式应用
from .plugins.edit_plugin import EditPlugin  # 导入 EditPlugin 插件，用于编辑表格数据
from .plugins.cell_plugin import CellPlugin  # 导入 CellPlugin 插件，用于单元格操作

class Mytable(PluginTable):  # Mytable 类继承自 PluginTable，继承了其所有功能
    def __init__(self, parent, initial_data=[], *args, **kwargs):  # 构造函数，接受父组件、初始数据以及其他参数
        # 调用父类 PluginTable 的构造函数初始化表格
        super().__init__(parent, initial_data, *args, **kwargs)
        
        # 注册插件：为表格增加额外的功能
        self.register_plugin(FilterPlugin())  # 注册过滤插件
        self.register_plugin(SortPlugin())  # 注册排序插件
        self.register_plugin(StylePlugin())  # 注册样式插件
        
        # 注册编辑插件，并保存返回值到实例变量 `self.edit_plugin`
        self.edit_plugin = self.register_plugin(EditPlugin())  # 注册编辑插件，用于表格数据编辑
        
        # 注册单元格操作插件
        self.register_plugin(CellPlugin())  # 注册单元格操作插件

    def set_editable_columns(self, editable_columns):  # 设置可以编辑的列
        """
        设置哪些列是可以编辑的
        :param editable_columns: 一个包含列名的列表，指定哪些列是可编辑的
        """
        # 使用编辑插件设置可编辑的列
        self.edit_plugin.set_editable_columns(editable_columns)  # 调用 EditPlugin 的方法设置可编辑列
