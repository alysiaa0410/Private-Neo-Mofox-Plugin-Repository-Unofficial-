## 贡献指南（Contributing）

欢迎你为这个插件合集贡献新插件、修复 bug 或优化文档。

### 贡献目标

- **可读性优先**：示例插件应尽量简单、易懂，适合新手二次开发。
- **可运行/可集成**：尽量遵循 MoFox 插件模板的写法（`__init__.py` + `plugin.py` + `README.md`）。
- **不引入不必要依赖**：能用标准库解决就不要拉大依赖。

### 新增一个插件（推荐流程）

1. 复制一个现有插件文件夹作为起点，或使用脚手架生成器（见 `tools/scaffold_mofox_plugin.py`）。
2. 每个插件文件夹至少包含：
   - `__init__.py`（定义 `__plugin_meta__`）
   - `plugin.py`（插件入口类 + 指令/组件）
   - `README.md`（功能/指令/权限节点/注意事项）
3. 在根 `README.md` 的插件列表里补充条目。
4. 运行校验脚本：
   - `python tools/validate_repo.py`
   - （可选）`ruff check .`、`ruff format .`

### 代码风格

- **Python**：推荐使用 Ruff（见 `pyproject.toml`）。
- **类型标注**：鼓励写，但不强制做到极致；以“新手能看懂”为标准。
- **错误处理**：指令入口处尽量给用户友好提示，避免异常直接炸出堆栈。

### 发布到 MoFox 官方插件索引的建议

这个仓库是“合集/示例”，在实际提交到官方索引（`plugins.json` / `plugin_details.json`）时：

- **每个插件应拆分为独立 GitHub 仓库**（一个仓库一个插件），更符合官方生态工作方式；
- 每个独立插件仓库都应带上 `LICENSE` 与清晰的 `README.md`；
- `__plugin_meta__` 里填写真实的 `repository_url`、`author`、`license`、`version`。

