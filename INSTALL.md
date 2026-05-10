# 安装提示词

复制下面整段，粘贴给你的 Claude Code：

```
请帮我安装两个 Claude Code Skill：

1. AgentMemory — 分层记忆系统
   https://github.com/BH2S/AgentMemory-skills
   安装: 克隆仓库，把 memory-system/ 文件夹复制到 ~/.claude/skills/

2. nx-modeling — NX 建模 + CAD 视觉分析
   https://github.com/BH2S/nx-modeling-skills
   安装: 克隆仓库，把 nx-reducer-modeling/ 和 cad-vision/ 复制到 ~/.claude/skills/

装完后，用 AgentMemory 的方法帮我创建初始记忆结构：
- 在项目根目录下创建 Memory/ 文件夹
- 建立 MEMORY.md（L1 路由索引入口）
- 建立 user-profile.md（L1 用户画像）
- 询问我这个项目的技术栈、工具链、偏好，填入对应的 L2 文件

最后告诉我记忆系统已经就绪，可以用"记住这个"来随时添加记忆。
```
