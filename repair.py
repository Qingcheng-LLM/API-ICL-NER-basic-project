
import json
from typing import Any
from json_repair import repair_json

#解析并修复 JSON 字符串
def repair_and_load(text: str) -> Any:
    fixed = repair_json(text)
    try:
        return json.loads(fixed)
    except Exception as e:# 解析仍然失败，就返回一个包含错误信息的字典
        return {
            "error": f"json.loads failed: {e}",
            "raw_output": text,
            "fixed_text": fixed,
        }
