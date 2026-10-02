# DGStudio 模块市场（dgstudio-modules-market）

本仓库是 **DGStudio**（[DG-LAB-X-VRChat-OSC](https://github.com/KelierAndes/DG-LAB-X-VRChat-OSC)）
的**模块市场总仓库**，采用与 AstrBot 插件生态一致的仓库管理方式：

* **每个联动模块一个独立仓库**，命名 `dgstudio-modules-<模块 id>`；
* 本总仓库通过 **GitHub Actions** 自动发现、拉取并解析各子仓库，
  生成统一的市场清单 [`market.yaml`](market.yaml)；
* DGStudio「模块」页（模组市场）**只读取 market.yaml** 这一个配置文件，
  下载模块时再按清单指向的子仓库取文件。

```
dgstudio-modules-osc_bridge ─────┐
dgstudio-modules-alice_cradle ───┤   GitHub Actions（每日 / 手动）
dgstudio-modules-vision_link ────┼──────────────────────► market.yaml ◄── DGStudio 模块页读取
dgstudio-modules-strength_logger─┘      拉取 + 解析 META / requirements.txt
```

## 模块列表

| 模块 | 仓库 | 版本 | 依赖 | 说明 |
|---|---|---|---|---|
| **VRChat OSC 联动** | [dgstudio-modules-osc_bridge](https://github.com/KelierAndes/dgstudio-modules-osc_bridge) | 1.5.0 | `python-osc` | 头像参数动态建表，核心参数映射表双向表达式驱动 |
| **Alice in Cradle 联动** | [dgstudio-modules-alice_cradle](https://github.com/KelierAndes/dgstudio-modules-alice_cradle) | 0.6.0 | 无（标准库） | 游戏侧 MOD 上报 HP/MP 等数值，映射表求值驱动设备并回传状态；携带 BepInEx 游戏模组 |
| **画面识别联动** | [dgstudio-modules-vision_link](https://github.com/KelierAndes/dgstudio-modules-vision_link) | 0.3.1 | `opencv-python-headless`（OCR 可选） | OpenCV 检测屏幕画面（颜色/图片/数值/数值条）产生实时参数 |
| **强度日志示例** | [dgstudio-modules-strength_logger](https://github.com/KelierAndes/dgstudio-modules-strength_logger) | 0.1.0 | 无（标准库） | 最小完整示例：订阅强度变化写入日志，可作开发模板 |

实际可用版本以 [`market.yaml`](market.yaml) 为准。

## 安装方式

### 方式一：DGStudio「模块」页（推荐）

1. 打开 DGStudio → 左侧导航「模块」→「获取在线列表」（首次打开自动获取）；
2. 点「下载」取回模块文件（自动放入应用目录 `modules/`）；
3. 点「安装并启动」——安装时**自动读取模块仓库的 `requirements.txt`** 并
   pip 补装依赖，无需手动处理；卸载 / 更新均**热重载**生效，无需重启。

之后可在「模块」页启停 / 卸载 / 删除，有新版本时在线列表会出现「更新」按钮。

### 方式二：手动放置

把子仓库内容整个放入 DGStudio 应用目录 `modules/<模块 id>/`，重启（或点
「扫描模块目录」）后即可在模块页看到；第三方依赖需自行
`pip install -r requirements.txt`。

## 发布一个新模块

1. 新建仓库，命名 **`dgstudio-modules-<模块 id>`**（必须以该前缀开头）；
2. 仓库根放置：
   * `plugin.py` —— 模块入口（`META` 纯字面量 + 模块类），`META["id"]` 与
     仓库后缀一致；
   * `requirements.txt` —— pip 依赖串列表（可选文件；「!」前缀 = 可选依赖，
     以 `--no-deps` 尽力安装、失败不阻断）；
   * `README.md` —— 会随模块一起下载到用户本地；
3. 推送后等待 Actions 重建（每日自动，或到总仓库手动 Run workflow
   「build market」），`market.yaml` 出现你的模块即上架；
4. 也可以在总仓库的 [`sources.txt`](sources.txt) 里追加一行仓库名作为兜底。

更新模块 = 子仓库提交新版本 + 等待/触发总仓库重建 market.yaml + 用户在
模块页点「更新」。

## 清单生成

* `_tools/build_market.py`：
  * CI 模式（默认）：`GITHUB_TOKEN` 经 GitHub API 搜索 `dgstudio-modules-`
    前缀仓库 → 逐仓库读取 `plugin.py`（AST 解析 META）、`requirements.txt`、
    文件树，写出 `market.yaml`；
  * 本地模式（`--local <目录>`）：扫描目录下匹配前缀的仓库文件夹直接生成，
    便于离线开发；
* `.github/workflows/market.yml`：push / 每日定时 / 手动触发，重建后自动提交。

## 开发文档

模块 API（生命周期、`ModuleContext`、配置声明、按键动作、联动参数模型）见
**[EXTENSIONS.md](EXTENSIONS.md)**。

## 许可

与 DGStudio 相同，以 **GNU General Public License v3.0**（GPL-3.0）发布，
全文见 [LICENSE](LICENSE)。各模块仓库同许可；模块运行于 DGStudio 宿主并
链接其核心代码。
