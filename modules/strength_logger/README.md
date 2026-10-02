# 强度日志示例（strength_logger）

依赖：无（仅 Python 标准库）。

最小完整示例模块：订阅引擎 `state` 事件，把每台设备 A/B 通道的强度变化写入应用日志（每设备限速 1 条/秒，避免刷屏）。演示了鸭子类型模块类、`ctx.log` / `ctx.events` 基本用法与高频事件限速。

作为开发模板使用：复制本目录、改 `META.id` 与类名，按开发文档（[EXTENSIONS.md](../../EXTENSIONS.md)）实现自己的联动逻辑。
