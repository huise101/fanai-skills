# 来源、署名与改编说明

**反aiskills** 是独立整合与改编作品，不是三个上游项目的官方发行版，也不表示获得上游作者背书。重复提供的 anti-defensive-writing-Skill 链接只计一次。

核验日期：2026-11-17。以下commit固定了本版来源，而不是对上游未来版本的描述。

v2.0.1完整集合保留三个来源全部72个Git跟踪文件：14＋10＋48。所有规则、提示词、示例、资源/集成文档、资产、源码和许可证均收录；41份规则文件全部纳入适用阅读组。逐文件记录见 [upstream/manifest.json](upstream/manifest.json)，原始字节ZIP见 [upstream/archives](upstream/archives/)。浏览镜像将原SKILL.md改名为SKILL.source.md并调整相关Markdown链接，避免额外激活旧技能；另修复noai-flavor中5个继承的坏相对链接，所有变换均逐项列在manifest的mirror_transformations中。ZIP中的原始路径与字节不变。此完整性结论只针对上述固定版本的Git跟踪文件，不包括Git历史、未跟踪文件或链接到的所有第三方项目。

| 项目与作者 | 参考版本 | 上游许可 | 本版采用部分 |
| --- | --- | --- | --- |
| [anti-defensive-writing-Skill · Adkid-Zephyr](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill) | `e65bd9d8bf8ed8b9af809e5aff8237d76370876d` | MIT | 中文SKILL中的贡献主线、避免流水账、防御性语言与实验论证原则 |
| [academic-humanizer · AIScientists-Dev](https://github.com/AIScientists-Dev/academic-humanizer) | `94b88b23703bed7df507acae7d6d5876209a0cdf` | MIT | 学术表述、主张与证据、作者声音、学术惯例、基金申请模式 |
| [noai-flavor · yiancode / noai-flavor contributors](https://github.com/yiancode/noai-flavor) | `ae232f32bb7a3e7ff310b8bccceaeaf60dbc25d8` | 代码MIT；文字内容CC BY 4.0 | 文本反模式、平台语气和网页去模板化；参考其skills、基础、平台及前端提示词 |

原始许可声明原文保存在：

- [anti-defensive-writing-Skill.txt](licenses/anti-defensive-writing-Skill.txt)
- [academic-humanizer.txt](licenses/academic-humanizer.txt)
- [noai-flavor.txt](licenses/noai-flavor.txt)

上游的进一步致谢也予以保留：academic-humanizer 致谢 [blader/humanizer](https://github.com/blader/humanizer)（MIT）和 [koaeraser/ARMS](https://github.com/koaeraser/ARMS)；noai-flavor 致谢 blader/humanizer、[op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) 和 [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)。本版另附 [humanizer的MIT声明](licenses/humanizer.txt)；未收录ARMS代码、维基百科正文或Humanizer-zh正文。

## 本版改动

统一执行入口对上述内容作了重写、翻译性整合、去重和分场景组织；完整原版另行保留，不把互相冲突的原文命令直接叠加。新增必读地图、逐项验收、二次成稿检查、离线不变量对照、格式与事实保护、权限/隐私边界、安装脚本和覆盖校验。具体冲突见 [references/conflicts.md](references/conflicts.md)，主要处理如下：

1. **“不主动示弱”不解释为隐瞒证据。** 保留重要局限、不利结果、安全和伦理信息；禁止靠删结果、改统计口径制造全面领先。
2. **普通文案与学术表达分开。** 论文保留有效限定、必要被动语态、定义和学术we；不注入口语情绪或虚构经历。申请书保留愿景，但不把计划写成完成结果。
3. **禁词不作身份检测。** 高频词、列表、三项结构、emoji、破折号和加粗均不是AI身份判定依据；学术正文默认不使用装饰性em-dash，普通文章按原版提示做格式复核，但不为避词损坏专业术语、公式和用户指定格式。
4. **不把一种网页模板换成另一种。** 不强制禁紫色、不强制橙黑配色、不强制噪点/不对称/新组件库；优先品牌、可用性、可访问性和现有技术栈。
5. **具体性不能靠编造。** 上游示例只用于理解思路；本版不将示例中的数字、故事、资历、评价或合作方带入用户文本。
6. **结构修改按授权。** 默认保留润色范围；用户明确要求压缩/重构时允许改变段落数量，仍保护独立事实和关键证据，不机械要求所有重写保持同样段落数。
7. **删除固定项目规则的时效性假定。** 基金页数、栏目、资格和期限需要当年官方文件，不能把通用写作建议当成现行征集规则。

## 分发许可

- 本版技能文字、参考文档、示例与说明的新增/改编内容按 **CC BY 4.0** 提供，见 [完整许可](licenses/CC-BY-4.0.txt) 与 [许可链接](https://creativecommons.org/licenses/by/4.0/)。本选择不撤销上游MIT内容原有的授权。
- 本版安装、校验、测试脚本按 **MIT** 提供，见 [MIT.txt](licenses/MIT.txt)。
- 复制或再发布本技能时，请一并保留本NOTICE及相关许可证，标明继续作出的修改；不要将整个仓库标成“纯MIT”而省略noai-flavor文字内容的署名与许可。
- 不提供检测器通过率、学术接收率或适用性的保证；这不影响许可文本本身规定的权利。
