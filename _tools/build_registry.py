"""扫描 modules/ 生成 registry.json（模块仓库的可用模块清单）。

DGStudio「模块」页从该清单获取可下载模块：id、名称、版本、描述、
依赖声明与文件列表。推送前运行（CI 亦会自动重建并提交）：

    python _tools/build_registry.py

规则：
* 每个模块一个文件夹 modules/<id>/，至少含 plugin.py（META 纯字面量）；
* META["id"] 必须与文件夹同名；dependencies 为 pip 依赖串列表，
  「!」前缀表示可选依赖（--no-deps 尽力安装）；
* files 列出模块内全部文件（相对模块目录），供逐文件下载回退使用。
"""
from __future__ import annotations

import ast
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD_ROOT = os.path.join(ROOT, "modules")
SKIP_DIRS = {"__pycache__"}
SKIP_EXT = {".pyc", ".pyo"}


def read_meta(plugin_py: str) -> dict:
    with open(plugin_py, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "META":
                value = ast.literal_eval(node.value)
                return value if isinstance(value, dict) else {}
    raise ValueError(f"{plugin_py} 未找到 META 字面量")


def list_files(folder: str) -> list[str]:
    out: list[str] = []
    for cur, dirs, names in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in sorted(names):
            if os.path.splitext(name)[1].lower() in SKIP_EXT:
                continue
            out.append(os.path.relpath(os.path.join(cur, name),
                                       folder).replace(os.sep, "/"))
    return sorted(out)


def main() -> int:
    entries = []
    for entry in sorted(os.listdir(MOD_ROOT)):
        folder = os.path.join(MOD_ROOT, entry)
        plugin_py = os.path.join(folder, "plugin.py")
        if not os.path.isfile(plugin_py):
            continue
        meta = read_meta(plugin_py)
        module_id = str(meta.get("id") or entry)
        if module_id != entry:
            print(f"[错误] META id ({module_id}) 与文件夹名 ({entry}) 不一致",
                  file=sys.stderr)
            return 1
        entries.append({
            "id": module_id,
            "name": str(meta.get("name") or module_id),
            "version": str(meta.get("version") or "0.1.0"),
            "description": str(meta.get("description") or ""),
            "dependencies": [str(d) for d in (meta.get("dependencies") or [])],
            "path": f"modules/{module_id}",
            "files": list_files(folder),
        })
        print(f"[模块] {module_id} v{entries[-1]['version']} "
              f"({len(entries[-1]['files'])} 个文件)")

    registry = {"schema": 1, "modules": entries}
    out_path = os.path.join(ROOT, "registry.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"已写入 {out_path}（{len(entries)} 个模块）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
