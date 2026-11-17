# 反aiskills

**完整集合版 v2.0.0：一个技能入口，收齐三个来源的全部资料，并执行必读与逐项验收。**

面向中文和英文：论文、摘要、引言、结论、rebuttal、基金申请、普通文章、平台文案，以及网页去模板化。改的是表达、叙事和视觉模板，不是事实。

> 把真正成立的价值讲清楚。少套话，少空泛拔高，少替自己辩解；保留证据、作者声音与必要边界。

## 合并了什么

| 上游项目 | 在本版中的作用 |
| --- | --- |
| [Adkid-Zephyr/anti-defensive-writing-Skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill) | 贡献主线、避免工作汇报式叙事、去除空洞自我削弱 |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) | 学术清晰度、主张与证据、作者风格、基金申请模式 |
| [yiancode/noai-flavor](https://github.com/yiancode/noai-flavor) | 中英文模板表达、平台语气、网页去模板化 |

这是**完整来源库＋统一执行规则**，不是只保留核心摘要，也不是把三个互相冲突的技能无条件叠加。

| 完整原版资料 | Git跟踪文件数 | 可浏览镜像 |
| --- | ---: | --- |
| anti-defensive-writing-Skill | 14 | [全部文件](skills/fanai-skills/upstream/anti-defensive-writing-Skill/) |
| academic-humanizer | 10 | [全部文件](skills/fanai-skills/upstream/academic-humanizer/) |
| noai-flavor | 48 | [全部文件](skills/fanai-skills/upstream/noai-flavor/) |
| **合计** | **72** | **41份规则文件全部进入适用阅读组** |

包括中英文SKILL、提示词、全部patterns、平台/前端规则、案例、资源推荐、集成文档、图像、源码和许可证。另提供 [三个原始ZIP](skills/fanai-skills/upstream/archives/) 保留原始路径与全部字节；[逐文件清单](skills/fanai-skills/upstream/manifest.json) 记录commit、Git blob和SHA256。可浏览镜像仅将原版 `SKILL.md` 改名以避免多技能激活，并调整相关本地链接；原始ZIP不做这些变更。

范围是最初给出的三个不同仓库（重复链接只计一次），不递归搬运其提及的所有第三方网站、工具或ARMS研究流水线。来源、版权和改编说明见 [NOTICE](skills/fanai-skills/NOTICE.md)。

## 名称与兼容性

- 显示名称：**反aiskills**。
- 技能标识及目录名：`fanai-skills`。Agent Skills 使用小写英文、数字和连字符；中文名称保留在标题、描述和UI元数据中。
- 核心技能是普通Markdown文件，不依赖Python、MCP、外部模型API或联网。可由支持 `SKILL.md` 的工具读取；实际自动发现和命令语法以各工具为准。
- 提供的安装、校验和测试脚本需要 Python 3.10+，仅使用标准库，无需 `pip install`。

## 每次使用的执行契约

让AI使用本仓库链接时，不能只读README后凭印象润色，必须：

1. 读取 [SKILL.md](skills/fanai-skills/SKILL.md)，确认当前版本和授权范围。
2. 读取 [完整阅读地图](skills/fanai-skills/references/reading-map.md)、[验收清单](skills/fanai-skills/references/acceptance-checklist.md) 和 [冲突处理表](skills/fanai-skills/references/conflicts.md)。
3. 读完当前文体所有适用来源组，不用普通文章口语规则覆盖学术准确性，不把原版示例当用户事实。
4. 修改后逐项检查事实、数字、公式、引用、范围、必要局限和全部适用反模式，再读成稿做第二遍检查。
5. 有原稿/修订稿文件和Python时运行不变量检查；否则人工对照。未读完或未核验的范围必须说明，不能把局部检查写成“全稿通过”。

同会话已完整读过且版本未变的内容可复用。安装后只有一个 `fanai-skills` 入口，原版资料不会自动激活成多套冲突的技能。技能把必读和检查流程固定下来，但静态脚本或模型自检都不是“以后永不出错”或“检测器必过”的保证。

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
  SKILL.md                  唯一执行入口与任务边界
  agents/openai.yaml        反aiskills显示名称
  references/               阅读地图、逐项验收、冲突表、分文体规则
  scripts/check_invariants.py 数值/引用/公式的离线对照
  upstream/
    manifest.json           72个原文件的覆盖与校验记录
    archives/               三个原始字节ZIP
    <三个项目目录>/         完整可浏览镜像
  NOTICE.md                 来源、版本、署名与改编说明
  licenses/                 完整许可与上游声明
scripts/
  install.py                安全安装/显式更新
  validate.py               结构、完整原版资料与发布检查
  source_bundle.py          ZIP/镜像/阅读覆盖一致性校验
  sync_sources.py           从固定版本本地Git副本重新生成来源库
  build_release.py          生成不含.git和缓存的发布ZIP
tests/                      安装、覆盖与不变量的自动化测试
.github/workflows/          Linux/Windows静态CI
```

## 校验与打包

```sh
python scripts/validate.py
python -B -m unittest discover -s tests -v
python scripts/build_release.py
```

打包输出为 `dist/fanai-skills-github.zip`，包含整合技能、完整原版资料、脚本、文档和许可证。校验同时检查72个原文件、三个ZIP、镜像校验和与规则阅读组覆盖，**不等于对模型改写效果或AI检测率的测量**。

对照UTF-8纯文本/Markdown/LaTeX原稿和修订稿：

```sh
python skills/fanai-skills/scripts/check_invariants.py original.tex revised.tex
```

脚本不改文件、不联网；发现数值、已识别的LaTeX引用/交叉引用或公式变化时返回非零状态供人工核对。它不能检查全部单位、科学含义、必要披露、PDF/Word对象或“变化是否获准”，不可把脚本通过当作完整学术核验。

来源固定在NOTICE所列commit。需要重建完整来源库时，准备三个包含这些commit的本地Git副本，按 `python scripts/sync_sources.py --help` 指定每个副本；该脚本不联网、不运行上游源码，也不会悄悄更新为未经审阅的新版本。

公开仓库：[huise101/fanai-skills](https://github.com/huise101/fanai-skills)，页面标题为“反aiskills”。再次分发时使用本目录内容，或解压上述ZIP后上传；不要上传 `dist/`、缓存或私人稿件。仓库已包含 `.gitignore` 和自动化校验；安装与打包脚本不会自动创建远程仓库或上传文件。

## 许可证与隐私

- 技能文字、参考文档和说明：**CC BY 4.0**。
- 本版Python脚本及测试：**MIT**。
- 上游MIT授权继续保留；再分发需保留原始署名与许可。详见 [LICENSE](LICENSE) 和 [NOTICE](skills/fanai-skills/NOTICE.md)，不能把整包标成纯MIT而省略文字许可。
- 整合版安装、校验和对照脚本不联网、不遥测。完整原版资料中的API/集成/下载示例只作参考保存，不自动执行。宿主AI工具如何处理输入取决于其配置和服务条款；这不表示模型推理一定离线。
