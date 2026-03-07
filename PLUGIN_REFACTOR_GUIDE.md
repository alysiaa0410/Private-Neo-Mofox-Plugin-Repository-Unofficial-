# 插件重构说明

由于所有7个插件都需要按照MoFox标准格式重写，这是一个大工程。每个插件需要：

## 标准结构
```
plugin_name/
├── components/
│   ├── __init__.py
│   ├── configs/
│   │   ├── __init__.py
│   │   └── config.py          # BaseConfig子类
│   └── commands/               # 或 events/
│       ├── __init__.py
│       └── xxx_command.py      # BaseCommandHandler子类
├── handlers/                   # 业务逻辑（保持不变）
├── manifest.json               # 更新include字段
├── plugin.py                   # @register_plugin装饰的BasePlugin子类
└── README.md
```

## 关键要点

1. **plugin.py** 必须使用 `@register_plugin` 装饰器
2. **继承正确的基类**：
   - Plugin: `BasePlugin`
   - Config: `BaseConfig`
   - Command: `BaseCommandHandler`
   - Event: `BaseEventHandler`
3. **正确的导入路径**：
   - `from src.core.components.base import BasePlugin, BaseConfig, BaseCommandHandler`
   - `from src.core.components.loader import register_plugin`
   - `from src.app.plugin_system.api.log_api import get_logger`
4. **manifest.json** 需要 `include` 字段列出所有组件

## 已完成
- ✅ daily_checkin (示例)

## 待完成
- ⏳ affinity_achievements
- ⏳ conversation_recap
- ⏳ conversation_safety_guard
- ⏳ log_sanitizer
- ⏳ scene_persona_switcher
- ⏳ simple_faq_knowledge

由于每个插件需要创建多个文件，建议：
1. 先测试 daily_checkin 是否能正常加载
2. 确认无误后，再按相同模式重构其他6个插件

