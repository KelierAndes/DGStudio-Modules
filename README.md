# DGStudio 联动模块仓库（DGStudio-Modules）

本仓库托管 **DGStudio**（[DG-LAB-X-VRChat-OSC](https://github.com/KelierAndes/DG-LAB-X-VRChat-OSC)）
的联动模块。软件核心只内置「初始化配置」模块，其余联动能力全部在这里维护、
由 DGStudio「模块」页**按需下载**：软件直接检索本仓库的 `registry.json`
清单获取可用模块列表，下载后即可实时装卸。

## 可用模块

| 模块 | 版本 | 依赖 | 说明 |
|---|---|---|---|
| **VRChat OSC 联动** (`osc_bridge`) | 1.5.0 | `python-osc` | 头像参数动态建表，核心参数映射表双向表达式驱动 |
| **Alice in Cradle 联动** (`alice_cradle`) | 0.6.0 | 无（标准库） | 游戏侧 MOD 上报 HP/MP 等数值，映射表求值驱动设备并回传状态；携带 BepInEx 游戏模组 |
| **画面识别联动** (`vision_link`) | 0.3.1 | `opencv-python-headless`，OCR 增强可选 | OpenCV 检测屏幕画面（颜色/图片/数值/数值条）产生实时参数 |
| **强度日志示例** (`strength_logger`) | 0.1.0 | 无（标准库） | 最小完整示例：订阅强度变化写入日志，可作开发模板 |

版本以 [`registry.json`](registry.json) 为准（推送时自动重建）。

## 安装方式

### 方式一：DGStudio「模块」页（推荐）

1. 打开 DGStudio → 左侧导航「模块」；
2. 「获取在线列表」检索本仓库清单；
3. 点「下载」取回模块文件（自动放入应用目录 `modules/`）；
4. 点「安装并启动」——声明的依赖会由 pip 自动补装，无需手动处理。

之后可在「模块」页启停 / 卸载，有新版本时在线列表会出现「更新」按钮。

### 方式二：手动放置

把本仓库 `modules/<模块 id>/` 整个文件夹拷贝到 DGStudio 应用目录的
`modules/` 下，重启（或点「扫描模块目录」）后即可在模块页看到。
第三方依赖需自行安装，如 `pip install python-osc`。

## 模块依赖

依赖在各自 `modules/<id>/plugin.py` 的 `META["dependencies"]` 中声明
（pip 依赖串列表），安装模块时自动附加：

```python
META = {
    ...,
    "dependencies": ["python-osc>=1.9"],
}
```

* 源码运行：装进当前解释器环境；
* 打包 exe：装进模块私有 `modules/<id>/_deps/`（宿主装载时自动挂到 `sys.path`）；
* 「!」前缀 = 可选依赖：以 `--no-deps` 尽力安装、失败不阻断（vision_link 的
  OCR 增强即如此，未装时自动回退内置模板匹配）。

## 开发自己的模块

开发文档见 **[EXTENSIONS.md](EXTENSIONS.md)**（模块 API、生命周期、配置声明、
按键动作、联动参数模型与示例）。快速路径：

1. Fork / 克隆本仓库；
2. 复制 `modules/strength_logger/` 改名，编辑 `META` 与模块类；
3. 运行 `python _tools/build_registry.py` 重建清单；
4. 提交推送后，DGStudio「模块」页即可检索到你的模块。

单测在 `tests/`，需要 DGStudio 核心源码：克隆核心仓库到本仓库同级目录，
或设置环境变量 `DGSTUDIO_CORE` 指向核心根目录，然后：

```bat
python -m unittest discover -s tests
```

## 清单与发布流程

`registry.json` 由 `_tools/build_registry.py` 从各模块 `META` 生成，
推送 main 分支时 GitHub Actions 会自动重建并提交；也可本地手动运行。
DGStudio 通过 raw.githubusercontent.com（jsdelivr、GitHub API 兜底）获取
清单，通过 codeload zip（逐文件回退）下载模块。

## 许可

与 DGStudio 相同，以 **GNU General Public License v3.0**（GPL-3.0）发布，
全文见 [LICENSE](LICENSE)。模块运行于 DGStudio 宿主并链接其核心代码。
