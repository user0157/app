class DictProcessor:
    def __init__(self, aliases=None, order=None, default_value=None):
        """
        aliases: dict 映射主键 -> 别名列表
        order: 期望的最终键顺序列表
        default_value: 用于填充缺失键的默认值（会被转换成字符串）
        """
        self.aliases = aliases or {}
        self.order = order or []
        self.default_value = default_value
        self.alias_to_main = self._create_alias_map()

    def _create_alias_map(self):
        # 创建一个字典，将所有别名映射到其主键
        mapping = {}
        for main_key, alias_list in self.aliases.items():
            mapping[main_key] = main_key  # 主键映射到自身
            for alias in alias_list:
                mapping[alias] = main_key
        return mapping

    def _normalize_dict(self, d):
        # 将键替换为标准化名称
        new_dict = {}
        for k, v in d.items():
            key = self.alias_to_main.get(k, k)
            new_dict[key] = v
        return new_dict

    def normalize(self, list_of_dicts):
        if not isinstance(list_of_dicts, list):
            raise ValueError("Input should be a list of dictionaries.")

        normalized = []
        used_keys = set()

        for d in list_of_dicts:
            norm = self._normalize_dict(d)
            normalized.append(norm)
            used_keys.update(norm.keys())

        # 定义最终键的顺序
        final_order = list(self.order)
        extras = [k for k in used_keys if k not in final_order]
        final_order += sorted(extras)

        # 填充缺失值并将所有值转换为字符串
        result = []
        for d in normalized:
            complete = {
                k: str(d.get(k, self.default_value)) for k in final_order
            }
            result.append(complete)

        return result

    def __call__(self, list_of_dicts):
        # 允许将对象当作函数使用
        return self.normalize(list_of_dicts)
