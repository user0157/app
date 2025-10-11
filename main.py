from app import App
from processors.controller import TextController
from processors.text_processor import TextProcessor
import threading
import requests
from config import API_URL

def make_request():
    requests.get(f"{API_URL}/ping")
    threading.Timer(600, make_request).start()

# =========================
# 启动
# =========================
if __name__ == "__main__":
    app = App()
    processor = TextProcessor()
    controller = TextController(processor)

    app.on("login", controller.login)
    app.on("fetch_profile", controller.fetch_profile)
    app.on("process", controller.process)
    app.on("create_cache", controller.create_cache)

    controller.on("login_success", lambda output: app.handle_login_success(output))
    controller.on("profile_fetched", lambda output: app.update_user_data(output))
    controller.on("text_processed", lambda output: app.handle_text_processed(output))
    controller.on("data_processed", lambda output: app.handle_data_processed(output))
    controller.on("error", lambda error: app.handle_error(error))

    app.mainloop()
    
    try:
        make_request()  # 启动定时请求
    except Exception as e:
        print(f"Error occurred: {e}")