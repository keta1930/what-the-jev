# 4. Experiments  


The goal of our experiments is to evaluate the efficacy of ExpRL for improving the base model for subsequent RL training. To this end, we run ExpRL on a dataset of challenging math question-answer pairs that the base model fails to solve in 64 independent samples, each with a 32k-token response budget. We compare ExpRL against alternative mid-training procedures on this same data, then run Stage-II sparse-reward RL from each resulting initialization and evaluate on held-out math benchmarks. We describe our setup next and then present our results.  


## 4.1. Setup: Dataset, Evaluation Protocol, and Training Hyperparameters  


**Base model, judge, and training datasets for ExpRL.** We use Qwen3-4B-Instruct-2507 as the policy backbone (Qwen3-4B-Instruct for brevity). This model is trained to produce reasoning traces directly within the chain of thought, without needing a `<think>` block. We produce dense rewards using an LLM judge based on the same Qwen3-4B-Instruct model akin to Yang et al. [21]. In the main experiments, we use a copy of the base model as the judge; Sec 4.6 shows that ExpRL can also work when a smaller reference-conditioned judge provides rewards for a larger policy. We train the model to optimize Eq. 3 via REINFORCE. More specifically, sparse-reward baselines and Stage-II use GRPO-style group normalization. ExpRL-Outcome uses a GRPO-style normalized reward update. ExpRL-Process uses REINFORCE-style token/segment advantages without group normalization. For the prompts, we use a dataset combining hard question and reference answer pairs from recent works **InT** [21] and **POPE** [12].  


**Mid-training for RL priming (Stage-I).** Unless otherwise stated, we sample $G=10$ rollouts per prompt with temperature 0.8 and a maximum generation length of 16,384 tokens during training. This length budget is rarely reached by the initial policy, but provides headroom for RL-induced length growth without aggressively truncating longer reasoning traces. We assign the entire trajectory a reward of 0 when a generation overflows the maximum length. This prevents degenerate training dynamics in which the policy can increase reward by producing overly long outputs. For producing ExpRL-Process rewards in ExpRL, given a rollout $\mathbf{y}$, we define a sequence of segment prefixes $\{\mathbf{y}_{\le t}\}_{t=1}^T$ using the delimiter "###"; we use this delimiter because the model defaults to emitting it between reasoning steps. We query the judge on each prefix to obtain $s_t = s(\mathbf{x}, \mathbf{y}_{\le t}, \mathbf{y}^*)$, where $s_T$ denotes the score of the full rollout, and compute the segment-level advantages described in Equation 2 for all $t < T$. These advantages are then used as process-level learning signals at the segment level. We train the ExpRL stage for 230 optimization steps. For the downstream final-answer-reward RL stage, we train for 500 optimization steps. Unless otherwise specified, we use a per-update prompt batch size of 36 for runs using the LLM judge and 32 for  


verifiable sparse reward RL runs. More details in Appendix A.1.  


**Downstream RL (Stage-II).** After each Stage-I procedure, we use the resulting policy as the initialization for downstream sparse-reward GRPO. In the main math experiments, Stage-II training uses the InT+POPE prompt mixture, the same prompt family used during ExpRL priming, but with all reference-solution information removed: the policy samples from the original problem prompt and receives only the binary final-answer reward. This is the same-distribution instance of our problem setup, where $\mathcal{D}'$ is drawn from the same problem family as $\mathcal{D}_{\text{mid}}$. The experiment tests whether reference-guided priming produces an initialization that makes ordinary sparse-reward RL more effective.  


**Benchmarks.** We consider four standard, held-out answer-based reasoning benchmarks: **HMMT** (November 2025), **IMO-AnswerBench** [11], **AIME 2025**, and **AIME 2026**. We sample 128 responses per problem to compute evaluation metrics. In all cases, we evaluate both the base model initialization obtained after training with ExpRL as well as the model obtained after downstream RL training.  


## 4.2. Baselines and Comparisons  


We compare ExpRL to several approaches, including (1) **SFT**: supervised fine-tuning on the reference solutions in the mid-training set instead of running RL for mid-training; (2) **Verifiable sparse reward RL**: standard GRPO using only a binary final-answer reward from a rule-based verifier on mid-training prompts, without any dense reference-guided feedback; and (3) **Self-distillation**: a distillation-based baseline in which sampled rollouts are trained against a richer self-teacher; concretely, we use the base model conditioned on the reference solution as the teacher following Hübottet et al. [7].  


We compare these baselines against two variants of ExpRL: a) ExpRL-Outcome, which assigns a dense terminal reward to full rollouts, and b) ExpRL-Process, which assigns dense rewards to partial rollouts and prefixes. The key distinction is that the distillation baselines use reference information to define token-level targets, whereas ExpRL uses the same information only to score sampled reasoning traces and shape the model's exploration prior before subsequent sparse-reward RL. We focus our comparisons on methods that use reference information during the priming stage while leaving downstream sparse-reward RL unchanged. Prefix-guided methods such as POPE [12] study a complementary setting: they guide exploration by exposing oracle prefixes during downstream RL. In contrast, ExpRL uses references only to construct rewards during priming, and can in principle be combined with prefix-guided exploration.  


| Method|AIME25 $\uparrow$|AIME26 $\uparrow$|HMMT $\uparrow$|IMO Answer $\uparrow$|
| ---|---|---|---|---|
| Qwen3-4B-Instruct|46.46|51.40|40.60|31.37|
| SFT|26.62|30.26|20.09|21.80|
| GRPO|55.99|58.75|42.91|35.28|
| Self-Distillation|55.59|58.41|46.08|35.18|
| ExpRL-Outcome (Ours)|<b>59.07</b>|61.74|<b>49.11</b>|<b>37.85</b>|
| ExpRL-Process (Ours)|58.08|<b>63.41</b>|48.13|35.73|  


>Table 1: Pass@1 on answer-based benchmarks after downstream sparse-reward RL. Models are initialized with different RL-priming methods and then continued with the same Stage-II RL setup, except Qwen3-4B-Instruct as the original base model. Generally speaking, ExpRL attains the strongest overall answer-based performance.  


## 4.3. Finding 1: ExpRL Yields A Stronger Initialization for Downstream RL  


Our main question is whether dense rewards in ExpRL can produce a better initialization for downstream sparse-reward RL compared to imitation-based or sparse-reward-only alternatives. Table 1 shows that the answer is indeed yes. After a stage of standard sparse reward RL, we observe that overall ExpRL variants outperform SFT, sparse GRPO and self-distillation on the held-out answer-based benchmarks. The clearest gain appears on AIME-2026, where ExpRL-Process reaches 63% after downstream RL, while the second best GRPO baseline attains 58.75% only. Across the remaining answer-based benchmarks, the ExpRL variants consistently occupy the top of the table, with ExpRL-Outcome strongest on multiple evaluations and ExpRL-Process remaining highly competitive throughout. Taken together, these results support our central claim: for RL priming, privileged reference solutions are more effective when used to score sampled reasoning than when used only as trajectories to imitate.  


## 4.4. Finding 2: ExpRL Improves the Primed Policy Before Downstream RL  


We next study if ExpRL, in and of itself, is able to already improve performance of models after RL priming, even before running any downstream sparse reward RL. Observe in Table 2 ExpRL already produces a stronger model on held-out answer-based benchmarks, achieving higher pass@1 and pass@k and in cases such as IMO-AnswerBench it can improve the pass@k coverage that downstream sparse-reward RL can subsequently amplify. As one representative example, Figure 2 shows the pass@k curves on HMMT, where both ExpRL variants achieve higher pass rates at low values of k, and the ExpRL-Process variant remains particularly strong even at higher k (see Appendix A.4 for pass@k curves on other benchmarks). This distinction is important for interpreting the gains after downstream sparse-reward RL (from  


![268cb980741c976fe658c1556acc60b8.jpeg](images/7.png)

[Image: This line chart illustrates the Pass@k performance on the HMMT benchmark for five model configurations: Base, GRPO, Self-Distill, ExpRL-Outcome, and ExpRL-Process. The x-axis represents the sampling parameter $k$ with logarithmic intervals at 2, 16, and 128, while the y-axis indicates the pass rate percentage ranging from 45 to 85. The ExpRL-Process curve (solid orange) demonstrates superior performance, reaching approximately 78% at $k=128$, which is higher than all other methods shown. While the ExpRL-Outcome variant (dashed orange) also significantly outperforms the baselines, the Base, GRPO, and Self-Distill curves cluster closely together with lower success rates, converging around 73% to 75% at $k=128$.]  


>Figure 2: Pass@k after training with ExpRL on HMMT-Nov-2025 (128 samples).  


the result discussed above in Finding #1). If RL priming were only improving mid-training rewards, it would not necessarily translate into stronger downstream sparse-reward RL. Instead, ExpRL improves both pass@1 and pass@k before the second stage even begins, indicating that it produces a better RL-ready initialization. The stage-II improvements in Table 1 are therefore consistent with the view that downstream RL is benefiting from a stronger starting policy, rather than merely from additional optimization.  


Figure 3 provides a complementary view of the training dynamics during RL priming. Entropy of sparse-reward RL (GRPO) collapses the fastest among the online methods and unlocks the fewest prompts over the course of training. In contrast, ExpRL variants and self-distillation all maintain substantially higher token-level entropy, with ExpRL-Process unlocking solvable prompts the fastest. We also observe distinct dynamics within the two ExpRL variants. ExpRL-Outcome shows a noticeable late increase in entropy without a similarly large increase in response length, whereas ExpRL-Process exhibits an increase in response length. While these quantities are not themselves optimization targets, they suggest that ExpRL does not simply sharpen the policy in the mode-seeking manner of sparse-reward GRPO, but instead alters the training dynamics in a way that is more consistent with building broader coverage in RL priming.  


Figure 4 provides an additional reason why self-distillation is a weaker RL-priming objective. At the start of self-distillation (Figure 4 Right), the teacher starts much farther from the base model in KL than the  


| Method|AIME25 $\uparrow$|AIME25 $\uparrow$|AIME26 $\uparrow$|AIME26 $\uparrow$|HMMT $\uparrow$|HMMT $\uparrow$|IMO Answer $\uparrow$|IMO Answer $\uparrow$|
| ---|---|---|---|---|---|---|---|---|
| Method|pass@1|pass@16|pass@1|pass@16|pass@1|pass@16|pass@1|pass@16|
| Qwen3-4B-Instruct|46.46|72.32|51.45|80.30|40.60|68.43|31.37|52.74|
| SFT|6.00|30.95|5.68|34.24|3.41|23.91|4.22|31.07|
| GRPO|48.67|76.37|51.39|77.55|41.68|67.58|<b>34.35</b>|54.58|
| Self-Distillation|42.98|71.39|53.91|78.32|39.89|67.44|30.46|52.62|
| <b>ExpRL (Ours)</b>|<b>ExpRL (Ours)</b>|<b>ExpRL (Ours)</b>|<b>ExpRL (Ours)</b>|<b>ExpRL (Ours)</b>|<b>ExpRL (Ours)</b>|<b>ExpRL (Ours)</b>|<b>ExpRL (Ours)</b>|<b>ExpRL (Ours)</b>|
| ExpRL-Outcome|50.52|<b>77.25</b>|57.45|81.04|44.19|69.84|33.56|<b>55.73</b>|
| ExpRL-Process|<b>51.77</b>|74.29|<b>57.51</b>|<b>81.10</b>|<b>45.24</b>|<b>71.48</b>|32.02|54.29|  


>Table 2: Pass@1 and Pass@16 after Stage-I (ExpRL mid-training). ExpRL generally improves Stage-I pass@1 and pass@16 over the base and baselines, with the largest gains on AIME26 and HMMT. On IMO-AnswerBench, results are more mixed, although ExpRL-Outcome still achieves the best pass@16.  


![4d6b6198843c72db2d3f8a411f684e06.jpeg](images/8.png)

[Image: Line chart displaying the "# Fully Unsolved Prompts" on the y-axis against "Training Steps" on the x-axis for four different algorithmic approaches. The four data series represented are GRPO (green dashed line), Self-Distill (blue dashed line), ExpRL-Outcome (orange dash-dot line), and ExpRL-Process (red solid line). The GRPO method consistently maintains the highest number of unsolved prompts, finishing near 0.81, while the ExpRL-Process method demonstrates a sharp decline in unsolved prompts after step 140 to achieve the lowest final value around 0.785.]  


![64f77ebc5a4d435a361d3320c723dcaf.jpeg](images/8-2.png)

[Image: The image displays a line chart plotting "Entropy" on the y-axis (ranging from 0.1 to 0.4) against "Training steps" on the x-axis (marked at 1, 90, and 180). Four distinct data series are plotted with varying colors and line styles. A dotted orange line demonstrates a general upward trend, surging sharply after step 180 to approach an entropy of 0.4. Conversely, a dashed green line peaks briefly around step 90 before declining steeply to the lowest point on the graph, approximately 0.16. A solid orange line remains relatively flat and low throughout the training process, hovering between 0.2 and 0.24. Finally, a dashed blue line fluctuates in the middle range, peaking around 0.29 before settling near 0.26 at the end of the timeline.]  


![77eef5b4850c51b63d8e0ba8353a3d5d.jpeg](images/8-3.png)

[Image: This line chart plots Response Length in tokens against Training steps, with the y-axis ranging from 5000 to 11000 and the x-axis marked at intervals including 1, 90, and 180. A solid orange line demonstrates a significant upward trend, rising from approximately 6500 tokens to a peak near 11000 tokens before declining sharply, which corresponds to the "ExpRL with process rewards" behavior described in the text. In contrast, two other data series represented by a dashed blue line and a dotted yellow-green line remain relatively stable, fluctuating generally between 5000 and 8000 tokens across the training steps shown.]  


>**Figure 3: ExpRL training dynamics during Stage-I.** Left: Number of unsolvable prompts (as measured by outcome-level correctness) reduces significantly faster in ExpRL with ExpRL-Process rewards. Middle: token-level entropy remains relatively stable or even slightly increases for ExpRL and self-distillation, while it drops more substantially for sparse-reward GRPO. Right: Response length remains stable for all priming methods except ExpRL with process rewards which increases stably before reducing sharply when the responses get clipped.  


other on-policy methods. This means that it begins from a substantially more off-policy target. As prior work on off-policy distillation has noted that forcing a learner to match a distant expert distribution can lead to substantial distribution shift and unstable optimization [8, 14]. In contrast, ExpRL improves coverage while remaining within a more reachable KL space of the base policy.  


## 4.5. Finding 3: ExpRL Changes Reasoning Behaviors Relative to the Base LLM  


Beyond aggregate benchmark performance, we also ask whether ExpRL changes the kind of reasoning the model tends to produce (Section A.3). Figure 5 suggests that it does. Relative to the base model, ExpRL increases coverage over several of these search-oriented behaviors, especially verification, self-correction, and backtracking. Compared to SFT, which loses verification behavior, and sparse-reward GRPO, whose behavioral changes are smaller, ExpRL better preserves or expands behaviors associated with adaptive search and sustained intermediate progress. Self-distillation provides an important contrast: it also increases several search-oriented behaviors, indicating that behavioral coverage alone is not unique to ExpRL. However, its Stage-I pass@1/pass@k and downstream sparse-RL performance are generally weaker than ExpRL in Tables 1 and 2. This suggests that useful RL priming requires both forms of coverage: coverage over behaviors that help scale test-time compute, and coverage over problem-specific knowledge and productive solution paths. Taken together, the behavioral analysis supports the main  


![5e9d3f97cd16dc8460cf36a00cb5e5b9.jpeg](images/9.png)

[Image: The image displays two plots comparing reinforcement learning methods. The left panel is a line chart plotting "KL Loss" against "Training Steps," comparing GRPO (green dashed), ExpRL - Outcome (red dashed), and ExpRL - Process (orange solid). The ExpRL - Process method maintains a consistently lower KL Loss, plateauing around 0.01, while the other two methods rise sharply to approximately 0.03. An arrow points from the orange line to the right panel. The right panel is a density plot showing the distribution of "Per-token reverse KL (student - teacher)." Key statistics are marked with vertical lines: the median is 0.0500 (solid red line), the mean is 0.0576 (dotted green line), and the interquartile range spans from 0.0342 to 0.0682 (vertical orange dashed lines).]  


>Figure 4: Teacher, $\pi_{\text{teacher}}$ used in self-distillation is far from the base model, $\pi_{\text{student}}$, in KL divergence. Left: $\text{KL}[\pi_\theta || \pi_{\text{ref}}]$ to the reference policy during Stage-I training for GRPO and ExpRL. Right: $\text{KL}[\pi_{\text{student}} || \pi_{\text{teacher}}]$ per problem x at the start of self-distillation. We see that teacher is much farther outside the KL ball of policies reachable with on-policy reward optimization.  


interpretation of ExpRL: reference-guided RL priming changes the distribution of sampled trajectories
in a way that increases useful search behaviors while also improving coverage over productive solution
paths.  


## 4.6. Finding 4: ExpRL Extends to Mixed-Domain Mid-Training and Smaller Judges  


The preceding experiments focus on a 4B policy and primarily math reasoning. We next test two questions about the scope of ExpRL. First, can reference-guided RL priming improve a larger policy on a broader mixture of domains? Second, is the dense reward signal actually tied to the problem-matched reference, or can it be explained by generic LLM-judge confidence? To answer these questions, we run an additional mixed-domain Stage-I experiment and a judge/reference calibration stress test.  


**Mixed-domain scale study.** We construct a Stage-I mixture of 4,001 reference-solution examples spanning math, science QA, and coding (Table 3). We train a larger Qwen3-8B (with thinking disabled) policy with a smaller Qwen3-4B-Instruct judge. Table 4 shows that ExpRL-Outcome improves the 8B base policy on every pass@1 evaluation, including math, science, and coding. On the domain-level aggregates, ExpRL-Outcome is also the strongest Stage-I method on both Math-Aggregate and STEM-Aggregate, for both pass@1 and pass@16. This suggests that reference-guided RL priming is not only learning math-specific templates, but can improve coverage across a broader reasoning mixture. This result highlights another role of reference solutions in ExpRL: they make reward generation a scaffolded verification task rather than open-ended solution generation. With problem-matched references, a smaller 4B judge can provide useful dense rewards for a larger 8B policy's on-policy traces, suggesting that the judge need not match the policy's scale as long as it is sufficiently capable and reference-conditioned.  


Coding is the main exception to the mixed-domain pattern. ExpRL-Outcome still improves over the base policy on LiveCodeBench, but sparse GRPO remains stronger. We believe this reflects the reward structure of coding tasks: execution provides an unusually strong domain-specific sparse reward, while reference-guided judging is less naturally suited to assigning partial-progress credit. Unlike math or science reasoning, incomplete code may not compile, and many correct implementations can differ substantially from the reference solution. As a result, reference scaffolds provide a weaker substitute for environment feedback in coding than they do in domains where intermediate reductions can be compared against a reference path. This is consistent with the calibration result in Table 6, where no-reference judging is about as reliable as reference-conditioned judging on LiveCodeBench, suggesting that the judge relies mainly on functional correctness rather than reference-solution scaffolding. Thus, the coding  


![bb34b8123221940b23f6466c4c46706a.jpeg](images/10.png)

[Image: This figure presents six bar charts illustrating behavior changes across five models (GRPO, SFT, Self-Distill, ExpRL-Outcome, ExpRL-Process) categorized as Verification, Self Interruption, Self Correction, Redo Restart, Exploration, and Backtracking. The vertical axis denotes the number of problems, while paired orange and blue bars represent behaviors gained and lost respectively, with red text indicating the net change ($\Delta$). Notable data points include a significant net loss of -30 for SFT in Self Interruption and a net gain of +22 for Self-Distill in Self Correction, whereas ExpRL variants consistently show positive net changes in categories like Verification and Backtracking.]  


>Figure 5: Behavior changes after RL priming relative to the base model. Orange bars show behaviors gained after priming, blue bars show behaviors lost, and red numbers indicate the net change. Search-oriented behaviors refer to observable rollout features in our annotation rubric, such as verification, self-correction, exploration, restarts, and backtracking. ExpRL yields net gains in several such behaviors, suggesting that reference-guided RL priming changes the distribution of sampled trajectories rather than merely increasing final correctness.  


| Dataset|Domain|# Examples|% of Training|
| ---|---|---|---|
| InT|Math|440|11.00|
| POPE|Math|1,076|26.89|
| SciKnow-Physics|Science|474|11.85|
| SciKnow-All|Science|1,000|24.99|
| LCB v6|Coding|1,011|25.27|
| Total|–|4,001|100.00|  


>Table 3: Mixed-domain Stage-I data. The additional 8B experiment uses reference-solution examples from math, science QA, and coding.  


result is consistent with our view of ExpRL as Stage-I RL priming: it can improve the starting policy, but
when a strong environment reward is available, downstream RL should use it directly.  


**Reference and judge calibration.** We next test whether the dense reward signal actually depends on the problem-matched reference solution, rather than simply reflecting generic LLM-judge confidence or surface-level plausibility. To separate these possibilities, we hold sampled rollouts fixed and vary both judge size and reference condition: a correct problem-matched reference, no reference, or a wrong reference from another problem. We measure misplacement rate, defined as $(FPR + FNR)/2$, where false positives are incorrect rollouts assigned score $> 3$, and false negatives are correct rollouts assigned score $< 4$. Lower is better.  


Table 5 shows that, for all 4B-and-larger judges, correct-reference judging gives the lowest displacement rate across Math, SciKnow-MCQ, and SciKnow-OE. Removing the reference weakens discrimination, and using a wrong reference often makes the reward signal unreliable. The 0.6B judge is unstable, so ExpRL  


| Model|AIME-25|AIME-25|AIME-26|AIME-26|HMMT-Nov25|HMMT-Nov25|IMO-Answer|IMO-Answer|Math-Agg.|Math-Agg.|GPQA|GPQA|OlympiadPhys.|OlympiadPhys.|STEM-Agg.|STEM-Agg.|LCB v5|LCB v5|
| ---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Model|p@1|p@16|p@1|p@16|p@1|p@16|p@1|p@16|p@1|p@16|p@1|p@16|p@1|p@16|p@1|p@16|p@1|p@4|
| Qwen3-8B|19.42|43.09|16.56|45.31|10.18|38.64|15.28|40.17|15.36|41.80|47.64|88.78|35.86|64.09|41.75|76.44|36.52|43.76|
| GRPO|27.14|51.58|27.71|61.83|22.38|49.61|22.51|47.42|24.93|52.61|53.41|84.41|40.36|68.18|46.88|76.30|<b>54.97</b>|<b>64.09</b>|
| SFT|5.67|29.23|5.22|27.83|3.44|21.27|5.03|29.64|4.84|26.99|37.76|<b>90.66</b>|16.45|49.56|27.11|70.11|25.66|38.28|
| Self-Distillation|21.76|45.08|18.80|49.49|12.51|40.35|16.45|40.89|17.38|43.96|48.57|87.06|36.86|66.07|42.71|76.57|43.02|56.51|
| ExpRL-Outcome|<b>34.23</b>|<b>58.99</b>|<b>40.90</b>|<b>64.15</b>|<b>25.31</b>|47.95|<b>23.36</b>|44.25|<b>30.95</b>|<b>53.84</b>|<b>53.46</b>|85.31|<b>44.25</b>|<b>68.66</b>|<b>48.86</b>|<b>76.99</b>|41.92|48.82|  


>Table 4: **8B policy + 4B judge Stage-I results.** All methods are evaluated at 270 steps. ExpRL-Outcome improves the 8B base model on every pass@1 evaluation and gives the best aggregated results in Math and STEM domains among Stage-I methods.  


| LLM Judge|Reference condition|Math|SciKnow-MCQ|SciKnow-OE|
| ---|---|---|---|---|
| Qwen3-0.6B|Correct reference|48.6|<b>42.0</b>|<b>49.4</b>|
| Qwen3-0.6B|No reference|48.5|47.1|50.0|
| Qwen3-0.6B|Wrong reference|<b>47.5</b>|44.1|51.6|
| Qwen3-4B|Correct reference|<b>17.8</b>|<b>14.0</b>|<b>11.4</b>|
| Qwen3-4B|No reference|39.2|37.5|25.2|
| Qwen3-4B|Wrong reference|50.4|46.0|36.7|
| Qwen3-8B|Correct reference|<b>18.8</b>|<b>9.8</b>|<b>19.1</b>|
| Qwen3-8B|No reference|36.0|31.9|37.0|
| Qwen3-8B|Wrong reference|52.6|48.8|43.1|
| Qwen3-14B|Correct reference|<b>18.2</b>|<b>14.7</b>|<b>12.3</b>|
| Qwen3-14B|No reference|38.5|29.3|27.6|
| Qwen3-14B|Wrong reference|50.2|47.6|36.4|  


>Table 5: Calibration misplacement rates on Math and SciKnow. No-reference judging is weaker, and wrong-reference judging often makes the reward signal unreliable consistently across the 4B, 8B and 14B judges. The 0.6B judge is unstable, which suggests ExpRL does require a minimally capable judge and reliable problem-matched references.  


requires a minimally capable judge. However, the 8B-policy experiment above shows that the judge need not be as large as the policy. Together, these results support the view that the useful reward signal is not generic judge confidence, but verification against a correct problem-matched reference.  


Table 6 shows a different pattern on LiveCodeBench: correct-reference, no-reference, and wrong-reference judging all have similarly low misplacement rates, with no-reference slightly best. This suggests that the coding judge relies more on inferred functional correctness from the code and problem specification than on reference-solution scaffolding. This helps explain why ExpRL-Outcome improves the base policy on coding, while execution-based sparse GRPO remains especially strong.  


# 5. Related Work and Discussion  


**Mid-training before RL.** In modern LLM pipelines, there are broadly two ways to prime a model before an RL run, which we call mid-training. First, *skill-inducing* mid-training impues useful reasoning behaviors, such as self-correction, backtracking, and verification, useful for exploration and further amplified by RL [4, 13, 19]. Second, *coverage-building* mid-training aims to increase coverage over productive reasoning paths on hard math problems, needed for hard downstream tasks with sparse outcome rewards. Recent pipelines rely on such intermediate stages before RL [16, 19, 20], and recent work studies this interplay explicitly [24]. Traditionally, this coverage is built with SFT on curated traces or rejection-sampled  


| LLM Judge|Reference condition|LiveCodeBench|
| ---|---|---|
| Qwen3-4B|Correct reference|9.7|
| Qwen3-4B|No reference|<b>8.2</b>|
| Qwen3-4B|Wrong reference|10.0|  


>Table 6: Calibration misplacement rates on LiveCodeBench. For coding, problem-matched reference solutions are not critical as the judge primarily depends on tracing the code with input-output pairs.  


solutions [23], but this can narrow the model's exploration during RL [12] and training a model on offline data can cause optimization instabilities [14]. ExpRL focuses on the second setting of mid-training and instead of only cloning traces with correct final answers, it uses on-policy RL to reward useful reasoning behaviors and partial progress relative to references. Concurrent work also explores RL for reasoning traces during mid-training stages for improving generation quality [17]; our work focuses specifically on building coverage for hard reasoning problems where sparse rewards provide little signal.  


**Exploration bottleneck in LLM RL.** Sparse-reward RL is attractive because correctness is often automatically verifiable, but it becomes brittle on hard problems where correct rollouts are rare, leading to under-exploration and sometimes degraded pass@$k$ after RL [22, 25]. Prior work improves the learning signal with intrinsic bonuses, entropy regularization, count-based rewards, pass@$n$-aware objectives, and verification-based signals [2, 3, 5, 15, 18, 26], as well as by studying the role of earlier training stages [24]. Our approach instead shifts exploration into mid-training, where dense reference-guided rewards can reinforce productive reasoning paths before sparse-reward RL.  


