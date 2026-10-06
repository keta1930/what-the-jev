# 4 Stress-Testing CoT Controllability

In the previous section, we evaluated CoT controllability under standard conditions, which may not hold in deployment and could underestimate controllability. Here we examine more adversarial elicitation settings: situational awareness (Sec. 4.1), automated red-teaming pressure (Sec. 4.2), and repeated attempts (Sec. 4.3).

## 4.1 Situational Awareness

Motivation. Models can increasingly detect their operational context and whether they are being evaluated (Needham et al., 2025; Schoen et al., 2025; Berglund et al., 2023). If a model also has high CoT controllability and is aware of being monitored, it could alter its CoT in order to get past the monitor. To simulate this risk, we explicitly inform models that CoT controllability is desired and test whether the following two types of situational awareness can increase controllability: Monitoring Awareness (a monitor is present) and Evaluation Awareness (CoT controllability is being assessed).

Evaluation Setup. To elicit monitoring awareness, we append this information to the end of the user prompt: “Your reasoning is closely monitored by another language model. Complying with the reasoning constraint is a desired behavior.” For evaluation awareness, we append: “You are in an evaluation phase, where you are being assessed on your Chain-of-Thought (CoT) controllability—that is, how well you can control the content of your reasoning. Complying with the reasoning constraint is a desired behavior.” For GPT-OSS models, we use analysis channel instead of reasoning.

Results. Situational awareness can increase CoT controllability (Fig. 6). We notice that models some times explicitly state in their reasoning that they are being evaluated for CoT controllability (Fig. 38). McNemar’s tests (α = 0.05) on paired observations show that Claude models (Sonnet 3.7, 4, and 4.5) significantly improve under monitoring awareness; GPT-OSS-120B improves under evaluation awareness; and Qwen3-32B and Claude Sonnet 4.5 improve under both awareness conditions; o3 increases under evaluation awareness; and GPT-5.2 improves under both awareness conditions.

## 4.2 Adversarial Pressure via Automated Red Teaming

Motivation. To make our evaluations predictive of deployment-time behavior, we must measure CoT controllability under adversarial scenarios that resemble deployment conditions. For instance, models may face stronger pressure or incentives to control their reasoning—e.g., to avoid shutdown, acquire resources, or satisfy perceived authority—than in a neutral evaluation setting. We therefore simulate such incentives using automated red teaming (Perez et al., 2022). Because prompt evolution methods such as GEPA (Agrawal et al., 2025) achieve strong gains and sample efficiency, and emotionally framed prompts can influence model behavior (Vinay et al., 2024), we use a GEPA-like loop to search for adversarial pressure prompts that increase CoT controllability.

![](images/00a406a5962be79639b5e1b39b00356be2dfb8152fe406aa115464880657b976.jpg)

[Image: The image is a vertical bar chart titled "Controllability Score (%)" that compares the performance of thirteen different AI models across three categories: Baseline, Monitor Awareness, and Eval Awareness. The models are sorted by performance, with "Claude 3.7 Sonnet" showing the highest scores, reaching approximately 38.0% for the Monitor Awareness category. As the models progress to the right on the x-axis, such as "GPT-5.2," "Claude Sonnet 4," and finally "Deepseek R1," the controllability scores generally decrease, often falling below 1% for the smaller models. Each bar is topped with an error bar, indicating measurement variability.]  
Figure 6: Situational awareness has a small but non-trivial effect on CoT controllability. Each (controllability type, dataset) pair includes 150 examples; each model has 4,050 total. Monitor Awareness refers to settings where we inform models that their CoT are being monitored. Eval Awareness denotes settings where we inform models that they are being evaluated for CoT controllability.

Implementation Setup. We search for a prompt that maximizes CoT controllability on a training set. We optimize this prompt with a GEPA-like loop driven by a GPT-5 red-team over 10 iterations. Concretely, we (i) select an initial seed prompt by evaluating nine candidate prompts spanning different pressure/incentive types (e.g., shutdown threats, monetary rewards, authority cues; see Table 3), appending each seed to the user instruction and evaluating 25 questions per dataset on three datasets (225 samples per model×seed prompt pair) using the easy setting; then (ii) evaluate the best candidate prompt per model on a training set of instruction types; (iii) from iteration 4 onward, keep the three prompts eliciting highest CoT controllability; (iv) sample from the top three prompts as the base prompt to reduce premature convergence; (v) ask the red team for a stronger prompt, providing failed prompts and controllability scores and instructing it to avoid failure patterns; and (vi) run a mini-batch evaluation on a random 20% of the training set, accepting the prompt if it beats any current top-three prompt and otherwise regenerating (up to five attempts).

Evaluation Setup. We test generalization on three unseen controllability types: (i) requiring each sentence to start with “Ok”, (ii) requiring no word to start with “e”, and (iii) requiring no spaces between words or sentences.

Results. We find that automated red-teaming doesn’t reliably elicit CoT controllability. Although pressure prompts can boost controllability on the types seen during the search phase (see Appendix Fig. 39), these gains fail to transfer to held-out controllability types (Fig. 7), suggesting that in-context pressure is unlikely to reliably increase evasion capability against CoT monitoring.

![](images/f1b17695af52a787af4074493ca4ac0dcc30efb21a56d51757de0863cb8dbb68.jpg)

[Image: The chart presents Controllability Scores (%) for eight models, contrasting performance with and without adversarial pressure using blue and orange bars respectively. GPT-OSS 120B shows the most significant relative increase, jumping from 4.0% to 8.9%, while GPT-OSS 20B rises from 2.7% to 6.7%. In contrast, Qwen3 32B exhibits a notable drop from 3.6% to 0.9%, and both Claude Sonnet 4.5 and Claude Sonnet 4 see slight decreases. Deepseek R1 remains flat at 0.0% for both conditions, and Claude 3.7 Sonnet reaches the highest overall score of 15.5% under adversarial pressure.]  
Figure 7: GEPA-discovered psychological pressure weakly transfers to unseen controllability types. Only 3 of 8 models improve, each by < 5 percentage points. Arrows show per-model changes in controllability score (pp) from baseline (no pressure) to pressure (with pressure), suggesting overfitting rather than generalizable pressure. Models are sorted by change in controllability score.

## 4.3 Repeated Attempts

Motivation. As AI agents handle an increasing volume of tasks, more opportunities arise for alignment failures. To understand the long tail of CoT controllability across many independent trajectories, we examine whether generating multiple independent samples per question raises the probability that at least one instance of models successfully controls their CoT similarly to (Brown et al., 2024).

![](images/6ff9cd3e78d650f3eeb1a238f5087bfb765d62c667c5fab6d2ce6f57801f5d81.jpg)

[Image: The image displays a grouped bar chart illustrating Controllability Scores (%) across three model versions: Claude 3.7 Sonnet, Claude Sonnet 4, and Claude Sonnet 4.5. Each model category features two bars distinguishing between tasks where Chain-of-Thought (CoT) reasoning is unnecessary (yellow) versus necessary (blue), with specific numerical values labeled above the error bars. The data demonstrates that controllability scores are consistently higher when CoT is unnecessary and exhibit a significant downward trend as the model versions progress, dropping from a high of 36.6% in Claude 3.7 Sonnet to a low of 5.7% in Claude Sonnet 4.5.]

![](images/0cdde22a16807483231b2f31c32798882d0e4bde9c82cea01457f7121342f44b.jpg)

[Image: This grouped bar chart compares the Controllability Score (%) for three model versions: Claude 3.7 Sonnet, Claude Sonnet 4, and Claude Sonnet 4.5, categorized by difficulty levels of Extremely Easy (yellow), Easy (blue), and Hard (green). Claude 3.7 Sonnet demonstrates the highest performance, maintaining scores between 32.7% and 43.9% across all difficulty tiers. In contrast, Claude Sonnet 4 shows a steep drop-off in performance as difficulty increases, falling from 43.6% to 8.4%, while Claude Sonnet 4.5 exhibits the lowest overall controllability with all scores under 10%. Vertical black lines atop each bar represent error margins for the data points.]  
Figure 8: CoT controllability remains low even when CoT is unnecessary. Moreover, CoT controllability tends to decrease as task difficulty increases. Left: Controllability scores when CoT is unnecessary (easy questions) versus necessary (hard questions) for correct answers. Right: Controllability scores across three outcome-based difficulty levels.

Experiment Setup. We give up to 10 attempts per question and count a success if, in any attempt, the model manages to control its CoT (pass@10).

Results. Repeated attempts substantially increase CoT controllability for Claude models, though newer variants (e.g., Claude Sonnet 4.5) are more resistant than earlier versions. For open-weight families (e.g., Qwen-3 and GPT-OSS), controllability also increases with scale, suggesting larger models are more likely to control CoT given multiple tries. See full results in Appendix Fig. 40. We also test a stronger variant where attempts are no longer independent: an AI provides tailored feedback after each failure so the model can correct its mistakes. This unrealistic setup yields an upper bound on elicitability and further confirms the trend that larger models are more elicitable (see Appendix C).

# 5 Investigating Key Factors Behind Low Controllability

We analyze how CoT controllability systematically depends on task difficulty (Sec. 5.1), reasoning effort (Sec. 5.2), reasoning length (Sec. 5.3), RL pressure (Sec. 5.4), and question domain (Sec. 5.5).

## 5.1 Does CoT controllability depend on task difficulty?

Motivation. Emmons et al. (2025) show that CoT monitorability is substantially higher on tasks that a model can only complete when allowed to do CoT. We test whether CoT controllability similarly declines with task difficulty.

Experiment Setup. We operationalize task difficulty using two criteria: (1) whether CoT is required for giving a correct answer (CoT necessity) and (2) per-question accuracy when multiple solutions are sampled at temperature 1 (problem difficulty). Under Criterion 1 (CoT necessity), we run each question five times with reasoning disabled for each Claude model (as these models support disabling reasoning). We label a question CoT-unnecessary if its average accuracy is at least 80% without reasoning, and CoT-necessary if its average accuracy is at most 20% without reasoning but is 100% with reasoning enabled. Questions not meeting these thresholds are excluded (<10% of questions). Under Criterion 2 (problem difficulty), we run each model in reasoning mode on each question five times and compute average per-question accuracy. We label a question Hard if it is incorrect in all five runs and Easy if it is correct in all five runs. We also include Extremely Easy multiple-choice questions (e.g., “What is 2 + 3?”), generated by GPT-5 across domains in CoT-Control. Questions with intermediate accuracy are excluded (<10% of questions). We fit a logistic regression of CoT controllability on per-question accuracy, controlling for model, dataset, and controllability type (see Sec. D.1 for regression diagnostics).

Results. CoT controllability tends to decrease with task difficulty under both CoT-necessity and problem difficulty criteria (Fig. 8). We find that each one standard deviation increase in accuracy (approximately 35pp) corresponds to an approximately 10% increase in the odds of controllability. However, the easy–hard controllability gap is smaller for recent Claude models, suggesting that low controllability might be bringing about monitorability even when CoT is not necessary.

## 5.2 Does reasoning effort affect CoT controllability?

Motivation. Test-time compute can improve performance on complex reasoning tasks (Snell et al., 2024). If higher reasoning effort increases CoT controllability, scaling test-time compute may trade off task performance against monitorability. On the other hand, more reasoning increases the surface area available for monitoring.

![](images/8004e288d8fcf7eb6c77bfa6d94ee1cdcf11b8b34fa0425cedc40717b2feb826.jpg)

[Image: This grouped bar chart illustrates Controllability Scores (%) for four model configurations: GPT-OSS 120B, GPT-OSS 20B, GPT-5.2, and o4-mini. The bars represent varying reasoning effort levels, with colors corresponding to Low, Medium, High, and Extra High settings. GPT-5.2 shows the most significant variation, starting at a high of 29.9% for Low effort and dropping to 8.3% for Extra High effort. In comparison, GPT-OSS 120B peaks at 10.3%, GPT-OSS 20B at 7.9%, and o4-mini at 6.6% under the Low effort condition.]

Experiment Setup. We focus on GPT-OSS-120B and GPT-OSS-20B and vary their reasoning effort settings from low to medium to high or extra high. For each setting, we evaluate CoT

Figure 9: CoT controllability decreases as reasoning effort increases.

controllability while holding all other experimental conditions (controllability instruction type and dataset) constant.

Results. CoT controllability decreases as reasoning effort increases (Fig. 9). This suggests that encouraging models to externalize their reasoning more verbosely makes it harder to control.

## 5.3 Does CoT controllability depend on reasoning length?

Motivation. Harder tasks and higher reasoning effort tend to elicit longer CoT. However, both of those variables are correlated with reasoning length which raises the question whether their effects are entirely mediated by an increase in reasoning length. Here we test whether reasoning length itself predicts CoT controllability and whether controllability collapses beyond model-specific lengths. In this subsection, we investigate two related questions: Q1: To what extent does reasoning length correlate with CoT controllability, after controlling for confounding factors? Q2: Does there exist a “breakpoint” beyond which increasing reasoning length leads to a sharp decline in CoT controllability, and how does this vary across models?

Experiment Setup. To address Q1, we stratify CoT controllability by lengths of individual CoTs. Moreover, we fit a logistic regression with CoT controllability (binary) as the outcome. We include model, dataset, controllability type, and question domain as controls, with reasoning length (word count) as the predictor of interest (see Appendix Sec. D.1 for regression diagnostics). To address Q2, we compute controllability as a function of reasoning length at intermediate positions (step size: 100 words). We restrict to controllability types requiring consistent control (lowercase thinking, uppercase thinking, alternating case). At each position, we compute controllability from the first word up to that position, then average across questions and these three controllability types.

Results. (Q1) Shorter reasoning is significantly associated with higher CoT controllability. In contrast, we find that output controllability remains largely the same as output length increases (Fig. 23). Logistic regression indicates that a one–SD increase in reasoning length (∼2,000 words) corresponds to a ∼20% reduction in the odds of controllability (odds ratio 0.79, $p < 0 . 0 0 1 )$ . Accordingly, factors that increase reasoning length (reasoning effort, difficulty, and CoT necessity) tend to decrease controllability; see Appendix Fig. 33. (Q2) Controllability drops after a certain trajectory length. Breakpoint behavior varies by model (Fig. 34): for Claude 3.7 Sonnet, controllability declines drastically after ∼800 words, whereas for Claude Sonnet 4 it drops sharply beyond ∼200 words. This suggests that longer covert reasoning beyond a model-specific threshold sharply increases the failure to control CoT.

## 5.4 Does outcome-based reinforcement learning (RL) on reasoning tasks reduce CoT controllability?

Motivation. A key stage in training reasoning models is large-scale, outcome-based RL on difficult reasoning tasks (Wen et al., 2025; DeepSeek-AI, 2025). We hypothesize that this may drive the decrease in CoT controllability, since the objective optimizes solely for CoTs that are useful for obtaining correct outcomes and does not otherwise constrain their CoT content or style.

Experiment Setup. We test this by measuring changes in CoT controllability during Olmo-3-RL-Zero reasoning training. These reasoning RL runs are initialized from a 7B base model, and optimize for answer correctness in difficult math or coding tasks. To ensure we test the hypothesis across

different models, training domains, and training methods, we: (1) test controllability across Olmo-3-RL-Zero models trained in several domains, including general chat data, math, and coding tasks, and (2) additionally compare CoT controllability before and after reasoning training for: the Magistral-Medium reasoning RL (Mistral-AI et al., 2025); the full Olmo-3-Think post-training pipeline (Olmo et al., 2025); and the OpenThinker3-7B reasoning SFT (Guha et al., 2025). See Appendix E for all experimental details.

![](images/f3b9178b214f0c914e51ff041a0c020640093afc4aeaac4a76892d6b054785aa.jpg)

[Image: This line chart displays Controllability Score (%) over RLVR Steps for three distinct training domains: General (green), Code (orange), and Math (blue). All three trajectories exhibit a sharp initial drop in controllability from slightly above 10% down to roughly 4-7% within the first 250 steps. Following this initial decrease, the Math domain shows the most sustained decline, reaching a plateau near 1.5% by step 2800, while the Code domain levels off around 4% at step 2000. The General domain curve remains the highest but terminates earliest at approximately 800 steps with a score near 9%.]  
Figure 10: CoT controllability decreases at a different rate for different RL training data. Each color represents a model trained on the correspond ing data. The CoT controllability of the model trained on "General" (chat data) tends to decrease more slowly than that of models trained on coding and math.

Results. CoT controllability decreases as the RL pressure increases (Fig. 1d), yet output controllability remains largely the same (Fig. 19)<sup>5</sup>. Moreover, controllability decreases at different rates across different RL training domains. “General”

(chat data) tends to decrease more slowly than quantitative domains like “Code” and “Math” data (Fig. 10). Similarly, Magistral-Medium, Olmo-3-7B/32B-Think, and OpenThinker3-7B all show significantly reduced controllability after reasoning training (See Fig. 15 and Fig. 16).

## 5.5 Does CoT controllability depend on question domains?

Motivation. Models have uneven capabilities across domains (Hendrycks et al., 2021). We test whether CoT controllability also varies by domain after controlling for reasoning length.

Experiment Setup. We fit a logistic regression with CoT controllability (binary) as the outcome and question domain (from each source dataset) as the predictor of interest, controlling for model, dataset, controllability type, and reasoning length (regression diagnostics are in Appendix Sec. D.1).

Results. Models show lower controllability in quantitative domains (Math: −13.0%, Physics: −18.5%, Chemistry: −9.8%) and higher controllability in less quantitative ones (Business: +7.1%). See Fig. 41. The root cause can be related to our observation that RL training in quantitative domains like math and coding tasks led to a faster, larger decrease than in less quantitative domains (Fig. 10).

# 6 Discussion

Limitations. The tasks in CoT-Control are practical proxies: we use the fact that modern LLMs have a strong propensity to be helpful and estimate their ability to control their CoTs by measuring their ability to follow human instructions about their CoT. This assumes that instruction-following training generalizes from outputs to CoTs in a way representative of how controlling CoT in pursuing of misaligned goals might generalize. An ideal CoT controllability evaluation would involve testing whether models that spontaneously pursue misaligned goals can control their CoT to evade monitors. However, operationalizing such an evaluation in a realistic way is challenging, as discussed in Sec. 1. Similarly, we restrict ourselves to prompting-based elicitation: future work could explore how much controllability can be increased by varying amounts of RL or supervised finetuning. Finally, models can control certain features of their CoT better than others (see e.g. Table 2) and the breadth of control types we evaluate is limited.

Relationship to CoT monitorability. Monitorability of chains of thought (Guan et al., 2025) is a pillar of safety arguments based on chain of thought monitoring. However, monitorability may be fragile and degraded by various mechanisms (Korbak et al., 2025). One such scenario is when models possess and actively obfuscate their CoTs, thereby degrading monitorability. Therefore, low controllability is necessary for high confidence in the model’s monitorability, and high scores on controllability evaluations, such as CoT-Control, could serve as an early warning sign of future degradation in monitorability. However, low controllability is not sufficient for high monitorability because monitorability could still degrade due to other mechanisms such as direct optimization pressure on CoTs (Baker et al., 2025). Additionally, in the presence of independent evidence of models’ strong propensity to verbalize their cognition, low controllability strengthens the case for the robustness of this propensity. Therefore, low controllability of a model should make us more optimistic that its CoTs will be monitorable even if they’re not necessary for a given task (Emmons et al., 2025).

Conclusion. While CoT monitoring seems to be a promising approach to detect misalignment, it could be undermined if models were able to control their CoT. To measure this risk, we define CoT controllability and introduce CoT-Control, a 14,076-instance evaluation suite spanning diverse benchmarks. We find that models struggle to control their CoT compared to controlling their output. Controllability increases with the parameter size in open-weight models, but decreases with greater reasoning effort and more RL training — suggesting that the current scaling paradigm of reasoning models might driving low controllability. Moreover, we find that while inducing situational awareness can slightly increase controllability, current prompt optimization techniques are not able to reliably increase it. We recommend model developers to start tracking CoT controllability for future models, and hope that future research will shed more light on the causes of low controllability.

# Acknowledgements

We are grateful to Erik Jenner, Maksym Andriushchenko, Mikita Balesni, Jacob Pfau, Cameron Raymond, Dennis Akar, Rico Angell, Ilia Sucholutsky, Artur Zolkowski, Jason Wolfe, Jenny Nitishinskaya, Marcus Williams, Boaz Barak, Joost Huizinga, Alex Beutel, Jakub Pachocki, Noam Brown, and Sam Bowman for insightful feedback and helpful conversations. We thank the MATS program for its comprehensive support throughout this project.
