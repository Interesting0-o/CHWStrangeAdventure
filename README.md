# CHW Strange Adventure

![title](resource/img/title/title.png)

## 介绍

`CHW Strange Adventure` 是一个基于 `Pygame` 的视觉小说（Galgame）引擎 Demo，包含：

- 游戏运行端（窗口渲染、页面/场景管理、角色/对话渲染、音频与存档管理）。
- 一个独立的剧情编辑器 `PlotWriter.py`（Tkinter GUI），用于创建和导出剧情 JSON。

## 联系方式

Email: <EMAIL>

## 快速开始

1. 安装 Python（推荐 3.8+）。
2. 安装依赖：

```bash
pip install pygame
```

（如果需要运行 `PlotWriter.py`，请确保系统上安装有 `tkinter`。）

## 运行游戏

在项目根目录运行：

```bash
python main.py
```

## 使用剧情编辑器

运行 `PlotWriter.py` 可打开图形化编辑器：

```bash
python PlotWriter.py
```

编辑完成后导出 JSON 到本地，然后将 JSON 文件放到 `resource/plot/` 目录即可在游戏中使用。

## 目录与重要文件

- `main.py`：程序入口与 `Game` 协调器。
- `ResourceLoader.py`：并行资源加载器，加载图片/按钮/字体/剧情/角色资源。
- `SaveManager.py`：存档读写（`save/` 下的 `.chw` 文件）。
- `VoiceManager.py`：音频控制（BGM、角色语音、特效通道）。
- `Pages/`：页面集合（`StartPage`、`GameScene`、`SettingsScene` 等）。
- `Elements/`：UI 组件（按钮、下拉、输入框等）。
- `Characters/`：角色定义与贴图加载。
- `resource/`：素材目录（图片、音频、剧情 JSON 等）。

## 开发者提示

- 资源加载是并行进行的，若在开发中希望跳过部分耗时资源以便快速测试，可短时修改 `ResourceLoader.load_all_resource()` 中的线程启动部分。
- 存档文件位于 `save/`，可以直接编辑或删除进行测试，`SaveManager.py` 管理这些文件。
- 建议改进点：
  - 自动计算 `ResourceLoader.final_progress` 以保证进度条准确。
  - 将 `SaveManager.wait_load_finish()` 中的 busy-wait 改为带短 sleep 的等待或使用线程同步原语（Condition/Event）。

## 更新日志

- 2025-10-18: v0.1.0（内部测试阶段）

## 许可与资源声明

项目中使用的部分音频/图像为网络资源或生成资源，请在分发时确认相应授权。

---

如果你希望我把本 `README_UPDATED.md` 的内容替换回仓库根的 `README.md`（覆盖原有文件），我可以再次尝试替换或直接把 `README_UPDATED.md` 重命名为 `README.md`（需覆盖权限）。