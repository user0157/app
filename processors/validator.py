import os
import pandas as pd

class Validator:
    REQUIRED_COLUMNS = {'name', 'price'}

    @staticmethod
    def is_valid_extension(file_path):
        return file_path.endswith('.xlsx')

    @staticmethod
    def has_required_columns(file_path):
        try:
            df = pd.read_excel(file_path)
            missing = Validator.REQUIRED_COLUMNS - set(df.columns)
            if missing:
                return False, f"Excel 文件缺少以下列: {', '.join(missing)}"
            return True, ""
        except Exception as e:
            return False, f"读取 Excel 文件时出错: {str(e)}"
