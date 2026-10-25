"""界面层：customtkinter 主窗口。

布局：
- 顶部：标题 + 当前连续 / 历史最长 / 总篇数
- 左栏：日期列表（历史回看 + 补卡入口）
- 右栏：正文编辑框 + 保存按钮
"""
from __future__ import annotations

from datetime import date, timedelta

import customtkinter as ctk

import storage
import streak

APP_TITLE = "日记打卡"


class DiaryApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("820x560")
        self.minsize(640, 440)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self._selected_date: date = date.today()
        self._build_widgets()
        self._refresh()

    # ---- 界面构建 ----
    def _build_widgets(self) -> None:
        # 顶部统计
        self.stats_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.stats_label.pack(pady=(16, 8), padx=16, anchor="w")

        # 主体：左列表 + 右编辑
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        # 左栏
        left = ctk.CTkFrame(body)
        left.pack(side="left", fill="y", padx=(0, 12))

        ctk.CTkLabel(left, text="日期 / 补卡", font=ctk.CTkFont(size=14, weight="bold")).pack(
            pady=(12, 6)
        )
        self.date_list = ctk.CTkScrollableFrame(left, width=220)
        self.date_list.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.btn_today = ctk.CTkButton(left, text="写今天", command=self._goto_today)
        self.btn_today.pack(fill="x", padx=8, pady=(0, 4))
        self.btn_yesterday = ctk.CTkButton(
            left, text="补写昨天", command=self._goto_yesterday, fg_color="transparent",
            border_width=1, text_color=("gray20", "gray80"),
        )
        self.btn_yesterday.pack(fill="x", padx=8, pady=(0, 12))

        # 右栏
        right = ctk.CTkFrame(body)
        right.pack(side="left", fill="both", expand=True)

        self.editor_title = ctk.CTkLabel(
            right, text="", font=ctk.CTkFont(size=15, weight="bold")
        )
        self.editor_title.pack(pady=(12, 4), padx=12, anchor="w")

        self.text = ctk.CTkTextbox(right, wrap="word", font=ctk.CTkFont(size=14))
        self.text.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        self.save_btn = ctk.CTkButton(right, text="保存", command=self._save)
        self.save_btn.pack(padx=12, pady=(0, 12), anchor="e")

        self.status_label = ctk.CTkLabel(right, text="", text_color=("gray40", "gray60"))
        self.status_label.pack(padx=12, pady=(0, 8), anchor="w")

    # ---- 刷新逻辑 ----
    def _refresh(self) -> None:
        dates = storage.all_dates()
        today = date.today()
        current, longest = streak.compute_streak(dates, today)
        total = len(dates)

        self.stats_label.configure(
            text=f"🔥 当前连续 {current} 天    🏆 历史最长 {longest} 天    📖 共 {total} 篇"
        )
        self._refresh_date_list(dates)
        self._load_editor()

    def _refresh_date_list(self, dates: list[date]) -> None:
        for w in self.date_list.winfo_children():
            w.destroy()

        today = date.today()
        if not dates:
            ctk.CTkLabel(self.date_list, text="还没有日记\n点「写今天」开始", text_color=("gray40", "gray60")).pack(pady=12)
            return

        for d in reversed(dates):  # 最新在上
            label = f"{d.isoformat()} {'· 今天' if d == today else ''}"
            btn = ctk.CTkButton(
                self.date_list, text=label, anchor="w", height=32,
                fg_color="transparent", text_color=("gray20", "gray80"),
                hover_color=("gray80", "gray25"),
                command=lambda dd=d: self._select_date(dd),
            )
            btn.pack(fill="x", pady=1)

    def _load_editor(self) -> None:
        d = self._selected_date
        entry = storage.load_entry(d)
        self.editor_title.configure(text=f"{d.isoformat()}  {_weekday_cn(d)}")
        self.text.delete("1.0", "end")
        if entry:
            self.text.insert("1.0", entry.get("content", ""))
        self.status_label.configure(text="")

    # ---- 事件 ----
    def _select_date(self, d: date) -> None:
        self._selected_date = d
        self._load_editor()

    def _goto_today(self) -> None:
        self._selected_date = date.today()
        self._load_editor()
        self.text.focus_set()

    def _goto_yesterday(self) -> None:
        self._selected_date = date.today() - timedelta(days=1)
        self._load_editor()
        self.text.focus_set()

    def _save(self) -> None:
        content = self.text.get("1.0", "end").strip()
        if not content:
            self.status_label.configure(text="内容为空，没保存", text_color=("gray40", "gray60"))
            return
        storage.save_entry(self._selected_date, content)
        self.status_label.configure(text=f"已保存 {self._selected_date.isoformat()}", text_color=("green", "lightgreen"))
        self._refresh()


def _weekday_cn(d: date) -> str:
    return ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()]
