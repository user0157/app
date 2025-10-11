def with_refresh_token_retry(method_name):
    """
    装饰器工厂，创建一个装饰器，用于自动处理访问令牌过期后刷新令牌并重试调用的方法。

    参数:
        method_name (str): 被装饰方法的名称，用于打印调试信息（目前被注释掉了）。

    返回:
        decorator: 一个装饰器，用于包装目标方法。
    """
    def decorator(func):
        """
        装饰器，包装目标函数，增加令牌刷新及重试机制。
        """
        def wrapper(self, *args, **kwargs):
            """
            包装函数，先调用目标函数，如果返回401（未授权），则尝试刷新令牌并重试。
            """
            # 调用目标方法
            result = func(self, *args, **kwargs)

            # 检查返回结果是否是401未授权，表示令牌可能已过期
            if isinstance(result, dict) and result.get("status") == 401:
                # print(f"[{method_name}] Token 已过期。正在尝试刷新...")

                # 尝试刷新访问令牌
                refresh_result = self.refresh_access_token()

                # 刷新成功，重新调用目标方法
                if refresh_result.get("success"):
                    # print(f"[{method_name}] 成功获取新的 token。正在重复调用...")
                    return func(self, *args, **kwargs)
                else:
                    # 刷新失败，返回错误提示，提示用户重新登录
                    # print(f"[{method_name}] 刷新 token 失败。需要重新登录。")
                    return {"success": False, "error": "会话已过期，请重新登录。", "status": 401}

            # 如果不是401，直接返回结果
            return result

        return wrapper
    return decorator
