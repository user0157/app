class EventEmitter:
    def __init__(self):
        # 初始化事件监听器字典，用于存储事件名称和回调函数
        self._listeners = {}

    def on(self, event_name, callback):
        """
        注册一个事件的监听器（回调函数）
        如果事件名称不存在，则会创建一个新的事件列表。
        :param event_name: 事件的名称
        :param callback: 事件触发时执行的回调函数
        """
        # 如果事件名称没有在监听器字典中，创建一个新的列表
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        # 将回调函数添加到事件名称对应的回调函数列表中
        self._listeners[event_name].append(callback)

    def emit(self, event_name, *args, **kwargs):
        """
        触发某个事件，调用与事件名称关联的所有回调函数
        :param event_name: 事件的名称
        :param args: 传递给回调函数的位置参数
        :param kwargs: 传递给回调函数的关键字参数
        """
        # 如果事件名称存在，则遍历所有注册的回调函数并执行它们
        if event_name in self._listeners:
            for callback in self._listeners[event_name]:
                # 使用args和kwargs将参数传递给回调函数
                callback(*args, **kwargs)
