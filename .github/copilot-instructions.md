# Copilot 使用说明（为 AI 编码代理准备）

目的：快速让 AI 代理理解并在本仓库中高效工作 — 项目结构、关键约定、运行/调试流程和可复用模式。

1) 大体架构与入口
- 运行入口：`main.py`（主游戏类 `Game` 在此创建并组织 `ResourceLoader`、`SaveManager`、`VoiceManager` 与 `PagesGroup`）。参见 [main.py](main.py).
- 主要子系统：资源加载（`ResourceLoader`）、页面框架（`Pages/` 下的 `Page` 子类）、角色模型（`Characters/`）、存档（`SaveManager`）、声音（`VoiceManager`）。

2) 关键文件/目录（要读的首选位置）
- [main.py](main.py)：程序启动与页面/角色/资源协调逻辑。
- [ResourceLoader.py](ResourceLoader.py)：多线程资源加载（`resource/` 目录约定）、`plot_dict`、`font_dict`、`button_dict` 等。
- [SaveManager.py](SaveManager.py)：读写 `save/*.chw`（JSON 格式），含线程读取与 busy-wait 检测函数。
- [Pages/](Pages/)：所有界面页面实现，基类为 [Pages/Page.py](Pages/Page.py)；新增页面需实现 `init/handle_event/draw/reset`。
- [Characters/](Characters/)：角色数据与群组管理，参考 [Characters/Character.py](Characters/Character.py) 与 `CharacterGroup.py`。
- [settings.py](settings.py) 与 `config.json`：分辨率、全屏、音量等配置索引由 `Settings` 与 config.json 决定。

3) 常见模式与约定（项目特有）
- 页面系统：每个 UI/场景是 `Page` 的子类；`PagesGroup` 管理页面集合并控制切换。要将页面暴露给主循环，需在 `main._page_define_()` 中实例化并 `pages_group.add_page(...)`。
- 资源路径约定：`resource/img`, `resource/font`, `resource/plot`, `resource/characters`。`ResourceLoader` 以文件名去除后缀作为键，例如 `resource/plot/C1.json` 被加载为 `plot_dict['C1']`。
- 资源加载：`ResourceLoader.load_all_resource()` 会启动多个线程并用 `current_progress` / `final_progress` 来表示进度；主循环通过 `loader.check_load_finish()` 与 `save_manager.check_load_finish()` 判断是否可以进入交互。
- 存档：保存文件放 `save/`，扩展名为 `.chw`，实际内容为 JSON，`SaveManager` 有 `save_save_data` / `cover_save_data` / `delete_save_data`。

4) 运行与开发工作流（具体命令）
- 运行游戏（依赖 pygame）：
```
python main.py
```
- 依赖在 `pyproject.toml` 中声明（Python >=3.13，`pygame>=2.6.1` 等）。在本地环境中推荐：
```
python -m pip install -U pip
python -m pip install -r requirements.txt  # 如果你生成了 requirements
python -m pip install pygame numpy opencv-python py-spy
```
- 调试要点：主线程依赖 `ResourceLoader` 与 `SaveManager` 的加载完成信号；若要快速跳过加载，可在 `main` 中模拟 `is_load_finish()` 返回 True 或直接构造必要状态供页面初始化。

5) 修改与扩展示例（快速上手）
- 新增页面：在 `Pages/` 下新建文件，继承 `Page` 实现四个方法，并在 `main._page_define_()` 中实例化并加入 `pages_group`。
- 添加新剧情：把 JSON 放 `resource/plot/`，文件名（去掉 .json）会作为场景键被加载到 `ResourceLoader.plot_dict`。
- 新角色素材：放 `resource/characters/<CharacterName>/`，`ResourceLoader.characters_resource_path` 现有条目参见 `ResourceLoader.py`，按格式加载图片并在 `Characters/` 中实现 `Character` 实例化逻辑。

6) 注意事项与陷阱（实务提示）
- `SaveManager.init_save_data()` 与 `ResourceLoader.load_all_resource()` 都使用线程；有些实现使用 busy-wait（例如 `wait_load_finish`），AI 修改时应避免引入死循环或未 join 的线程。
- 路径构造多处使用 `__file__` 切片来推断仓库根路径，Windows 路径分隔符在代码中以 `\` 或 `r"..."` 方式使用，修改路径时请保持一致。
- 音量/分辨率由 `config.json` 的索引控制，直接修改为实际数值会改变与 `Settings` 的契约；首选通过 `settings_scene` 的界面 API 修改并调用 `_save_config_()`。

7) 我需要优先关注的文件（按重要性）
- [main.py](main.py)
- [ResourceLoader.py](ResourceLoader.py)
- [SaveManager.py](SaveManager.py)
- [Pages/Page.py](Pages/Page.py) 与 `Pages/` 下具体页面实现

如果有你希望我补充的细节（例如运行脚本、CI 配置、或把 `pyproject.toml` 转为 `requirements.txt` 的自动化），指出来我会把对应部分补到本文件里并再次提交。 
