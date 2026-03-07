# 插件重构状态

## 已完成
- ✅ **daily_checkin** - 每日签到插件
  - 已按MoFox标准格式重构
  - 使用BaseEventHandler
  - 监听ON_MESSAGE_RECEIVED事件
  - 已修复__init__参数问题
  - 可以正常加载（虽然命令可能还需要调试）

## 待重构（共6个）
由于每个插件需要创建多个文件，建议：

### 方案1：逐个重构（推荐）
先确保daily_checkin完全正常工作后，再按相同模式重构其他插件

### 方案2：批量重构
我可以一次性创建所有插件的文件，但如果格式还有问题需要全部返工

## 插件列表
1. ⏳ affinity_achievements - 亲密度与成就系统
2. ⏳ conversation_recap - 对话回顾  
3. ⏳ conversation_safety_guard - 情绪分析
4. ⏳ log_sanitizer - 日志脱敏
5. ⏳ scene_persona_switcher - 场景切换
6. ⏳ simple_faq_knowledge - FAQ知识库

## 下一步
请告诉我：
1. 是否继续批量重构所有插件？
2. 还是先解决daily_checkin的命令不生效问题？

