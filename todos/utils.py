import hashlib
import json
from typing import Dict, Any


def generate_todo_cache_key(filters: Dict[str, Any], limit: int, offset: int) -> str:
    filters_str = json.dumps(filters, sort_keys=True)
    key_data = f"todos_list:{filters_str}:{limit}:{offset}"

    key_hash = hashlib.md5(key_data.encode()).hexdigest()
    return f"todos:{key_hash}"
