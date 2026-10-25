"""连续打卡（streak）计算。

规则（决策记录 2026-10-25）：
- 自然日制：某天写了就算当天打卡。
- 允许补写昨天（补卡），补写后若能与已有连续区间衔接，则连续天数自动续上。
- 历史最长连续永久保留，断签只清空当前连续。
"""
from __future__ import annotations

from datetime import date, timedelta


def compute_streak(dates: list[date], today: date) -> tuple[int, int]:
    """返回 (当前连续天数, 历史最长连续天数)。

    当前连续：从 today（含）往前数，若今天/昨天没写则从最近一天连续区间算起，
    且该区间必须「贴住今天或昨天」才算当前连续（否则当前连续为 0）。
    """
    if not dates:
        return 0, 0

    days = set(dates)
    longest = _longest_run(sorted(days))

    # 当前连续：允许今天没写但昨天写了（连续到昨天仍算连续中）
    current = 0
    cursor = today
    if cursor not in days:
        cursor = today - timedelta(days=1)
    while cursor in days:
        current += 1
        cursor -= timedelta(days=1)
    return current, longest


def _longest_run(sorted_days: list[date]) -> int:
    """连续日期区间的最长长度。"""
    if not sorted_days:
        return 0
    best = run = 1
    prev = sorted_days[0]
    for d in sorted_days[1:]:
        if (d - prev).days == 1:
            run += 1
            best = max(best, run)
        else:
            run = 1
        prev = d
    return best
