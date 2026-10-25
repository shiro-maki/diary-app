"""日记打卡 v1 入口。"""
import ui


def main() -> None:
    app = ui.DiaryApp()
    app.mainloop()


if __name__ == "__main__":
    main()
