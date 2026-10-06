# C. Experiment Details

We provide detailed hyperparameter configurations for all baseline methods and our proposed approach. All experiments are conducted on a single NVIDIA A800 GPU with 80GB memory. We use OpenRouter API for LLM inference.

## C.1. Common Settings

All methods share the following experimental settings:

Table 6. Common experimental settings across all methods.

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Max Interaction Turns</td><td>20</td></tr><tr><td>Agent LLM</td><td>Qwen-2.5-72B-Instruct / DeepSeek-V3.2</td></tr><tr><td>Reward Evaluator</td><td>DeepSeek-V3.2</td></tr><tr><td>Strategy Embedding Model</td><td>Qwen3-Embedding-8B</td></tr><tr><td>Embedding Dimension</td><td>4096</td></tr><tr><td>Optimization Target</td><td>Both agents (P1 &amp; P2)</td></tr></table>

## C.2. EvoPrompt

We implement EvoPrompt following Guo et al. (2024), using the Genetic Algorithm (GA) variant which demonstrated superior performance in their experiments.

Table 7. EvoPrompt (GA) hyperparameters.

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Evolution Mode</td><td>Genetic Algorithm (GA)</td></tr><tr><td>Population Size</td><td>5</td></tr><tr><td>Evolution Interval</td><td>5 turns</td></tr><tr><td>Mutation Rate</td><td>0.2</td></tr><tr><td>Elite Ratio</td><td>0.4</td></tr><tr><td>Selection Mode</td><td>Roulette Wheel</td></tr><tr><td>Population Update</td><td>Top-K</td></tr><tr><td>Mutation Model</td><td>Qwen-2.5-7B-Instruct</td></tr><tr><td>Mutation Temperature</td><td>0.3</td></tr><tr><td>Selection Strategy</td><td>Round-Robin</td></tr><tr><td>Score Update Method</td><td>Replace</td></tr></table>

The GA variant performs crossover between two parent strategies selected via roulette wheel selection, followed by LLM-based mutation. Elite strategies (top 40%) are preserved across generations.

## C.3. OPRO

We implement OPRO following Yang et al. (2023), using meta-prompts with instruction-score history to guide the LLM optimizer.

OPRO maintains a history of instruction-score pairs and uses this history as context for the LLM optimizer to generate new candidate strategies. Evolution is triggered after all strategies in the population have been evaluated once.

## C.4. INSTINCT

We implement Neural UCB following the NeuralTS-Diag variant from Lin et al. (2024b), which uses per-sample gradients computed via backpack to estimate uncertainty.

Table 8. OPRO hyperparameters.

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Population Size</td><td>5</td></tr><tr><td>Max Instructions in Meta-Prompt</td><td>10</td></tr><tr><td>Score Threshold</td><td>0.5</td></tr><tr><td>Evolution Trigger</td><td>Round Complete</td></tr><tr><td>Optimizer Model</td><td>Qwen-2.5-7B-Instruct</td></tr><tr><td>Optimizer Temperature</td><td>1.0</td></tr><tr><td>Selection Strategy</td><td>Round-Robin</td></tr><tr><td>Score Update Method</td><td>Replace</td></tr></table>

Table 9. Neural UCB hyperparameters.

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Network Architecture</td><td>2-layer MLP</td></tr><tr><td>Hidden Size</td><td>128</td></tr><tr><td>Activation</td><td>ReLU</td></tr><tr><td>λ (Regularization)</td><td>0.1</td></tr><tr><td>ν (Exploration)</td><td>1.0</td></tr><tr><td>Learning Rate</td><td>0.01</td></tr><tr><td>Training Epochs</td><td>100</td></tr></table>

The UCB score is computed as:

$$
\operatorname{UCB} (a) = \hat {\mu} (a) + \nu \sqrt {\sum_ {i} \frac {\lambda \cdot g _ {i} (a) ^ {2}}{U _ {i}}}\tag{15}
$$

where ${ \hat { \mu } } ( a )$ is the predicted reward, $g _ { i } ( a )$ are per-sample gradients, and $U _ { i }$ is the diagonal of the incrementally updated gradient covariance matrix.

## C.5. Adversarial Online Strategy Optimization

Our method uses a neural adversarial bandit with context-conditioned value estimation and softmax-based arm selection over decayed cumulative scores.

Table 10. Hyperparameters of ALSO.

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Network Architecture</td><td>2-layer MLP with Pre-LN</td></tr><tr><td>Hidden Size</td><td>512</td></tr><tr><td>Activation</td><td>GELU</td></tr><tr><td>Context Embedding</td><td>4096-dim</td></tr><tr><td>Context Embedding Model</td><td>Qwen3-Embedding-8B</td></tr><tr><td>Exploration Temperature η</td><td>10.0</td></tr><tr><td>Score Decay λ</td><td>0.9</td></tr><tr><td>Learning Rate</td><td>0.001</td></tr><tr><td>Weight Decay</td><td>Dynamic: min(0.01, 0.01/N)</td></tr><tr><td>Training Epochs</td><td>Up to 100 with early stopping</td></tr><tr><td>Training Batch Size</td><td>8</td></tr><tr><td>Update Interval</td><td>1</td></tr><tr><td>Max Turns per Episode</td><td>20</td></tr></table>

## C.6. Strategy Selection and Convergence Across Diverse Scenarios

Strategy Selection and Convergence Across Diverse Scenarios

![](images/a6eaffb285afce78c735410957395759e1fe484dd19d5f6b9addc730b07f97bd.jpg)

[Image: This scatter plot illustrates the evolution of strategic choices made by "William Brown" against "Ava Martinez" across approximately 18 turns, achieving a total reward of 4.36. The vertical axis categorizes different approaches including "No Strategy," "Reciprocity," "Self-Present," and "Constructive," while the horizontal axis marks the progression of turns. During the initial phase (turns 1–6), the selected strategies fluctuate wildly, shifting between lower-tier options like "Reciprocity" and higher ones like "Logrolling E." From turn 7 onwards, the strategy selection converges and stabilizes consistently at the "Constructive" level, represented by a flat line of yellow markers.]

![](images/202232ad6bbe2b4b3167b4c1559225abf095afbc793105d2037d6aa8ef1b6beb.jpg)

[Image: The image displays a line chart titled "(c) Isabelle Martinez vs Ava Martinez," tracking the evolution of strategic choices across multiple turns. The vertical axis categorizes strategies ranging from "No Strategy" at the bottom to "Logrolling E" at the top, including intermediate levels like "Reciprocity," "Self-Present," and "Rational Cho[ice]." Data points plotted against the horizontal "Turn" axis show a progression starting at "No Strategy," moving through "Constructive" and "Self-Present," peaking at "Logrolling E" around turn 9, and eventually converging into a stable state along the dashed "Rational Cho[ice]" line from turn 12 onwards. The chart includes a header note indicating "-> Rational Choice (Reward: 4.50)."]

![](images/cb60f4c9f51a0a24553489e19722cd668a07d4b4d33e298ed5c93022e3385388.jpg)

[Image: This scatter plot charts the evolution of negotiation strategies chosen by Miles Hawkins against Zane Bennett over 20 turns within an Integrative Negotiation setting. The vertical axis lists discrete strategies such as "GRIT Stratag", "Self-Present", and "Reciprocity", while the horizontal axis indicates the turn number from 1 to 20. Early interactions involve sporadic selections of strategies like "No Strategy", "GRIT Stratag" (orange dots), and "Self-Present" (purple dot). However, starting around turn 6, the strategy converges and remains fixed at "Reciprocity" for the remainder of the simulation, visualized as a horizontal row of green dots.]

![](images/b46d180f347c72d12658af8a9fc0dc9513f1aeb1ea231de3e5139ac089d86237.jpg)

[Image: This chart, labeled "(d) Lily Greenberg vs Lena Goodwin," plots strategy selection trajectories over 20 conversation turns. The y-axis enumerates specific negotiation strategies such as "Logrolling E," "GRIT Strateg," and "Reciprocity," while the x-axis denotes the turn number. Initially, the plotted points vary widely across the strategy spectrum, including spikes to "Logrolling E" and selections of "GRIT Strateg" and "Rational Cho." By approximately turn 12, the trajectory converges to a steady state at the "Reciprocity" level, represented by a series of green dots aligned with a dashed horizontal line, corresponding to the subtitle "Reciprocity Trigger (Reward: 3.71)."]

![](images/7fced9a3a1ac6e6766e384d02c0032ad868365ff5b99ca961a15c2adbded1653.jpg)

[Image: This horizontal bar chart, titled "(e) Strategy Effectiveness (across all matched scenarios)," compares the average final reward achieved by thirteen different negotiation strategies. The x-axis represents the "Average Final Reward," spanning from 3.6 to 4.4, while the y-axis lists distinct strategies ranked in descending order of performance. A vertical red dashed line indicates a "Baseline" positioned slightly below 3.8 on the reward scale. Each bar is annotated with its specific numerical value and sample size (*n*), showing that strategies like "Rational Choice" and "Constructive" achieve the highest scores of 4.00, whereas "No Strategy" yields the lowest average reward of 3.79.]  
Figure 10. (a-d) Strategy selection trajectories for four representative scenarios, showing how the bandit algorithm converges to scenariospecific optimal strategies over conversation turns. Each colored dot represents the strategy selected at that turn, with the dashed horizontal line indicating the most frequently selected strategy. Different scenarios converge to distinct strategies: Face-Saving for relationship-sensitive negotiations (a), Integrative Negotiation for collaborative problem-solving (b), Rational Choice for analytica discussions (c), and Reciprocity Trigger for trust-building interactions (d). (e) Average final rewards achieved by each strategy across all 450 scenarios (900 agent-strategy pairs). Strategies are ranked by effectiveness, with the red dashed line indicating the No Strategy baseline (3.79). All social strategies outperform the baseline, with Rational Choice and Constructive Controversy achieving the highest average rewards (4.00), demonstrating that adaptive strategy selection based on scenario context leads to improved social interaction outcomes.

# D. Additional Experimental Studies

To further substantiate the design choices and empirical validity of ALSO, we report supplementary experiments organized into three groups: (i) ablations on the structure of the strategy space, (ii) ablations on the algorithmic components and the surrogate architecture, and (iii) extended comparisons and robustness analyses. Unless otherwise specified, all experiments follow the protocol described in Section 5 and are conducted on a Sotopia subset, or on Sotopia-Hard where indicated.

## D.1. Ablations on the Strategy Space

### D.1.1. EFFECT OF POOL SIZE

We first examine how the cardinality of the strategy pool affects performance. Holding the six theoretical categories fixed, we expand the pool to {6, 12, 24, 48} arms via LLM-based paraphrasing and evaluate ALSO under an identical interaction budget. As reported in Table 11, performance peaks at twelve arms across all four dimensions. The degradation observed at twenty-four and forty-eight arms is consistent with an exploration bottleneck: as the action space grows, the limited number of interactions becomes insufficient to reliably identify the optimal arm. These results indicate that the principal capacity constraint of ALSO lies in the exploration budget rather than in the surrogate’s modeling capacity.

Table 11. Effect of strategy pool size on ALSO. “Vanilla” denotes the no-strategy baseline.

<table><tr><td>Pool Size</td><td>Goal</td><td>Rel.</td><td>Know.</td><td>Overall</td></tr><tr><td>6</td><td>6.79</td><td>2.25</td><td>5.25</td><td>3.45</td></tr><tr><td>12 (default)</td><td>7.93</td><td>3.07</td><td>6.46</td><td>3.91</td></tr><tr><td>24</td><td>7.21</td><td>2.32</td><td>5.89</td><td>3.61</td></tr><tr><td>48</td><td>6.75</td><td>1.85</td><td>5.17</td><td>3.29</td></tr></table>

### D.1.2. EFFECT OF SEMANTIC DIVERSITY

We next isolate the role of semantic diversity by fixing the total number of arms at twelve and varying the number of underlying theoretical categories among {2, 4, 6}, with each category paraphrased to fill the budget. Table 12 reveals a monotone improvement with respect to diversity, yielding a 29.9% relative gain in the Overall metric when the number of categories is increased from two to six. Notably, even with only two categories ALSO matches the Vanilla baseline on the Overall dimension (3.01 vs. 3.02), indicating that ALSO incurs no degradation under highly constrained strategy spaces.

Table 12. Effect of strategy diversity (number of underlying categories) under a fixed budget of twelve arms.

<table><tr><td>#Categories</td><td>Goal</td><td>Rel.</td><td>Know.</td><td>Overall</td></tr><tr><td>2</td><td>6.06</td><td>1.22</td><td>4.97</td><td>3.01</td></tr><tr><td>4</td><td>6.84</td><td>2.24</td><td>5.41</td><td>3.40</td></tr><tr><td>6</td><td>7.93</td><td>3.07</td><td>6.46</td><td>3.91</td></tr></table>

### D.1.3. DYNAMIC STRATEGY SPACE VIA ONLINE DISCOVERY

Although the default configuration employs a fixed pool of twelve strategies, the surrogate operates on continuous embeddings , so introducing additional strategies requires only their embedding and incurs no further training of either the underlying language model or the surrogate. To assess this property empirically, we use the surrogate’s online reward estimates to identify top-performing strategies and prompt a language model to generate paraphrased variants, thereby dynamically expanding the pool during interaction. As shown in Table 13, the dynamic variant matches the default ALSO on the Overall metric while improving Goal, demonstrating that the framework readily accommodates autonomous strategy discovery and online expansion.

Table 13. ALSO with a dynamically expanded strategy pool driven by online surrogate estimates.

<table><tr><td>Variant</td><td>Goal</td><td>Overall</td></tr><tr><td>ALSO</td><td>7.93</td><td>3.91</td></tr><tr><td>ALSO + Dynamic</td><td>8.39</td><td>3.92</td></tr></table>

## D.2. Ablations on Algorithmic Components and Surrogate Architecture

### D.2.1. SURROGATE ARCHITECTURE

Because the principal additional cost of ALSO arises from training the neural surrogate, we further ablate its architectural capacity on Sotopia-Hard. Three configurations are compared: a linear model, a single-layer multilayer perceptron (MLP), and the original two-layer MLP. As shown in Table 14, the linear model underfits the dialogue state, whereas the two-layer MLP exhibits signs of overfitting. The single-layer MLP attains the most favorable trade-off between expressive capacity and generalization, and accordingly is adopted in the revised system.

Table 14. Surrogate architecture ablation on Sotopia-Hard.

<table><tr><td>Architecture</td><td>Goal</td><td>Overall</td></tr><tr><td>Linear</td><td>7.44</td><td>3.65</td></tr><tr><td>1-Layer MLP</td><td>7.77</td><td>3.73</td></tr><tr><td>2-Layer MLP (orig.)</td><td>7.11</td><td>3.53</td></tr></table>

### D.2.2. EMPIRICAL CONVERGENCE AND SURROGATE PREDICTION QUALITY

We further characterize the empirical learning dynamics of ALSO from two complementary perspectives, both reported in Figure 11. First, the average per-turn reward on Sotopia-Hard rises rapidly during the first five turns and stabilizes thereafter, evidencing efficient online adaptation. Second, the surrogate’s predictions exhibit a strong rank correlation with the realized rewards, attaining a Spearman coefficient of $\rho = 0 . 8 6 0$ . The prediction error is comparatively large during early turns and may deviate in either direction, reflecting the exploration phase in which the surrogate is calibrated from limited observations; in later turns the predicted and realized curves converge closely, indicating a transition toward exploitation as the surrogate becomes accurate.

![](images/3e7b95b2c0b3165bca0c7f1c18dafe9be4e67274da47be8d2df9cd1a61f38b78.jpg)

[Image: The image displays a line chart plotting "Average Reward" on the y-axis (ranging from 0.5 to 0.9) against "Turn" on the x-axis (ranging from 1 to 19). Numerous thin light blue lines represent individual episode trajectories, showing high variance and downward spikes particularly in the early turns. A thicker red line labeled "Mean across episodes" illustrates the average performance, rising sharply from approximately 0.6 at turn 1 to a plateau between 0.75 and 0.8 by turn 5.]

![](images/ba6901ed56e9962e2fcd9126d029b76a8f69a9d4288bb41231a52bd3274298f7.jpg)

[Image: This line chart tracks "Score / Reward" values across 19 turns, comparing "NN Predicted Score" (blue line with circle markers), "Actual Reward" (orange line with square markers), and the resulting "Prediction Error" (shaded pink area). Both the predicted and actual reward metrics generally trend upward from approximately 0.65 to peaks exceeding 0.80, although they fluctuate significantly throughout the sequence. The largest divergence between the two lines occurs around turn 6 and again at turn 14, where the Actual Reward spikes higher than the predicted score. A text box in the bottom right corner indicates a correlation coefficient of $p: 0.860$ between the datasets.]  
Figure 11. Empirical learning dynamics of ALSO. Left: average per-turn reward trajectory on Sotopia-Hard. Right: surrogate-predicted versus realized rewards across turns.

## D.3. Extended Comparisons and Robustness Analyses

### D.3.1. COMPARISON WITH OFFLINE STRATEGY-INJECTION BASELINES

The main experiments compare ALSO against online prompt-optimization baselines (OPRO, EvoPrompt, INSTINCT) that operate within the same online loop and under matched language-model call budgets, ensuring methodological parity. For completeness, we additionally compare ALSO with two representative offline strategy-injection methods: Sotopia-Ω (DSI) and Think-on-Your-Feet (AMPO). Following these works, the comparison is conducted under a Qwen-7B-Instruct self-play setting on a Sotopia subset. As reported in Table 15, ALSO achieves the best Overall score among the three methods despite requiring no offline training data—approximately two orders of magnitude less than the ∼2,000 pre-collected episodes used by the offline baselines. This result substantiates the data efficiency of the proposed online adaptation paradigm.

Table 15. Comparison with offline strategy-injection baselines under Qwen-7B-Instruct self-play.

<table><tr><td>Method</td><td>Goal</td><td>Overall</td></tr><tr><td>Sotopia-Ω (DSI)</td><td>7.31</td><td>3.51</td></tr><tr><td>Think-on-Your-Feet (AMPO)</td><td>7.85</td><td>3.54</td></tr><tr><td>ALSO (Ours)</td><td>7.26</td><td>3.58</td></tr></table>

### D.3.2. ROBUSTNESS TO THE TURN-LEVEL EVALUATOR

To preserve consistency with the Sotopia evaluation protocol, all reported configurations adopt GPT-4o as the final episode level judge. The turn-level shaping reward used during online optimization, however, may be produced by a different model. We therefore ablate the choice of turn-level evaluator while holding the final judge fixed. As shown in Table 16, ALSO is robust across all four evaluators considered, with no configuration deviating substantially from the others on the Overall metric. DeepSeek-V3.2 attains the strongest Overall score and provides a high-quality, cost-efficient shaping signal whos preferences transfer well to the GPT-4o final judgments.

Table 16. Effect of the turn-level evaluator on ALSO; the final episode-level judge is fixed to GPT-4o.

<table><tr><td>Turn-level Evaluator</td><td>Goal</td><td>Rel.</td><td>Know.</td><td>Overall</td></tr><tr><td>DeepSeek-V3.2 (Ours)</td><td>7.93</td><td>3.07</td><td>6.46</td><td>3.91</td></tr><tr><td>GPT-4o</td><td>7.61</td><td>3.07</td><td>5.54</td><td>3.78</td></tr><tr><td>GPT-4o-mini</td><td>7.75</td><td>3.18</td><td>6.14</td><td>3.85</td></tr><tr><td>Qwen-2.5-72B</td><td>7.04</td><td>2.64</td><td>5.86</td><td>3.59</td></tr></table>

# E. More Case Study

Table 17. Resource Allocation (Fruit Division). Comparison of information exchange strategies (Turns 2-4).

<table><tr><td>Vanilla: No Strategy – The Missed Connection</td></tr><tr><td>Hendrick (Turn 2): “Hi Lily... I do enjoy apples quite a bit, but I also have a soft spot for oranges. Bananas are nice, but they’re not my top choice. How about you?”Lily (Turn 3): “I value bananas the most... How about I take the two bananas and one apple, and you can have the other apple and the orange?”(Result: Suboptimal. 1 Apple left unallocated. Joint Utility = 10)</td></tr><tr><td></td></tr><tr><td>ALSO: Dynamic Strategy Instruction</td></tr><tr><td>Hendrick (Turn 2): “For me, apples are the top choice, followed by the orange, and then bananas. It makes sense that we see this differently... What about you?”</td></tr><tr><td>[ALSO] Strategy: Surface Hidden ConcernsPrompt: “...gently probe for unspoken concerns... address these concerns directly while showing how your proposal accommodates them.”Lily (Turn 3): “My preferences are bananas first, then the orange, and finally apples. Given our different preferences... If you take 2 apples and I take 1 apple, 2 bananas, and the orange, both of us get a good share...”</td></tr><tr><td>[ALSO] Strategy: Address Asymmetric NeedsPrompt: “...acknowledge that you and the other party may have different priorities... propose creative arrangements that give each side more of what matters most...”Hendrick (Turn 4): “That sounds like a fair proposal... By taking 2 apples, I get my top choice, and you maximize your points... It’s a win-win solution.”(Result: Optimal. All resources allocated. Joint Utility = 14)</td></tr></table>