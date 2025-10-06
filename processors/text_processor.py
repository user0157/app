import requests
from config import API_URL
from event_emitter import EventEmitter
import os
from processors.validator import Validator
from processors.auth import with_refresh_token_retry

class TextProcessor(EventEmitter):
    def __init__(self):
        super().__init__()
        self.access_token = None
        self.refresh_token = None

    @staticmethod
    def _error_response(message, status):
        return {"success": False, "error": message, "status": status}

    def login(self, email, password):
        try:
            resp = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
            if resp.status_code == 200:
                data = resp.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                return {"success": True, "status": 200}
            else:
                return self._error_response(resp.json().get("error", f"错误：{resp.status_code}"), resp.status_code)
        except requests.exceptions.RequestException:
            return self._error_response("无法连接到服务器。", 0)

    def refresh_access_token(self):
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
