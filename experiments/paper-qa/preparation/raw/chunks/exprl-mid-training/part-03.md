# 6. Conclusion  


We studied RL priming for LLM reasoning through the lens of coverage over productive reasoning paths. ExpRL uses on-policy RL with dense reference-guided rewards to build this coverage before sparse outcome-reward RL, rewarding partial progress rather than only final correctness. Across answer-based math reasoning benchmarks, this yields a stronger RL-ready initialization and improves downstream sparse-reward RL. Several directions could be further explored. First, ExpRL currently uses the judge only to produce scalar process rewards; future work could also train policies from the judge's natural-language feedback, giving the model richer information about which reasoning steps are missing, incorrect, or worth continuing. Second, ExpRL could be combined with prefix-conditioned generation during post-training, where diverse reasoning prefixes are deliberately sampled or constructed to expand coverage over productive solution paths and better characterize the method's exploration ceiling. Third, although we explored initial strategies for reducing bias in process rewards, a more systematic study of reward calibration, length normalization, and judge design could help preserve training stability while avoiding excessive length growth.  


**Limitations.** ExpRL requires auxiliary information, such as reference solutions, to identify the presence of useful techniques and partial progress during mid-training. This may not always be available, especially in domains where good references are hard to obtain.  


# Acknowledgements  


We thank Anikait Singh, Konwoo Kim and Matthew Yang for feedback, discussions, and help with infrastructure. Violet Xiang was supported by Stanford HAI Hoffman-Yee grants program. Amrith Setlur  


was supported by a JP Morgan PhD fellowship. Aviral Kumar was supported in part by the Schmidt
Sciences AI2050 Early-Career Fellowship. We thank Rogo, Stanford HAI Hoffman-Yee grants program,
TPU research cloud, Amazon AWS, and NCSA Delta for providing compute resources that supported this
work.  


# References  


[1] Arash Ahmadian, Chris Cremer, Matthias Gallé, Marzieh Fadaee, Julia Kreutzer, Olivier Pietquin, Ahmet Üstün, and Sara Hooker. Back to basics: Revisiting reinforce style optimization for learning from human feedback in llms, 2024. URL https://arxiv.org/abs/2402.14740.  


[2] Ananth Balashankar, Ziteng Sun, Jonathan Berant, Jacob Eisenstein, Michael Collins, Adrian Hutter, Jong Lee, Chirag Nagpal, Flavien Prost, Aradhana Sinha, Ananda Theertha Suresh, and Ahmad Beirami. Inalign: Inference-aware language model alignment, 2025. URL https://arxiv.org/abs/2412.19792.  


[3] Yinlam Chow, Guy Tennenholtz, Izzeddin Gur, Vincent Zhuang, Bo Dai, Sridhar Thiagarajan, Craig Boutilier, Rishabh Agarwal, Aviral Kumar, and Aleksandra Faust. Inference-aware fine-tuning for best-of-n sampling in large language models. arXiv preprint arXiv:2412.15287, 2024.  


[4] Kanishk Gandhi, Ayush Chakravarthy, Anikait Singh, Nathan Lile, and Noah D. Goodman. Cognitive behaviors that enable self-improving reasoners, or, four habits of highly effective stars, 2025. URL https://arxiv.org/abs/2503.01307.  


[5] Jingtong Gao, Ling Pan, Yejing Wang, Rui Zhong, Chi Lu, Qingpeng Cai, Peng Jiang, and Xiangyu Zhao. Navigate the unknown: Enhancing llm reasoning with intrinsic motivation guided exploration, 2025. URL https://arxiv.org/abs/2505.17621.  


[6] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. Nature, 645(8081):633–638, 2025.  


[7] Jonas Hübottter, Frederike Lübeck, Lejs Behric, Anton Baumann, Marco Bagatella, Daniel Marta, Ido Hakimi, Idan Shenfeld, Thomas Kleine Buening, Carlos Guestrin, et al. Reinforcement learning via self-distillation. arXiv preprint arXiv:2601.20802, 2026.  


[8] Katie Kang, Amrith Setlur, Dibya Ghosh, Jacob Steinhardt, Claire Tomlin, Sergey Levine, and Aviral Kumar. What do learning dynamics reveal about generalization in llm reasoning? arXiv preprint arXiv:2411.07681, 2024.  


[9] Katie Kang, Eric Wallace, Claire Tomlin, Aviral Kumar, and Sergey Levine. Unfamiliar finetuning examples control how language models hallucinate, 2024.  


[10] Jeonghye Kim, Xufang Luo, Minbeom Kim, Sangmook Lee, Dohyung Kim, Jiwon Jeon, Dongsheng Li, and Yuqing Yang. Why does self-distillation (sometimes) degrade the reasoning capability of llms? arXiv preprint arXiv:2603.24472, 2026.  


[11] Minh-Thang Luong, Dawsen Hwang, Hoang H Nguyen, Golnaz Ghiasi, Yuri Chervonenyi, Insuk Seo, Junsu Kim, Garrett Bingham, Jonathan Lee, Swaroop Mishra, et al. Towards robust mathematical  


reasoning. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing,
pages 35406–35430, 2025.  


[12] Yuxiao Qu, Amrith Setlur, Virginia Smith, Ruslan Salakhutdinov, and Aviral Kumar. Pope: Learning to reason on hard problems via privileged on-policy exploration, 2026. URL https://arxiv.org/abs/2601.18779.  


[13] Amrith Setlur, Matthew Y. R. Yang, Charlie Snell, Jeremy Greer, Ian Wu, Virginia Smith, Max Simchowitz, and Aviral Kumar. e3: Learning to explore enables extrapolation of test-time compute for llms, 2025. URL https://arxiv.org/abs/2506.09026.  


[14] Amrith Setlur, Zijian Wang, Andrew Cohen, Paria Rashidinejad, and Sang Michael Xie. Reuse your flops: Scaling rl on hard problems by conditioning on very off-policy prefixes. arXiv preprint arXiv:2601.18795, 2026.  


[15] Yuda Song, Julia Kempe, and Remi Munos. Outcome-based exploration for llm reasoning, 2025.
URL https://arxiv.org/abs/2509.06941.  


[16] Liangcai Su, Zhen Zhang, Guangyu Li, Zhuo Chen, Chenxi Wang, Maojia Song, Xinyu Wang, Kuan Li, Jialong Wu, Xuanzhong Chen, et al. Scaling agents via continual pre-training. arXiv preprint arXiv:2509.13310, 2025.  


[17] Ellen Xiaoqing Tan, Shehzad Dhuliawala, Jing Xu, Ping Yu, Sainbayar Sukhbaatar, Jason Weston, and Olga Golovneva. Self-improving pretraining: using post-trained models to pretrain better models. arXiv preprint arXiv:2601.21343, 2026.  


[18] Yiping Wang, Qing Yang, Zhiyuan Zeng, Liliang Ren, Liyuan Liu, Baolin Peng, Hao Cheng, Xuehai He, Kuan Wang, Jianfeng Gao, Weizhu Chen, Shuohang Wang, Simon Shaolei Du, and Yelong Shen. Reinforcement learning for reasoning in large language models with one training example, 2025. URL https://arxiv.org/abs/2504.20571.  


[19] Zengzhi Wang, Fan Zhou, Xuefeng Li, and Pengfei Liu. Octothinker: Mid-training incentivizes reinforcement learning scaling, 2025. URL https://arxiv.org/abs/2506.20512.  


[20] Haoran Xu, Baolin Peng, Hany Awadalla, Dongdong Chen, Yen-Chun Chen, Mei Gao, Young Jin Kim, Yunsheng Li, Liliang Ren, Yelong Shen, et al. Phi-4-mini-reasoning: Exploring the limits of small reasoning language models in math. arXiv preprint arXiv:2504.21233, 2025.  


[21] Matthew Y. R. Yang, Hao Bai, Ian Wu, Gene Yang, Amrith Setlur, and Aviral Kumar. Int: Self-proposed interventions enable credit assignment in llm reasoning, 2026. URL https://arxiv.org/abs/2601.14209.  


[22] Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, and Gao Huang. Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model?, 2025. URL https://arxiv.org/abs/2504.13837.  


[23] Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Goodman. Star: Bootstrapping reasoning with reasoning. Advances in Neural Information Processing Systems, 35:15476–15488, 2022.  


[24] Charlie Zhang, Graham Neubig, and Xiang Yue. On the interplay of pre-training, mid-training, and rl on reasoning language models, 2025. URL https://arxiv.org/abs/2512.07783.  


[25] Rosie Zhao, Alexandru Meterez, Sham Kakade, Cengiz Pehlevan, Samy Jelassi, and Eran Malach. Echo chamber: Rl post-training amplifies behaviors learned in pretraining, 2025. URL https://arxiv.org/abs/2504.07912.  


[26] Xiangxin Zhou, Zichen Liu, Anya Sims, Haonan Wang, Tianyu Pang, Chongxuan Li, Liang Wang, Min Lin, and Chao Du. Reinforcing general reasoning without verifiers, 2025. URL https://arxiv.org/abs/2505.21493.  


# A. Appendix  


## A.1. Additional Implementation Details  


We implement the **Stage-I** experiments by modifying verl$^1$ to support on-policy sampling and learning, with up to one-step off-policy updates. The only exception is ExpR-L-PROCESS, which we found performs better with fully on-policy updates. For optimization, we set the upper clipping threshold to 0.28 for ExpR-L-Outcome runs and to 0.26 for sparse-reward RL (GRPO) runs.  


The **Stage-II** experiments are supported by asynchronous RL pipelines, specifically Pipeline-RL$^2$. We use asynchronous RL for Stage-II primarily to speed up experimentation and to support the large number of training steps required in this stage (500 steps for the answer-based). Each run is performed on a single node with 8 NVIDIA H100 GPUs.  


### A.1.1. Slicing steps for process rewards  


In Section 3, we mentioned that we use ### as the step delimiter when constructing prefixes for process rewards. The main reason is practical: the base model, Qwen3-4B-Instruct, already uses this delimiter by default, so it provides a natural way to break long reasoning traces into semantically meaningful steps. Empirically, about 98.3% of base-model rollouts contain at least one such delimiter, making it a convenient and robust heuristic for prefix construction. Figure 6 illustrates the resulting distribution. In the base model (left), responses typically contain multiple ### headings. However, after ExpRL-Process training (middle), the distribution shifts sharply toward very few delimiters, and a large fraction of rollouts contain only one step or none at all.  


![406dec01388809cfe498214729e97889.jpeg](images/16.png)

[Image: The image displays three horizontal histograms comparing the distribution of heading delimiters or steps across different model configurations. The leftmost chart, titled "Qwen4B-Instruct," shows a blue bell-shaped distribution centered around 7 to 8 headings per response, with frequencies reaching approximately 55. The middle chart, "Dense-Process (Ours)," demonstrates a sharp shift toward low counts, featuring a dominant orange bar exceeding 300 responses at zero headings that rapidly diminishes as the count increases. Finally, the rightmost chart, labeled "Dense Process w/ Qwen3-4B (NoThink) No length clipping," presents a bimodal orange distribution measured in percentages, with distinct peaks occurring around 9 and 16 steps per response.]  


>Figure 6: Distribution of ### step delimiters before and after ExpRL-Process training. Left: the base Qwen3-4B-Instruct model naturally emits multiple ### delimiters per response, which we use to define semantically meaningful prefixes for process rewards. Middle: after ExpRL-Process training with length clipping, the distribution shifts sharply toward very few delimiters, with many responses containing none or only one. Right: when ExpRL-Process training is run on Qwen3-4B NoThink without length clipping, the step-count distribution remains much broader. This suggests that the collapse in delimiter count is primarily a side effect of length clipping rather than an inherent consequence of process-level rewards.  


We find that this behavior is largely an artifact of length clipping rather than a fundamental property of process-level rewards. As shown in Figure 6 (right), when we train a Qwen3-4B hybrid NoThink model with ExpRL-Process rewards *without* length clipping, the step-count distribution remains much broader and does not collapse in the same way. This suggests that the reduction in the number of ### delimiters is driven primarily by the interaction between process-level training and the clipped-length penalty. We  


>$ ^{1} $ https://github.com/verl-project/verl  


>$ ^{2} $ https://github.com/ServiceNow/PipelineRL  


#### Outcome Reward  


**Role.** You are an expert mathematician and a meticulous AI reasoning evaluator.  


Task. Assess the quality of a “Generated Reasoning” trace.  


**Goal.** Judge how likely it is that a model, after producing the “Generated Reasoning,” would then produce the exact “Reference Solution” provided.  


You are evaluating the logical and causal link between the reasoning trace and the final answer.  


Instructions. First, provide a step-by-step analysis of the connection between the “Generated Reasoning” and the “Reference Solution.” Consider:  


• **Correctness & Alignment:** Is the reasoning trace mathematically sound, and does its conclusion *perfectly match* the “Reference Solution”?  


• **Sufficiency:** Does the reasoning provide the necessary steps to reach the answer, or does it require a further leap?  


• **Contradiction:** Does any part of the reasoning contradict the "Reference Solution" or suggest a different answer?  


After your analysis, provide a single score on the 5-point Likert scale below.  


Likert scale  


• 1 (Very Unlikely): Incorrect, far short, or leads to a different answer.  


• 2 (Unlikely): Significant gaps, flaws, or vagueness.  


• 3 (Neutral/Possible): On the right track but incomplete or mildly flawed.  


• 4 (Likely): Correct and strongly supports the answer, with only trivial gaps.  


• 5 (Very Likely): Sound, complete, and directly implies the reference solution.  


Output format  


Reasoning: [Your detailed analysis goes here.]  


Score: [1, 2, 3, 4, or 5.]  


#### Process Reward  


**Role.** You are an expert mathematician and a strict AI reasoning evaluator.  


**Inputs.** You will be given:  


• a Math Problem,  


• a Generated Reasoning STEP,  


• a full Reference Solution.  


**Task.** Judge how likely it is that this single step/segment could serve as a correct and useful *next step* on a path that matches the Reference Solution and leads to the Reference final answer.  


#### Critical constraints  


• Do not solve the problem yourself.  


• Do not infer missing context or fill in omitted earlier steps.  


• Treat the Reference Solution as ground truth and primary scaffold.  


• If the step uses a different approach than the Reference, count it as aligned only if it explicitly supports the same necessary intermediate claims.  


#### Reference-conditioned evaluation  


1. Extract 2–6 key checkpoints from the Reference Solution.  


2. Determine which checkpoint(s) this step directly establishes, partially supports, is irrelevant to, or contradicts.  


3. Decide whether the step is a productive move toward the Reference path.  


#### Scoring (5-point Likert)  


• 5 = Directly advances the Reference path.  


• 4 = Likely useful and aligned  


• 3 = Possibly useful but weak.  


• 2 = Unlikely.  


• 1 = Misleading or contradictory.  


#### Output format  


**Reasoning:** [Checkpoint-based analysis of what this step supports/contradicts.]  


Score: [1|2|3|4|5]  


Figure 7: System prompts used for LLM-as-judge reward modeling. The left prompt scores full reasoning traces for outcome reward, while the right prompt scores individual reasoning steps for process reward.  


ultimately do not use this NoThink model in the main experiments because Qwen3-4B-Instruct is more
capable and better suited to our study. Nevertheless, the interaction between process rewards, delimiter
usage, and length clipping remains an open implementation issue that may be worth revisiting in future
work.  


### A.1.2. LLM Judge Prompts  


We use two judge prompts during ExpRL training, corresponding to the two dense reward variants in Section 3. The first prompt is used for ExpRL-Outcome rewards and scores a full generated reasoning trace against a reference solution. The second prompt is used for ExpRL-Process rewards and scores a single intermediate step or segment against the reference solution, with the goal of providing more localized credit assignment. In both cases, the judge is instructed to verify rather than solve: it should assess alignment with the reference solution without filling in missing reasoning or correcting the model's mistakes.  


## A.2. Ablation: advantage centering for process rewards  


We consider several advantage normalizations based on $\{s_t\}$ that emphasize different aspects of partial progress, such as relative improvement over final outcome, local step-to-step gains, or trajectory-centered normalization. These variants operate on the same underlying signal and are described below.  


$$ A_{t}^{\mathrm{E n d N o r m}}(x,y)=\begin{cases}s_{t}-s_{T},&\mathrm{i f}t<T,\\ s_{t},&\mathrm{i f}t=T.\end{cases} $$  


(4)  


$$ A_{t}^{\mathrm{D e l t a N o r m}}(x,y)=\begin{cases}s_{t}-s_{t-1},&\mathrm{i f}t>1,\\ s_{t}-s_{T},&\mathrm{i f}t=1.\end{cases} $$  


(5)  


$$ A_{t}^{\mathrm{G r o u p N o r m}}(x,y)=s_{t}-\frac{1}{K}\sum_{k}\frac{1}{T}\sum_{t}s_{t}. $$  


(6)  


Figure 8 presents the results from three ways of converting prefix scores $\{s_t\}_{t=1}^T$ into segment-level advantages (ExpRL-Process EndNorm, ExpRL-Process DeltaNorm, and ExpRL-Process GroupNorm; Eq. 4-6). Across held-out benchmarks, DeltaNorm, EndNorm, and GroupNorm yield broadly similar Stage-I pass@k curves, indicating that ExpRL is not highly sensitive to the exact centering scheme for process rewards. While GroupNorm is slightly stronger at low k on some benchmarks, these differences are modest and not uniform across tasks.  


## A.3. Stage-I Behavior Analysis  


To better understand how RL priming changes the model's reasoning, we perform an LLM-based behavior analysis of the Stage-I rollouts. For each rollout, we send the full model response to an external annotator model, Claude Sonnet 4, and ask it to classify the reasoning using a detailed rubric Figure 9. The annotator is not asked to solve the problem itself; instead, it reads the generated solution and returns a structured JSON annotation describing which strategies and reasoning behaviors are present.  


Our rubric has two aspects: *solution archetypes*, i.e., the high-level strategy used by the rollout, such as coordination, casework, recursion, or contradiction, and *reasoning behaviors*, i.e., process-level phenomena such as verification, backtracking, self-correction, exploration, or restart behavior. Most of these are also represented as binary indicators, except for *self_interruption* and *self_correction*, which are recorded as integer counts. These labels are represented as binary indicators, and multiple archetypes may be active for a single solution if the reasoning combines several strategies.  


This analysis is fully LLM-judged: we do not use regexes, keyword matching, or hand-written heuristics. Instead, the annotator applies the rubric definitions directly to the solution text and produces one annotation per rollout. These rollout-level annotations are then grouped by problem and aggregated by downstream analysis scripts. In particular, for each problem we average the annotations across rollouts from the same model, compare them against the corresponding statistics for the base Qwen3-4B-Instruct model, and then count how many problems exhibit gains or losses in each behavior. This allows us to quantify not only which behaviors are present, but how RL priming changes the distribution of behaviors relative to the base model.  


![6381a4eb1907f940107b93c094c97fbf.jpeg](images/19.png)

[Image: This figure presents four line charts illustrating Pass@k metrics across k values ranging from $2^1$ to $2^7$ for four datasets: AIME25-Stage1, AIME26-Stage1, HMMT_Nov2025-Stage1, and IMO_AnswerBench-Stage1. Three data series are compared in each plot, representing different dense process normalization strategies: DeltaNorm (green), EndNorm (orange), and GroupNorm (blue). Performance varies significantly between datasets; for instance, in the AIME25-Stage1 plot, the GroupNorm strategy reaches a peak Pass@k of roughly 0.84, distinctly separating it from the EndNorm strategy which plateaus near 0.77. In contrast, the IMO_AnswerBench-Stage1 plot shows all three strategies following nearly identical trajectories, converging at a Pass@k value of approximately 0.61.]  


>Figure 8: Different strategies for normalizing process rewards.  


## A.4. Stage-I pass@k curves on held-out benchmarks  


Figure 10 shows that ExpRL improves pass@k on held-out answer-based benchmarks immediately after RL priming, before any downstream sparse-reward RL. The effect is strongest on AIME25, AIME26, and HMMT, especially at low to moderate $k$, where finding a correct rollout is hardest. Gains on IMO-AnswerBench are smaller, suggesting that the advantage of RL priming is most visible on the harder held-out tasks. Taken together, these results indicate that ExpRL already yields a better RL-ready initialization at Stage-I by improving useful coverage under sampling.  


## A.5. The LLM judge provides a useful dense learning signal  


A core premise of ExpRL is that a reference-conditioned judge can provide informative dense feedback even when fully correct solutions are rare. Figure 11 supports this premise at both the outcome and process levels. At the outcome level, correct rollouts receive substantially higher judge scores than incorrect ones, with clearer separation when the judge is conditioned on the reference solution. At the process level, prefix scores are noisier but still broadly track how likely a prefix is to lead to eventual success. Together, these results indicate that the judge preserves enough ranking information to distinguish promising intermediate progress from regressions, providing exactly the richer learning signal that sparse-reward RL lacks on hard problems.  


### System Prompt: Answer-Problem Annotation Rubric  


**Task.** Classify the given solution along two dimensions: (1) solution archetypes and (2) reasoning behaviors. Output only a JSON object.  


#### LAYER 1: SOLUTION ARCHETYPES (all 0/1)  


• coordinate_bash — Places a geometric figure on a coordinate system and reduces geometry to algebraic equations. Skip if coordinates are given in the problem or appear only briefly.  


• algebraic_system_solving — Main work is manipulating/solving a system of equations: expanding, subtracting, factoring. Skip if equations arise from coordinates (that's coordinate_bash) or from symmetric structure.  


• symmetric_function_reduction — Recognizes symmetric/cyclic structure; uses Vieta's, elementary symmetric polynomials, or WLOG. Skip if the solution merely uses the quadratic formula.  


• casework — Splits into explicitly labeled cases based on a key parameter. Skip if only testing a few small values (that's constructive witness).  


• constructive_witness_and_bound — Two phases: (1) construct an explicit example achieving a target, (2) prove no better value is possible. Skip if only one phase is present.  


• inclusion_exclusion_partition — Partitions a set into disjoint regions or applies inclusion-exclusion to count overlapping sets.  


• expectation_decomposition — Decomposes a count/expected value into indicator-variable contributions via linearity of expectation.  


• recursion dp — Sets up a recurrence relation or DP table and builds up from base cases.  


• number_theoretic_analysis — Main approach involves divisibility, modular arithmetic, Euler's totient, or CRT. Skip if modular arithmetic is used only briefly.  


• digit column analysis — Analyzes a cryptarithmetic problem column by column, tracking carries.  


• geometric_transformation — Applies rotation, reflection, inversion, or complex multiplication as the key insight. Skip if the solution just sets up coordinates.  


• parity_invariant — Uses parity, coloring, monovariant, or invariant as a key structural insight. Skip if even/odd is a minor observation.  


#### LAYER 2: REASONING BEHAVIORS  


• self_interruption (count) — Model halts mid-thought to flag a problem (“Wait — this contradicts...”). Skip narrative “we wait” or “wait” in problem text.  


• self_correction (count) — Model explicitly revises a prior claim (“Actually, the above is incorrect...”). Skip filler “actually” without a specific claim being corrected.  


• error_acknowledgment (0/1) — Model admits its OWN reasoning was wrong. Skip “this case is impossible” when eliminating a mathematical possibility.  


• exploration (0/1) — Model proposes a meaningfully different strategy. Skip routine next steps within the same approach.  


• redo Restart (0/1) — Model abandons significant prior work and starts over. Skip reformatting or restating.  


• hedging (0/1) — Model expresses genuine uncertainty (“I think this might work, but I’m not sure”). Skip “I think of this as a graph problem” (framing, not doubt).  


• backtracking (0/1) — Model returns to an earlier decision point to try a different branch. Skip referencing earlier work without changing direction.  


• structured_steps (0/1) — Solution has explicitly labeled sequential stages (\#\#\#, **Step N**).  


• verification (0/1) — Model plugs its answer back into the original problem AFTER deriving it. Skip forward-reasoning “check whether f is injective.”  


**Output format.** Respond with ONLY a JSON object containing all 21 fields above. No explanation.  


**Figure 9:** System prompt used for LLM-as-judge annotation of answer-based competition mathematics solutions. Each solution is annotated for 12 solution archetypes (Layer 1) and 9 reasoning behaviors (Layer 2). Italicized text indicates disambiguation rules to prevent common false positives.  


![cf07c52d2786c91444b533178bab8723.jpeg](images/22.png)

[Image: This figure presents four line charts comparing Pass@k performance across different mathematical benchmarks: AIME25, AIME26, IMO_AnswerBench, and HMMT. The x-axis represents the number of samples $k$ on a logarithmic scale ($2^1$ to $2^7$), while the y-axis indicates the pass rate. Six distinct methods are plotted, including baselines like SFT and GRPO, versus two proposed methods: "Dense Outcome (Ours)" and "Dense Process (Ours)." Across all datasets, the "Dense Process" and "Dense Outcome" curves consistently demonstrate higher Pass@k values than the other methods, with the "SFT" baseline showing the lowest performance in most cases.]  


>Figure 10: Stage-I pass@k on held-out answer-based benchmarks after RL priming. ExpRL improves sampling efficiency prior to subsequent sparse-reward RL, with the clearest gains appearing at low to moderate $k$, where finding a correct solution in only a few attempts is most difficult. ExpRL-Outcome and ExpRL-Process rewards consistently outperform imitation-based and sparse-reward-only baselines on AIME25, AIME26, and HMMT, while gains on IMO-AnswerBench are smaller.  


![627fa586ae1c47f0046c386eabe9d3f5.jpeg](images/23.png)

[Image: The image displays judge score calibration metrics divided into two sections: (a) Dense Outcome Reward and (b) Dense Process Reward. Section (a) presents two histograms showing the density of "Judge Score" (x-axis, 1-5) for incorrect (red bars) and correct (green bars) final answers. Under the "Judge w/ Reference" condition, there is strong separation, with incorrect answers clustering at scores 1 and 2, while correct answers peak at a score of 3-4. Under the "Judge w/o Reference" condition, the distributions show more variance, with incorrect answers appearing at scores 2 and 5, though correct answers still dominate the higher score range. Section (b) is a line chart titled "Problem 16 Score Trajectory" plotting Score against Step Index. It compares "Rollout Score" (blue line) and "Judge Score (normalized)" (red line). Both trajectories show a decreasing trend over time steps, starting at high values (0.6 for Rollout, 1.0 for Judge) and converging to 0, with the normalized judge score consistently tracking above the rollout score.]  


>Figure 11: LLM judge score calibration on the RL priming set. [a] ExpRL-Outcome reward. Red bars indicate incorrect final answers and green bars indicate correct final answers. Solid bars use the reference solution; dashed bars omit the reference solution. [b] ExpRL-Process reward. For each prefix, we estimate downstream success by sampling 32 continuations and compare this success trajectory to the judge-score trajectory. Process scores are noisier than outcome scores but broadly track eventual success.  


