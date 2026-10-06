# A Notation

The formalization (Section 2), evaluation framework (Section 3), and leaf- and prefix-level variants in $\mathrm { A p - }$ pendices B and C use a common notation.

## Core objects and budgeted inference.

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td> $x \in \mathcal{X}$ </td><td>Input prompt or problem instance.</td></tr><tr><td> $p_{\theta}(\cdot \mid x)$ </td><td>Base autoregressive language model.</td></tr><tr><td> $\mathcal{T}(x)$ </td><td>Implicit rooted prefix tree induced by generation from  $x$ .</td></tr><tr><td> $\mathcal{L}(x)$ </td><td>Terminal leaves of  $\mathcal{T}(x)$ , i.e., completed generations.</td></tr><tr><td> $z \preceq y$ </td><td>Prefix relation: search state or prefix  $z$  lies on the path to completed leaf  $y$ .</td></tr><tr><td> $\pi$ </td><td>Local generation policy or decoder used to extend a trajectory.</td></tr><tr><td> $q_{\pi}(y \mid x)$ </td><td>Proposal distribution over completed leaves induced by  $p_{\theta}$  together with policy  $\pi$ .</td></tr><tr><td> $\mathcal{A}_{B}$ </td><td>Budgeted test-time algorithm with total cost at most  $B$ .</td></tr><tr><td> $\mathcal{B}$ </td><td>Declared set of allowed nonnegative budgets.</td></tr><tr><td> $o_{t}, c(o_{t})$ </td><td>Primitive operation at step  $t$  and its associated cost.</td></tr><tr><td> $B, b_{t}$ </td><td>Total test-time budget and remaining budget at step  $t$ .</td></tr><tr><td> $\mathcal{O}(x)$ </td><td>Disjoint union of completed-leaf and answer-valued output spaces.</td></tr><tr><td> $U_{x}(o)$ </td><td>Task utility of output  $o \in \mathcal{O}(x)$  on instance  $x$ .</td></tr><tr><td> $\hat{o}_{B}(x)$ </td><td>Unified output returned by  $\mathcal{A}_{B}$ ; written  $\hat{y}_{B}(x)$  or  $\hat{a}_{B}(x)$  according to its type.</td></tr><tr><td> $\xi$ </td><td>Internal (algorithmic) randomness of  $\mathcal{A}_{B}$ ;  $\xi_{q}$  is its realization on prompt  $x_{q}$ .</td></tr><tr><td> $G(B)$ </td><td>Test-time scaling curve  $\mathbb{E}_{x \sim \mathcal{P}, \xi} [U_{x}(\hat{o}_{B}(x; \xi))]$ .</td></tr><tr><td> $\pi_{\text{seq}}, \nu_{t}$ </td><td>Single-trajectory controller and its meta-action at step  $t$  (distinct from the correct-candidate count  $\nu_{q}$ ).</td></tr></table>

## Output interpretation and evaluation signals.

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td> $Parse(y) = (r, a)$ </td><td>Deterministic parser that extracts reasoning trace  $r$  and answer  $a$  from completed generation  $y$ .</td></tr><tr><td> $\Psi(y) = (d, s)$ </td><td>Decomposition of  $y$  into a deterministically verifiable component  $d$  and a non-verifiable remainder  $s$ .</td></tr><tr><td> $V_P(x, d)$ </td><td>Programmatic verifier applied to instance  $x$  and verifiable artifact  $d$ .</td></tr><tr><td> $\mathcal{V}$ </td><td>Codomain of verifier outputs, which may be Boolean, graded, diagnostic, or canonicalized.</td></tr><tr><td>PASS</td><td>Subset of verifier outputs treated as acceptable by a reducer.</td></tr><tr><td> $J_\phi(x, \omega)$ </td><td>Learned evaluator on object  $\omega$ , where  $\omega$  may be a completed leaf  $y$  or a partial state  $z$ .</td></tr></table>

## Decoding protocols and induced proposals.

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td> $\Sigma$ </td><td>Token vocabulary.</td></tr><tr><td> $h_t, \ell_t, p_t$ </td><td>Partial generation  $(x, y_{<t})$ , its logits, and the softmax token probabilities.</td></tr><tr><td> $D_\lambda, \sigma_t, \chi_t$ </td><td>One-token decoder with configuration  $\lambda$ , its finite state, and side information.</td></tr><tr><td> $u_t, S_t$ </td><td>Nonnegative token measure and retained support of the energy-gate decoder (distinct from the MBR utility  $u(\cdot,\cdot)$  and the prefix score  $S(z)$ ).</td></tr><tr><td> $\widetilde{q}_t$ </td><td>One-token proposal  $\text{Norm}_{S_t}(u_t)$ .</td></tr><tr><td> $q_\lambda(y \mid x)$ </td><td>Sequence-level proposal induced by composing the local kernels; written  $q_\pi$  when the protocol is denoted  $\pi$ .</td></tr></table>

Evaluation under test-time scaling.

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td> $\mathcal{P}$ </td><td>Task distribution over problem instances.</td></tr><tr><td> $\mathcal{D}_{\text{eval}} = \{x_q\}_{q=1}^Q$ </td><td>Evaluation set with  $Q$  prompts or problem instances.</td></tr><tr><td> $M_B, \widehat{M}_B$ </td><td>Population and empirical end-to-end performance of algorithm  $\mathcal{A}_B$  under budget  $B$ .</td></tr><tr><td> $Z_{q,i}$ </td><td>Binary correctness indicator for candidate  $i$  on prompt  $q$  inside a sampled bank.</td></tr><tr><td> $\nu_q$ </td><td>Number of correct candidates in the bank for prompt  $q$ , i.e.,  $\sum_{i=1}^N Z_{q,i}$ .</td></tr><tr><td> $p_q$ </td><td>Latent single-attempt success probability for prompt  $q$  under the fixed proposal.</td></tr><tr><td> $k, t$ </td><td>Attempt budget of a repeated-sampling diagnostic and success-count threshold,  $1 \leq t \leq k$ ; finite-bank versions require  $k \leq N$ .</td></tr><tr><td> $\kappa_{k,t}(p)$ </td><td>Binomial tail kernel  $\Pr\{\text{Binomial}(k,p) \geq t\}$ .</td></tr><tr><td> $S_{k,t}$ </td><td>Discovery-stability profile coordinate: expected fraction of prompts with at least  $t$  correct candidates among  $k$  fresh attempts.</td></tr><tr><td> $\widehat{S}_{k,t}^{\text{bank}}$ </td><td>Finite-bank (without-replacement) estimate of the same threshold event computed from an  $N$ -candidate bank.</td></tr><tr><td> $\mathcal{H}_n, \mathcal{F}_{i,t}$ </td><td>Information available after  $n$  completed rollouts and through token  $t$  of rollout  $i$ , respectively.</td></tr><tr><td> $\tau_{\text{roll}}, \tau_{\text{tok}}$ </td><td>Across-rollout and within-rollout stopping times.</td></tr></table>

Leaf-level scaling.

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td>N</td><td>Number of completed candidates in a leaf bank.</td></tr><tr><td>[N]</td><td>Candidate-index set {1,...,N}.</td></tr><tr><td> $\mathcal{Y}_N(x) = \{Y_i\}_{i=1}^N$ </td><td>Multiset of completed candidates generated for input x.</td></tr><tr><td> $Y_i$ </td><td>ith completed candidate (leaf).</td></tr><tr><td> $a_i, m_i$ </td><td>Canonical answer parsed from  $Y_i$  and its inference-time signals;  $a_i = \perp$  denotes an invalid candidate when applicable.</td></tr><tr><td> $\mathcal{I}_{valid}$ </td><td>Indices of reducer-eligible candidates, excluding  $a_i = \perp$  for answer-valued tasks.</td></tr><tr><td> $v_i, j_i$ </td><td>Verifier output  $V_P(x, d_i)$  and learned score  $J_\phi(x, Y_i)$  for candidate  $Y_i$ .</td></tr><tr><td> $E_\eta, \mathcal{E}, e_i$ </td><td>Evidence map, evidence space, and candidate evidence object  $e_i = E_\eta(x, Y_i, m_i)$ ;  $e_i$  is scalar for score-based rules.</td></tr><tr><td> $\mathbf{W}_n$ </td><td>Pairwise utility matrix over the first n completed candidates.</td></tr><tr><td> $\mathcal{G}_\delta, \hat{o}_n$ </td><td>Fixed-bank decision rule and its returned leaf, answer, or output set.</td></tr><tr><td> $\mathcal{R}_N$ </td><td>Leaf-level reducer that maps a candidate bank to a final leaf or answer.</td></tr><tr><td> $T(x, Y_i, v_i, j_i)$ </td><td>Tie-breaking score used by verifier-constrained selection.</td></tr><tr><td> $i^*$ </td><td>Index of the selected candidate when the reducer returns one sampled leaf.</td></tr><tr><td> $\hat{q}_N(a \mid x)$ </td><td>Empirical answer distribution induced by the leaf bank.</td></tr><tr><td> $\psi(\cdot)$ </td><td>Deterministic projection of a leaf used inside an MBR objective.</td></tr><tr><td> $u(\cdot, \cdot)$ </td><td>Utility or similarity function used by an MBR-style reducer.</td></tr><tr><td> $C_{\text{gen}}(n), C_{\text{eval}}(n)$ </td><td>Generation cost and inference-time scoring, control, and reduction cost for a bank of size n.</td></tr><tr><td> $C_{\text{signal}}, C_{\text{control}}, C_{\text{decision}}, C_{\text{total}}$ </td><td>Evidence-acquisition, controller, decision, and total protocol cost.</td></tr></table>

Prefix-level scaling.

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td>z</td><td>Search state: a literal token prefix or a macro-prefix consisting of one or more reasoning steps.</td></tr><tr><td>Succ(z)</td><td>Allowed successor states obtained by expanding prefix z.</td></tr><tr><td> $\mathcal{F}_{t}$ </td><td>Active frontier of unfinished search states at step t.</td></tr><tr><td> $\mathcal{Y}_{t}$ </td><td>Bank of completed leaves accumulated by a prefix search up to step t.</td></tr><tr><td>ρ</td><td>Rollout policy used to continue a prefix to completion.</td></tr><tr><td> $q_{\rho}(\cdot | x, z)$ </td><td>Distribution over completed leaves obtained by continuing from prefix z with rollout policy ρ.</td></tr><tr><td> $Q_{\rho}^{\star}(z)$ </td><td>Continuation value of prefix z under rollout policy ρ.</td></tr><tr><td> $\widehat{Q}(z)$ </td><td>Approximate continuation-value estimate used for pruning or prioritization.</td></tr><tr><td> $S(z)$ </td><td>Generic prefix score used by the search controller.</td></tr><tr><td> $S_{\text{LL}}(z)$ </td><td>Likelihood-based prefix score.</td></tr><tr><td> $R_{\phi}, S_{\text{PRM}}(z)$ </td><td>Process reward model (step-level scorer) and the prefix score it induces.</td></tr><tr><td> $H(x, z)$ </td><td>Partial check; sound for rejection when  $H(x, z) = 0$  implies  $U_x(y) = 0$  for all y ≥ z.</td></tr><tr><td> $\pi_{\text{ctrl}}, a_t$ </td><td>Search controller and its meta-action (expand, generate successors, allocate rollouts, prune, terminate).</td></tr><tr><td> $\widehat{Q}_{\text{MC}}(z)$ </td><td>Monte Carlo estimate of continuation value using  $M_{\text{roll}}$  rollouts from prefix z.</td></tr><tr><td>K</td><td>Beam width in beam search.</td></tr><tr><td> $M_{\text{roll}}$ </td><td>Number of rollouts used when estimating  $\widehat{Q}_{\text{MC}}(z)$ .</td></tr><tr><td> $n(z), n(z, a)$ </td><td>Visit counts for state z and action a in an MCTS-style search tree.</td></tr><tr><td> $q_{\text{search},B}(y | x)$ </td><td>Effective leaf distribution induced by a prefix-level search algorithm under budget B.</td></tr><tr><td> $Q_{\text{search},B}(\mathcal{Y} | x)$ </td><td>Joint law of an ordered bank or multiset returned by prefix search.</td></tr></table>

# B Leaf-level reduction: additional derivations and variants

Under the leaf-level formalism of Section 2.3, self-consistency is an empirical MBR rule, and weighted candidate banks use the same template. Answer selection and rationale presentation remain separate decisions.

## B.1 Self-consistency as empirical MBR

Let $\psi ( y )$ be the extracted answer, i.e., $\psi ( y ) = a$ with $( r , a ) = \mathrm { P a r s e } ( y )$ , let ${ \mathcal { T } } _ { \mathrm { v a l i d } } = \{ i \in [ N ] : a _ { i } \neq \perp \}$ , and suppose this set is nonempty. With $u ( a , a ^ { \prime } ) = \mathbf { 1 } [ a = a ^ { \prime } ]$ , the empirical MBR objective over the eligible leaves of $\mathcal { Y } _ { N } ( x ) = \{ Y _ { i } \} _ { i = 1 } ^ { N }$ is

$$
\widehat {R} _ {N} (i) = \frac {1}{| \mathcal {I} _ {\mathrm{valid}} |} \sum_ {k \in \mathcal {I} _ {\mathrm{valid}}} u (a _ {i}, a _ {k}) = \frac {1}{| \mathcal {I} _ {\mathrm{valid}} |} \sum_ {k \in \mathcal {I} _ {\mathrm{valid}}} \mathbf {1} [ a _ {i} = a _ {k} ] = \hat {q} _ {N} (a _ {i} \mid x).
$$

Therefore,

$$
i ^ {\star} \in \arg \max _ {i \in \mathcal {I} _ {\text {valid}}} \widehat {R} _ {N} (i) \qquad \Longleftrightarrow \qquad \hat {a} \in \arg \max _ {a \neq \bot} \hat {q} _ {N} (a \mid x).
$$

Plurality self-consistency is thus exactly empirical MBR with a zero-one answer-agreement utility (Wang et al., 2023; Kumar & Byrne, 2004). The declared all-invalid fallback and deterministic tie rule from Sec tion 2.3 complete both definitions.

## B.2 Weighted banks and heterogeneous proposals

A weighted variant replaces the uniform empirical distribution by

$$
\hat {q} _ {w} (a \mid x) = \frac {\sum_ {i \in \mathcal {I} _ {\mathrm{valid}}} w _ {i} \mathbf {1} [ a _ {i} = a ]}{\sum_ {i \in \mathcal {I} _ {\mathrm{valid}}} w _ {i}}, \qquad w _ {i} \geq 0, \quad \sum_ {i \in \mathcal {I} _ {\mathrm{valid}}} w _ {i} > 0.
$$

The corresponding weighted MBR objective is

$$
\widehat {R} _ {w} (i) = \sum_ {k \in \mathcal {I} _ {\mathrm{valid}}} \bar {w} _ {k} \left. u (\psi (Y _ {i}), \psi (Y _ {k})\right), \qquad \bar {w} _ {k} = \frac {w _ {k}}{\sum_ {j \in \mathcal {I} _ {\mathrm{valid}}} w _ {j}}.
$$

The weighting scheme applies to confidence-weighted consensus and to banks built from heterogeneous proposal distributions. If candidate $Y _ { i }$ is drawn from proposal $q _ { i } ( \cdot \mid x )$ but the desired risk is defined under target proposal $q _ { \star } ( \cdot \mid x )$ , assume $q _ { \star } ( \cdot \mid x )$ is absolutely continuous with respect to every contributing $q _ { i } ( \cdot \mid x )$ Then importance weights

$$
w _ {i} \propto \frac {q _ {\star} (Y _ {i} \mid x)}{q _ {i} (Y _ {i} \mid x)}
$$

define a self-normalized importance estimator when the probability ratios are available. If truncated decoding or adaptive search prevents their evaluation, replacement weights are heuristic rather than an exact correction.

## B.3 Beyond exact-match consensus

Open-ended outputs may not admit a canonical exact-match representation. A reducer can instead use a utility or similarity kernel over projected candidates,

$$
s _ {i} = \sum_ {\ell = 1} ^ {N} u (\psi (Y _ {i}), \psi (Y _ {\ell}))  , \qquad i ^ {\star} \in \arg \max _ {i} s _ {i}.
$$

Neural MBR instantiates this template with learned reference-based metrics (Freitag et al., 2022), while Universal Self-Consistency uses an LLM-mediated notion of consistency to extend self-consistency beyond exact answer extraction (Chen et al., 2023).

## B.4 Proxy misspecification and regularized selection

When a reducer scores candidates using an imperfect proxy $j _ { i }$ , hard argmax selection can overoptimize proxy error as the bank grows (Gao et al., 2023). One stochastic alternative replaces hard argmax selection with

$$
\operatorname * {P r} (\hat {y} = Y _ {i} \mid x, \mathcal {Y} _ {N}) \propto \exp (\alpha j _ {i}), \quad \alpha \geq 0,
$$

which is uniform at $\alpha = 0$ and converges as $\alpha  \infty$ to uniform selection over the tied maximum-score candidates. More generally, one can combine a proxy score with Bayes-risk regularization (Jinnai et al., 2025), or soften the hard argmax into stochastic selection (Verdun et al., 2025), so that selection is not determined by the single largest proxy score alone. Because the reducer is part of the inference system being evaluated, changing the strength or regularization of selection changes the object under comparison.

## B.5 Answer selection versus rationale presentation

When benchmark utility depends only on the final answer, answer selection and rationale presentation are distinct decisions:

$$
\hat {a} \in \arg \max _ {a \neq \bot} \hat {q} _ {N} (a \mid x), \qquad i ^ {\star} \in \arg \max _ {i: a _ {i} = \hat {a}} \tilde {T} (x, Y _ {i}).
$$

The first rule selects the returned answer. Conditional on that answer, the second uses a rationale-quality score $\tilde { T }$ (for example, the learned score $j _ { i } )$ to choose a sampled rationale for presentation. Both argmax operations use the protocol’s fixed tie rule; the all-invalid case uses its declared fallback. Keeping these decisions separate prevents silent reversion to full-string MAP selection. In neural machine translation, for example, MAP decoding can be a poor output-quality rule (Eikema & Aziz, 2020).

# C Prefix-level search: controller and evaluator variants

Prefix search allocates computation using scores on unfinished states. Its evaluator and controller are separate design choices; together, they determine the proposal distribution over leaves. A completed-leaf count also omits computation spent on prefix scoring and tree maintenance.

## C.1 Evaluator–controller factorization

A prefix-level search procedure can be written as a pair $( S , \pi _ { \mathrm { c t r l } } )$ , where $S$ maps a partial state to a score or summary statistic and $\pi _ { \mathrm { c t r l } }$ uses those summaries to choose meta-actions,

$$
a _ {t} \sim \pi_ {\mathrm{ctrl}} (\cdot | x, \mathcal {F} _ {t}, \mathcal {Y} _ {t}, b _ {t}).
$$

The action $a _ { t }$ may specify which node to expand, how many successors to generate, how many rollouts to allocate, which states to prune, or when to terminate. Classical MCTS-style procedures (Kocsis & Szepesvári, 2006; Browne et al., 2012), Tree-of-Thoughts-style search (Yao et al., 2023), and RAP (Hao et al., 2023) all instantiate this evaluator–controller pattern with diferent scorers and control rules; beam and best-first search fit the same factorization. A factorial ablation over S and $\pi _ { \mathrm { c t r l } }$ can separate gains due to local evaluation, compute allocation, and their interaction.

## C.2 Search-induced proposal shift

Any controller together with its scorer and stopping rule induces an efective leaf distribution

$$
q _ {\mathrm{search}, B} (y \mid x) = \operatorname * {P r} \bigl (\hat {y} _ {B} (x) = y \bigr),
$$

which generally difers from the decoder-induced proposal $q _ { \pi } ( y \mid x )$ . When search returns an ordered bank or multiset ${ \mathcal { V } } ,$ the corresponding object is its joint law $Q _ { \mathrm { s e a r c h } , B } ( \mathcal { V } \mid x )$ (Section 2.4); per-leaf inclusion probabilities are only marginals of this law. Prefix search therefore changes both compute allocation and the proposal over leaves. The dependence structure and leaf frequencies of a returned bank reflect the controller’s branch-selection decisions. Threshold metrics such as Pass@k and the profile coordinates $\widehat { S } _ { k , t } ^ { \mathrm { b a n k } }$ (Section 3.4) can still be computed on such banks, but they should be interpreted as descriptive summaries of the search-induced bank unless the experimental protocol explicitly averages over repeated executions of the full search algorithm.

When S is a learned reward or value model, prefix search is susceptible to proxy misspecification in rewardmodel selection (Gao et al., 2023). Reward-guided tree search may prune or replace low-scoring states (Hung et al., 2025). A branch that would yield a high-utility leaf can therefore be eliminated before that leaf is generated. This failure cannot occur in pure leaf-level reranking after the bank has been generated.

## C.3 Compute accounting

Prefix search incurs compute costs for partial-state scoring, rollouts, and tree maintenance, in addition to final generations. Reporting only the number of completed leaves can therefore be misleading: two methods may return the same number of leaves while using very diferent amounts of model computation and evaluator computation. At minimum, empirical comparisons should separate generated-token cost from evaluator cost in a declared additive work unit, and report latency, throughput, peak memory, and noncommensurate calls separately. Comparisons should also report whether the implementation supports shared-prefix execution. Tree-structured kernels can reuse key–value caches across prefixes, changing the wall-clock frontier for search based methods (Yao et al., 2025a).

