import requests
from config import API_URL
from event_emitter import EventEmitter
import os
from processors.validator import Validator
from processors.auth import with_refresh_token_retry

class TextProcessor(EventEmitter):
    """
    负责调用后端 API 进行登录、刷新令牌、获取用户资料、发送请求、处理文本和创建缓存等操作。
    继承 EventEmitter，可发出事件（你当前代码中未见 emit，方便后续扩展）。
    """

    def __init__(self):
        super().__init__()
        self.access_token = None      # 当前有效的访问令牌
        self.refresh_token = None     # 用于刷新访问令牌的刷新令牌

    @staticmethod
    def _error_response(message, status):
        """
        返回统一格式的错误响应字典。
        """
        return {"success": False, "error": message, "status": status}

    def login(self, email, password):
        """
        通过账号密码登录，成功时保存 access_token 和 refresh_token。
        返回成功或失败的结果字典。
        """
        try:
            resp = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
            if resp.status_code == 200:
                data = resp.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                return {"success": True, "status": 200}
            else:
                # 从服务器错误响应中提取错误信息
                return self._error_response(resp.json().get("error", f"错误：{resp.status_code}"), resp.status_code)
        except requests.exceptions.RequestException:
            # 网络请求失败
            return self._error_response("无法连接到服务器。", 0)

    def refresh_access_token(self):
        """
        使用刷新令牌向后端请求新的访问令牌。
        刷新成功更新 self.access_token，否则返回错误。
        """
        if not self.refresh_token:
            return self._error_response("无可用的刷新令牌。", 401)

        try:
            resp = requests.post(f"{API_URL}/refresh", json={"refresh_token": self.refresh_token})
            if resp.status_code == 200:
                data = resp.json()
                self.access_token = data["access_token"]
                return {"success": True, "status": 200}
            else:
                return self._error_response("无法刷新令牌。", resp.status_code)
        except requests.exceptions.RequestException:
            return self._error_response("刷新令牌时无法连接到服务器。", 0)

    @with_refresh_token_retry("fetch_profile")
    def fetch_profile(self):
        """
        获取用户资料接口。
        使用访问令牌授权，失败返回401错误。
        """
        if not self.access_token:
            return self._error_response("未认证。", 401)

        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            resp = requests.get(f"{API_URL}/profile", headers=headers)
            if resp.status_code == 200:
                return {"success": True, "profile": resp.json(), "status": 200}
            elif resp.status_code == 401:
                return self._error_response("未授权。令牌可能已过期。", 401)
            else:
                return self._error_response(f"错误：{resp.status_code}", resp.status_code)
        except requests.exceptions.RequestException:
            return self._error_response("无法连接到服务器。", 0)

    @with_refresh_token_retry("send_request")
    def send_request(self, endpoint):
        """
        发送带授权的 POST 请求到指定 API 端点。
        返回成功消息或错误信息。
        """
        if not self.access_token:
            return self._error_response("未认证。", 401)

        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            resp = requests.post(f"{API_URL}{endpoint}", headers=headers)
            if resp.status_code == 200:
                return {"success": True, "message": resp.json().get("message", "成功！"), "status": 200}
            elif resp.status_code == 403:
                return self._error_response("您没有执行此操作的权限。", 403)
            elif resp.status_code == 401:
                return self._error_response("未授权。令牌可能已过期。", 401)
            else:
                return self._error_response(f"错误：{resp.status_code}", resp.status_code)
        except requests.exceptions.RequestException:
            return self._error_response("无法连接到服务器。", 0)

    @with_refresh_token_retry("process")
    def process(self, lines):
        """
        将文本行列表发送到后端进行处理。
        返回处理结果或错误。
        """
        if not self.access_token:
            return self._error_response("未认证。", 401)

        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            resp = requests.post(f"{API_URL}/process", json={"lines": lines}, headers=headers)
            if resp.status_code == 200:
                return {"success": True, "results": resp.json().get("results", ""), "status": 200}
            elif resp.status_code == 401:
                return self._error_response("未授权。令牌可能已过期。", 401)
            else:
                return self._error_response(f"错误：{resp.status_code}", resp.status_code)
        except requests.exceptions.RequestException:
            return self._error_response("无法连接到服务器。", 0)

    @with_refresh_token_retry("create_cache")
    def create_cache(self, file_path):
        """
        上传 Excel 文件创建缓存数据。
        验证文件存在、格式及必需列。
        返回处理后的数据或错误。
        """
        if not self.access_token:
            return self._error_response("未认证。", 401)

        if not os.path.exists(file_path):
            return self._error_response("未找到文件。", 400)

        if not Validator.is_valid_extension(file_path):
            return self._error_response("格式无效。请使用 .xlsx 文件。", 400)

        valid, error_msg = Validator.has_required_columns(file_path)
        if not valid:
            return self._error_response(error_msg, 400)

        headers = {"Authorization": f"Bearer {self.access_token}"}

        try:
            with open(file_path, 'rb') as f:
                files = {
                    'file': (
                        os.path.basename(file_path),
                        f,
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                }
                resp = requests.post(f"{API_URL}/create-cache", files=files, headers=headers)

            if resp.status_code == 200:
                return {"success": True, "processed_data": resp.json().get("processed_data", []), "status": 200}
            elif resp.status_code == 401:
                return self._error_response("未授权。令牌可能已过期。", 401)
            else:
                try:
                    backend_error = resp.json().get("error", "")
                except Exception:
                    backend_error = ""
                return self._error_response(f"错误：{resp.status_code}。{backend_error}", resp.status_code)

        except requests.exceptions.RequestException:
            return self._error_response("无法连接到服务器。", 0)
