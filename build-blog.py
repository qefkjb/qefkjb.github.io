#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 /blog 和 /projects 目录下的 .md 文件，分别生成 manifest.json。
前端通过读取 manifest.json 获取列表，再 fetch 单个 md 渲染。
纯静态工作，无需 GitHub API。

用法： python build-blog.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 支持的内容目录：每项为 (目录名, 排序字段)
# date 降序（按日期，新→旧）；order 升序（自定义排序，小→大）
SECTIONS = [
    ("blog", "date"),
    ("projects", "order"),
]

FM_RE = re.compile(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$")


def parse_frontmatter(content):
    m = FM_RE.match(content)
    if not m:
        return {}, content
    fm = {}
    for line in m.group(1).splitlines():
        idx = line.find(":")
        if idx > -1:
            val = line[idx + 1:].strip()
            # 去掉首尾成对引号
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]
            fm[line[:idx].strip()] = val
    return fm, m.group(2)


def first_h1(body):
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else None


def build_section(dir_name, sort_key):
    """扫描指定目录的 .md，生成 manifest.json"""
    section_dir = ROOT / dir_name
    if not section_dir.exists():
        print(f"[{dir_name}] 目录不存在: {section_dir}", file=sys.stderr)
        return 0

    items = []
    for md in sorted(section_dir.glob("*.md")):
        name = md.name.lower()
        if name in ("index.md", "readme.md"):
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[{dir_name}] 读取失败 {md.name}: {e}", file=sys.stderr)
            continue
        fm, body = parse_frontmatter(content)
        slug = md.stem
        item = {
            "slug": slug,
            "file": md.name,
            "title": fm.get("title") or first_h1(body) or slug,
            "date": fm.get("date", ""),
            "tags": fm.get("tags", ""),
        }
        # projects 额外字段
        if dir_name == "projects":
            item["order"] = fm.get("order", "9999")
            item["emoji"] = fm.get("emoji", "📄")
            item["summary"] = fm.get("summary", "")
            item["link"] = fm.get("link", "")
        items.append(item)

    # 排序：date 降序（新→旧）；order 升序（小→大），同 order 时日期降序
    if sort_key == "date":
        items.sort(key=lambda p: p["date"], reverse=True)
    else:
        items.sort(key=lambda p: (p.get("order", "9999"), "".join(reversed(p.get("date", "")))))

    output = section_dir / "manifest.json"
    output.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{dir_name}] 已生成 {output.relative_to(ROOT)}，共 {len(items)} 项")
    return len(items)


def main():
    total = 0
    for dir_name, sort_key in SECTIONS:
        total += build_section(dir_name, sort_key)
    print(f"全部完成，共 {total} 项")
    return 0


if __name__ == "__main__":
    sys.exit(main())
