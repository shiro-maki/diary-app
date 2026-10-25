"""存储层：日记的读写，一天一个 JSON 文件。

数据目录：<项目>/data/YYYY/YYYY-MM-DD.json
JSON 结构：{"date": "YYYY-MM-DD", "content": "正文", "created_at": ISO, "updated_at": ISO}
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional


def _data_dir() -> Path:
    """数据目录，固定在项目根下的 data/。"""
    return Path(__file__).resolve().parent / "data"


def _file_for(day: date) -> Path:
    """某一天对应的 JSON 文件路径。"""
    return _data_dir() / f"{day.year}" / f"{day.isoformat()}.json"


def save_entry(day: date, content: str) -> Path:
    """保存（或覆盖）某一天的日记，返回文件路径。"""
    day_str = day.isoformat()
    path = _file_for(day)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing = load_entry(day)
    created_at = existing["created_at"] if existing else datetime.now().isoformat(timespec="seconds")

    payload = {
        "date": day_str,
        "content": content,
        "created_at": created_at,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_entry(day: date) -> Optional[dict]:
    """读取某一天的日记，不存在返回 None。"""
    path = _file_for(day)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def all_dates() -> list[date]:
    """扫描数据目录，返回所有已写日记的日期（升序）。"""
    result: list[date] = []
    root = _data_dir()
    if not root.exists():
        return result

    for year_dir in sorted(root.iterdir()):
        if not year_dir.is_dir():
            continue
        for f in year_dir.glob("*.json"):
            stem = f.stem  # e.g. 2026-10-25
            try:
                result.append(date.fromisoformat(stem))
            except ValueError:
                continue
    return sorted(result)


def count_entries() -> int:
    """已写日记总篇数。"""
    return len(all_dates())
