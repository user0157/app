from app import App
from processors.controller import TextController
from processors.text_processor import TextProcessor

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