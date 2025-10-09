import os
import json
import re
from tkinter import messagebox

def load_cache(file_path='cache.json'):
    if os.path.exists(file_path):
        with open(file_path, encoding='utf-8') as f:
            return json.load(f)
    else:
        messagebox.showwarning(
            "警告",
            "缓存为空。请先上传一个 Excel 文件。"
        )
        return None
    
def generate_product_map(products):
    sku_product_map = {}

    for product in products:
        price = product.get("price")
        for sku in product.get("skus", []):
            if sku not in sku_product_map or price < sku_product_map[sku]["price"]:
                sku_product_map[sku] = product

    return sku_product_map

def wrap_number(text, key=None, direction="forward"):
    inside_brackets = False

    pattern = re.compile(r"(?<![\[\d])(\d+(?:\s*[.,]\s*\d+)?)(?![\d\]])")

    if direction == "forward":
        i = 0
        while i < len(text):
            if text[i] == "[":
                inside_brackets = True
            elif text[i] == "]":
                inside_brackets = False

            if not inside_brackets:
                match = pattern.search(text, i)
                if match:
                    raw_number = match.group(1)
                    start_pos, end_pos = match.span(1)
                    clean_number = re.sub(r"\s*", "", raw_number)

                    replacement = f"[{key}:{clean_number}]" if key else f"[{clean_number}]"
                    return text[:start_pos] + replacement + text[end_pos:]
                break
            i += 1

    elif direction == "backward":
        i = len(text) - 1
        while i >= 0:
            if text[i] == "]":
                inside_brackets = True
            elif text[i] == "[":
                inside_brackets = False

            if not inside_brackets:
                matches = list(pattern.finditer(text[:i + 1]))
                if matches:
                    match = matches[-1]
                    raw_number = match.group(1)
                    start_pos, end_pos = match.span(1)

                    clean_number = re.sub(r"\s*", "", raw_number)
                    replacement = f"[{key}:{clean_number}]" if key else f"[{clean_number}]"
                    return text[:start_pos] + replacement + text[end_pos:]
                break
            i -= 1

    return text

def wrap_letter(text, letters, key=None, ignore_case=True):
    last_char = text[-1]

    if ignore_case:
        last_char = last_char.lower()
        letters = [letter.lower() for letter in letters]

    if last_char in letters:
        if len(text) == 1 or text[-2] in [' ', '\n', '\t']:
            replacement = f"[{key}:{last_char}]" if key else f"[{last_char}]"
            return text[:-1] + replacement
    return text

def wrap_number_to_lines(text, key=None, direction="forward"):
    lines = text.splitlines()
    wrapped_lines = [wrap_number(line, key=key, direction=direction) for line in lines]
    return "\n".join(wrapped_lines)

def wrap_letter_to_lines(text, letters, key=None, ignore_case=True):
    lines = text.splitlines()
    wrapped_lines = [wrap_letter(line, letters, key=key, ignore_case=ignore_case) for line in lines]
    return "\n".join(wrapped_lines)

def generate_aliases(name: str) -> list:
    parts = name.split('-')
    if not parts:
        return []

    first_part = parts[0]
    rest = parts[1:]

    if '/' in first_part:
        aliases = first_part.split('/')
        return [f"{alias}-{'-'.join(rest)}" for alias in aliases]
    else:
        return [name]
