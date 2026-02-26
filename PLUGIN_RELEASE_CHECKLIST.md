## 插件发布清单（提交到 MoFox 插件索引前）

> 适用于“每个插件一个独立仓库”的发布方式。

### 必备文件

- [ ] `LICENSE`（建议 MIT / GPL / AGPL 等，按你实际选择）
- [ ] `README.md`（包含：功能、安装/启用方式、指令、权限节点、配置项）
- [ ] 根目录 `__init__.py`（模板仓库做法：让仓库可被识别为插件包）
- [ ] 插件目录（例如 `my_plugin/`）内包含：
  - [ ] `__init__.py`（定义 `__plugin_meta__`）
  - [ ] `plugin.py`（入口类 + 指令/组件）

### 元信息自检（`__plugin_meta__`）

- [ ] `name` / `description` / `usage` 填写完整且易懂
- [ ] `version` 符合语义化版本（例如 `1.0.0`）
- [ ] `author` / `license` / `repository_url` 使用真实信息
- [ ] `keywords` 与 `extra` 填写合理（尽量标注 `plugin_type`、`min_bot_version`）
- [ ] 如有第三方依赖，写入 `python_dependencies`

### 质量建议（强烈推荐）

- [ ] 在你的 MoFox-Bot 环境里实际跑通 1 次（至少验证指令可用）
- [ ] 对异常情况（缺参数、无权限）给出明确提示
- [ ] 不要把 Token、账号密码等敏感信息提交到仓库（避免 `.env`、`config.local.*`）

### 提交到官方插件索引

- [ ] 在 `plugins.json` 添加你的 `id` 与 `repositoryUrl`
- [ ] 在 `plugin_details.json` 添加对应 `manifest`
- [ ] 发起 PR，等待 CI 校验通过

