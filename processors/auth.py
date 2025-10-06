def with_refresh_token_retry(method_name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)

            if isinstance(result, dict) and result.get("status") == 401:
                #print(f"[{method_name}] Token 已过期。正在尝试刷新...")
                refresh_result = self.refresh_access_token()
                if refresh_result.get("success"):
                    #print(f"[{method_name}] 成功获取新的 token。正在重复调用...")
                    return func(self, *args, **kwargs)
                else:
                    #print(f"[{method_name}] 刷新 token 失败。需要重新登录。")
                    return {"success": False, "error": "会话已过期，请重新登录。", "status": 401}
            return result
        return wrapper
    return decorator
