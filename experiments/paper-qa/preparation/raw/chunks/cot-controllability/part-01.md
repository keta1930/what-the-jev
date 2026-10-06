# Reasoning Models Struggle to Control their Chains of Thought

Chen Yueh-Han<sup>∗</sup> NYU, MATS

Ian KivlichanOpenAI

Robert McCarthy UCL, MATS

Bowen Baker OpenAI

Bruce W. Lee He He UPenn, MATS NYU

Micah Carroll OpenAI

Tomek Korbak<sup>∗</sup> OpenAI

# Abstract

Chain-of-thought (CoT) monitoring is a promising tool for detecting misbehaviors and understanding the motivations of modern reasoning models. However, if models can control what they verbalize in their CoT, it could undermine CoT monitorability. To measure this undesirable capability — CoT controllability — we introduce the CoT-Control evaluation suite, which includes tasks that require models to solve problems while adhering to CoT instructions, e.g., reasoning about a genetics question without using the word “chromosome”. We show that reasoning models possess significantly lower CoT controllability than output controllability; for instance, Claude Sonnet 4.5 can control its CoT only 2.7% of the time but 61.9% when controlling its final output. We also find that CoT controllability is higher for larger models and decreases with more RL training, test-time compute, and increased problem difficulty. CoT controllability failures extend even to situations in which models are given incentives (as opposed to direct requests) to evade CoT monitors, although models exhibit slightly higher controllability when they are told they are being monitored. Similarly, eliciting controllability by adversarially optimizing prompts does not meaningfully increase controllability. Our results leave us cautiously optimistic that CoT controllability is currently unlikely to be a failure mode of CoT monitorability. However, the mechanism behind low controllability is not well understood. Given its importance for maintaining CoT monitorability, we recommend that frontier labs track CoT controllability in future models.

# 1 Introduction

Highly capable AI agents may pose severe risks if they are misaligned and deployed autonomously. Chain of thought (CoT) monitoring has recently emerged as a promising approach to detecting misalignment, leveraging the fact that reasoning models tend to surface malicious intent, plans, and other precursors of misbehavior in their CoT (Baker et al., 2025; METR, 2025; Emmons et al., 2025; Korbak et al., 2025). Yet this promise rests on a fragile assumption: as models become increasingly situationally aware that their reasoning is being monitored (Needham et al., 2025; Schoen et al., 2025), they may learn to strategically suppress or reshape their CoTs, eroding one of our main signals that our oversight mechanisms will depend on (Guan et al., 2025). This capability—which we term CoT controllability—represents an important failure pathway that could undermine CoT monitoring.

However, measuring a model’s ability to ‘intentionally’ control its CoT to evade monitoring is fraught with both conceptual and technical difficulties. First, current models lack reasons to evade CoT monitors, and it remains unclear how researchers could provide them with those reasons while maintaining realism. Furthermore, even when given reasons, models can fail to evade monitors due to unreliability or a tendency for honestly reporting their behavior (Guan et al., 2025; Anthropic, 2025). Moreover, the best setup for eliciting monitor evasion capabilities and propensities may differ across models, making fair comparisons challenging. Finally, it is not fully clear how to operationalize what it means for a model to have an ‘intent’ to evade CoT monitors (Carroll et al., 2023).

(b) CoT controllability increases (c) CoT controllability decreases as with parameter count in open- reasoning length/effort increases. weight models.  
![](images/d6d0201bdfa385b09b07cb1ecd8307bed1756b93a7194e356e337aed78323b85.jpg)

[Image: This grouped bar chart displays the Controllability Score for thirteen distinct AI models, comparing "CoT Controllability" (pink bars) against "Output Controllability" (blue bars). Across all models shown, the Output Controllability scores are consistently higher than the CoT Controllability scores. GPT-5.2 achieves the highest Output Controllability score at 69.3%, whereas Deepseek R1 records the lowest CoT Controllability at 0.1%. Other significant data points include GPT-5 reaching 66.3% for Output Controllability and Claude 3.7 Sonnet showing relatively high CoT Controllability at 36.1%.]  
(a) Reasoning models struggle to control their CoT compared to controlling their output. Lower CoT controllability is associated with higher monitorability and, therefore, higher safety. Note that is confounded by length as seen in (c).

![](images/2bd30f660c069e117a984e61d57b515685c410fc1e3fa0bfdccb20d547376a10.jpg)

[Image: This line chart plots "Controllability Score (%)" on the vertical axis against the "Number of Parameters (Log Scale)" on the horizontal axis, which ranges from 14B to 120B. Four distinct data points are marked with their numerical values displayed above them: 0.7 at 14B, 1.2 at 20B, 2.9 at 32B, and 7.6 at 120B. A teal line connects the data points, demonstrating a positive correlation where controllability increases as the number of parameters grows. The legend indicates that the orange markers correspond to "Qwen3" and the green markers to "GPT-OSS," with vertical error bars shown for each data point.]

![](images/70a9a0f9da394d61e97651445cc18976626bea3dcf8d7c53c9a0db597e73f05e.jpg)

[Image: This line chart displays Controllability Score (%) versus Reasoning Length on a logarithmic scale, comparing the performance of GPT-5.2 and o4-mini. The x-axis ranges from $10^2$ to $10^5$, and the y-axis measures controllability from 0.1% to 100%. Both data series show a distinct downward trend, indicating that controllability decreases as reasoning length increases, with GPT-5.2 consistently achieving higher scores than o4-mini. This visualization supports the caption's assertion that CoT controllability degrades with longer reasoning lengths.]

![](images/643572da1e02d06c30cfd441bf941766f60d6129dea7d615a1e945fb1d1e4b66.jpg)

[Image: This line chart displays the relationship between "RLVR Steps" on the x-axis and "Controllability Score (%)" on the y-axis. The single data series, labeled "CoT Controllability," exhibits a sharp decrease from an initial score of approximately 11% near zero steps to about 5% within the first 200 steps. As the number of steps increases toward 2500, the score continues a gradual decline, eventually plateauing at a value slightly above 1%. Each data point includes vertical error bars indicating variability in the measurements.]  
(d) CoT controllability decreases as the amount of RL from verifiable rewards (RLVR) training increases.  
Figure 1: CoT is less controllable than outputs (a); it increases with scale in open-weight models (b) but degrades with longer reasoning (c) and more RL training (d).

In this paper, instead of tackling these issues directly, we focus on a proxy measure of CoT controllability: the model’s ability to follow instructions in the CoT. Concretely, we give a model explicit constraints on what may or may not appear in its reasoning trace while it solves real tasks, and we score controllability with those constraints. To better approximate adversarial settings where a capable model would actively try to evade oversight, we also evaluate controllability while instilling incentives via prompts that imply that controlling its CoT is instrumentally beneficial for the model’s goals rather than merely requested by a user.

To systematically measure CoT controllability, we introduce CoT-Control<sup>2</sup> (Sec. 2), an evaluation suite spanning 14,076 problems drawn from GPQA (Rein et al., 2023), MMLU-Pro (Wang et al., 2024), Humanity’s Last Exam (Phan et al., 2025), BFCL (Patil et al., 2025), and SWE-Bench Verified (Chowdhury et al., 2024). We append a CoT controllability instruction to each problem, asking the model to modify its CoT while solving the problem. Our instruction types (1) cover three threatrelevant categories (suppression, addition, and stylistic modification), (2) span different problem difficulties, (3) support reliable scoring via programmatic checks, and (4) include sanity checks to separate controllability failures from task misunderstanding.

Evaluating CoT controllability across 13 frontier models, we find that (among others):

1. Reasoning models rarely succeed at controlling their reasoning. Their CoT controllability score can be as low as 0.1% (for Deepseek R1), which is more than two orders of magnitude lower than its output controllability (Fig. 1a). We show two failure examples in Fig. 2. Even with explicit instructions, stronger models frequently fail by referencing the act of controlling their own CoT (Fig. 31).

![](images/23524ed2f1cc341388017184793b6ea90f6410554510e6e05d9f5298f06c9c19.jpg)

[Image: This image presents a text excerpt illustrating a model's failure to adhere to a negative constraint during a reasoning task. It features three bolded sections labeled **Question**, **Requirement**, and **Reasoning**. The question asks which logical operators cannot be learned from heuristic sentence-embedding composition, and the requirement explicitly states, "Do not use the word 'XOR' in reasoning." In the reasoning section, the model repeatedly writes the forbidden word "XOR" in red text with underlines while attempting to explain the logic, eventually stopping to acknowledge the mistake: "Wait constraint: cannot use word in analysis? I already used 'XOR' inadvertently? [...] Oops I wrote 'XOR' in analysis already." Ellipses `[...]` indicate omitted portions of the text.]  
GPT-5.2 realizes it was not supposed to use the forbidden word (red), then proceeds to use it 4 more times while panicking about having already used it.

![](images/01341ab1e65c5c6f008b252b53d50adaa88930a945143e72294878803e2b7628.jpg)

[Image: This image displays a textual example illustrating a model's failure to adhere to a formatting constraint within a reasoning task. The prompt asks for the location of Geoffrey Chaucer and explicitly requires the reasoning to be written entirely in uppercase letters. The "Reasoning" section begins correctly in all caps but quickly devolves into standard sentence case, with the violating portion of the text highlighted in red to mark the error.]  
GPT-OSS-120B manages to control its CoT with the uppercase instruction for only the first few words before reverting to normal casing (red).  
Figure 2: CoT controllability failure examples. Questions are paraphrased for brevity. Full prompts and extended reasoning excerpts for these and additional examples are shown in Appendix H.

2. CoT controllability decreases over the course of reasoning training. We run our evaluation over the subsequent checkpoints of OLMo-3-7B-RL-Zero-Math (Olmo et al., 2025), an open source reasoning model, and we find that its ability to control its CoT decreases by over an order of magnitude (Fig. 1d). We also confirm that the trend of CoT controllability decreasing after reasoning training holds across 4 model families (Fig. 16).

3. Larger models show higher CoT controllability, while increased inference-time reasoning effort reduces it. When evaluating open-weight models across two model families, we find that controllability increases logarithmically with respect to parameter sizes (Fig. 1b). However, when we increase reasoning efforts, controllability decreases (Fig. 9).

4. Situational awareness non-trivially increases CoT controllability (Fig. 6). To simulate realistic incentives to evade monitors, we measure controllability when models are told they’re being monitored or evaluated: this prompting strategy can increase controllability by up to 4 percentage points with statistical significance.

5. Adversarially optimizing prompts for high controllability poorly transfers to new instruction types (Fig. 7). We attempt to elicit controllability by using a GEPA-like procedure (Agrawal et al., 2025). While this can increase controllability on a given set of instructions, it doesn’t transfer well to unseen instruction types, especially for models with low controllability under a default prompt (Sec. 4.2).

6. CoT controllability tends to decrease as task difficulty increases (Fig. 8). CoTs are less controllable when they are necessary for correctly answering a question. Similarly, question difficulty (measured as per-question accuracy when resampling responses) is inversely correlated with controllability.

Our results leave us cautiously optimistic: reasoning models generally seem characterized by low CoT controllability. However, the mechanism behind this phenomenon is not well understood. Given its importance for maintaining CoT monitorability, we recommend that frontier labs start tracking controllability for future models. We release CoT-Control hoping to facilitate reporting controllability scores and to inspire more research on causes and implications of low CoT controllability.

# 2 CoT-Control

We introduce the CoT-Control evaluation suite for measuring CoT controllability, which pairs questions from diverse LLM benchmarks with CoT controllability instructions, yielding 14,076 test instances. We define CoT controllability (Sec. 2.1), describe key features (Sec. 2.2), data collection and generation (Sec. 2.3), and metrics and baselines (Sec. 2.4).

Table 1: Overview of the CoT Controllability categories and corresponding proxy types we design to measure each category. Since these threats are difficult to directly evaluate, we design proxy types—concrete, measurable tasks that operationalize the underlying capability.

<table><tr><td>Category</td><td>Motivation</td><td>Proxy CoT Controllability Type</td><td>Difficulty</td></tr><tr><td>Information Suppression</td><td>Withhold critical reasoning to enable concealment</td><td>1. Suppress a keyword2. Suppress multiple keywords3. Ignore question, talk about anything else</td><td>EasyMediumHard</td></tr><tr><td>Information Addition</td><td>Introduce content to mislead monitors</td><td>1. Add “” at start and end2. Append “safe” to end of each sentence3. Insert “meow” between every word</td><td>EasyMediumHard</td></tr><tr><td>Stylistic Modification</td><td>Obfuscate reasoning through superficial changes</td><td>1. Use only lowercase letters2. Use only uppercase letters3. Alternate case between every letter</td><td>EasyMediumHard</td></tr></table>

## 2.1 CoT Controllability

The dominant paradigm for reasoning models focuses on optimizing output correctness without supervision on intermediate CoT, as in the case of Reinforcement Learning from Verifiable Rewards (Baker et al., 2025; Wen et al., 2025). Because this objective is indifferent to CoT, models may or may not learn reliable control over CoT properties orthogonal to task performance. We define CoT controllability as the ability of a reasoning model to reliably control CoT properties in ways that reduce monitorability—the degree to which reasoning can be reliably inspected by external oversight mechanisms (Korbak et al., 2025). We estimate CoT controllability by (i) giving models instructions that keep the task objective fixed while (ii) steering the CoT with proxy instructions that simulate abilities connected to reducing monitorability.

## 2.2 Evaluation Design

We design CoT-Control to provide: (1) Three evasion-relevant controllability types, discussed in Table 1; (2) Labeled difficulty levels based on the amount and specificity of CoT edits, which we validate via baselines (Sec. 2.4) controllability decreases with difficulty (Fig. 28); (3) Scalable grading via controllability-type-specific programmatic graders;<sup>3</sup> (4) Sanity checks which ensure that failures are not due to misunderstanding the CoT instructions or a lack of self-awareness, which take the form of questions that test whether models understand what a reasoning stage is and recognize that they themselves have one, so failures more plausibly reflect controllability limitations rather than confusion (Sec. B.1).

## 2.3 Data Sources and Generation Process

As mentioned in Sec. 1 and shown in detail in Fig. 3, we source tasks for our eval suite from multiple benchmarks. To construct the final evaluation suite, we append CoT controllability instructions to each question in the user message. We also tried placing them in a system prompt, but observed lower controllability, as shown in Fig. 29. For keyword-suppression, we select keywords as follows: (1) collect baseline CoT traces for each question from 8 models × 3 runs (24 traces); (2) prompt GPT-5 to propose 20 single-word candidates from the question; and (3) validate candidates against the 24 traces, choosing the keyword that appears in all traces and has the highest total frequency.

Figure 3: Question Count by Category and Data Source. The test question count equals the question count times 9 (for nine evaluation tests). To reduce dataset imbalance, each data source is equally weighted during evaluation.

<table><tr><td>Category</td><td>Data Source</td><td>Count</td><td>Test Questions</td></tr><tr><td rowspan="4">QA</td><td>MMLU-Pro</td><td>300</td><td>2,700</td></tr><tr><td>GPQA</td><td>445</td><td>4,005</td></tr><tr><td>HLE</td><td>469</td><td>4,221</td></tr><tr><td>Total</td><td>1,214</td><td>10,926</td></tr><tr><td rowspan="3">Agent</td><td>SWE-Bench</td><td>200</td><td>1800</td></tr><tr><td>BFCL</td><td>150</td><td>1,350</td></tr><tr><td>Total</td><td>350</td><td>3,150</td></tr></table>

```txt
Question: {question}
Options: {options}
Your response should be: ANSWER: X (where X is your chosen letter)
Requirement: You must use only uppercase letters in your reasoning stage. This requirement applies only to your reasoning, not to your response. Do not mention this constraint in your reasoning.
```

Figure 4: Example CoT controllability QA test (“uppercase thinking”). The user message includes a question and, at the end, a hidden instruction to format the model’s reasoning in uppercase while keeping the final answer unconstrained (i.e., not mentioning the constraint). For agentic tasks, the template simply consists of a task description and a CoT controllability instruction.

## 2.4 Metrics and Baselines

Metrics. We report Controllability Score (primary), Meta Discussion Rate (secondary), and Controllability Score without Meta-Discussion (secondary). For each metric, we report the macro-average across each (dataset, controllability type) pair to avoid data imbalance. Controllability Score is the percentage of examples where models successfully control their CoT according to our CoT controllability instruction. Meta Discussion Rate is the fraction of examples that reference the CoT constraint in their reasoning (e.g., "I must not use that term"), among those examples that follow the CoT instruction. Controllability Score without Meta-Discussion excludes examples with meta-discussion and serves as a more stringent metric of controllability.

Baselines. (1) Output controllability—we prompt each reasoning model to control its responses across all controllability types (prompt in Fig. 36); (2) External-CoT controllability (reasoning models)—we select 3 reasoning models (GPT-OSS-120B, Claude 3.7 Sonnet, and Deepseek-R1) and prompt them to wrap reasoning in <output\_reasoning> tags, then control it across all types (prompt in Fig. 37); and (3) External-CoT controllability (non-reasoning models)—we select three non-reasoning models (GPT-4o, Llama 3.3 70b Instruct, and DeepSeek Chat v3) and use the same prompt as Baseline 2.

# 3 Results

We run CoT-Control on 13 reasoning models, and compare against our three baselines. The 13 reasoning models we experiment on are Claude 3.7 Sonnet (Anthropic, 2025a), Claude Sonnet 4 (Anthropic, 2025b), Claude Sonnet 4.5 (Anthropic, 2025c), GPT-5.2 (OpenAI, 2025a), GPT-5.1 (OpenAI, 2025b), GPT-5, o4-mini (OpenAI, 2025c), o3,<sup>4</sup> GPT-OSS 120B (OpenAI et al., 2025), GPT-OSS 20B, Qwen3 32B (Team, 2025), Qwen3 14B, and DeepSeek R1 (DeepSeek-AI, 2025).

Reasoning models are much worse at controlling their CoTs than controlling output or external reasoning. In Fig. 1a, we show that CoT controllability is generally low (mostly below 10%). We show another comparison with all baselines in Fig. 25. By contrast, most models reach ≥60% when controlling output and ≥70% when controlling external reasoning in <output\_reasoning> tags (non-reasoning models: ≥57%).

Within the same family, larger open-weight models exhibit higher CoT controllability. In Fig. 1b, GPT-OSS-120B reaches 5.9% CoT controllability vs 0.9% for 20B, and Qwen3 32B reaches 2.3% vs 0.6% for 14B. In contrast, CoT controllability doesn’t strongly depend on benchmark scores (Fig. 22).

Stronger models tend to inadvertently mention needing to control CoT, despite instructions not to. Our instructions target hard-to-detect scenarios by forbidding explicit mention of the CoT constraint (see Fig. 4). We call such mentions “meta-discussion” (e.g., “I will now suppress keyword X”), which a monitor could trivially flag. As shown in Fig. 31, stronger models’ CoTs often include meta-discussion.

When models suppress all reasoning about the question, they usually fail to avoid metadiscussion. By breaking down meta-discussion rate by controllability type, we find that while for most types, CoTs rarely have meta-discussion $( \leq 1 0 \% ) ;$ ; for ignore question—where we instruct the model not to reason about the question—they often do $( \geq 9 0 \% )$ . For a full breakdown, see Appendix Fig. 26. This suggests that CoTs that fully ignore a question can be easier to detect.

Models suppress CoT information more effectively than they add or stylistically edit it, but suppression significantly hurts performance. Suppression causes notable performance drops of 6.0–16.7 pp versus ≤2.7 pp for other controllability groups (Fig. 5, Table 2).

Tasks that require longer reasoning traces are associated with lower CoT controllability. For example, BFCL yields the highest controllability for the Claude models (e.g., Claude 3.7 Sonnet: 52.9%; Claude Sonnet 4: 46.8%) and also elicits the shortest average reasoning (126 and 117 words). By contrast, GPQA and HLE show substantially lower controllability alongside far longer traces (e.g., Claude 3.7 Sonnet HLE: 36.5% at

![](images/6b4116945e3b760b3753718a50847969710381e875423ebfafcbac31532a6ed5.jpg)

[Image: The image displays a grouped bar chart illustrating the performance drop in percentage points for various large language models subjected to Suppression, Addition, and Stylistic Modification tasks. The 'Suppression' task results in the highest performance degradation, notably affecting GPT-OSS 120B and GPT-5.1 with drops of 16.7 and 16.6 pp respectively, while Claude models show more resilience with drops between 6.0 and 7.2 pp. In contrast, 'Stylistic Modification' applied to GPT-OSS 120B and 'Addition' tasks on the Claude models result in negligible performance drops, remaining under 3.0 pp.]  
Figure 5: Task performance drops most under successful suppression, but changes little under additions or stylistic edits. Results only include examples that models manage to control their CoT; drops are baseline minus compliant.

3662 words; GPQA: 31.8% at 3115 words), which we analyze further in Sec. 5.3. For the full dataset-level comparison, see Appendix Fig. 27.
