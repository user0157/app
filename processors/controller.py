from event_emitter import EventEmitter
import threading
import functools

def run_in_thread(func):
    """
    装饰器：将被装饰的方法放到一个后台守护线程中运行，避免阻塞主线程。

    当被装饰函数执行出错时，尝试通过 self.emit 发出 "error" 事件，否则打印错误。
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        def thread_target():
            try:
                func(self, *args, **kwargs)
            except Exception as e:
                if hasattr(self, 'emit'):
                    self.emit("error", str(e))
                else:
                    print(f"线程错误: {e}")
        threading.Thread(target=thread_target, daemon=True).start()
    return wrapper


class TextController(EventEmitter):
    """
    文本处理控制器，继承自 EventEmitter，支持事件监听。

    通过多线程异步调用 processor 的方法，执行登录、获取用户资料、发送请求、处理文本、创建缓存等操作，
    并通过事件通知调用方结果或错误。
    """

    def __init__(self, processor):
        """
        初始化方法，传入处理器实例。
        """
        super().__init__()
        self.processor = processor

    @run_in_thread
    def login(self, input, page_id):
        """
        异步登录方法，使用 processor.login，完成后发出 "login_success" 或 "error" 事件。
        """
        email = input.get("email")
        password = input.get("password")
        result = self.processor.login(email, password)
        result["page_id"] = page_id

        if result.get("success"):
            self.emit("login_success", result)
        else:
            self.emit("error", result)

    @run_in_thread
    def fetch_profile(self, page_id):
        """
        异步获取用户资料，完成后发出 "profile_fetched" 或 "error" 事件。
        """
        result = self.processor.fetch_profile()
        result["page_id"] = page_id

        if result.get("success"):
            self.emit("profile_fetched", result)
        else:
            self.emit("error", result)

    @run_in_thread
    def send_request(self, endpoint, page_id):
        """
        异步发送请求，完成后发出 "action_success" 或 "error" 事件。
        """
        result = self.processor.send_request(endpoint)
        result["page_id"] = page_id

        if result.get("success"):
            self.emit("action_success", result)
        else:
            self.emit("error", result)

    @run_in_thread
    def process(self, text, page_id):
        """
        异步处理文本，先验证文本非空，拆分成行，调用 processor.process。
        完成后发出 "text_processed" 或 "error" 事件。
        """
        if not text or not text.strip():
            self.emit("error", {
                "page_id": page_id,
                "success": False,
                "error": "输入不能为空。",
            })
            return

        lines = text.strip().splitlines()
        result = self.processor.process(lines)
        result["page_id"] = page_id

        if result.get("success"):
            self.emit("text_processed", result)
        else:
            self.emit("error", result)

    @run_in_thread
    def create_cache(self, file_path, page_id):
        """
        异步创建缓存，完成后发出 "data_processed" 或 "error" 事件。
        """
        result = self.processor.create_cache(file_path)
        result["page_id"] = page_id

        if result.get("success"):
            self.emit("data_processed", result)
        else:
            self.emit("error", result)
