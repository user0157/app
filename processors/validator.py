import os
import pandas as pd

class Validator:
    """
    验证器类，用于校验上传的 Excel 文件的格式和内容。
    """

    REQUIRED_COLUMNS = {'name', 'price'}  # Excel 文件必须包含的列名集合

    @staticmethod
    def is_valid_extension(file_path):
        """
        判断文件扩展名是否是 .xlsx，符合 Excel 文件格式。
        """
        return file_path.endswith('.xlsx')

    @staticmethod
    def has_required_columns(file_path):
        """
        读取 Excel 文件，检查是否包含所有必需的列。
        
        返回：
        - (True, "") 如果文件包含所有必须的列。
        - (False, 错误消息) 如果缺少某些列或读取文件出错。
        """
        try:
            df = pd.read_excel(file_path)  # 读取 Excel 文件为 DataFrame
            missing = Validator.REQUIRED_COLUMNS - set(df.columns)  # 计算缺失列
            if missing:
                return False, f"Excel 文件缺少以下列: {', '.join(missing)}"
            return True, ""
        except Exception as e:
            # 读取 Excel 过程中出现异常时，返回失败和异常信息
            return False, f"读取 Excel 文件时出错: {str(e)}"
