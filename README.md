# 反aiskills

**一个技能，处理反防御性写作、学术人性化和通用去 AI 味。**

面向中文和英文：论文、摘要、引言、结论、rebuttal、基金申请、普通文章、平台文案，以及网页去模板化。改的是表达、叙事和视觉模板，不是事实。

> 把真正成立的价值讲清楚。少套话，少空泛拔高，少替自己辩解；保留证据、作者声音与必要边界。

## 合并了什么

| 上游项目 | 在本版中的作用 |
| --- | --- |
| [Adkid-Zephyr/anti-defensive-writing-Skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill) | 贡献主线、避免工作汇报式叙事、去除空洞自我削弱 |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) | 学术清晰度、主张与证据、作者风格、基金申请模式 |
| [yiancode/noai-flavor](https://github.com/yiancode/noai-flavor) | 中英文模板表达、平台语气、网页去模板化 |

这是**去重、重写并解决规则冲突的独立整合版**，不是三个技能依次执行。来源版本、许可证和改编说明见 [NOTICE](skills/fanai-skills/NOTICE.md)。

## 名称与兼容性

- 显示名称：**反aiskills**。
- 技能标识及目录名：`fanai-skills`。Agent Skills 使用小写英文、数字和连字符；中文名称保留在标题、描述和UI元数据中。
- 核心技能是普通Markdown文件，不依赖Python、MCP、外部模型API或联网。可由支持 `SKILL.md` 的工具读取；实际自动发现和命令语法以各工具为准。
- 提供的安装、校验和测试脚本需要 Python 3.10+，仅使用标准库，无需 `pip install`。

## 安装

先克隆本仓库并进入目录。默认安装到用户级共享技能目录：

```sh
git clone https://github.com/huise101/fanai-skills.git
cd fanai-skills
python scripts/install.py
```

也可以通过 GitHub 的 **Code → Download ZIP** 下载，解压后在仓库目录执行 `python scripts/install.py`。

Windows也可用：

```powershell
py -3 scripts/install.py
```

默认目标为 `~/.agents/skills/fanai-skills`，Pi可自动发现它。按所用工具选其他位置，**同一工具不要重复安装多份**：

```sh
python scripts/install.py --target pi
python scripts/install.py --target codex
python scripts/install.py --target claude
python scripts/install.py --path "/your/skills/fanai-skills"
```

| 参数 | 目标 |
| --- | --- |
| 默认 / `--target agents` | `~/.agents/skills/fanai-skills` |
| `--target pi` | `${PI_CODING_AGENT_DIR:-~/.pi/agent}/skills/fanai-skills` |
| `--target codex` | `${CODEX_HOME:-~/.codex}/skills/fanai-skills` |
| `--target claude` | `~/.claude/skills/fanai-skills` |
| `--path` | 指定完整目标目录，末级目录名须为 `fanai-skills` |

已安装相同内容时不重复写入；内容不同则拒绝覆盖。更新前先审阅改动，再显式执行：

```sh
python scripts/install.py --replace
```

替换会先在技能扫描目录之外保存旧目录，输出备份位置，失败则尝试恢复原目录。不会删除已安装的上游或其他技能，也不修改全局配置。

不使用脚本也可以：把 `skills/fanai-skills/` **整个目录**复制到所用工具的技能目录，保留 `NOTICE.md` 和 `licenses/`。

## 使用

安装后重启工具或新开会话；Pi当前会话可运行 `/reload`。

**Pi：**

```text
/skill:fanai-skills academic 润色下面这段论文，保留数值、公式、引用和真实局限。
```

**Codex：**

```text
使用 $fanai-skills 压缩这段摘要，保留全部结论、数据和引用。
```

**Claude Code：**

```text
/fanai-skills writing 改一下这篇公众号文章，不要套话，不要虚构个人经历。
```

也可以直接说：

```text
用反aiskills润色引言，不改机制、不改实验结论。
用反aiskills改基金申请，保留愿景，但区分计划和已有结果。
用反aiskills去掉这篇文章的机械过渡和空泛结尾。
用反aiskills调整网页的默认模板感，保留品牌、功能和现有组件库。
只检查AI味，不重写、不修改文件。
```

`academic`、`proposal`、`writing`、`web` 是供模型理解的模式提示，不是额外程序命令；不写时按材料判断。已有其他润色技能时，显式调用本技能可明确本次意图；本项目不自动禁用它们。

## 不会做的事

- 不捏造数字、引文、统计显著性、案例、资历、使用体验、资助和合作方。
- 不把“反防御性”理解为隐藏重要局限、删不利结果或改变比较口径。
- 不把合法术语、必要限定、被动语态、列表或破折号一律判错。
- 不为“像人”添加错别字、口头禅、随机情绪和假故事。
- 不强制把所有网页改成同一套配色或安装新组件库。
- 不承诺绕过AI检测、降低检测率或提高录用率；不取消应有的AI辅助披露。
- 不自动上传稿件、运行检测器、编译论文、提交Git或修改未授权文件。

## 一个例子

**修改前**

> 虽然本方法在两个同领域数据集上提高了准确率，但必须承认，我们尚未测试跨领域泛化，因此应谨慎理解这些结果。

**修改后**

> 本方法在两个同领域数据集上提高了准确率；跨领域泛化尚未评估。

少了重复免责，没丢事实，也没偷偷扩大主张。更多示例见 [examples.md](skills/fanai-skills/references/examples.md)；示例都是演示材料，不是真实实验。

## 仓库结构

```text
skills/fanai-skills/
  SKILL.md                  统一入口与任务边界
  agents/openai.yaml        反aiskills显示名称
  references/               分文体规则、模式表和示例
  NOTICE.md                 来源、版本、署名与改编说明
  licenses/                 完整许可与上游声明
scripts/
  install.py                安全安装/显式更新
  validate.py               静态结构与发布检查
  build_release.py          生成不含.git和缓存的ZIP
tests/                      安装与校验的自动化测试
.github/workflows/          Linux/Windows静态CI
```

## 校验与打包

```sh
python scripts/validate.py
python -B -m unittest discover -s tests -v
python scripts/build_release.py
```

打包输出为 `dist/fanai-skills-github.zip`，包含源码、安装与校验脚本、文档和许可证。校验检查结构、链接、许可证、编码和明显的本机路径泄漏，**不等于对模型改写效果或AI检测率的测量**。

公开仓库：[huise101/fanai-skills](https://github.com/huise101/fanai-skills)，页面标题为“反aiskills”。再次分发时使用本目录内容，或解压上述ZIP后上传；不要上传 `dist/`、缓存或私人稿件。仓库已包含 `.gitignore` 和自动化校验；安装与打包脚本不会自动创建远程仓库或上传文件。

## 许可证与隐私

- 技能文字、参考文档和说明：**CC BY 4.0**。
- 本版Python脚本及测试：**MIT**。
- 上游MIT授权继续保留；再分发需保留原始署名与许可。详见 [LICENSE](LICENSE) 和 [NOTICE](skills/fanai-skills/NOTICE.md)，不能把整包标成纯MIT而省略文字许可。
- 本技能不含联网/遥测代码。宿主AI工具如何处理输入取决于其配置和服务条款；“技能无遥测”不表示模型推理一定离线。
