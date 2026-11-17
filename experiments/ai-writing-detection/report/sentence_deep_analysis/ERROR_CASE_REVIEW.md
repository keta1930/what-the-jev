# Jev逐句检测典型错误案例抽查

## 方法

以0.50为固定阈值，中英文分别在四个结果类别中抽取最多10条。高置信类别按Jev概率从高到低选择，低置信类别按概率从低到高选择；同分按样本ID排序。因此选择规则确定且可复现，不依赖人工主观挑选。

这些样本是各类别的概率极端案例，用于诊断而非估计总体比例。语言现象由简单可复现规则编码，属于探索性定性分析，不能解释因果。完整80条案例见CSV/JSON。

## 样本构成

| 语言 | 类别 | 候选总数 | 抽查数 | 概率范围 |
| --- | --- | ---: | ---: | ---: |
| 中文 | 高置信误报人工句 | 133 | 10 | 0.63–0.73 |
| 中文 | 低置信漏检AI句 | 1555 | 10 | 0.08–0.13 |
| 中文 | 正确高置信AI句 | 331 | 10 | 0.69–0.76 |
| 中文 | 正确低置信人工句 | 3633 | 10 | 0.03–0.06 |
| 英文 | 高置信误报人工句 | 444 | 10 | 0.72–0.86 |
| 英文 | 低置信漏检AI句 | 809 | 10 | 0.22–0.24 |
| 英文 | 正确高置信AI句 | 1149 | 10 | 0.78–0.81 |
| 英文 | 正确低置信人工句 | 3461 | 10 | 0.06–0.13 |

## 规则化语言现象汇总

一个案例可同时具有多个标签。

| 语言 | 类别 | very_short | short | quote_or_dialogue | question_or_exclamation | numeric_or_reference | first_person | connective | punctuation_heavy | no_rule_flag |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 中文 | 高置信误报人工句 | 0 | 2 | 1 | 1 | 0 | 1 | 1 | 2 | 5 |
| 中文 | 低置信漏检AI句 | 2 | 7 | 5 | 6 | 0 | 4 | 0 | 1 | 0 |
| 中文 | 正确高置信AI句 | 0 | 0 | 2 | 1 | 0 | 2 | 1 | 0 | 5 |
| 中文 | 正确低置信人工句 | 0 | 2 | 0 | 1 | 0 | 1 | 0 | 2 | 7 |
| 英文 | 高置信误报人工句 | 0 | 0 | 0 | 1 | 0 | 2 | 4 | 1 | 4 |
| 英文 | 低置信漏检AI句 | 1 | 5 | 9 | 4 | 1 | 3 | 0 | 6 | 0 |
| 英文 | 正确高置信AI句 | 0 | 0 | 2 | 0 | 0 | 3 | 3 | 1 | 2 |
| 英文 | 正确低置信人工句 | 0 | 0 | 4 | 5 | 0 | 8 | 6 | 4 | 0 |

## 案例预览

下表每组显示概率最极端的前3条；完整案例及哈希见附件。

### 中文：高置信误报人工句

| ID | 概率 | 现象标签 | 句子 |
| --- | ---: | --- | --- |
| ZH005-sentence-049 | 0.73 | first_person | 我们也要几间满沿着爬山虎的高雪克屋子来安息我们的灵性，我们说。 |
| ZH045-sentence-007 | 0.70 | punctuation_heavy | ……尹氏心营世事，虑钟家业，心形俱疲，夜亦昏惫而寐。 |
| ZH051-sentence-045 | 0.70 | connective | 来到重庆，她拿出搁在箱里的六只虾，请朋友们看，于是重庆造了她带来一箱子白石翁的画之谣。 |

### 中文：低置信漏检AI句

| ID | 概率 | 现象标签 | 句子 |
| --- | ---: | --- | --- |
| ZH099-sentence-001 | 0.08 | short | 古人云：十年树木，百年树人。 |
| ZH002-sentence-001 | 0.12 | short;question_or_exclamation;first_person | 爲什麼我會失眠呢？ |
| ZH037-sentence-008 | 0.12 | short;quote_or_dialogue;question_or_exclamation;first_person | 快來幫我提一桶水！” |

### 中文：正确高置信AI句

| ID | 概率 | 现象标签 | 句子 |
| --- | ---: | --- | --- |
| ZH022-sentence-042 | 0.76 | quote_or_dialogue | 廟牆上，赫然書寫著“觀世音菩薩”四字，莊嚴而靜穆，這裡是重慶唯一一個未受外界擾動的聖地。 |
| ZH018-sentence-011 | 0.73 | no_rule_flag | 身邊有一位美麗的女子相伴的男子，與臃腫的女僕之間的親密行為，或許也正是旅行者心中那份對於新奇事物的渴望。 |
| ZH054-sentence-030 | 0.73 | first_person | 瞬間，高山上雲霧升起，輕盈如飛絮般掠過我們的肩頭；腳下的市鎮溪山，彷彿沉浸在雲海中；我們彼此對視，感受到隱隱的幻影，似在袅袅香煙中，童心再現，我們這群大小，竟如樂園中的童男童女，一同卸下了尊嚴，重拾自然，齊聲呼喊： |

### 中文：正确低置信人工句

| ID | 概率 | 现象标签 | 句子 |
| --- | ---: | --- | --- |
| ZH089-sentence-017 | 0.03 | no_rule_flag | 层层的叶子中间，零星地点缀着些白花，有嬝娜地开着的，有羞涩地打着朶儿的；正如一粒粒的明珠，又如碧天里的星星，又如刚出浴的美人。 |
| ZH011-sentence-006 | 0.04 | no_rule_flag | 在北平即使不出門去罷，就是在皇城人海之中，租人家一椽破屋來住着，早晨起來，泡一碗濃茶、向院子一坐，你也能看得到很高很高的碧綠的天色，聽得到青天下馴鴿的飛聲。 |
| ZH089-sentence-018 | 0.04 | no_rule_flag | 微风过处，送来缕缕清淸香，仿佛远处高楼上渺茫的歌声似的。 |

### 英文：高置信误报人工句

| ID | 概率 | 现象标签 | 句子 |
| --- | ---: | --- | --- |
| EN015-sentence-014 | 0.86 | no_rule_flag | When gas first spread along a city, mapping it forth about evenfall for the eye of observant birds, a new age had begun for sociality and corporate pleasure-… |
| EN068-sentence-023 | 0.82 | first_person | We are all in the quest and our captains are those who lead us to the highest peaks of revelation—Bach fashioning that immortal Concerto for Two Violins that… |
| EN006-sentence-029 | 0.76 | connective | Spring and sunrise are forever miracles, but the early hour of the wonder hardly hints the exuberance of its fulfilment. |

### 英文：低置信漏检AI句

| ID | 概率 | 现象标签 | 句子 |
| --- | ---: | --- | --- |
| EN065-sentence-028 | 0.22 | short;quote_or_dialogue;punctuation_heavy | TUESDAY.—"Received a letter from Jane. |
| EN019-sentence-014 | 0.23 | short;quote_or_dialogue;question_or_exclamation;punctuation_heavy | “Do you come to Yarmouth for that?” he inquired. |
| EN035-sentence-003 | 0.23 | quote_or_dialogue;first_person;punctuation_heavy | I distinctly remember him telling me, “A man can’t get on nowadays by hanging about with his hands in his pockets.” |

### 英文：正确高置信AI句

| ID | 概率 | 现象标签 | 句子 |
| --- | ---: | --- | --- |
| EN047-sentence-024 | 0.81 | quote_or_dialogue | Surely, it was through the ancient and noble act of lying in bed that Michelangelo envisioned transforming the Sistine Chapel’s ceiling into a grand portraya… |
| EN067-sentence-029 | 0.80 | connective | Therefore, if in the future you happen to watch a film featuring a captivating narrative involving a horse that only appears to shiver in the dialogue displa… |
| EN023-sentence-006 | 0.79 | first_person | The man engaged in conversation with me appeared as an articulate tree, while the van driver, animatedly gesturing for me to move aside, resembled branches d… |

### 英文：正确低置信人工句

| ID | 概率 | 现象标签 | 句子 |
| --- | ---: | --- | --- |
| EN052-sentence-041 | 0.06 | quote_or_dialogue;question_or_exclamation;connective;punctuation_heavy | "'So she makes,' said Mr. Barkis, after a long interval of reflection, 'all the apple parsties, and does all the cooking, do she?' |
| EN052-sentence-043 | 0.06 | quote_or_dialogue;question_or_exclamation;first_person;punctuation_heavy | "'Well, I'll tell you what,' said Mr. Barkis. 'P'raps you might be writin' to her?' |
| EN052-sentence-046 | 0.09 | quote_or_dialogue;question_or_exclamation;punctuation_heavy | If you was writin' to her, p'raps you'd recollect to say that Barkis was willin', would you?'" |

## 探索性观察

- 极端错误并不只发生在短句；长句和普通陈述句也会进入高置信误报或低置信漏检组，说明错误不能由句长单独解释。
- 引语、问句、第一人称、连接词等现象在不同类别均出现，需结合全量分层统计判断其总体关联，不能仅凭本抽查推断。
- 中文漏检组的低概率极端案例说明部分GPT-4o-mini改写句在表面风格上仍非常接近人工原文；英文高置信误报则提示规范、流畅或概括式措辞也可能被Jev视为AI特征。
- 本抽查适合展示模型错误形态；关于各因素是否系统性影响检测，应以实验2的全量分层结果为准。
