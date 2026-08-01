#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 /blog 目录下的 .md 文件，生成 blog/manifest.json。
前端通过读取 manifest.json 获取文章列表，再 fetch 单个 md 渲染。
这样无需调用 GitHub API，纯静态即可工作。

用法： python build-blog.py
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BLOG_DIR = ROOT / "blog"
OUTPUT = BLOG_DIR / "manifest.json"

FM_RE = re.compile(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$")


def parse_frontmatter(content):
    m = FM_RE.match(content)
    if not m:
        return {}, content
    fm = {}
    for line in m.group(1).splitlines():
        idx = line.find(":")
        if idx > -1:
            fm[line[:idx].strip()] = line[idx + 1:].strip()
    return fm, m.group(2)


def first_h1(body):
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else None


def main():
    if not BLOG_DIR.exists():
        print(f"[blog] 目录不存在: {BLOG_DIR}", file=sys.stderr)
        return 1

    posts = []
    for md in sorted(BLOG_DIR.glob("*.md")):
        name = md.name.lower()
        if name in ("index.md", "readme.md"):
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[blog] 读取失败 {md.name}: {e}", file=sys.stderr)
            continue
        fm, body = parse_frontmatter(content)
        slug = md.stem
        posts.append({
            "slug": slug,
            "file": md.name,
            "title": fm.get("title") or first_h1(body) or slug,
            "date": fm.get("date", ""),
            "tags": fm.get("tags", ""),
        })

    posts.sort(key=lambda p: p["date"], reverse=True)

    OUTPUT.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[blog] 已生成 {OUTPUT.relative_to(ROOT)}，共 {len(posts)} 篇文章")
    return 0


if __name__ == "__main__":
    sys.exit(main())
