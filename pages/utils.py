import os
import json
import re
from tkinter import messagebox

def load_cache(file_path='cache.json'):
    """
    加载缓存文件。如果缓存文件存在，返回其内容（JSON格式）。
    如果文件不存在，显示警告信息，提示用户先上传 Excel 文件。
    :param file_path: 缓存文件的路径，默认为 'cache.json'
    :return: 缓存文件的内容（字典格式），如果文件不存在则返回 None。
    """
    if os.path.exists(file_path):
        with open(file_path, encoding='utf-8') as f:
            return json.load(f)  # 解析 JSON 格式的缓存文件内容
    else:
        # 文件不存在时，弹出警告框
        messagebox.showwarning(
            "警告",
            "缓存为空。请先上传一个 Excel 文件。"
        )
        return None  # 返回 None，表示没有找到缓存文件
    
def generate_product_map(products):
    """
    生成 SKU 到产品的映射表。此函数根据产品的 SKU 和价格来构建映射。
    如果一个 SKU 已经存在，但当前产品的价格更低，则会更新映射。
    :param products: 产品列表，每个产品是一个字典，包含 'skus' 和 'price' 等字段。
    :return: 一个字典，键为 SKU，值为对应的产品信息。
    """
    sku_product_map = {}

    for product in products:
        price = product.get("price")  # 获取产品价格
        for sku in product.get("skus", []):  # 遍历该产品的所有 SKU
            # 如果 SKU 不在映射表中，或者当前产品价格更低，则更新映射
            if sku not in sku_product_map or price < sku_product_map[sku]["price"]:
                sku_product_map[sku] = product  # 更新 SKU 对应的产品信息

    return sku_product_map  # 返回 SKU 到产品的映射表

def wrap_number(text, key=None, direction="forward"):
    """
    将文本中的数字进行包裹，包裹形式为 [key:数字] 或 [数字]。
    该函数根据指定的方向（"forward" 或 "backward"）来选择处理方向。
    :param text: 输入文本，包含需要处理的数字
    :param key: 如果提供了 key，则格式为 [key:数字]，否则格式为 [数字]
    :param direction: 处理方向，"forward" 从前往后处理，"backward" 从后往前处理
    :return: 处理后的文本
    """
    inside_brackets = False  # 用于标记是否在方括号内

    # 正则表达式，用于匹配数字（可能包含小数）
    pattern = re.compile(r"(?<![\[\d])(\d+(?:\s*[.,]\s*\d+)?)(?![\d\]])")

    if direction == "forward":
        # 从文本开头开始遍历
        i = 0
        while i < len(text):
            if text[i] == "[":
                inside_brackets = True
            elif text[i] == "]":
                inside_brackets = False

            if not inside_brackets:
                match = pattern.search(text, i)  # 查找数字
                if match:
                    raw_number = match.group(1)  # 获取原始数字
                    start_pos, end_pos = match.span(1)  # 获取匹配的开始和结束位置
                    clean_number = re.sub(r"\s*", "", raw_number)  # 清理数字中的空格

                    # 根据是否提供 key 来决定包裹格式
                    replacement = f"[{key}:{clean_number}]" if key else f"[{clean_number}]"
                    return text[:start_pos] + replacement + text[end_pos:]
                break
            i += 1

    elif direction == "backward":
        # 从文本结尾开始遍历
        i = len(text) - 1
        while i >= 0:
            if text[i] == "]":
                inside_brackets = True
            elif text[i] == "[":
                inside_brackets = False

            if not inside_brackets:
                matches = list(pattern.finditer(text[:i + 1]))  # 查找所有数字的匹配项
                if matches:
                    match = matches[-1]  # 选择最后一个匹配
                    raw_number = match.group(1)
                    start_pos, end_pos = match.span(1)

                    clean_number = re.sub(r"\s*", "", raw_number)  # 清理数字中的空格
                    replacement = f"[{key}:{clean_number}]" if key else f"[{clean_number}]"
                    return text[:start_pos] + replacement + text[end_pos:]
                break
            i -= 1

    return text  # 如果没有找到数字，则返回原文本

def wrap_number_to_lines(text, key=None, direction="forward"):
    """
    将文本中的每一行数字进行包裹处理。调用 wrap_number 函数来处理每一行的数字。
    :param text: 输入文本
    :param key: 如果提供了 key，则格式为 [key:数字]，否则格式为 [数字]
    :param direction: 处理方向，"forward" 从前往后，"backward" 从后往前
    :return: 处理后的文本
    """
    lines = text.splitlines()  # 按行拆分文本
    wrapped_lines = [wrap_number(line, key=key, direction=direction) for line in lines]  # 对每一行调用 wrap_number 进行处理
    return "\n".join(wrapped_lines)  # 将处理后的行合并成一个文本

def wrap_letter(text, letters, key=None, ignore_case=True):
    """
    将文本中的字母进行包裹处理。如果文本以指定字母结尾，则将其包裹为 [key:字母] 或 [字母]。
    :param text: 输入文本
    :param letters: 要处理的字母列表
    :param key: 如果提供了 key，则格式为 [key:字母]，否则格式为 [字母]
    :param ignore_case: 是否忽略大小写，默认为 True
    :return: 处理后的文本
    """
    last_char = text[-1]  # 获取文本的最后一个字符

    if ignore_case:
        last_char = last_char.lower()  # 转为小写字母
        letters = [letter.lower() for letter in letters]  # 转换字母列表为小写字母

    if last_char in letters:
        if len(text) == 1 or text[-2] in [' ', '\n', '\t']:  # 如果是单个字母，或者前一个字符是空格、换行或制表符
            replacement = f"[{key}:{last_char}]" if key else f"[{last_char}]"
            return text[:-1] + replacement  # 替换最后一个字母
    return text  # 如果没有匹配字母，返回原文本

def wrap_letter_to_lines(text, letters, key=None, ignore_case=True):
    """
    将文本中的每一行字母进行包裹处理。调用 wrap_letter 函数来处理每一行的字母。
    :param text: 输入文本
    :param letters: 要处理的字母列表
    :param key: 如果提供了 key，则格式为 [key:字母]，否则格式为 [字母]
    :param ignore_case: 是否忽略大小写
    :return: 处理后的文本
    """
    lines = text.splitlines()  # 按行拆分文本
    wrapped_lines = [wrap_letter(line, letters, key=key, ignore_case=ignore_case) for line in lines]  # 对每一行调用 wrap_letter 进行处理
    return "\n".join(wrapped_lines)  # 将处理后的行合并成一个文本

def generate_aliases(name: str) -> list:
    """
    根据给定的名称生成别名。如果名称包含 '-'，则通过拆分名称并根据 '/' 创建别名。
    :param name: 输入的名称
    :return: 返回生成的别名列表
    """
    parts = name.split('-')  # 按 '-' 拆分名称
    if not parts:
        return []

    first_part = parts[0]
    rest = parts[1:]

    if '/' in first_part:
        aliases = first_part.split('/')  # 如果名称的第一部分包含 '/'，则按 '/' 拆分
        return [f"{alias}-{'-'.join(rest)}" for alias in aliases]  # 为每个别名生成新的名称
    else:
        return [name]  # 如果没有 '/'，返回原名称作为别名
