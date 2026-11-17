# 去模板表达模式表

以下都是需要结合上下文判断的信号，不是词语黑名单，也不是AI作者身份的检测规则。命中一个词不能证明文本由AI生成。

| 模式 | 常见信号 | 判断与处理 |
| --- | --- | --- |
| 空泛开头 | 在当今社会、随着时代发展、In recent years | 若删去不损失背景和问题，就直接进入内容；真实时间趋势须保留 |
| 无依据拔高 | 革命性、至关重要、pivotal、paves the way，或只堆媒体/顶刊名号 | 说明已有材料支持的具体作用和来源内容，不用名号代替论证，不编数值或因果 |
| 宣传口吻 | 无缝、赋能、卓越体验、groundbreaking | 说明实际动作和能力；产品正式术语或原文引述保留 |
| 模糊归因 | 专家认为、研究表明、it is widely believed | 用已经给出的具体来源；缺来源时指出或删掉无根据的权威背书 |
| 装深度尾句 | 体现了、彰显了、highlighting、underscoring | 是否说明机制或证据？没有就删；承载真实推论则保留 |
| 高频抽象词 | 深入探讨、格局、delve、tapestry、landscape | 看是否只是装饰；专业含义不改，如 energy landscape |
| 系动词绕行 | serves as、具有……的功能 | 能用“是/有”清楚表达就缩短；有真实角色差异则保留，不丢“超过/至少”等数量限定 |
| 否定排比与虚假范围 | 不仅……更……、not just X but Y；把不同维度硬写成from X to Y | 保留真正对比和真实数值/时间/尺度范围，删掉伪造的范围感与重复包装 |
| 凑三项 | 每个贡献都分三点、三组近义形容词 | 按实际内容数量组织，不按审美删掉真实第三项 |
| 术语轮换 | 方法/框架/体系/引擎交替指同一对象 | 同一实体保持稳定称呼，避免让读者误判为不同组件 |
| 机械连接 | 此外、同时、Moreover逐句开头 | 让因果和指代连接内容；必要转折和递进词保留 |
| 列表强迫 | 每段加标题、每句编号或加粗 | 列表用于并列、步骤、检索，不把连续论证切碎 |
| 格式装饰 | emoji、粗体、破折号密集 | 删除不服务语义的装饰；不破坏公式负号、数值区间、命令或规范格式 |
| 重复模糊 | 可以潜在地可能、somewhat relatively | 给出不确定的具体对象与原因，留下证据需要的限定 |
| 聊天痕迹 | 好问题、希望对您有帮助、作为AI | 移除不属于最终作品的助手话语；真实AI/利益披露与有意义的as-of日期保留 |
| 通用结尾 | 综上所述、未来可期、despite challenges | 用当前内容支持的结论或行动收尾，前文已完整则结束 |
| 防御性堆叠 | 必须承认、谨慎解读、虽然只做了 | 删掉空洞自我削弱，保留会影响结论的范围和真实限制 |
| 平铺实验日志 | 我们先试……然后又试…… | 获准重构时按问题、设计和证据组织；必要可复现过程保留 |

## 修改时的三个问题

- 去掉这个词/句子，读者是否会失去条件、事实、来源或必要语气？若会，不直接删。
- 替换后是否更准确，还是只是换了另一套AI常用词？不要为了避词轮换术语。
- 这段是否清楚说出了作者真正知道的内容？缺证据就保留边界，不以自信语气补缺。

## 子规则来源与验收定位

| 原始子规则/边界 | 完整来源 | 执行验收 |
| --- | --- | --- |
| 不同维度硬写成“从X到Y”的虚假范围 | [grammar-tricks](../upstream/noai-flavor/patterns/grammar-tricks.md) | T10；真实范围保留 |
| 只堆知名媒体/顶刊名字而不说明内容 | [significance-inflation](../upstream/noai-flavor/patterns/significance-inflation.md) | T05；保留真实引用键 |
| 原型占位与最终内容替换 | [empty-content](../upstream/noai-flavor/patterns/frontend/empty-content.md)、[image-resources](../upstream/noai-flavor/resources/image-resources.md) | D09；缺材料可待确认，不造内容 |
| 示例可能丢数量限定或改变确定性 | [grammar-tricks](../upstream/noai-flavor/patterns/grammar-tricks.md)、[over-hedging](../upstream/noai-flavor/patterns/over-hedging.md) | F01/F03；以保真规则覆盖示例改法 |
| 聚合图库的许可概述不代表具体资产许可 | [image-resources](../upstream/noai-flavor/resources/image-resources.md) | D05；条件适用，逐件核许可 |
| 原版将ease-in-out误称线性 | [anti-ai-web](../upstream/noai-flavor/prompts/frontend/anti-ai-web.md) | D07/conflicts；归档保留，执行不沿用误称 |

以上是明确子规则的执行定位，不以文件数量代替检查记录。其他来源按reading-map读取全文并应用适用验收组。
