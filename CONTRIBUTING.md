# 贡献指南

感谢想要贡献本项目！这份文档说明怎么提 issue、怎么提 PR、什么样的贡献最受欢迎。

## 🎯 我们最欢迎的贡献

按优先级排序：

1. **新的参考案例**（`skill/references/examples/` 下加 `.md`）—— 比如电商销售、金融交易、运动数据、医疗指标等不同形态
2. **troubleshooting 文档补充** —— 你遇到过的真实报错 + 解决方案
3. **demo 截图** —— 仓库里目前是占位符，欢迎实拍补上
4. **翻译** —— 英文版 README、INSTALL 等
5. **代码模板优化** —— 后端模板更健壮、前端模板更美观
6. **bug 修复**

## 📝 怎么提 Issue

### 报 Bug

用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug_report.md)，提供：

- 你跑的具体命令
- 完整的报错输出
- 你的环境（OS、Python 版本、Claude 客户端版本）
- 复现步骤（最小可复现示例最好）

### 提功能请求

用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature_request.md)，说明：

- 你想做什么 / 想解决什么问题
- 现在你怎么变通的
- 理想的解决方式

## 🔧 怎么提 Pull Request

### 流程

1. Fork 仓库
2. 创建分支：`git checkout -b feat/your-feature` 或 `fix/your-bug`
3. 改代码 / 文档
4. 本地验证：
   - 改了 demo 代码 → `cd demo && python app.py` 跑一下
   - 改了 Skill 文档 → 检查 markdown 渲染是否正常
5. 提交：`git commit -m "feat: 添加 XX 功能"`（中英都行，写清楚动机）
6. 推送：`git push origin feat/your-feature`
7. 在 GitHub 上提 PR，关联相关 issue

### Commit Message 规范

不强制，但推荐用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/) 格式：

- `feat:` 新功能
- `fix:` bug 修复
- `docs:` 只改文档
- `refactor:` 重构（不影响功能）
- `test:` 加测试
- `chore:` 构建配置等杂项

例子：

- `feat: 在 examples 里添加电商销售案例`
- `fix: troubleshooting 里 Windows 端口排查命令错了`
- `docs: README 加上更多徽章`

### Code Review 期待

- 维护者会在 1-2 周内 review，复杂 PR 可能更久
- 可能会要求改动，请耐心
- 不被 merge 不代表 PR 不好——可能是方向不太对，会解释原因

## 📐 代码风格

### Python

- 缩进 4 空格
- 每个函数加中文 docstring
- 复杂逻辑加行内注释解释**为什么**这么做（不是**做了什么**——代码本身能看出来）

### 文档

- 中文为主
- 命令示例用代码块包起来
- 截图存 `docs/images/` 或 `demo/screenshots/`
- 链接尽量用相对路径（仓库内）

### 案例文档（`skill/references/examples/`）

按现有四个案例的结构来：

```markdown
# 案例：XX 仪表盘

**适合场景**：什么时候用这个案例

## 假设的数据形态

列：...

## 接口设计

- /api/xxx → ...

## 图表（按重要性排序）

1. ...

## 这个案例独特的地方

...
```

## 🧪 添加新案例的特别说明

新案例不需要带完整代码，只需要：

1. 描述清楚数据形态（哪些列、什么类型）
2. 给出推荐的 API 划分
3. 推荐的图表类型 + 为什么这么选
4. 这个场景特有的坑或技巧

完整代码留给 Claude 按案例文档生成即可。

如果你想配套做完整 demo（像 `demo/` 那样），更欢迎，但请：

- 数据集 < 5MB
- 数据合法（公开数据集 / 自己合成 / 已获授权）
- 在 PR 里说明数据来源

## 🤝 行为准则

简单原则：**对人友善，对事严格**。

- 不接受人身攻击、骚扰、歧视
- 技术讨论可以激烈，但保持就事论事
- 维护者保留删除不当评论的权力

## 📮 联系

- 一般问题：开 Issue
- 安全问题：私信仓库维护者，不要公开 issue
- 想聊更深入：开 Discussion（如果仓库开了）

谢谢你的贡献！
