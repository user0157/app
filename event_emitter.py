# =========================
# EventEmitter 基类
# =========================
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        # 注册监听器
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def emit(self, event, *args, **kwargs):
        # 触发事件
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(*args, **kwargs)