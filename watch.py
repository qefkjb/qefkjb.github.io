#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监听 /blog 和 /projects 目录下的 .md 文件变化，自动重建 manifest.json。
省去每次手动跑 build-blog.py 的麻烦。

用法：
    python watch.py

依赖：
    pip install watchdog

按 Ctrl+C 退出。
"""
import subprocess
import sys
import time
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    print("缺少依赖，正在安装 watchdog ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog"])
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

ROOT = Path(__file__).resolve().parent
WATCH_DIRS = [ROOT / "blog", ROOT / "projects"]
# 延迟时间（秒）：短时间内的多次修改合并为一次重建
DEBOUNCE = 0.8


class MdChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_run = 0.0

    def _maybe_rebuild(self, reason):
        now = time.time()
        if now - self._last_run < DEBOUNCE:
            return  # 防抖：忽略短时间内的重复触发
        self._last_run = now
        print(f"\n[watch] 检测到变化（{reason}），重建 manifest...")
        try:
            subprocess.run(
                [sys.executable, "build-blog.py"],
                cwd=str(ROOT),
                check=True,
                capture_output=True,
                text=True,
            )
            print("[watch] 重建完成，刷新浏览器即可（Ctrl+F5 强制刷新）")
        except subprocess.CalledProcessError as e:
            print(f"[watch] 重建失败：\n{e.stderr}")
            print("[watch] 等待下次变化继续尝试...")

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            self._maybe_rebuild(f"修改 {Path(event.src_path).name}")

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            self._maybe_rebuild(f"新建 {Path(event.src_path).name}")

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            self._maybe_rebuild(f"删除 {Path(event.src_path).name}")

    def on_moved(self, event):
        if not event.is_directory and event.dest_path.endswith(".md"):
            self._maybe_rebuild(f"重命名 {Path(event.dest_path).name}")


def main():
    print("=" * 50)
    print("  博客 manifest 自动重建监听器")
    print("=" * 50)
    print(f"  监听目录：")
    for d in WATCH_DIRS:
        print(f"    - {d}")
    print(f"  防抖延迟：{DEBOUNCE}s")
    print("  按 Ctrl+C 退出")
    print("=" * 50)

    # 启动时先重建一次，确保 manifest 最新
    print("\n[watch] 启动时先重建一次 manifest...")
    try:
        subprocess.run(
            [sys.executable, "build-blog.py"],
            cwd=str(ROOT),
            check=True,
        )
    except subprocess.CalledProcessError:
        print("[watch] 初始重建失败，仍继续监听")

    observer = Observer()
    handler = MdChangeHandler()
    for d in WATCH_DIRS:
        if d.exists():
            observer.schedule(handler, str(d), recursive=False)
        else:
            print(f"[watch] 警告：目录不存在 {d}")

    observer.start()
    print("\n[watch] 开始监听...（编辑 md 后会自动重建，浏览器需手动刷新）\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[watch] 收到退出信号，停止监听...")
        observer.stop()
    observer.join()
    print("[watch] 已退出")


if __name__ == "__main__":
    main()
