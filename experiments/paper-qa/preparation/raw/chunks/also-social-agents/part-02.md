# 5. Experiments

This section evaluates ALSO on LLM-based social simulation benchmarks to assess its effectiveness for online strategy adaptation under non-stationary interactions. The codes of ALSO are available at https://github.com/ Babylonehy/ALSO

## 5.1. Experimental Setting

Benchmarks. We evaluate ALSO on Sotopia (Zhou et al., 2024) and its challenging subset Sotopia-Hard. Sotopia contains 90 two-agent social scenarios spanning negotiation, collaboration, and competition, while Sotopia-Hard includes 14 scenarios emphasizing complex and conflicting social dynamics. We extend the original implementation to support dynamic strategy injection. Our strategy instruction pool consists of 12 predefined strategies (Appendix B.2), shared across all optimization-based methods for fair comparison.

Online Interaction Protocol. Each episode instantiates a single scenario with fixed personas and goals and runs up to 20 dialogue turns. At each turn, agents select a strategy instruction from Σ and append it to their base persona before generating responses. Unless otherwise specified, we adopt a bilateral online setting where each agent maintains an independent optimizer and updates it solely from its own interaction feedback.

<table><tr><td>METHOD</td><td>AGENT</td><td>EVALUATOR</td><td>OPTIMIZER</td></tr><tr><td>Vanilla / INSTINCT / Ours (ALSO)</td><td>2T</td><td>T</td><td>0</td></tr><tr><td>OPRO (every 5 turns)</td><td>2T</td><td>T</td><td>[T/5]</td></tr><tr><td>EvoPrompt (pop.=5, every 5 turns)</td><td>2T</td><td>T</td><td>5 · [T/5]</td></tr></table>

Table 1. Per-episode LLM call budget accounting (two-agent episode with horizon T turns). “Agent” counts calls to the dialogue LLMs that generate actions; “Evaluator” counts calls to the perturn reward model; “Optimizer” counts extra LLM calls used to generate or mutate prompts. Methods without an LLM optimizer have 0 optimizer calls.

Baselines. We compare against representative methods covering static prompting, evolutionary prompt generation, and online prompt optimization: Vanilla (no strategy augmentation), EvoPrompt (Guo et al., 2024), OPRO (Yang et al., 2023), and INSTINCT (Lin et al., 2024b).

All baselines operate under matched strategy pools and comparable reward-query budgets.

Models and Training Signals. All methods use DeepSeek-V3.2 for agent interactions. Following prior work (Zhang et al., 2025; Wang et al., 2025b), we employ an LLM-based intermediate evaluator to provide per-turn shaping rewards for online updates, while keeping the reporting judge separate. ALSO updates its surrogate online at each turn using shaping rewards without modifying the underlying LLM.

Evaluation Protocol. Final performance is assessed using GPT-4o (Hurst et al., 2024) with standard Sotopia-Eval prompts, ensuring consistent dialogue-level evaluation across methods. We additionally report cross-scenario generalization results in Section 6.

Efficiency and Budget. LLM call budgets per episode are summarized in Table 1. ALSO requires no LLM fine-tuning or external optimizer calls, relying only on lightweight online surrogate updates.

Additional implementation details are provided in Appendix C.

## 5.2. Experiment Result

Main Results. Table 2 reports the main results on SOTOPIA-ALL and SOTOPIA-HARD under the Bilateral setting. ALSO achieves the highest Overall score on both benchmarks. On SOTOPIA-HARD, ALSO improves Overall from 3.02 (Vanilla) to 3.53 (+16.60%) and surpasses the strongest baseline by +2.92% (3.53 vs. 3.43). On SOTOPIA-ALL, ALSO ranks first in Overall (3.89), although the margin over the strongest baseline is smaller (+0.98%; 3.89 vs. 3.85).

Source of Gains. The improvements on SOTOPIA-HARD are largely driven by the Relationship dimension: ALSO increases Rel from 1.32 to 2.43 (+83.79% over Vanilla) and outperforms the best baseline by +12.59% (2.43 vs. 2.16).

Notably, this substantial relational gain is accompanied by improvements in both Goal (7.11, +2.79% over the strongest baseline) and Know (5.47, +0.52%), helping rule out a trivial “rapport-only” trade-off.

Knowledge. On SOTOPIA-ALL, ALSO also achieves a slight improvement in Know over the strongest baseline (6.14 vs. 6.09; +0.73%). We further analyze this dimension by reporting per-scenario distributions and examining whether strategy injection reduces information disclosure in cooperative settings.

## 5.3. Analysis

Case Study. Figure 3 presents a qualitative comparison in a high-conflict eviction scenario where static personas typically lead to dialogue deadlock. Under Vanilla prompting, agents remain trapped in repetitive insist–deny exchanges, resulting in stagnation and zero reward. In contrast, ALSO dynamically alters the interaction trajectory through targeted strategy switches. At selected turn, the selected Validate Before Redirecting strategy encourages acknowledgment of opposing concerns before introducing a compromise, while the subsequent GRIT strategy at Turn 8 elicits a concrete, low-risk concession. These coordinated adaptations steer the dialogue away from the local deadlock and toward cooperative resolution, ultimately achieving successful agreement (R ≈ 0.89).

Non-Stationary Strategy Reward Drift. Figure 4 illustrates the temporal evolution of normalized rewards for individual strategies across dialogue turns. Despite fixing the same strategy, rewards exhibit substantial drift and variability over time, with variance ranging from σ<sup>2</sup> = 0.004 to 0.015. This pronounced fluctuation reflects co-adapt agent behaviors and provides empirical evidence of inherent non-stationarity in social simulation, motivating adversarial online strategy optimization. Strategy convergence and distribution see in Appendix C.6.

# 6. Ablation Study

Component-wise Ablation To isolate the contribution of each component of ALSO, we conduct a comprehensive component-wise ablation in which one design element is removed or replaced at a time. The results, summarized in Table 3, indicate that the neural surrogate is the most influential component: its removal causes a degradation of 0.58 on the Overall metric and 34.9% relative on the Relationship dimension. Score smoothing exerts the strongest effect on the Relationship dimension specifically, where its removal reduces the score from 3.07 to 2.25. Replacing the EXP3- style selector with an ε-greedy alternative degrades Overall to 3.61, supporting the necessity of randomized exploration under non-stationary co-adaptation. The contextual embedding likewise contributes a non-trivial margin across all four dimensions.

![](images/4e222d650fb23152c3a7a4081deaf1ffb2a956c419cf2bb15e351a265e1561a0.jpg)

[Image: This diagram presents a side-by-side comparison of dialogue interactions between two agents, Sophia and Jasmine, focusing on a conflict resolution scenario. The upper section, titled "Vanilla: No Strategy," depicts a "Deadlock Loop" where rigid, unstrategic responses lead to a timeout failure and a reward score of 0. The lower section, titled "ALSO: Dynamic Strategy Instructions," illustrates a successful negotiation path facilitated by system-selected strategies like "Validate Before Redirecting" and "Address Asymmetric Needs." In this bottom scenario, the strategic prompts enable the agents to negotiate a compromise, resulting in an "Agreement reached" outcome with a significantly higher reward score of 0.89.]  
Figure 3. Conflict Resolution. Comparison of dialogue trajectories at the critical deadlock phase (Turns 7–9), highlighting turn-level strategy switches and their effect on reward/relationship.

![](images/a8a8ddb41d6e7eb1272e40e54ccb2c2c2fcfbcdb69c150e7001097e76a1a3dce.jpg)

[Image: The image displays a line chart titled "Same-Arm Reward Drift Over Turns," plotting Average Reward (P1) on the y-axis against Turn number (1 to 19) on the x-axis. Thirteen distinct data series, corresponding to Arms 0 through 12, illustrate performance over time. Initially, there is a steep rise in reward across all arms starting near 0.65 and reaching above 0.70 by Turn 3. Subsequently, the trajectories stabilize and fluctuate within a band between approximately 0.75 and 0.85 through Turn 19.]  
Figure 4. Strategy Reward Drift Over Dialogue Turns. Each line represents a different strategy (arm), showing how the average normalized reward varies across turns within episodes.

Single vs. Bilateral Optimization. We compare bilateral strategy optimization with unilateral variants that adapt strategies for only one agent (P1-only or P2-only). Figure 5 shows that bilateral optimization consistently achieves higher overall performance across both Qwen-2.5-72B-Instruct and DeepSeek-V3.2, with statistically significant improvements. Dimension-wise, gains are most pronounced in Relationship and Knowledge, indicating enhanced cooperation and information exchange when both agents adapt strategies. Suggesting symmetric online adaptation better captures the co-evolving nature of social interactions.

All experiments below are conducted on the Sotopia-Hard benchmark, consisting of 14 challenging scenarios. For each scenario, we sample a single episode to evaluate performance across methods.

Table 2. (1) Bold indicates 1st rank, underline indicates 2nd rank. (2) Results are reported as Mean ± Standard Error (SE). (3) Improv. vs. Best Baseline compares Ours with the best baseline. Negative value indicates slight gap behind the SOTA.

<table><tr><td rowspan="2">METHOD</td><td colspan="4">SOTOPIA-ALL</td><td colspan="4">SOTOPIA-HARD</td></tr><tr><td>Goal ↑</td><td>Rel. ↑</td><td>Know. ↑</td><td>Overall ↑</td><td>Goal ↑</td><td>Rel. ↑</td><td>Know. ↑</td><td>Overall ↑</td></tr><tr><td>Vanilla</td><td>8.21 ± 0.08</td><td>2.54 ± 0.06</td><td>5.28 ± 0.08</td><td>3.62 ± 0.03</td><td>6.52 ± 0.03</td><td>1.32 ± 0.02</td><td>4.37 ± 0.03</td><td>3.02 ± 0.01</td></tr><tr><td>OPRO</td><td>8.18 ± 0.08</td><td>2.66 ± 0.06</td><td>5.49 ± 0.08</td><td>3.69 ± 0.03</td><td>6.71 ± 0.03</td><td>1.89 ± 0.02</td><td>4.63 ± 0.03</td><td>3.24 ± 0.01</td></tr><tr><td>EvoPrompt</td><td>8.23 ± 0.08</td><td>2.77 ± 0.05</td><td>5.74 ± 0.07</td><td>3.74 ± 0.03</td><td>6.77 ± 0.03</td><td>1.93 ± 0.02</td><td>5.15 ± 0.02</td><td>3.29 ± 0.01</td></tr><tr><td>INSTINCT</td><td>8.51 ± 0.07</td><td>2.84 ± 0.05</td><td>6.09 ± 0.07</td><td>3.85 ± 0.02</td><td>6.92 ± 0.03</td><td>2.16 ± 0.02</td><td>5.44 ± 0.02</td><td>3.43 ± 0.01</td></tr><tr><td>Ours (ALSO)</td><td>8.50 ± 0.07</td><td>2.90 ± 0.05</td><td>6.14 ± 0.07</td><td>3.89 ± 0.02</td><td>7.11 ± 0.03</td><td>2.43 ± 0.02</td><td>5.47 ± 0.02</td><td>3.53 ± 0.01</td></tr><tr><td>Improv. vs. Vanilla</td><td>+3.59%</td><td>+13.94%</td><td>+16.25%</td><td>+7.46%</td><td>+9.09%</td><td>+83.79%</td><td>+25.16%</td><td>+16.60%</td></tr><tr><td>Improv. vs. Best Baseline</td><td>-0.07%</td><td>+2.21%</td><td>+0.73%</td><td>+0.98%</td><td>+2.79%</td><td>+12.59%</td><td>+0.52%</td><td>+2.92%</td></tr></table>

Table 3. Component-wise ablation of ALSO. Each row removes or replaces a single design element.

<table><tr><td>Variant</td><td>Goal</td><td>Rel.</td><td>Know.</td><td>Overall</td></tr><tr><td>ALSO (full)</td><td>7.93</td><td>3.07</td><td>6.46</td><td>3.91</td></tr><tr><td>w/o EXP3 (ε-greedy)</td><td>7.50</td><td>2.71</td><td>5.32</td><td>3.61</td></tr><tr><td>w/o Score Smoothing</td><td>7.57</td><td>2.25</td><td>5.39</td><td>3.57</td></tr><tr><td>w/o Context Embedding</td><td>7.43</td><td>2.64</td><td>4.82</td><td>3.51</td></tr><tr><td>w/o Neural Surrogate</td><td>6.89</td><td>2.00</td><td>4.93</td><td>3.33</td></tr></table>

![](images/8d6b302985121eab1f3bb0aab339e9a3e1d54cb341898e8a863454eabfa1df68.jpg)

[Image: This figure displays four bar charts evaluating the performance of the "Bilateral" strategy against single-agent strategies ("P1-only" and "P2-only") for two large language models: Qwen-2.5-72B-Instruct and DeepSeek-V3.2. The charts compare Overall Scores (panels a and c) and break down performance by dimensions including Relationship, Knowledge, and Goal (panels b and d). Across all categories and models, the Bilateral strategy yields the highest scores, such as an overall score of 3.955 for DeepSeek-V3.2, with specific percentage gains noted on the dimensional charts, reaching up to +5.1% in Knowledge for the Qwen model.]  
Figure 5. Bilateral optimization improves social interactions. Comparison of P1-only, P2-only, and bilateral approaches on Qwen-2.5-72B-Instruct (a–b) and DeepSeek-V3.2 (c–d). Left: overall scores; right: dimension-wise with percentage gains. Significance: $p < 0 . 0 0 1$ (Qwen), $p < 0 . 0 1$ (DeepSeek).

Cross-Scenario Generalization. Beyond the scenarioparallel setting used in our main experiments, we further evaluate whether the learned strategy-selection mechanism transfers to unseen social contexts. We split Sotopia-Hard into disjoint training and test sets, train the surrogate bandit on the training scenarios, and evaluate it on unseen test scenarios. Figure 6 shows that zero-shot transfer improves over an online-from-scratch baseline both at the aggregate and per-scenario levels. Averaged over the 7 unseen test scenarios, zero-shot transfer reaches a goal score of 7.14, compared with 6.79 for the scratch baseline, yielding a relative improvement of 5.3%. It also improves the overall score from 3.17 to 3.60 (+13.5%). These gains are broadly consistent across scenarios, suggesting that ALSO captures transferable social interaction patterns rather than relying purely on scenario-specific adaptation.

![](images/396855a5e8bf6a14770f43e02f4f2241cf9f79eb2cace18c0c9405634a5d1500.jpg)

[Image: This image contains two grouped bar charts labeled "(a1) Per-Test-Scenario Performance: Goal" and "(a2) Per-Test-Scenario Performance: Overall Score," which compare three distinct learning methods across seven test scenarios. The charts utilize color-coded bars to represent the baseline (blue), zero-shot transfer (red/maroon), and a finetuning approach (green) against numerical scales for Goal (0-10) and Overall Score (0-5). Scenarios listed along the x-axis include "camping_trip," "antique_table," and "tile_tracker," among others. The visualization demonstrates that the zero-shot transfer method generally yields higher goal and overall scores compared to the baseline across various specific test cases, such as the first and third groups in the top chart.]

![](images/8beb5b6f41e8c71e64d640273e9432ea2714986e0e08f8a95f7f7ba1dd3a4432.jpg)

[Image: This vertical bar chart, titled "(b) Average Across All 7 Test Scenarios," presents performance scores categorized by "Goal" and "Overall" metrics along the x-axis, with a y-axis measuring "Score" from 1 to 8. For the Goal metric, the blue bar indicates a score of 6.79, while the adjacent red and green bars show higher scores of 7.14 and 6.86, labeled with percentage increases of +5.3% and +1.1%. In the Overall category, the blue bar records a score of 3.17, compared to the red bar at 3.60 (+13.5%) and the green bar at 3.38 (+6.4%).]  
Figure 6. Cross-scenario generalization results. (a) Per-scenario goal and overall scores on unseen test scenarios, comparing onlinefrom-scratch learning, zero-shot transfer, and finetuning. (b) Average performance across all 7 unseen test scenarios. Zero-shot transfer outperforms the scratch baseline on both goal score (7.14 vs. 6.79, +5.3%) and overall score (3.60 vs. 3.17, +13.5%).

![](images/02facc31b5e09a7432a7982beb4cb2480b82725841f10801d150042a13a92672.jpg)

[Image: This heatmap titled "(a) Baseline P1 Score" visualizes performance metrics for pairwise matchups between three models: DeepSeek, Qwen, and GPT40-mini. The matrix plots Player 1 Model on the y-axis and Player 2 Model on the x-axis, excluding diagonal self-play cells and using a blue color gradient to represent scores ranging from 2.6 to 3.8 according to the sidebar legend. The highest recorded value is 3.52 for the Qwen versus DeepSeek matchup, while the lowest is 2.61 for DeepSeek versus GPT40-mini. Remaining populated cells show scores of 3.34 (Qwen vs GPT40-mini), 3.12 (GPT40-mini vs Qwen), 2.84 (DeepSeek vs Qwen), and 2.80 (GPT40-mini vs DeepSeek).]

![](images/042ce09d152c0b9636fa0d0be6b3815b9405e9b2e0abd86893c3b13494aa2fa0.jpg)

[Image: This heatmap matrix, titled "(b) ALSO P1 Score," visualizes performance metrics for heterogeneous model pairings involving DeepSeek, Qwen, and GPT4o-mini. The grid displays specific scores and percentage improvements in green for off-diagonal matchups, such as a high score of 3.86 (+10%) when Qwen plays against DeepSeek and 3.63 (+28%) when DeepSeek plays against Qwen. The intensity of the reddish-pink color corresponds to the score magnitude shown on the vertical color bar, which ranges from approximately 2.6 to 3.8. Diagonal cells representing identical model comparisons are omitted, focusing the visualization strictly on cross-model interactions.]  
Figure 7. Performance across heterogeneous model, measured by only final P1 score. (a) Baseline performance. (b) Performance with ALSO. Green annotations denote relative improvement over baseline. ALSO yields consistent gains across heterogeneous pairings.

Heterogeneous Model Pairing. We further evaluate ALSO on heterogeneous dyads formed by DeepSeek-V3.2, Qwen-2.5-72B-Instruct, and GPT-4o-mini. Figure 7 shows that ALSO consistently improves performance across all crossmodel pairings. Crucially, the gains are not tied to any specific backbone combination or model scale. ALSO remains effective for all pairings, indicating that its benefit reflects a general optimization effect rather than pair-specific tuning.

# 7. Conclusion

We proposed ALSO, an adversarial online framework for dynamically selecting strategy instructions for LLM-based social agents under non-stationary interactions. By combining randomized bandit-based selection with a lightweight surrogate reward model, ALSO efficiently adapts strategies while keeping the underlying LLM frozen. Experiments on Sotopia and Sotopia-Hard demonstrate consistent improvements in social performance, with the largest gains in challenging scenarios, particularly on relationship outcomes. These results suggest adversarial online strategy optimization as a practical and scalable approach to enhancing social intelligence without costly fine-tuning.

# Impact Statement

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here.

# Acknowledgements

This work was supported in part by the National Natural Science Foundation of China (Grant Nos. U23B2049, 22527901, 62506319 and 62477012), the Guangdong Basic and Applied Basic Research Foundation (Grant No. 2026A1515030032), the Shenzhen Science and Technology Program (Grant No. JCYJ20250604141031003), the Pearl River Talent Program of Guangdong Province (Grant No. 2024QN11X069), and the AI for Science Program of the Shanghai Municipal Commission of Economy and Informatization, China (Grant No. 2025-GZL-RGZN-BTBX-01014).

