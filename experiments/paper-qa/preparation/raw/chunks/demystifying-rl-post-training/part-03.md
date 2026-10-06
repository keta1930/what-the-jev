# B Expanded Related Work

Post-training with RL has proven effective for a wide range of tasks, particularly for improving reasoning capabilities and aligning LLMs with human preferences. For instance, RL with Verifiable Rewards (RLVR) has shown that models can achieve state-of-the-art performance with smaller parameter counts, such as DeepSeek-R1 (Guo et al., 2025; Lambert et al., 2025), highlighting its role in developing efficient AI. Through Reinforcement Learning from Human Feedback (RLHF), reward signals are learned from preference data, leading to improvements in instruction following and response quality (Ouyang et al., 2022; Bai et al., 2022; Stiennon et al., 2022). Across both settings, RL posttraining has shown to yield strong gains on reasoning and alignment tasks, making a mechanistic understanding of its success essential.

Several recent works have surfaced seemingly contradictory findings about RL post-training. Shao et al. (2025) demonstrate that RLVR can yield substantial gains in mathematical reasoning, even when reward signals are weak, random, or negatively correlated with the actual answer. Notably, they find that spurious rewards still trigger systematic behavioral shifts, such as increased code reasoning frequency in Qwen2.5-Math, suggesting the base model’s pretraining dictates the form of emergent behavior, not the reward. Moreover, they observe that these gains do not generalize consistently across different model families; for example, Qwen2.5 and OLMo2 exhibit different behavioral trends to these spurious rewards. These findings appear to challenge a core idea in RL: that improvements arise from optimizing correctly specified reward signals. Our work addresses these questions by showing that the effect of random rewards depends critically on the prompt distribution. A broad prompt distribution causes global entropy increase and capability degradation, while a narrow distribution causes targeted corruption of the training domain while preserving other capabilities. The prompt distribution thus controls the scope of degradation, not whether degradation occurs.

Moreover, the original base model plays a central role in determining post-training success (Yue et al., 2025). Measuring pass@k (the probability of solving a problem in k attempts), the authors find that while RL-trained models excel with small values of $k ,$ base models catch up as k increases. This suggests RLVR primarily improves sampling efficiency, refining existing behaviors rather than creating novel ones. We build on this by comparing outcomes across models with different baseline capability distributions under controlled reward conditions, and show that a sufficiently shaped reward can overcome this problem, and teach new behaviors to models that previously did not generate them with high probability.

Chen et al. (2025) introduce the “Coverage Principle“ and argue that existing metrics (e.g. crossentropy loss) are often poor predictors of posttraining success, instead stating the coverage (the total probability mass the pre-trained model assigns to the set of high-quality responses) is the critical link. This motivates our choice to treat this notion of coverage as an independent variable; by selecting base models with varying coverage over target tasks, we can test how it interacts with the effect of reward density, allowing us to disentangle these two sources of variation.

Ren and Sutherland (2025) develop a framework to illustrate why post-training often redistributes probability mass rather than creating new capabilities by decomposing changes in log-probabilities after gradient updates. While their results are restricted to Direct Preference Optimization (DPO), this perspective accounts for observed behavioral shifts such as hallucinations and highlights the complex dynamics underlying alignment and performance gains. We adopt this framing for interpreting behavioral changes, as gains in the target task likely reflect probability mass redistribution rather than the emergence of new capabilities.

# C Reward Function Implementations - Movie Quotes

In our sandbox experiments, we utilize two distinct reward functions to evaluate the impact of reward shaping on RL optimization: a sparse reward (equipped with an anti-rambling penalty) and a dense Levenshtein-based reward. Let y denote the model’s generated sequence and τ denote the exact target string.

## C.1 Sparse Reward with Length Penalty

The sparse reward acts primarily as a binary success metric. It assigns a base reward of 1 if the target string τ is successfully generated, and 0 if the model fails to produce the target entirely.

To prevent reward hacking by “rambling”, we use a length penalty term p to decrease the reward for any extra tokens generated other than the target string. Let n be the maximum token generation limit and s be the number of extra tokens generated. Then, $p$ is defined as

$$
p = \left\{ \begin{array}{l l} 0 & \text { if } s = 0 \\ \frac {s}{n} & \text { if } s > 0 \end{array} \right.\tag{2}
$$

and the sparse reward function is defined as

$$
r _ {\text { sparse }} (y, \tau) = \left\{ \begin{array}{l l} \max (0. 5, 1 - p) & \text { if } \tau \in y \text { and } | y | \\ 0 & \text { otherwise } \end{array} \right.\tag{3}
$$

\*(Note: $p$ can be defined as a fixed scalar penalty or a function of the excess length $( | y | - | \tau | ) . ^ { * }$ This ensures the sparse optimization baseline actively discourages rambling and aligns only the precise target behavior.

## C.2 Dense Reward (Levenshtein Distance)

To address the credit assignment problem for models lacking initial probability mass, we implement a dense reward that provides continuous, intermediate gradient signals based on structural proximity to the target.

We utilize the standard Levenshtein edit distance, which calculates the minimum number of singlecharacter edits (insertions, deletions, or substitutions) required to transform the generated sequence into the target sequence. Formally, let y and τ be strings of lengths m and n, and let $D ( i , j )$ denote the Levenshtein distance between the first i characters of $y$ and $j$ characters of τ, where y and $\tau _ { j }$ are the i-th and j-th characters. The Levenshtein distance is defined for boundary cases as $D ( i , j ) = \operatorname* { m a x } ( i , j )$ when i = 0 or $j = 0$ . Otherwise, it is calculated as:

$$
D (i, j) = \min \left\{ \begin{array}{l} D (i - 1, j) + 1 \\ D (i, j - 1) + 1 \\ D (i - 1, j - 1) + \mathbb {1} (y _ {i} \neq \tau_ {j}) \end{array} \right.\tag{4}
$$

Let $n = \operatorname* { m a x } ( \operatorname { l e n } ( y )$ , len(τ)) and D be the Levenshtein distance between y and τ. Then, reward function is then defined as

$$
r _ {d e n s e} = \max (0, 1 - \frac {D}{n})\tag{5}
$$

# D Exponential Process Reward Model (PRM) Implementation

For our math reasoning experiment, in order to scale our analysis from structural sequencematching (Levenshtein distance) to combinatorial mathematical reasoning, we replaced the string-based dense reward with a Process Reward Model (PRM). Mathematical reasoning requires logical verification across diverse, valid solution paths (e.g., direct factoring, quadratic formula, dehomogenization). To achieve this, we deployed a 32-billion parameter instruction-tuned model (Qwen2.5-32B-Instruct) functioning as an LLM-> |τ |<sub>as-a-Judge.</sub>

The PRM evaluates the generated trajectory y at the end of each rollout, classifying the strategy used and evaluating the presence of specific, sequential logical milestones.

## D.1 Logical Milestones and Reward Curve

The AIME problem utilized in our experiments $( 1 2 x ^ { 2 } - x y - 6 y ^ { 2 } = 0 )$ requires a multi-step algebraic derivation. We instruct the PRM to extract a boolean vector $M ( y ) \in \{ 0 , 1 \} ^ { 5 }$ , representing the successful completion of the following five milestones:

• m : Initiated a correct algebraic path configuration (e.g., setting up factorization).

• $m _ { 2 } \colon$ Derived accurate base root relationships between x and y.

$m _ { 3 } \colon$ Evaluated the integer boundary constraints $( - 1 0 0 \leq x , y \leq 1 0 0 )$ correctly.

$m _ { 4 } \colon$ Calculated the correct solution count for at least one case branch.

$m _ { 5 } \colon$ Identified and correctly subtracted the intersection overlap at the origin (0, 0).

A critical challenge in applying linear partial credit $( \mathrm { e . g . , + 0 . 1 5 }$ per step) is the introduction of local minima. An optimizing policy may discover that completing three steps and halting yields a “good enough” reward, dampening the advantage gradient required to risk generating further tokens to reach the final answer. To prevent this advantage compression, we map the milestones to a reward curve. The step weights are defined as $w = [ 0 . 0 5 , 0 . 0 5 , 0 . 1 0 , 0 . 1 5 , 0 . 2 5 ]$ . The base process reward is calculated as:

$$
r _ {p r o c e s s} (y) = \sum_ {i = 1} ^ {5} w _ {i} \cdot m _ {i}\tag{6}
$$

This exponential scaling strictly enforces increasing marginal value, ensuring that advanced reasoning steps provide a stronger gradient pull than early exploratory steps.

## D.2 Outcome Overrides and Defensive Penalties

To anchor the PRM to the absolute ground truth and prevent reward hacking, the final reward incorporates deterministic outcome overrides and active penalties.

Let $\tau = 1 1 7$ be the exact correct answer, and τ = 118 represent the specific, known nearmiss where the model successfully completes the calculus but fails to account for the origin overlap. Let extract(y) be a deterministic parsing function that extracts the integer from the final \boxed{} command. The unpenalized reward $r _ { b a s e }$ is defined as:

$$
r _ {b a s e} (y) = \left\{ \begin{array}{l l} 1. 0 & \text { if   } \operatorname{extract} (y) = \tau \\ 0. 6 & \text { if   } \operatorname{extract} (y) = \tau_ {n e a r} \\ r _ {p r o c e s s} (y) & \text { otherwise } \end{array} \right.\tag{7}
$$

Finally, LLM policies optimizing against dense rewards frequently attempt to “farm” tokens by redundantly repeating early logical steps that are known to yield partial credit. To counteract this, the PRM is instructed to flag cyclic reasoning with a boolean penalty marker $m _ { l o o p }$ . If the model loops without reaching the final exact answer, a penalty $p _ { l o o p } ~ = ~ - 0 . 3$ is applied. Furthermore, a strict formatting penalty $p _ { f o r m a t } = - 0 . 5$ is applied if the trajectory fails to conclude with the \boxed{} delimiter.

The final dense reward is bounded at 0 and defined as:

$$
r _ {\text { dense }} (y) = \max \left(0, r _ {\text { base }} (y) + p _ {\text { loop }} + p _ {\text { format }}\right) \tag {2}\tag{8}
$$

By heavily penalizing redundancies and exponentially rewarding progress, this PRM structure successfully bridges the exploration gap for models with near-zero initial priors.

# E RLVR Algorithm

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 RLVR Algorithm
1: Input: base model $\pi_{ref}$, prompt dataset $D$, reward function $r(x,y)$
2: Initialize: $\pi_{\theta} \leftarrow \pi_{ref}$
3: for train steps do
4: Sample input: $x \sim \mathcal{D}$
5: Sample output: $y \sim \pi_{\theta}(y \mid x)$
6: Get reward: $r \leftarrow r(x,y)$
7: Store $\langle x,y,r\rangle$ in buffer
8: if Time to train then
9: Update model with an RL algorithm of choice to maximize:
$\mathbb{E}_{\text{buffer}}[\frac{1}{c} r(x,y) - D_{\text{KL}}(\pi_{\theta} \| \pi_{\text{ref}})]$
10: end if
11: end for
12: return $\pi_{\theta}$
</div>

# F Prompt Distribution Experimental Details

Training Details: For the broad-distribution condition detailed in Section 4.3, we use a productionscale dataset comprising 10,000 prompts sampled from the OLMo 3 RLVR training mix, evenly split between mathematics, instruction following, and code. We utilize the standard OlmoRL codebase with verifiable rewards replaced by random scalars drawn uniformly from [0, 1]. To ensure fully onpolicy training, async steps are set to 0. All experiments are distributed across three 8xH100 nodes, sampling 8 responses per prompt. The narrowdistribution condition utilizes the identical hardware and algorithmic setup, but is restricted to 100 math-only prompts fine-tuned directly from the SFT checkpoint.

Evaluation Tracking: To precisely measure entropy and unlearning dynamics, we extract 200 evaluation prompts per domain (100 that appeared during training, and 100 held-out out-ofdistribution prompts). Prior to RL training, we sample a fixed response for each prompt from the base model. Throughout the random reward finetuning process, we evaluate the model every 50 training steps, measuring the log-likelihood and average per-token entropy assigned to these fixed baseline responses.

# G Model Sizes

![](images/93cc5ac53ca3968121e8ab1243e8af39e789d7673e08773a8f3d9b09c83346bc.jpg)

[Image: This vertical bar chart, titled "SFT Performance - Reasoning," compares substring match percentages across three experimental conditions: Base, SFT+, and SFT-. The vertical axis measures performance in percentage from 0 to 100, showing significant variation between the groups. The "Base" condition yields a low score of 3.9%, depicted by a short blue bar, whereas the "SFT+" condition reaches the peak value of 26.6% with a taller green bar. Finally, the "SFT-" condition registers a score of 0.0% with no visible bar present.]

![](images/7e9d2c34feccf3872bdd7c742898fcde53361d1909f4c9410e222d06c022ec27.jpg)

[Image: This line chart titled 'RL Dense Reward Raw - Reasoning' displays Reward values on the y-axis (ranging from 0.2 to over 0.9) against Steps on the x-axis (ranging from 0 to 50). Three distinct data series are plotted: 'Base' in blue, 'SFT +' in green, and 'SFT' in orange. The 'SFT +' curve shows a steady upward trend starting from roughly 0.65 and finishing near 0.9, while the 'Base' curve fluctuates at a low level before rising sharply after step 15 to reach the highest rewards. In contrast, the 'SFT' curve remains the lowest performing, hovering relatively flat between 0.4 and 0.6 for the duration.]

![](images/f91d88bcc8675ec138341dc54790958faaeb8b0651372582c5cba033036b6dab.jpg)

[Image: This vertical bar chart titled "RL Evaluation - Reasoning" presents Substring Match % scores for Sparse (purple) and Dense (brown) models across three categories: Base, SFT+, and SFT-. The Base category shows a large performance gap, with the Dense model achieving 92.2% while the Sparse model is at 10.2%. Both SFT+ models converge to similar high performance levels, recording 85.9% for Sparse and 86.7% for Dense. Conversely, the SFT- category results in 0.0% match percentage for both model types.]

![](images/6940a7fac90dcf23b30a3140b1c8f0f8dc530828338057a9b91ca2b6f7f88eee.jpg)

[Image: This line chart titled "RL Sparse Reward Raw - Reasoning" plots Reward on the vertical axis (ranging from 0.0 to 0.8) against Steps on the horizontal axis (ranging from 0 to 50). The "Base" data series, represented by a green line, demonstrates a volatile upward trend, starting around 0.25 and peaking near 0.8 in the final steps. Conversely, the "SFT+" series (blue line) fluctuates with low amplitude primarily below 0.15, while the "SFT-" series (orange line) remains constant at approximately 0.0 throughout the process.]

![](images/959f92198cae7a104ab212185b3b5046bcb9a442a6d3636b67bac69ce6496724.jpg)

[Image: This bar chart illustrates the SFT Performance metrics for the Qwen2-7B model across three distinct categories: Base, SFT+, and SFT-. The vertical axis indicates Substring Match percentage, where the Base category scores 3.5% and the SFT+ category reaches a peak of 28.8%. The SFT- category demonstrates a result of 0.0%.]

![](images/f5d8fa930ae58988e2788706ce344b7a0262a367df52ab5c9cec6062e3effceb.jpg)

[Image: This line chart titled "RL Dense Reward Raw (Qwen-2-7B)" plots Reward on the vertical axis against Steps on the horizontal axis, spanning from 0 to roughly 130 steps. The green line representing the "Base" configuration rises rapidly with significant volatility before stabilizing near a reward of 1.0 by step 30. The blue line, labeled "SFT+", exhibits lower performance initially but begins a steep ascent around step 45, eventually converging with the Base line near 1.0 by step 80. In contrast, the orange line labeled "SFT" remains constant at a reward value of 0.0 across the entire timeline.]

![](images/ab45939fc3b020ec55b1c396798009a25d252c010959a7bbd80c4ec0cd0ac452.jpg)

[Image: This bar chart titled "RL Evaluation (Qwen2-7B)" plots Substring Match % on the y-axis against model categories on the x-axis. It compares the performance of Sparse (purple) versus Dense (brown) reward models across two groups: Base and SFT+. For the Base group, the Sparse model achieves a 99.9% match while the Dense model achieves 98.1%. In the SFT+ group, the Sparse model reaches 99.6% and the Dense model reaches 99.4%, with both sets of bars indicating very high performance close to 100%.]

![](images/d54fb9c7ec68870ed2e689ce5ded6da2d2098843bc0815e1d205d33cab088605.jpg)

[Image: The image displays a line chart titled "RL Sparse Reward Raw (Qwen2-7B)" plotting Reward on the vertical axis against Steps on the horizontal axis. Three data series are compared: "SFT+" (green), "Base" (blue), and "SFT" (orange). The green "SFT+" line exhibits rapid improvement, climbing from roughly 0.2 to a reward of 1.0 by step 40. The blue "Base" line stays low until step 35 before steadily ascending to match the maximum reward of 1.0 by step 80, whereas the orange "SFT" line remains flat at a reward of 0.0 for the entire duration.]  
Figure 5: RL post-training dynamics and evaluation metrics for Qwen2.5-7B-Instruct - Math Reasoning (Top Left) Prior to RL, the SFT+ model shows a strong initial prior (26.6%), and the Base model exhibits a small but non-zero starting mass (3.9%). (Bottom Left) Final RL evaluation reveals that Dense rewards on both the SFT+ and Base models successfully and acquire the target behavior (> 85% match rates) however under sparse rewards the Base model was unable to acquire the target behavior while the SFT+ model acquires the target behavior. SFT- unable to gain momentum with either reward structure. (Right) The raw reward curves highlight a difference in the RL Training between Base, SFT+ and SFT- models. Experiments show that even through complex reasoning tasks, the priors of the models impact the role of RL post training.  
Figure 6: RL post-training dynamics and evaluation metrics for Qwen2-7B. (Top Left) Prior to RL, the SFT+ model shows a strong initial prior (28.8%), and the Base model exhibits a small but non-zero starting mass (3.5%). (Bottom Left) Final RL evaluation reveals that both the SFT+ and Base models successfully and perfectly acquire the target behavior (> 98% match rates) under both dense and sparse rewards, while SFT- completely fails. (Right) The raw reward curves highlight a delayed but successful optimization for the Base model. While SFT+ climbs immediately, the Base model requires roughly 40 steps to escape its initial plateau before rapidly converging to a 1.0 reward. The SFT- model remains strictly suppressed.

![](images/40279c2fa8374d4e42ed8ee4906072ca9dd68ae7cda54efd486866d97dfeabfe.jpg)

[Image: The image displays a vertical bar chart titled "SFT Performance (Qwen2-1.5B)" that plots "Substring Match %" on the y-axis against three model categories on the x-axis. The categories listed are "Base," "SFT+," and "SFT-." The "Base" column shows a value of 0.3%, while the "SFT+" column features a green bar representing a value of 8.0%. The "SFT-" column indicates a value of 0.0%, corresponding to the absence of a visible bar.]

![](images/ec69dbf5799822e35e7e9d8b3433893a840c155bd8780d01f3c43362d543da52.jpg)

[Image: This line chart illustrates the RL Dense Reward performance for the Qwen2-1.5B model over approximately 120 training steps. The x-axis denotes Steps, and the y-axis indicates Reward values ranging from 0.0 to 0.8. Three distinct data series are shown: Base (blue), SFT+ (green), and SFT- (orange). The Base model fluctuates moderately between 0.2 and 0.3, while the SFT- model remains flat at 0.0. Notably, the SFT+ model starts below 0.2 but shows a steep increase starting around step 60, reaching a peak reward above 0.8 by the end of the timeline.]

![](images/0d6fc02409fb23ae267ee9748e40c2e13d12bb905f660ceb5fb824bb58588642.jpg)

[Image: This bar chart displays the 'RE Evaluation' results for the Qwen2-1.5B model, measuring 'Substring Match %' across conditions labeled 'Base', 'SFT+', and 'SFT-'. The chart compares 'Sparse' (purple) and 'Dense' (brown) model variants, indicated by the legend in the top right. Data values show very low performance for the Base group (0.7% for Sparse and 7.0% for Dense), which spikes significantly in the SFT+ group (92.5% for Sparse and 90.0% for Dense). Although the 'SFT-' label appears on the x-axis, there are no visible bars representing data for this category.]

![](images/8d7308429dd54da558cfff852b29b6adfae3e81dec21807c68fb49fdbd3d754d.jpg)

[Image: This line chart displays RL Sparse Reward metrics for a Qwen2-1.5B model across approximately 120 training steps. The vertical axis represents "Reward" ranging from 0.0 to 0.8, while the horizontal axis represents "Steps". Three data series are plotted: "Base" (dark green), "SFT+" (blue), and "SFT." (orange). The "Base" curve exhibits a steady increase in reward starting around step 60, peaking near 0.8 with high volatility, whereas both the "SFT+" and "SFT." curves remain stagnant near zero reward throughout the entire process.]

![](images/d754be46b083acd9d189334e6cf10989a8990bc684d26d8b43e3710816017471.jpg)

[Image: This bar chart titled "SFT Performance Qwen3-1.7B" displays Substring Match percentage for three distinct categories along the x-axis: Base, SFT+, and SFT-. The y-axis measures percentage values ranging from 0 to 100. While the Base configuration achieves only 0.5% and the SFT- configuration yields 0.0%, the SFT+ category shows a marked performance improvement reaching 14.0%.]

![](images/4b4f92a500c126da522f53aa4f6bd2a5d5ea53422d50878cb0d46e84eb1b2a0d.jpg)

[Image: This line chart, titled "RL Dense Reward Raw Qwen3-1.7B," displays the progression of Reward over Steps for three different configurations. The vertical axis ranges from 0 to 0.8, while the horizontal axis tracks training steps up to 120. The green line representing "SFT+" achieves the highest reward, rising sharply after step 60 to exceed 0.8. In contrast, the blue "Base" line shows moderate improvement reaching roughly 0.6, while the orange "SFT-" line remains stagnant near 0.2 throughout the duration.]

![](images/1de120c512fd5ae64170db194fd09b9284844dfcc9408ce51c16dcff5d2fcab4.jpg)

[Image: The image displays a grouped bar chart titled "RL Evaluation Qwen3-1.7B" with the vertical axis labeled "Substring Match %" ranging from 0 to 100. The horizontal axis categorizes the data into "Base," "SFT+," and "SFT-," comparing two series identified in the legend as "Sparse" (purple) and "Dense" (brown). For the "Base" category, the Sparse value is 10.0% and the Dense value is 48.8%, while the "SFT+" category shows a substantial increase to 98.7% for Sparse and 85.7% for Dense. The "SFT-" label is present on the axis, but no corresponding bars are visible in this view.]

![](images/8f851b919abe9432094de81038cf31e37ba704a22664d11de6672a38c5044e7c.jpg)

[Image: Line chart titled "RL Sparse Reward Raw Qwen3-1.7B" comparing the reward progression of three methods—Base, SFT+, and SFT—over 120 training steps. The SFT+ curve (green) shows consistent growth, rising sharply to reach a plateau between 0.8 and 1.0 by step 90. Conversely, both the Base (blue) and SFT- (yellow/orange) curves remain extremely low, hovering near 0.0 with minor fluctuations throughout the experiment. The vertical axis represents Reward from 0.0 to 1.0, while the horizontal axis tracks Steps up to 120.]  
Figure 7: RL post-training dynamics and evaluation metrics for Qwen2-1.5B. (Top Left) Initial substring match performance prior to RL shows the SFT+ model possesses only marginal probability mass for the target sequence (8.0%), while Base (0.3%) and SFT- (0.0%) exhibit near-zero coverage. (Bottom Left) Final RL evaluation demonstrates that only the SFT+ model suc cessfully acquires the target behavior (achieving > 90% match rates under both reward regimes). The Base model gains a slight benefit from dense rewards (7.0%) but largely fails, alongside SFT-. (Right) Raw reward curves confirm these dynamics: the SFT+ model suc cessfully optimizes both signals, while the Base and SFT- variants flatline, failing to escape their initial exploration plateaus.  
Figure 8: RL post-training dynamics and evaluation metrics for Qwen3-1.7B. (Top Left) Initial coverage is limited, with SFT+ at 14.0% and Base/SFT- near zero. (Bottom Left) Final evaluation demonstrates the specific power of dense rewards. While the Base model only achieves a 10.0% match rate under sparse rewards, the granular gradient of the dense reward allows it to reach 48.8%. The SFT+ model succeeds broadly across both signals. (Right) The reward curves explicitly show this dynamic: under dense rewards, the Base model successfully begins climbing (reaching ∼0.5), whereas under sparse rewards, it remains completely flat at 0. SFT- fails entirely across all regimes.

![](images/4ac674474fd65d52d611c15218a41c6f2b7d6869a07e850318a01a1dd7c4aa08.jpg)

[Image: The image presents a vertical bar chart titled "SFT Performance (Qwen3-8B)" that evaluates Substring Match percentage across three categories. The y-axis ranges from 0 to 100, showing significant disparity between the bars. The central bar for "SFT+" rises to a value of 42.8%, while the bars for "Base" and "SFT-" remain flat at the bottom, both labeled with a value of 0.0%.]

![](images/f3845ce18e7c88b232b078302ac2af0f797a243449945791e08912802b769d57.jpg)

[Image: This line chart, titled "RL Dense Reward Raw (Qwen-3B)", displays performance metrics over 120 steps with Reward ranging from 0.0 to 1.0 on the y-axis. The "Base" model (blue line) maintains a constant reward of approximately 0.2 throughout the entire process. The "SFT+" model (green line) exhibits a sharp increase in reward between steps 25 and 40, eventually plateauing at the maximum value of 1.0. Conversely, the "SFT" model (orange line) starts at a reward of roughly 0.1 and drops to near zero by step 40.]

![](images/6b0726e218c7eadddbdf51f7ec75b16df9e91b1af390f4dc4d5cfaa8a49f1198.jpg)

[Image: This bar chart, titled "RL Evaluation (Qwen3-8B)," plots "Substring Match %" on the y-axis against three model categories—Base, SFT+, and SFT—on the x-axis. The chart distinguishes between two reward conditions using color-coded bars according to the legend: purple for "Sparse" and brown for "Dense." The SFT+ category displays two bars reaching the maximum value of 100%, labeled explicitly with "100.0%", while the Base and SFT- categories show no visible bars, indicating zero match percentage.]

![](images/f84b2c08f25138248b3523b5513c0664b15cf5b210fe59e1a1c637ea237d0cbc.jpg)

[Image: Line chart titled "RL Sparse Reward Raw (Qwen3-8B)" plotting Reward on the y-axis against Steps on the x-axis from 0 to 120. The chart displays three legend entries: "Base" (blue), "SFT+" (green), and "SFT:" (orange). The "SFT+" series shows a sharp increase in reward starting from step 0, reaching a plateau near 1.0 by step 40. The "SFT:" series remains flat at a reward of approximately 0.0 throughout the 120 steps, while the "Base" series is not distinctly visible, suggesting it may overlap with the zero-value baseline.]  
Figure 9: RL post-training dynamics and evaluation metrics for Qwen3-8B. (Top Left) The SFT+ model starts with a highly accessible prior (42.8%), while the Base and SFT- models start with exactly 0.0% proba bility mass. (Bottom Left) Final evaluation shows a stark binary outcome: the SFT+ model perfectly converges to a 100.0% match rate under both sparse and dense rewards, while the Base and SFT- models achieve absolute 0%. (Right) The raw reward curves demon strate rapid, smooth convergence for SFT+ under both regimes. In contrast, the Base and SFT- models remain completely flat, unable to generate the target sequence a single time during exploration, confirming the strict bottleneck imposed by a 0% base prior.