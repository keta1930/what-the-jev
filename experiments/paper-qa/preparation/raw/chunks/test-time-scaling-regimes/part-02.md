# 3 Evaluating Test-Time Scaling

Under test-time scaling, reported performance depends on the full inference protocol defined over the prefix tree in Section 2.1. The protocol determines both the candidate distribution and the final output rule. Its specification includes budget allocation, decoding or search, inference-time evidence, aggregation and stopping rules, and any verifier or judge calls. A report should state the benchmark structure, the induced proposal distribution, the aggregation and stopping protocol, the reported estimand, and the uncertainty procedure.

## 3.1 Benchmark design as evaluation structure

Benchmark design determines which capability is measured and whether additional inference-time compute can change outcomes. Under test-time scaling, benchmark suites should be organized by evaluation structure as well as task domain.

One distinction is between verifiable and open-ended tasks. In verifiable settings such as mathematics and code generation, correctness can be checked exactly or by execution, so repeated sampling and terminal reduction target a directly checkable criterion (Chen et al., 2021; Li et al., 2022). In open-ended settings, evaluation relies on rubrics, pairwise preferences, or judge models. Prompts, comparison order, side randomization, and aggregation can change the scores and must be reported with the results (Liang et al., 2023; Zheng et al., 2023; Chiang et al., 2024). Additional compute also afects reducers diferently: verifier-based selection, agreement-based aggregation, and judge-based reranking need not improve at the same rate as the budget increases (Cobbe et al., 2021; Lightman et al., 2024; Zheng et al., 2023).

The benchmark structure should also match the task’s interaction model. Single-turn exact-answer tasks probe discovery of a correct terminal leaf, whereas interactive agent benchmarks evaluate multi-step user/tool interactions and their terminal state (Yao et al., 2025b). Inference-time algorithms may also use environment feedback, backtracking, or iterative refinement during a trajectory (Welleck et al., 2024). The same inference algorithm may score well under “any correct sample” reporting but poorly under trajectory-level reliability metrics (Section 3.4).

Benchmark dificulty should leave room for a scaling curve: if tasks are too easy, additional compute has little efect; if they are uniformly dificult, correct solutions are rarely reached and the curve remains flat (Snell et al., 2025). Because many reasoning benchmarks are small, dataset size limits the statistical resolution of scaling comparisons (Miller, 2024; Ye et al., 2024) (see Section 3.5).

## 3.2 Decoding protocols and induced proposal distributions

Under test-time scaling, the inference system samples from the proposal distribution induced by a complete decoding protocol rather than directly from the raw model distribution $p _ { \theta }$ . Let Σ denote the token vocabulary. At a partial generation $h _ { t } = ( x , y _ { < t } )$ , the model produces logits $\boldsymbol { \ell } _ { t } \in \mathbb { R } ^ { | \Sigma | }$ and token probabilities

$$
p _ {t} (i) = \frac {\exp \ell_ {t} (i)}{\sum_ {j \in \Sigma} \exp \ell_ {t} (j)}, \qquad i \in \Sigma .
$$

A one-token decoder with configuration λ and finite state $\sigma _ { t }$ returns

$$
(\widetilde {q} _ {t}, a _ {t} ^ {\mathrm{tok}}, \sigma_ {t + 1}) = D _ {\lambda} (h _ {t}, \ell_ {t}, p _ {t}, \chi_ {t}, \sigma_ {t}),
$$

where $\chi _ { t }$ denotes side information available to the decoder, such as hidden states, token embeddings, auxiliary scores, rollout estimates, or controller state. If $a _ { t } ^ { \mathrm { t o k } } \neq \perp$ , the next token is set deterministically to $y _ { t } = a _ { t } ^ { \mathrm { t o k } }$ ; otherwise $y _ { t } \sim \mathrm { C a t } ( \widetilde { q } _ { t } )$

A broad class of stochastic decoders admits an energy–gate form (Figure 3). For a nonnegative token measure $u _ { t } : \Sigma \to { \mathbb { R } _ { \geq 0 } }$ and support $S _ { t } \subseteq \Sigma$ with $\begin{array} { r } { \sum _ { j \in S _ { t } } u _ { t } ( j ) > 0 } \end{array}$

$$
\widetilde {q} _ {t} (i) = \operatorname{Norm} _ {S _ {t}} (u _ {t}) _ {i} = \frac {u _ {t} (i) \mathbf {1} \{i \in S _ {t} \}}{\sum_ {j \in S _ {t}} u _ {t} (j)}.\tag{1}
$$

The measure $u _ { t }$ determines relative weights, while the support $S _ { t }$ determines which tokens remain eligible. Ordinary temperature sampling uses $u _ { t } ( i ) = \exp ( \ell _ { t } ( i ) / T )$ and $S _ { t } = \Sigma ;$ ordinary truncation rules restrict $S _ { t }$ and renormalize the same measure; uniform or coverage-based samplers change the weights inside the retained set. Thus support equivalence and distribution equivalence are distinct: two decoders can retain the same candidate set while inducing diferent token probabilities. If a gate retains zero measure, the decoder must invoke a declared fallback before applying Norm; otherwise its token kernel is undefined.

We treat EOS or STOP as an absorbing action and require termination almost surely; a hard length cap or causal truncation maps the current prefix to an explicit terminal outcome. Under these conditions, composing the local kernels gives the leaf-level proposal distribution used in Section 2.3:

$$
q _ {\lambda} (y \mid x) = \prod_ {t = 1} ^ {\tau (y)} K _ {\lambda , t} (y _ {t} \mid x, y _ {<   t}, \sigma_ {t}),\tag{2}
$$

where $\tau ( y )$ denotes the termination step of $y$ (its length in tokens) and $K _ { \lambda , t }$ is a point mass when the decoder takes a deterministic token action and otherwise equals $\widetilde { q } _ { t }$ . When the protocol π fixes a single configuration $\lambda ,$ we write $q _ { \pi } = q _ { \lambda } ;$ if the protocol randomizes over configurations, $q _ { \pi }$ averages $q _ { \lambda }$ over that outer randomness; if a bank uses heterogeneous protocols, then candidate i is drawn from its own proposal $q _ { \pi _ { i } } ( \cdot \mid x )$ rather than from a common i.i.d. proposal.

Support construction captures the common part of many truncation rules. Each gate below takes the live candidate set A and a reference token score $r ,$ typically $p _ { t }$ or a monotone transform of it; under sequential composition, the renormalized $r ^ { ( j ) }$ in Equation (8) plays this role. We use three gate families. A level gate keeps tokens above a data-dependent threshold,

$$
G _ {\mathrm{lev}} (A; r, g, \tau_ {g}) = \{i \in A: g (i; r, \ell_ {t}, \chi_ {t}) \geq \tau_ {g} (r, \ell_ {t}, \chi_ {t}) \}.\tag{3}
$$

This family includes absolute-probability, mode-relative, entropy-scaled, and logit-band thresholds. A headbudget gate sorts the live set $A$ in increasing order of a cost key $\kappa$ (for probability-ranked truncation, $\kappa ( i ) = - r ( i ) )$ ) and retains the first $m _ { \beta }$ tokens permitted by the gate parameter $\beta$ (a fixed rank for top-k; the smallest count whose retained mass reaches the target for cumulative-mass rules),

$$
G _ {\mathrm{head}} (A; r, \kappa , \beta) = \{i _ {(1)}, \ldots , i _ {(m _ {\beta})} \}, \quad \kappa (i _ {(1)}) \leq \dots \leq \kappa (i _ {(| A |)}).\tag{4}
$$

![](images/c617fdc42e172de00eb8c156d5ad16e6d5174e942ef7e67e96353bd30a61175f.jpg)

[Image: The image displays a flowchart illustrating a computational process starting with "Prefix-local inputs" ($h_t, \ell_t, p_t, \chi_t, \sigma_t$). This input branches into two parallel stages: "Measure construction," which yields non-negative values $u_t(i)$, and "Support construction," which defines a subset $S_t \subseteq \Sigma$. These outputs feed into an "Energy-gate interface" block that normalizes the measure over the support, denoted as $\text{Norm}_{S_t}(u_t)$. A dashed line connects this interface to a formula below defining $\tilde{q}_t(i)$ as the normalized measure restricted to $S_t$, which finally leads to a "Token decision" step involving either categorical sampling or an argmax operation.]  
Figure 3: Elementwise view of a one-token sampling protocol. The sequence-level proposal distribution $q _ { \pi } ( \cdot \mid x )$ is induced by composing these local kernels until termination.

This family includes fixed-rank, cumulative-mass, curvature, entropy-budget, and typicality-based truncation. An objective gate chooses a support by solving, or approximating, a set objective,

$$
G _ {\mathrm{obj}} (A; r, J) \in \arg \min _ {\emptyset \neq A ^ {\prime} \subseteq A} J (A ^ {\prime}; r, \chi_ {t}).\tag{5}
$$

This separates the support decision from the weighting rule in Equation (1).

A special case is the family of mode-preserving head gates. Fix a reference distribution $r _ { t }$ whose rank order is the model rank order, for example $p _ { t }$ or a positive-temperature rescaling, and write

$$
r _ {t} (i _ {1}) \geq r _ {t} (i _ {2}) \geq \dots \geq r _ {t} (i _ {| \Sigma |}), \quad K _ {m} = \{i _ {1}, \dots , i _ {m} \}.
$$

If each gate $g$ in a parallel composition H returns a model-ranked prefix $K _ { m _ { g } } ,$ , then the composed support collapses to the strictest retained prefix:

$$
\bigcap_ {g \in \mathcal {H}} K _ {m _ {g}} = K _ {m _ {\cap}}, \qquad m _ {\cap} = \min _ {g \in \mathcal {H}} m _ {g}.\tag{6}
$$

Thus, any parallel combination of top-k (Fan et al., 2018), nucleus (Holtzman et al., 2020), probabilitythreshold (Hewitt et al., 2022), mode-relative, or logit-band head gates has the common form

$$
\widetilde {q} _ {t} ^ {\mathcal {H}} (i) = \frac {u _ {t} (i) \mathbf {1} \{i \in K _ {m _ {\cap}} \}}{\sum_ {j = 1} ^ {m _ {\cap}} u _ {t} (i _ {j})}.\tag{7}
$$

The diferent named rules specify diferent ways of computing $m _ { g } ;$ once their head supports are evaluated in parallel, only the smallest retained prefix remains active.

This collapse does not apply to all decoders. Locally typical sampling can skip high-probability tokens because it orders tokens by the distance of their surprisal $- \log p _ { t } ( i )$ from the conditional entropy of $p _ { t }$ rather than by model probability (Meister et al., 2023); geometry- or objective-based crops can select nonprefix supports; and measure-changing rules can reorder candidates even when the support is fixed. Ordered composition also difers from parallel masking. For probability-only gates, a sequential protocol has the form

$$
A _ {0} = \Sigma , \qquad r ^ {(0)} = p _ {t}, \qquad A _ {j} = G _ {j} (A _ {j - 1}; r ^ {(j - 1)}, \ell_ {t}, \chi_ {t}), \qquad r ^ {(j)} = \mathrm{Norm} _ {A _ {j}} (w ^ {(j)}),\tag{8}
$$

where $w ^ { ( j ) }$ is the measure exposed by the j-th operator. Thus top-p followed by top-k need not match top-k followed by top-p, because cumulative masses, entropies, thresholds, and ranks may be recomputed after renormalization. Temperature before a mass gate can change the support, whereas temperature after a fixed support only changes within-support weights. Each sequential gate must leave positive exposed mass, or apply its declared fallback, before the next normalization.

For evaluation, these distinctions determine the estimand. In leaf-level scaling with a fixed stochastic protocol, the usual candidate bank is

$$
Y _ {1}, \ldots , Y _ {N} \stackrel {\text {i.i.d.}} {\sim} q _ {\pi} (\cdot \mid x).
$$

A deterministic configuration sweep instead returns a reproducible set of design points, not Monte Carlo samples from a single proposal. Prefix-level search induces its own budget-dependent proposal $q _ { \mathrm { s e a r c h } , B } ( \cdot \mid x )$ through the scorer, controller, branching rule, rollout policy, and stopping criterion, and its returned leaves are generally dependent. Accordingly, the repeated-sampling diagnostics of Section 3.4 have an i.i.d. interpretation only when the bank is generated by independent draws from a declared fixed proposal; otherwise they are descriptive summaries of the returned bank.

A sampling report should specify the token measure, support gates, reference score space, gate ordering, deterministic actions or stochastic draws, state updates, stopping and length rules, number of samples, seeds or randomized configuration policy, and any approximation or fallback behavior. These details define the proposal distribution over reasoning traces and the test-time scaling system being evaluated.

## 3.3 Aggregation and stopping under sampled inference

A sampled candidate bank does not by itself define the submitted prediction. The inference protocol must say how evidence is extracted from each trace and how a fixed, completed bank is converted into an output. If either the number or length of rollouts is adaptive, the protocol must also specify when generation stops. Changing the evidence map or decision rule can improve accuracy without reducing generation cost; Figure 4 separates this completed-bank pathway from causal controllers that can avoid later rollouts or truncate the current one.

Evidence and fixed-bank decisions. For completed candidate i, let $m _ { i }$ contain signals available at inference time; the benchmark utility $U _ { x }$ is excluded. Examples include chosen-token log-probabilities, nexttoken distributions, process-reward scores, and verifier or judge outputs. An evidence map produces an evidence object

$$
e _ {i} = E _ {\eta} (x, Y _ {i}, m _ {i}) \in \mathcal {E},
$$

where $\mathcal { E }$ may be scalar or structured and $E _ { \eta }$ includes any reduction over tokens or reasoning steps required by the downstream rule. We use scalar $e _ { i } \in$ R for the score-based rules below. Sequence log-likelihood and mean token log-likelihood (Wang et al., 2023), statistics of next-token distributions (Kang et al., 2025; Fu et al., 2026), reductions of per-step process scores (Lightman et al., 2024), and external verifier or rewardmodel scores (Cobbe et al., 2021) are distinct evidence maps even when passed to the same selector. Pairwise methods may instead construct

$$
[ \mathbf {W} _ {n} ] _ {i j} = u (\psi (Y _ {i}), \psi (Y _ {j})).
$$

A fixed-bank decision rule then returns a leaf, an answer, or a set of outputs,

$$
\hat {o} _ {n} = \mathcal {G} _ {\delta} \big (x, \big ((Y _ {i}, a _ {i}, e _ {i}) \big) _ {i = 1} ^ {n}, \mathbf {W} _ {n} \big).
$$

Together, $E _ { \eta }$ and $\mathcal { G } _ { \delta }$ refine the generic leaf-level reducer $\mathcal { R } _ { N }$ of Section 2.3 into evidence and decision stages. The evidence source and decision rule are separate choices. Scores from one source can be used for reranking, filtering, or vote weighting. Conversely, a voting rule may take model likelihoods as evidence or replace them with self-evaluations or an external verifier.

For answer-valued tasks, write $a _ { i } = \perp$ when parsing or canonicalization declares a candidate invalid, let ${ \mathcal { T } } _ { \mathrm { v a l i d } } = \{ i : a _ { i } \neq \bot \}$ , and let ${ I _ { a } } = \{ i \in \mathbb { Z } _ { \mathrm { v a l i d } } : a _ { i } = a \}$ . Plurality self-consistency<sup>2</sup> scores a group by $\left| I _ { a } \right|$ (Wang et al., 2023). Hard Best-of-N chooses the largest-e candidate in $\mathcal { T } _ { \mathrm { v a l i d } }$ , equivalently scoring each valid answer group by $\operatorname* { m a x } _ { i \in I _ { a } } e _ { i }$ (Cobbe et al., 2021). Score-aware consensus pools evidence within a valid group using raw sums or means, softmax-normalized weights, rank weights, or calibrated log-odds (Taubenfeld et al., 2025; Kang et al., 2025; Kuang et al., 2026). Every rule must declare deterministic tie handling and a fallback submitted output when $\mathcal { T } _ { \mathrm { v a l i d } } = \emptyset$

Other completed-bank reducers combine filtering, resampling, and gated selection. Ofline DeepConf removes low-confidence traces; Majority-of-the-Bests bootstraps Best-of-N decisions and returns their mode;

![](images/fd8b62584d6e31617998f7a4bedf384ea4924051b9ddd43a3a6ea532b5fd1d4a.jpg)

[Image: The diagram displays a flowchart for a generative model's decoding process, beginning with a "Sample stream completed leaves $Y_{1:n}$" that inputs into an "Evidence map $E_\eta$" for computing confidence scores. The workflow proceeds horizontally to a "Fixed-bank decision $\mathcal{G}_\delta$" module, which applies aggregation methods like voting or Maximum Bank Reward (MBR) before generating a "Submitted output $\hat{o}$". Two auxiliary controllers manage the execution via dashed lines: an "Across-rollout controller $\tau_{roll}$" that processes history and future rollouts, and a "Within-rollout controller $\tau_{tok}$" that monitors token prefixes and suffixes.]  
Figure 4: Aggregation and stopping under sampled inference. Evidence extraction and fixed-bank selection operate on completed traces, so they cannot save generation already spent. Causal controllers inspect only revealed history: across-rollout stopping avoids later traces, whereas token-prefix stopping can also truncate the current trace. The evidence map, controller, and final decision are all part of the evaluated protocol.

and Best-of-Majority filters answer groups by frequency before reward-ranking the retained responses for Pass@k (Fu et al., 2026; Rakhsha et al., 2025; Di et al., 2026). When valid candidates exist, MBR selects

$$
i ^ {\star} \in \arg \max _ {i \in \mathcal {I} _ {\mathrm{valid}}} \frac {1}{| \mathcal {I} _ {\mathrm{valid}} |} \sum_ {j \in \mathcal {I} _ {\mathrm{valid}}} [ \mathbf {W} _ {n} ] _ {i j},
$$

with the same all-invalid fallback (Kumar & Byrne, 2004; Freitag et al., 2022; Bertsch et al., 2023). Each method specifies a decision structure while leaving the evidence source separate. If the output contains both a canonical answer and a rationale, the protocol must also specify which trace accompanies the winning answer.

Score semantics are part of the algorithm. Naming the scorer does not fully specify a score-aware reducer. The protocol must state where scores come from, whether larger values are better, and how tokenor step-level scores are reduced. Answer canonicalization and invalid-output handling determine which candidates enter the rule. Score transformations, temperatures, and filtering thresholds determine how evidence enters the decision. The protocol must also define ties and fallbacks, and identify any evaluator prompts or models. Calibration parameters and other tunable values must be fixed on held-out data, not test labels.

Order-only rules such as hard Best-of-N, rank-based filtering, rank voting, and Majority-of-the-Bests are invariant to strictly increasing score transformations that preserve ties. Rules based on raw sums or means, softmax weights, or log-odds are not. Sequence and mean log-probability impose diferent length preferences. Cross-question calibration need not predict a confidence score’s usefulness for within-question aggregation (Taubenfeld et al., 2025); calibrated log-odds may assign negative evidence to low-scoring can didates (Kuang et al., 2026). With hard maximization, exposure to proxy-score errors increases as the bank grows (Gao et al., 2023; Huang et al., 2025).

Causal stopping. Generation cost can fall only when a causal controller stops future work; evidence extraction and fixed-bank selection act after their required traces are complete. Let

$$
\mathcal {H} _ {n} = \sigma (x, (Y _ {i}, a _ {i}, m _ {i}, e _ {i}) _ {i \leq n}, \mathbf {W} _ {n}, \zeta_ {0: n})
$$

be the information available after n completed rollouts, including all revealed evidence, pairwise values, and controller random state $\zeta _ { 0 : n }$ . An across-rollout rule is a bounded stopping time $\tau _ { \mathrm { r o l l } } \le N _ { \mathrm { m a x } }$ satisfying $\left\{ \tau _ { \mathrm { r o l l } } \ \leq \ n \right\} \in \ \mathcal { H } _ { n }$ , and its final decision may use only the bank observed through $\tau _ { \mathrm { r o l l } }$ . In plain terms, whether the procedure has stopped by rollout n may depend on the first n completed rollouts, but not on any later candidate or inference-time signal. Adaptive-Consistency stops when the posterior probability that the current count leader has greater latent mass than its runner-up crosses a threshold, whereas Early Stopping Self-Consistency stops after a valid unanimous answer window (Aggarwal et al., 2023; Li et al.,

2024). The sample cap $N _ { \mathrm { m a x } }$ is separate from the cumulative budget B: before launching or continuing an operation, the controller must establish that its declared worst-case charge keeps total cost at most $B .$ . We assume operations that would overshoot are not launched; a protocol using causal truncation instead must declare that terminal rule. Warm-up, discarded, evaluator, controller, and final-decision work all consume the same declared budget unit.

For rollout $i ,$ let $\mathcal { F } _ { i , t }$ contain the permitted prior history, revealed evaluator/controller state, and the current rollout’s information through token t. A within-rollout stopping time $\tau _ { \mathrm { t o k } }$ satisfies $\{ \tau _ { \mathrm { t o k } } \leq t \} \in \mathcal { F } _ { i , t } \colon$ it cannot use the hidden sufix or eventual answer to decide whether to truncate the current trace. Truncation emits an explicit terminal outcome, which may parse as invalid, rather than treating an unfinished prefix as a completed leaf. DeepConf, for example, uses completed warm-up traces to calibrate a confidence threshold and may terminate later traces when sliding-window token confidence falls below it (Fu et al., 2026). Acrossrollout rules can avoid only later traces, whereas within-rollout rules can also avoid a sufix of the curren trace. Ofline filtering of completed traces may change the returned answer but saves no generation tokens.

Comparison and compute accounting. A shared-bank comparison measures aggregation conditional on one completed bank. Each ofline protocol receives the same candidates and only the inference-time signals it is permitted to use. Holding $E _ { \eta } ,$ , parsing, canonicalization, candidate eligibility, and score transformations fixed isolates ${ \mathcal { G } } _ { \delta } ;$ otherwise, those diferences belong to the compared post-generation protocols. If both evidence and decision components vary, the comparison covers the full post-generation stage $( E _ { \eta } , \mathcal { G } _ { \delta } )$ under a fixed proposal and realized bank. Neither variant can estimate savings from adaptive stopping or changes caused by a diferent generation policy. Generalization beyond the realized bank still requires uncertainty estimates over prompts and candidate draws. An end-to-end comparison instead allows each complete protocol to generate its own stream, acquire its own evidence, execute its stopping rule, and be evaluated by $M _ { B }$

For one declared additive work unit, the matched budget decomposes as

$$
C _ {\mathrm{total}} = C _ {\mathrm{gen}} + C _ {\mathrm{eval}}, \qquad C _ {\mathrm{eval}} = C _ {\mathrm{signal}} + C _ {\mathrm{control}} + C _ {\mathrm{decision}}.
$$

This accounting includes warm-up and discarded tokens, verifier or judge calls, repeated controller evalu ations, and aggregation itself. Equal sample counts need not imply equal compute: external scoring adds candidate-wise cost, and naive pairwise MBR requires $O ( n ^ { 2 } )$ utility evaluations (Cheng & Vlachos, 2023; Jinnai & Ariu, 2024). Latency under parallel or overlapping stages, throughput, peak memory, and other noncommensurate resources are not additive terms in this equation and should be reported separately alongside any scalar work budget. End-to-end utility should be plotted against total cost. Shared-bank results instead identify diferences attributable to the post-generation aggregation stage, and holding evidence fixed narrows attribution to the decision rule. The discovery–stability profile in Section 3.4 remains complementary because it describes candidate availability under the proposal, not the success probability of a particula aggregation protocol.

