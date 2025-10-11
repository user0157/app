from event_emitter import EventEmitter

class Processor(EventEmitter):
    """
    处理器类，继承自 EventEmitter，支持事件驱动编程。

    你可以在这个类中添加各种处理方法，比如登录、数据处理等，
    并通过 self.emit 发送事件，让监听者能够接收到处理结果或错误。
    """
    def __init__(self):
        super().__init__()
        # 这里可以初始化一些状态或者资源
