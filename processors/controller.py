from event_emitter import EventEmitter
import threading
import functools

def run_in_thread(func):
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
    def __init__(self, processor):
        super().__init__()
        self.processor = processor

    @run_in_thread
    def login(self, input, page_id):
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
        result = self.processor.fetch_profile()
        result["page_id"] = page_id

        if result.get("success"):
            self.emit("profile_fetched", result)
        else:
            self.emit("error", result)

    @run_in_thread
    def send_request(self, endpoint, page_id):
        result = self.processor.send_request(endpoint)
        result["page_id"] = page_id

        if result.get("success"):
            self.emit("action_success", result)
        else:
            self.emit("error", result)

    @run_in_thread
    def process(self, text, page_id):
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
        result = self.processor.create_cache(file_path)
        result["page_id"] = page_id

        if result.get("success"):
            self.emit("data_processed", result)
        else:
            self.emit("error", result)