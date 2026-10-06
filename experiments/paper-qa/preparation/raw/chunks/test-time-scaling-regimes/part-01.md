# Test-Time Scaling in Reasoning LLMs: Inference Regimes, Evaluation, and Reproducibility

Mohsen Hariri Weicong Chen Nahal Shahini Vikash Singh Kai Ye Amirhossein Samandar Debargha Ganguly Sreehari Sankar Yanyan Zhang Shouren Wang Jerry Peng Biyao Zhang Michael Hinczewski Vipin Chaudhary {mohsen.hariri,weicong,nxs814,vikash,kxy406,axs2935,debargha,sxs2284,yxz3106,sxw992,jxp1146,bxz297, mxh605,vipin}@case.edu Case Western Reserve University

# Abstract

Large language models can solve harder reasoning problems with more inference-time compute. The term test-time scaling, however, covers several inference algorithms: extending deliberation along one trajectory, sampling completed candidates and aggregating them by voting or verification, and searching over partial states. These algorithms difer in statistical structure, compute requirements, and failure modes. Treating them as interchangeable under a scalar “budget,” or reporting accuracy without specifying the inference protocol, makes results dificult to compare across studies. We study test-time scaling along three axes. First, we formalize it as budgeted inference over the implicit prefix tree of an autoregressive model and distinguish single-trajectory sequential scaling, leaf-level scaling with terminal reduction, and prefix-level scaling. Second, we treat the full inference system as the evaluated object and separate end-to-end performance from candidate-bank diagnostics. We introduce an evaluation profile whose coordinates and simple functionals recover or bound common repeated-sampling metrics, and require compute accounting and uncertainty estimates that match the protocol. Third, we distinguish exact replay from distributional reproducibility and state the requirements for each. We also organize open-weight reasoning models by model-side and interface mechanisms. Our empirical study covers broad knowledge, symbolic reasoning, and competition mathematics, and we publicly release 1,403,520 sampled model attempts.<sup>1</sup>

https://mohsenhariri.github.io/scorio/tts

Datasets: Trace Lite Math SuperGPQA

# 1 Introduction

Large language models (LLMs) often perform better on reasoning tasks when they generate intermediate steps and use more computation at inference time. Early work on chain-of-thought prompting and self-consistency showed gains on arithmetic, symbolic, and commonsense tasks from generating multi-step solutions and aggregating samples (Wei et al., 2022; Wang et al., 2023). More recent systems make deliberate reasoning a training and interface objective rather than relying on prompting alone: DeepSeek-R1 uses reinforcement learning to elicit long-form reasoning (Guo et al., 2025); Phi-4-reasoning uses curated supervised traces, while Phi-4-reasoning-plus adds outcome-based reinforcement learning (Abdin et al., 2025); Qwen3 exposes explicit “thinking” modes and reasoning-budget controls (Yang et al., 2025a); and the gpt-oss release provides open-weight reasoning models post-trained with chain-of-thought reinforcement learning (OpenAI et al., 2025). Reasoning performance therefore depends on how computation is allocated at test time as well as on pretraining and post-training.

![](images/85a4ae81e24c313d078688d14a3d5f25cbb4d867c797f9bef30f83adf9ce1820.jpg)

[Image: This chart presents a strategic roadmap forecasting the development of AI reasoning systems from 2021 to 2026, structured into four horizontal tracks: Test-Time Inference, Model & Interface Mechanisms, Evaluation & Reporting, and Evaluated System. The timeline visualizes a progression from early ensemble methods like "Self-consistency" and "Verifier selection" toward advanced techniques involving "Value-guided search," "Adaptive deliberation," and "Budget forcing." Key milestones include the emergence of "Native reasoners" and "Hybrid modes" in the middle section, alongside specific system architectures like "Controller + reducer" and "Verifier + judge proxy." The bottom rows correlate these algorithmic shifts with corresponding changes in evaluation protocols, such as "Judge validity" and "Reward overoptimization."]  
Figure 1: A selective chronology of reasoning systems from elicited chains to budgeted inference. The top band traces single-trajectory elicitation, leaf-level sampling with terminal reduction, prefix-level search, and budget-aware control (Section 2.1). The middle band groups model and interface mechanisms into verified distillation, reward optimization, reasoning controls, and parameter-space composition (Appendices D and E). The lower bands show evaluation and reproducibility requirements (Section 3) and identify the evaluated system: checkpoint, prompt, decoder, controller or reducer, verifier or judge, budget, and stopping rule. Utility, candidate-bank profile, cost, and uncertainty are reported together. Green dots mark families represented in the experimental roster; dashed boxes denote contextual milestones. Era labels indicate shifts in emphasis rather than mutually exclusive periods.

The phrase test-time scaling describes several distinct inference algorithms. Some methods allocate extra compute to a single trajectory by forcing longer deliberation or intervening adaptively during generation (Muennighof et al., 2025). Others sample completed candidates and reduce them by voting, reranking, verifier-based selection, or minimum-Bayes-risk decoding (Wang et al., 2023; Cobbe et al., 2021; Freitag et al., 2022). Still others search over partial states, as in Tree-of-Thoughts, RAP, and value-guided decoding (Yao et al., 2023; Hao et al., 2023; Yu et al., 2024). These regimes difer in statistical structure, induced proposal distributions, compute requirements, and failure modes. Treating them as interchangeable under a scalar “budget” obscures the procedure being evaluated and makes cross-paper comparisons dificult to interpret (Welleck et al., 2024; Snell et al., 2025).

Evaluating these methods requires more than benchmarking a base model in isolation. Measured performance depends on the full inference protocol: the prompt template, decoder, search controller, reducer, verifier or judge, stopping rule, and numerical settings. Best-of-N and verifier-guided reranking can improve accuracy, but selection can overoptimize imperfect proxy scores as the candidate set grows (Gao et al., 2023; Huang et al., 2025; Khalaf et al., 2025). LLM judges can evaluate open-ended outputs, but prior work documents position and verbosity biases, and their reliability depends on the task and procedure in test-time scaling settings (Zheng et al., 2023; Zhou et al., 2025). Even with fixed prompts and methods, stochastic decoding and implementation details can change benchmark estimates (Miller, 2024; Blackwell et al., 2024; Ye et al., 2024; Liu et al., 2025b). Studies of reasoning under test-time scaling must define the algorithm being evaluated and match the evaluation to the deployed inference protocol. They should also report model training, inference controls, and uncertainty with enough procedural detail for independent reruns.

Comparisons of open-weight reasoning models require system-level evaluation because their training and in ference mechanisms vary. Recent releases include reinforcement-learning-first reasoning models (Guo et al., 2025), data-centric and verification-focused SFT pipelines (Ye et al., 2025; Guha et al., 2026), open reproductions built from released trace corpora and training code (Hugging Face, 2025; Open-R1 Team, 2025b), checkpoints with thinking and non-thinking modes (Yang et al., 2025a), and model-fusion systems that combine reasoning experts (FuseAI, 2025a;b). This variation confounds checkpoint comparisons because two checkpoints may difer at once in their supervision signals, reasoning styles, compute budgets, and aggregation protocols. Comparisons should separate these axes and treat reasoning as a property of the full inference system rather than of model weights alone. The chronology in Figure 1 places these developments alongside the components that determine system performance: checkpoint, interface, controller or reducer, evaluator, stopping rule, and budget.

We formalize test-time scaling as a family of budgeted inference algorithms over the implicit prefix tree of an autoregressive model. For sampled inference, the formalization separates evidence computed for each trace from decisions over a completed pool. It treats causal stopping separately because stopping changes generation cost. Shared-bank comparisons isolate aggregation, whereas end-to-end evaluation measures the full inference system. We report candidate-bank quality with repeated-sampling diagnostics that capture the trade-of between discovering a correct candidate and producing correct candidates consistently. We apply the framework to open-weight reasoning models on benchmarks in broad knowledge, symbolic reasoning, and competition mathematics.

The paper makes four contributions:

• Formalizing test-time scaling. We model test-time scaling as budgeted inference over the implicit prefix tree and distinguish single-trajectory sequential scaling, leaf-level scaling, and prefix-level scaling.

• Establishing evaluation principles for test-time scaling. We treat the base model, prompting, decoder, inference-time evidence, search or aggregation rule, stopping controller, evaluator, and budget as one inference system. We distinguish shared-bank aggregation comparisons from end-toend evaluation and post-hoc selection from causal stopping. The evaluation principles also require compute reporting on the relevant axes and uncertainty estimates matched to the protocol.

• Providing a model-centric view of the open reasoning ecosystem. We organize and compare representative open-weight reasoning models by model-side and interface mechanisms: verified SFT and distillation, reinforcement learning or preference optimization, inference-time control, and parameter-space fusion.

• Releasing a large-scale reasoning-trace resource. We release 1,403,520 sampled attempts across competition mathematics and broad graduate-level knowledge for reasoning-behavior analysis, evaluator training or calibration, and reproducibility studies.

# 2 Formalizing Test-Time Scaling

Test-time scaling comprises a family of budgeted inference algorithms built on a fixed autoregressive model. Repeated sampling with terminal reduction, adaptive single-trajectory deliberation, and search over partial reasoning states allocate additional inference-time computation in diferent ways (Welleck et al., 2024; Snell et al., 2025; Muennighof et al., 2025; Wu et al., 2024). All operate over the implicit prefix tree induced by generation: compute may be spent along one trajectory, across completed leaves, or over internal prefixes before completion. These choices define three structural regimes.

## 2.1 Problem setup and three-regime taxonomy

Let $x \in \mathcal { X }$ be an input prompt and let $p _ { \theta } ( \cdot \mid x )$ be an autoregressive language model. The finite prefixes reachable from x define an implicit rooted tree $\tau ( x ) { \mathrm { ; } }$ we write $z \preceq y$ when prefix z lies on the path to completed generation y, and $\mathcal { L } ( x )$ for the set of terminal leaves (Welleck et al., 2024). A local generation policy π, such as greedy decoding, temperature sampling, or nucleus sampling, induces a proposal distribution $q _ { \pi } ( y \mid x )$ over completed leaves. This proposal may difer from the raw model distribution because decoding can truncate, renormalize, or otherwise transform token probabilities. We treat EOS, a declared length cap, and a causal stop issued by a controller as terminal actions; a stopped output that cannot be parsed remains a terminal leaf with invalid answer $a = \perp$ 1

A completed generation y may contain both intermediate reasoning and a task answer. We write ${ \mathrm { P a r s e } } ( y ) =$ $( r , a )$ , where $r$ is the reasoning trace and a is the extracted answer. When only part of the output can be checked programmatically, we further write $\Psi ( y ) = ( d , s )$ , where d is the deterministically verifiable component and s is the remainder. Depending on the task, d may be the final answer string, an executable program, an action sequence, or any other artifact that admits task-specific checking.

Our object of interest is a family of budgeted inference algorithms $\{ { \mathcal { A } } _ { B } \} _ { B \in B }$ , where $B \subseteq \mathbb { R } _ { \geq 0 }$ is the set of allowed budgets. Each family defines an additive cost function c with a declared unit; resources that are not commensurate are reported separately. Algorithm $\mathcal { A } _ { B }$ may adaptively interleave primitive operations $o _ { t }$ such as token generation, prefix expansion, verifier calls, judge calls, or terminal reduction, subject to $\textstyle \sum _ { t } c ( o _ { t } ) \leq$ $B .$ . Let $\mathcal { O } ( x ) = \mathcal { L } ( x ) \sqcup \mathcal { A } _ { \mathrm { a n s } } ( x )$ be the disjoint union of completed leaves and answer-valued outputs. The algorithm returns $\hat { o } _ { B } ( x ) \in { \cal O } ( x )$ , written ${ \hat { y } } _ { B } ( x )$ or ${ \hat { a } } _ { B } ( x )$ according to its type, and $U _ { x } : \mathcal { O } ( x ) \to \mathbb { R }$ denotes task utility. In reasoning benchmarks $U _ { x }$ is often exact correctness, but the same abstraction also covers graded utilities such as execution score or preference reward.

Task utility is usually observed through evaluation signals. A programmatic verifier $V _ { P } ( x , d ) \in \mathcal { V }$ may return a Boolean decision, a scalar score, a diagnostic object, or a canonicalized answer representation. A learned evaluator $J _ { \phi } ( x , \omega )$ scores either a completed leaf $\omega = y$ or a partial state $\omega = z$ . Unlike programmatic checks, learned evaluators are proxies whose validity depends on their supervision and test-time protocol (Cobbe et al., 2021; Lightman et al., 2024; Zheng et al., 2023; Zhou et al., 2025).

For a task distribution ${ \mathcal { P } } ,$ the associated test-time scaling curve is

$$
G (B) = \mathbb {E} _ {x \sim \mathcal {P}, \xi} \big [ U _ {x} (\hat {o} _ {B} (x; \xi)) \big ],
$$

where $\xi$ denotes the algorithm’s internal randomness. The term scaling refers to how performance varies with budget; it does not imply that performance must be monotone for every method.

We use the following operational taxonomy, illustrated in Figure 2.

Single-trajectory sequential scaling. At every step, there is at most one unfinished active prefix. Additional computation changes how that prefix is extended, revised, or terminated, but never branches into a competing frontier.

Leaf-level scaling. Additional compute produces a bank of completed candidates. Any interaction between candidate trajectories is deferred until after the candidates have completed, via a terminal reducer.

Prefix-level scaling. Additional compute is allocated based on scores for unfinished prefixes. Expansion, pruning, rollout allocation, or termination decisions depend on partial states before completion.

These regimes are not mutually exclusive at the system level: many practical methods are hybrids, most commonly prefix search followed by a leaf-level reducer.

## 2.2 Single-trajectory sequential scaling

A single-trajectory method maintains one active state $z _ { t }$ and remaining budget $b _ { t }$ . At step $t ,$ a controller chooses a meta-action

$$
\nu_ {t} \sim \pi_ {\mathrm{seq}} (\cdot | x, z _ {t}, b _ {t}),
$$

then extends only the active path,

$$
z _ {t + 1} \sim \mathrm{Extend} (z _ {t}; \nu_ {t}, p _ {\theta}), \qquad b _ {t + 1} = b _ {t} - c (\nu_ {t}).
$$

![](images/69c3c6e62903c9d09d8fcda8d142a0ba40cfb047e9bfdd0befdbb1d1ea23382b.jpg)

[Image: The image presents three schematic diagrams illustrating different scaling strategies for sequential processes. The left panel, titled 'Single-trajectory sequential scaling,' shows a linear progression from input $x$ to output $\hat{y}$ with an adaptive control variable $\nu_t$ applied along a single path. The middle panel, 'Leaf-level scaling,' depicts a branching tree where an initial state $x$ generates $N$ complete leaves ($y_1$ to $y_4$) that are aggregated via an operator $\mathcal{R}$ to form the final result. The right panel, 'Prefix-level scaling,' visualizes a tree search where multiple incomplete prefixes are retained (orange branches) while others are pruned (red crosses), culminating in a final output $\hat{y}$.]  
Figure 2: Three regimes of test-time scaling over the implicit prefix tree. Left: single-trajectory sequential scaling allocates compute to one evolving response without maintaining a competing frontier. Middle: leaflevel scaling allocates compute to completed root-to-leaf trajectories and reduces them to one output. Right: prefix-level scaling allocates compute to internal prefixes, expanding promising continuations and pruning others before committing to a completed leaf.

Actions include continuing generation, suppressing eos, appending a control string or critique, changing decoding hyperparameters, or stopping. Budget-forcing methods such as s1 fit this template. Inferencetime meta-generation procedures also fit when they maintain one evolving response rather than a branching frontier (Muennighof et al., 2025; Welleck et al., 2024).

This regime has low orchestration overhead because all extra compute goes to one candidate. Without a competing unfinished prefix, however, recovery from an early misconception requires self-revision along the same path rather than a search over alternatives.

## 2.3 Leaf-level scaling: sampling and reduction

In leaf-level scaling, additional compute produces completed leaves and a terminal reducer chooses the output. Write $[ N ] = \{ 1 , \dots , N \}$ . In the canonical case,

$$
\mathcal {Y} _ {N} (x) = \{Y _ {i} \} _ {i = 1} ^ {N}, \qquad Y _ {i} \stackrel {\mathrm{i.i.d.}} {\sim} q _ {\pi} (\cdot | x),
$$

where $q _ { \pi }$ is a common proposal distribution induced by the base model and decoding policy. Appendix B extends this template to weighted and heterogeneous-proposal banks. For each candidate, let $m _ { i }$ contain signals available at inference time, and define

$$
(r _ {i}, a _ {i}) = \operatorname{Parse} (Y _ {i}), \qquad (d _ {i}, s _ {i}) = \Psi (Y _ {i}), \qquad v _ {i} = V _ {P} (x, d _ {i}), \qquad j _ {i} = J _ {\phi} (x, Y _ {i}).
$$

Given the proposal, the terminal stage is specified by a reducer

$$
\mathcal {R} _ {N}: \left(x, \{(Y _ {i}, m _ {i}, v _ {i}, j _ {i}) \} _ {i = 1} ^ {N}\right) \mapsto \hat {y} \text {or} \hat {a}.
$$

The fixed-bank leaf template separates generation from reduction. Scores assigned to one unfinished candidate cannot afect another; cross-candidate interaction begins inside $\mathcal { R } _ { N }$ after all N leaves are complete. Adaptive stopping preserves this separation between unfinished candidates. A controller may use completed leaves to decide whether to launch another independent rollout, or it may truncate a rollout using only that rollout’s prefix-local evidence. It does not reallocate compute among competing unfinished prefixes (Section 3.3). Such controllers change the realized sample count or trace length and are not fixed-bank reducers.

### 2.3.1 Canonical reduction rules

Verifier-constrained selection. Let ${ \mathcal { T } } _ { \mathrm { p a s s } } = \{ i : V _ { P } ( x , d _ { i } ) \in { \mathrm { P A S S } } \}$ . A verifier-constrained reducer selects

$$
i ^ {\star} \in \arg \max _ {i \in \mathcal {I} _ {\mathrm{pass}}} T (x, Y _ {i}, v _ {i}, j _ {i}),
$$

where $T$ ranks the passing candidates using, for example, the learned score $j _ { i }$ or sequence likelihood. The reducer uses a declared fallback if ${ \mathcal { T } } _ { \mathrm { p a s s } }$ is empty. This is the generate-test-select pattern used in programsynthesis and verifier-based reasoning systems (Li et al., 2022; Cobbe et al., 2021).

For answer-valued tasks, define the eligible set ${ \mathcal { T } } _ { \mathrm { v a l i d } } = \{ i \in [ N ] : a _ { i } \neq \bot \}$ . For tasks without an invalidanswer state, take ${ \mathcal { I } } _ { \mathrm { v a l i d } } = [ N ]$ . Every reducer must declare a deterministic tie rule and a fallback outpu for ${ \mathcal { T } } _ { \mathrm { v a l i d } } = \emptyset$

Answer marginalization and self-consistency. When answers or verifier outputs can be canonicalized and $\mathcal { T } _ { \mathrm { v a l i d } } \neq \emptyset$ , define the empirical answer distribution over eligible candidates

$$
\hat {q} _ {N} (a \mid x) = \frac {1}{| \mathcal {I} _ {\mathrm{valid}} |} \sum_ {i \in \mathcal {I} _ {\mathrm{valid}}} \mathbf {1} [ a _ {i} = a ], \quad a \neq \bot .
$$

Self-consistency selects

$$
\hat {a} \in \arg \max _ {a \neq \bot} \hat {q} _ {N} (a \mid x).
$$

Appendix B shows that this is exactly empirical MBR with agreement utility $u ( a , a ^ { \prime } ) = \mathbf { 1 } [ a = a ^ { \prime } ]$ (Wang et al., 2023; Kumar & Byrne, 2004; Bertsch et al., 2023).

Learned reranking (Best-of-N). When programmatic verification is unavailable or incomplete, a standard reducer chooses among eligible candidates

$$
i ^ {\star} \in \arg \max _ {i \in \mathcal {I} _ {\mathrm{valid}}} j _ {i}.
$$

This covers learned verifiers, reward models, and LLM judges used as inference-time rerankers (Cobbe et al., 2021; Snell et al., 2025; Huang et al., 2025; Zhou et al., 2025).

Empirical expected-utility selection. More generally, with a projection $\psi$ and utility u, one may select

$$
i ^ {\star} \in \arg \max _ {i \in \mathcal {I} _ {\mathrm{valid}}} \frac {1}{| \mathcal {I} _ {\mathrm{valid}} |} \sum_ {k \in \mathcal {I} _ {\mathrm{valid}}} u (\psi (Y _ {i}), \psi (Y _ {k})).
$$

This MBR template unifies plurality vote, semantic-consensus rules, and neural-metric reranking under a common expected-utility objective (Kumar & Byrne, 2004; Freitag et al., 2022; Bertsch et al., 2023).

These rules cover the main structural forms of leaf-level reduction. Appendix B details weighted aggregation, semantic kernels, pairwise aggregation, regularized selection, and the separation of answer selection from rationale presentation.

### 2.3.2 Failure modes and budget allocation

Increasing the number of samples from a fixed proposal expands candidate coverage without early pruning, but the reducer introduces its own failure modes. An incomplete verifier can admit false positives as N grows, while hard argmax selection can overoptimize a misspecified learned score. This produces the nonmonotone Best-of-N behavior documented in work on reward-model overoptimization and inference-time reward hacking (Gao et al., 2023; Huang et al., 2025; Khalaf et al., 2025). Judge-based reducers also inheri position and verbosity biases, so judge design and prompting are part of the method under evaluation (Zheng et al., 2023; Zhou et al., 2025). Leaf count and evaluator-call count are separate budget axes: MBR-style reducers may require $O ( N ^ { 2 } )$ utility calls, which motivates approximations such as confidence-based pruning and approximate MBR (Cheng & Vlachos, 2023; Jinnai & Ariu, 2024).

A fixed sample count is therefore only one leaf-level design choice. Let $\hat { o } _ { n } ( x )$ denote the output of the declared size-n leaf algorithm. One may instead choose $N = N ( x )$ by solving

$$
N (x) \in \arg \max _ {n: C _ {\mathrm{gen}} (n) + C _ {\mathrm{eval}} (n) \leq B} \mathbb {E} \big [ U _ {x} (\hat {o} _ {n} (x)) \big ],
$$

where $C _ { \mathrm { g e n } }$ denotes generation cost and $C _ { \mathrm { e v a l } }$ covers inference-time scoring, control, and reduction. Recent studies of inference-time scaling optimize budget allocation across strategies (Wu et al., 2024); dificultyadaptive allocation can outperform fixed-N baselines (Snell et al., 2025)

## 2.4 Prefix-level scaling: search over partial states

Prefix-level scaling allocates compute before trajectories are complete. To cover both token-level search and step-level methods such as Tree-of-Thoughts, RAP, and AlphaZero-like decoding, let z denote a search state representing either a literal token prefix or a macro-prefix composed of one or more reasoning steps, and write Succ(z) for its allowed expansions (Yao et al., 2023; Hao et al., 2023; Wan et al., 2024b).

### 2.4.1 Frontier, terminal bank, and budget

A prefix-level method maintains an active frontier $\mathcal { F } _ { t }$ , a bank of completed leaves $\mathcal { \partial } _ { t }$ , and remaining budget $b _ { t }$ . A generic iteration is

$$
z _ {t} \in \operatorname{Select} (\mathcal {F} _ {t}) \to \mathcal {C} _ {t} \subseteq \operatorname{Succ} (z _ {t}) \to \text { score } \mathcal {C} _ {t} \to (\mathcal {F} _ {t + 1}, \mathcal {Y} _ {t + 1}, b _ {t + 1}).
$$

The budget may count generated tokens, node expansions, rollout calls, verifier or judge calls, or wall-clock cost. Unlike leaf-level scaling, prefix-level search uses evaluations of unfinished states to allocate compute among competing prefixes.

### 2.4.2 Prefix evaluation as continuation-value estimation

When a search commits to a single prefix and returns one completion drawn from it, the Bayes-optimal prefix score is the continuation value

$$
Q _ {\rho} ^ {\star} (z) = \mathbb {E} _ {Y \sim q _ {\rho} (\cdot | x, z)} \left[ U _ {x} (Y) \right],
$$

where $q _ { \rho } ( \cdot \mid x , z )$ denotes the distribution over completed leaves obtained by continuing from prefix z with rollout policy $\rho .$ . If search instead accumulates a bank that is later passed to a reducer R, the exact marginal value of expanding z becomes history-dependent because it depends on how future leaves from z will interact with the leaves already collected. One-leaf surrogates such as correctness probability, process reward, or rollout return ignore this coupling.

### 2.4.3 Canonical prefix evaluators

Likelihood-based scoring. A canonical heuristic is cumulative log-probability under the local generation policy:

$$
S _ {\mathrm{LL}} (z) = \sum_ {j = 1} ^ {| z |} \log \pi (z _ {j} \mid x, z _ {<   j}).
$$

Implementations sometimes modify this score with a length penalty. With $\pi = p _ { \theta }$ , the unnormalized form is the standard beam-search score and ranks prefixes by proposal probability. Length-penalized variants need not preserve that ranking. Neither form directly measures downstream utility.

Outcome-supervised value models. Outcome-supervised value models approximate the probability that a prefix reaches a correct completion and use that estimate for pruning, either directly or in combination with likelihood:

$$
\widehat {Q} (z) \approx \operatorname * {P r} _ {Y \sim q _ {\rho} (\cdot | x, z)} \bigl (U _ {x} (Y) = 1 \bigr), \qquad S (z) = \widehat {Q} (z) \mathrm{or} S (z) = \alpha S _ {\mathrm{LL}} (z) + \beta \widehat {Q} (z).
$$

Such value-guided decoding is explored for mathematical reasoning in OVM-style systems (Yu et al., 2024).

Process reward models (PRM). When supervision is available on intermediate reasoning steps, a process reward model can score a partial path directly. $\mathrm { I f } \ z = ( s _ { 1 } , \ldots , s _ { t } )$ is a sequence of steps, one may use

$$
S _ {\mathrm{PRM}} (z) = \sum_ {k = 1} ^ {t} R _ {\phi} (x, s _ {\leq k}) \qquad \text {or} \qquad S _ {\mathrm{PRM}} (z) = R _ {\phi} (x, z),
$$

where $R _ { \phi }$ scores each step in the context of the problem and the preceding steps and is learned from step-level supervision (Lightman et al., 2024).

Rollout-based evaluation. When learned value estimates are unreliable, continuation value can be estimated by Monte Carlo completion:

$$
\widehat {Q} _ {\mathrm{MC}} (z) = \frac {1}{M _ {\mathrm{roll}}} \sum_ {m = 1} ^ {M _ {\mathrm{roll}}} U _ {x} \Bigl (Y ^ {(m)} \Bigr), \qquad Y ^ {(m)} \sim q _ {\rho} (\cdot | x, z).
$$

MCTS-style reasoning methods can be interpreted as structured rollout allocation together with backup of these estimates (Hao et al., 2023; Wan et al., 2024b).

Sound partial checks. A partial check $H ( x , z ) \in \{ 0 , 1 \}$ is sound for rejection if

$$
H (x, z) = 0 \implies U _ {x} (y) = 0 \quad \text { for   all } y \succeq z.
$$

Only sound prefix tests justify safe pruning. Learned value or reward models generally do not provide this guarantee.

### 2.4.4 Score-induced search procedures

Beam search. Beam search keeps a frontier of size K and updates it by

$$
\mathcal {F} _ {t + 1} = \operatorname{TopK} \Bigl (\bigcup_ {z \in \mathcal {F} _ {t}} \operatorname{Succ} (z); S (\cdot) \Bigr).
$$

Standard beam search uses $S = S _ { \mathrm { L L } }$ , while verifier-guided and value-guided variants replace or augment likelihood with learned prefix scores (Yu et al., 2024).

Best-first search. Best-first search repeatedly expands the highest-scoring active prefix,

$$
z ^ {\star} \in \arg \max _ {z \in \mathcal {F} _ {t}} S (z), \qquad \mathcal {F} _ {t + 1} = (\mathcal {F} _ {t} \setminus \{z ^ {\star} \}) \cup \operatorname{Succ} (z ^ {\star}).
$$

In classical search, admissible heuristics can yield optimality guarantees. In LLM-agent search, learned model-based value functions can be used heuristically; Koh et al. provide a best-first example (Koh et al., 2025).

MCTS-style search. Monte Carlo tree search alternates selection, expansion, evaluation, and backup. A standard UCT rule selects

$$
a _ {t} \in \arg \max _ {a} \left(Q (z, a) + c _ {\mathrm{uct}} \sqrt {\frac {\log n (z)}{n (z , a)}}\right),
$$

where $n ( z )$ and $n ( z , a )$ are visit counts and unvisited actions are selected first. Policy-prior variants such as PUCT replace the pure UCT bonus with one modulated by an action prior. In LLM reasoning, RAP, AlphaZero-like search, and related methods instantiate this template with rollout-based or learned value estimates (Kocsis & Szepesvári, 2006; Browne et al., 2012; Hao et al., 2023; Wan et al., 2024b). Tree-of-Thoughts can be viewed as a related search controller operating over thought-level rather than token-leve expansions (Yao et al., 2023).

Additional controller variants, including learned search policies and reward-guided objectives, are discussed in Appendix C.

### 2.4.5 Scaling behavior and comparison to leaf-level methods

Prefix-level search can use compute more eficiently than unguided leaf sampling when prefix scores concentrate budget on high-value branches. Its risk is that pruning changes the support of reachable completions. If every ancestor of a correct leaf is pruned, no later computation can recover that leaf. For pruning, the within-instance ordering of competing frontier states often matters more than global calibration.

Under a fixed budget B, prefix search induces an efective proposal distribution over completed leaves,

$$
q _ {\mathrm{search}, B} (y \mid x) = \operatorname * {P r} \bigl (\hat {y} _ {B} (x) = y \bigr),
$$

which depends jointly on the scorer, controller, and stopping rule. When search returns an ordered bank or multiset Y rather than one leaf, its corresponding object is the joint law $Q _ { \mathrm { s e a r c h } , B } ( \mathcal { V } \mid x ) ;$ per-leaf inclusion probabilities are only marginals and do not determine bank size, multiplicity, order, or dependence. Candidate banks returned by prefix search are therefore not i.i.d. draws from $q _ { \pi } ( \cdot \mid x )$ , so direct comparisons to leaf-level Best-of-N must account for generation, evaluation, control, and decision costs.

Prefix search creates branching structures with shared prefixes. Tree-structured inference kernels can reuse key-value caches across these prefixes and thereby change the compute frontier; DEFT is one example (Yao et al., 2025a). A hybrid system can first construct a search-induced bank of completed leaves and then apply a leaf-level reducer. Such banks can be summarized by the repeated-sampling metrics in Section 3.4.

