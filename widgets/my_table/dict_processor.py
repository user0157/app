class DictProcessor:
    def __init__(self, aliases=None, order=None, default_value=None):
        """
        初始化参数：
        aliases: dict，键是主字段名，值是该字段的别名列表，例如 {"name": ["姓名", "名称"]}
        order: list，指定字段的输出顺序
        default_value: 缺失字段时填充的默认值，会被转换成字符串
        """
        self.aliases = aliases or {}
        self.order = order or []
        self.default_value = default_value
        # 生成别名->主键映射字典
        self.alias_to_main = self._create_alias_map()

    def _create_alias_map(self):
        # 创建一个字典，映射所有别名和主键自身到主键
        mapping = {}
        for main_key, alias_list in self.aliases.items():
            mapping[main_key] = main_key  # 主键映射自己
            for alias in alias_list:
                mapping[alias] = main_key
        return mapping

    def _normalize_dict(self, d):
        """
        输入一个字典，将其所有键名转换为主键名（如果有别名的话）
        """
        new_dict = {}
        for k, v in d.items():
            # 如果 k 是别名，转为主键名，否则保持不变
            key = self.alias_to_main.get(k, k)
            new_dict[key] = v
        return new_dict

    def normalize(self, list_of_dicts):
        """
        规范化一组字典：
        - 将别名转换成主键
        - 确定最终字段顺序，先按 order 参数排序，额外字段按字母顺序排在后面
        - 缺失字段填充默认值，所有值转字符串
        """
        if not isinstance(list_of_dicts, list):
            raise ValueError("Input should be a list of dictionaries.")

        normalized = []
        used_keys = set()

        # 先将每个字典转换成标准字段名的字典
        for d in list_of_dicts:
            norm = self._normalize_dict(d)
            normalized.append(norm)
            used_keys.update(norm.keys())

        # 根据指定顺序和剩余字段组合最终顺序
        final_order = list(self.order)
        extras = [k for k in used_keys if k not in final_order]
        extras.sort()  # 额外字段按字母顺序排列
        final_order += extras

        # 用默认值补齐字段，所有值转字符串
        result = []
        for d in normalized:
            complete = {
                k: str(d.get(k, self.default_value)) for k in final_order
            }
            result.append(complete)

        return result

    def __call__(self, list_of_dicts):
        """
        支持将实例当作函数调用，直接调用 normalize
        """
        return self.normalize(list_of_dicts)
