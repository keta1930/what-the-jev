## 3.4 Evaluation targets and metrics

Evaluation under test-time scaling should separate the performance of the deployed inference system from the shape of the candidate bank it induces.

End-to-end system performance. Let $\mathcal { P }$ denote the task distribution and ${ \mathcal { D } } _ { \mathrm { e v a l } } = \{ x _ { q } \} _ { q = 1 } ^ { Q }$ the evaluation set. For task utility $U _ { x }$ , budgeted algorithm $\mathcal { A } _ { B }$ , and algorithmic randomness $\xi ,$

$$
M _ {B} = \mathbb {E} _ {x \sim \mathcal {P}, \xi} [ U _ {x} (\hat {o} _ {B} (x; \xi)) ], \qquad \widehat {M} _ {B} = \frac {1}{Q} \sum_ {q = 1} ^ {Q} U _ {x _ {q}} (\hat {o} _ {B} (x _ {q}; \xi_ {q})).
$$

This is the estimand for capability claims: it is the scaling curve $G ( B )$ of Section 2.1, with the algorithmic randomness $\xi$ written explicitly. Pairwise win rates, judge-aggregated rankings, and other relative comparisons define separate estimands; when they are used, the judge prompt, response order, reference material, and aggregation rule are part of the evaluation protocol.

Discovery–stability profile. For repeated-sampling diagnostics, fix the proposal or inference protocol that produces completed candidates. Let $Z _ { q , i } \in \{ 0 , 1 \}$ indicate whether candidate i for prompt q is correct. Under the independent-attempt abstraction, let $p _ { q } = \operatorname* { P r } ( Z _ { q , i } = 1 \mid x _ { q } )$ be the latent single-attempt success probability for prompt q. For k fresh attempts,

$$
X _ {q, k} \mid p _ {q} \sim \operatorname{Binomial} (k, p _ {q}).
$$

For threshold $t \in \{ 1 , \ldots , k \}$ , define the binomial tail kernel

$$
\kappa_ {k, t} (p) = \operatorname * {P r} \{\text { Binomial } (k, p) \geq t \} = \sum_ {j = t} ^ {k} \binom {k} {j} p ^ {j} (1 - p) ^ {k - j}.
$$

The dataset-level discovery–stability profile at budget k is

$$
S _ {k} = (S _ {k, 1}, \dots , S _ {k, k}), \qquad S _ {k, t} = \frac {1}{Q} \sum_ {q = 1} ^ {Q} \kappa_ {k, t} (p _ {q}).
$$

Thus $S _ { k , t }$ is the expected fraction of prompts on which a fresh k-attempt evaluation produces at least t correct candidates. Low thresholds measure discovery, high thresholds measure repeatability, and the full profile records how quickly occasional success decays into stable success.

When an observed bank contains N candidates per prompt and $k \leq N$ , let $\begin{array} { r } { \nu _ { q } = \sum _ { i = 1 } ^ { N } Z _ { q , i } } \end{array}$ . The corresponding finite-bank diagnostic is the without-replacement tail

$$
\widehat {S} _ {k, t} ^ {\text {bank}} = \frac {1}{Q} \sum_ {q = 1} ^ {Q} \sum_ {j = t} ^ {k} \frac {\binom {\nu_ {q}} {j} \binom {N - \nu_ {q}} {k - j}}{\binom {N} {k}},
$$

with invalid binomial coeficients interpreted as zero. This statistic evaluates the threshold event for a size-k subset drawn without replacement from the observed bank, whereas $S _ { k }$ is the prospective latent profile. For banks produced by adaptive search or other dependent procedures, the finite-bank profile remains a descriptive summary of the returned bank; the latent i.i.d. interpretation should be invoked only when it matches the sampling protocol.

A Bayesian report separates finite-bank evidence from the latent profile. With $p _ { q } \sim \mathrm { B e t a } ( \alpha _ { q } ^ { 0 } , \beta _ { q } ^ { 0 } )$ , defaulting to Beta(1, 1) unless an auxiliary prior bank is declared, conjugacy gives

$$
p _ {q} \mid Z _ {q, 1: N} \sim \mathrm{Beta} (a _ {q}, b _ {q}), \qquad a _ {q} = \alpha_ {q} ^ {0} + \nu_ {q}, \quad b _ {q} = \beta_ {q} ^ {0} + N - \nu_ {q}.
$$

The posterior mean of each profile coordinate is the beta-binomial predictive tail

$$
\mu_ {k, t} = \frac {1}{Q} \sum_ {q = 1} ^ {Q} \sum_ {j = t} ^ {k} {\binom {k} {j}} \frac {\mathrm{B} (a _ {q} + j , b _ {q} + k - j)}{\mathrm{B} (a _ {q} , b _ {q})}, \qquad t = 1, \ldots , k,
$$

where $\operatorname { B } ( \cdot , \cdot )$ is the beta function. Shared posterior draws of $p _ { 1 : Q }$ should be used to evaluate all thresholds and all scalar summaries, preserving their posterior dependence.

For rubric-valued outcomes, the same construction replaces the Bernoulli model with a Dirichlet–categorical model, fixes a category score vector in advance, and computes tail probabilities of the normalized k-sample rubric score. The binary exact-match profile above is the two-category case with score vector (0, 1).

Scalar views of the profile. The profile $S _ { k }$ is the primary bank-level object. A scalar metric is a prespecified functional $f ( S _ { k } )$ , not a replacement for the profile. For a linear threshold utility with weights $\omega _ { t , k } \geq 0$ and $\textstyle \sum _ { t = 1 } ^ { k } \omega _ { t , k } = 1$

$$
U _ {\omega} (k) = \sum_ {t = 1} ^ {k} \omega_ {t, k} S _ {k, t}.
$$

Common repeated-sampling metrics are coordinates or simple functionals of the same profile, or are bounded by them:

$$
\mathrm{Pass} @ k = S _ {k, 1}, \qquad \mathrm{pass} ^ {k} = S _ {k, k}, \qquad \mathrm{Maj} @ k \geq S _ {k, \lfloor k / 2 \rfloor + 1} \quad (\mathrm{singlecanonicaltarget}),
$$

$$
\mathrm{G-Pass@} k _ {\tau} = S _ {k, \lceil \tau k \rceil}, \qquad 0 <   \tau \leq 1,
$$

$$
\mathrm{mG-Pass@} k = \frac {1}{k - \lfloor k / 2 \rfloor} \sum_ {t = \lfloor k / 2 \rfloor + 1} ^ {k} S _ {k, t}, \qquad \mathrm{Geom@} k = (S _ {k, 1} S _ {k, k}) ^ {1 / 2},
$$

where the averaged form of mG-Pass@k coincides with the definition of Liu et al. (2025a) for even $k .$ The finite-bank versions are obtained by replacing $S _ { k , t }$ with $\widehat { S } _ { k , t } ^ { \mathrm { b a n k } }$ ; in particular, $\widehat { \mathrm { P a s s } } \ @ k \ : = \ : \widehat { S } _ { k , 1 } ^ { \mathrm { b a n k } }$ . The strict-majority coordinate $S _ { k , \lfloor k / 2 \rfloor + 1 }$ lower-bounds plurality voting: a strict majority of correct candidates guarantees that the correct answer wins the vote, whereas plurality can also succeed with fewer correct candidates when incorrect answers disagree. Ordinary single-sample pass rate is $S _ { 1 , 1 }$ , and for any k the uniform-threshold area recovers the same quantity:

$$
\frac {1}{k} \sum_ {t = 1} ^ {k} S _ {k, t} = \frac {1}{Q} \sum_ {q = 1} ^ {Q} p _ {q}.
$$

These quantities characterize candidate availability under the proposal; they do not give the success probability of an aggregation rule. Selection rules such as self-consistency, verifier reranking, MBR, and judge-based selection must be evaluated end-to-end through $M _ { B }$ . The same applies to adaptive stopping, which changes the realized bank. Under the complete protocol in Section 3.3, $S _ { k }$ remains a complementary diagnostic of the candidate bank and its discovery–stability shape.

## 3.5 Reproducibility

Under test-time scaling, a candidate bank and its submitted output together form one realization of a randomized inference protocol. Exact replay reconstructs the same candidates, inference-time signals, stopping and aggregation decisions, and scores under fixed inputs, random streams, software, and hardware. Distributional reproducibility instead asks whether an independent rerun returns a statistically compatible estimate of the same estimand, such as $M _ { B }$ , the profile $S _ { k }$ , or a judge-defined win rate. A fixed seed can support exact replay, but it does not measure variation over prompts, candidate draws, judge calls, or numerical execution (Bethard, 2022).

Candidate banks are not always independent. Shared prefix-search state, verifier feedback, tool state, or controller decisions can couple candidates; adaptive stopping can also make bank size depend on earlier outcomes. In these cases, the latent i.i.d. interpretation of $S _ { k }$ does not apply, although the finite-bank profile remains descriptive (Section 3.4). A replay record should include the raw candidates, inference-time signals, stopping and aggregation decisions, and a random-stream identifier for each candidate. Deriving each candidate’s random state from the run, prompt, sample index, and stream name prevents asynchronous batching from reassigning random variates across candidates.

Quantifying variability. A distributional reproducibility claim should specify a compatibility criterion and the random sources it covers. A prompt bootstrap over observed candidate banks estimates variation due to prompt composition conditional on those banks; it does not include new candidate draws, judge calls, or numerical execution (Efron, 1979). Claims that average over these sources require independent protocol reruns or a resampling design that includes the corresponding stages (Bouthillier et al., 2021; Blackwell et al., 2024). Each replicate must recompute the reported bank statistic, reducer, or stopping rule rather than resample an already aggregated score. Otherwise, uncertainty can be narrower than rerun variability, and system rankings can change across runs (Miller, 2024; Ye et al., 2024; Hariri et al., 2026b;a).

<table><tr><td>Study block</td><td>Questions</td><td>Banks</td><td>N</td><td>Responses</td><td>Other recorded signals</td></tr><tr><td>MMLU-Pro + BBH</td><td>18,543</td><td>27</td><td>1</td><td>500,661</td><td>Parsed answers</td></tr><tr><td>AIME&#x27;24/&#x27;25, HMMT&#x27;25, and BrUMO&#x27;25</td><td>120</td><td>20</td><td>80</td><td>192,000</td><td>Chosen-token log probability and rank; outcome-verifier score</td></tr><tr><td>AIME&#x27;26, HMMT Nov.&#x27;25/Feb.&#x27;26, CMIMC&#x27;25, and SMT&#x27;25</td><td>186</td><td>7</td><td>80</td><td>104,160</td><td>Top-20 token probabilities; reference-based and reference-free verifiers</td></tr><tr><td>SuperGPQA (subset)</td><td>3,600</td><td>4</td><td>80</td><td>1,152,000</td><td>Top-20 token probabilities and both verifier families</td></tr><tr><td>Total</td><td>22,449</td><td>-</td><td>-</td><td>1,948,821</td><td></td></tr></table>

Table 1: Response-bank inventory. A bank is one model configuration evaluated over a complete question set; N is the number of responses per question in that bank. The signal-rich mathematics row includes three independently generated medium-efort repeats used only for repeated-run diagnostics.

Numerical execution. Precision, kernels, and batching can change a near-tied next-token decision and propagate the diference through a reasoning trace; even greedy decoding may therefore fail to replay exactly (Hochlehnert et al., 2025; Tahmasivand et al., 2025; Yuan et al., 2025). An exact-replay report should specify the inference library and version, numerical formats, quantization, kernels, and batch schedule. A matched FP32 or higher-precision audit using the same prompts and random-stream assignments can estimate sensitivity to numerical format, but does not establish deterministic replay (Yuan et al., 2025).

# 4 Empirical Study and Trace Corpus

Our empirical study uses fixed response banks to measure how quickly additional sampling reveals a correct candidate and how often practical reducers select one. The public release retains the responses, outcomes, and recorded signals for three collections, so new reducers can be evaluated without regenerating those responses. The empirical study has four blocks spanning diferent tasks, model rosters, sampling protocols, and levels of signal detail (Table 1). We therefore report each block separately.

## 4.1 Broad evaluation across knowledge and symbolic reasoning

This block covers 14 MMLU-Pro domains (Wang et al., 2024) and the 23 BIG-Bench Hard tasks (Suzgun et al., 2023). We evaluate 27 open-weight reasoning models with one zero-shot chain-of-thought response per question, yielding 500,661 responses. Across the roster, MMLU-Pro exact match ranges from 3.13% to 70.47%, and BBH flexible-extraction exact match ranges from 25.97% to 82.20%. We report the suites separately because their tasks, answer spaces, and parsers difer.

## 4.2 Candidate discovery outpaces answer selection

This block contains 80 seeded responses for every combination of 20 model configurations and 120 questions from AIME’24, AIME’25, HMMT’25, and BrUMO’25 (Jia, 2024; Zhang & Math-AI, 2025; MathArena, 2025c;a), for 192,000 responses. We compute exact candidate-bank statistics under without-replacement sampling at k ∈ {1, 2, 4, 8, 16, 32, 64, 80}, and replay reducers on nested random subsets of the same banks. Because every reducer sees subsets of the same response banks, diferences among reducers cannot be attributed to newly generated candidates.

Across the roster, the median Pass@k rises from 56.49% at k = 1 to 82.08% at k = 80, whereas the median all-correct coordinate falls to 15.00%. For this roster, mean Spearman agreement with the N = 80 accuracy ranking is 0.967 at k = 1 and 0.992 at k = 8. These values describe the 20 configurations and their sampled banks; they do not establish a general small-sample guarantee.

Qwen3-30B-A3B-Thinking-2507 has the highest single-response accuracy in the roster, at 75.56%. At k = 80, Pass@80 is 91.67% and the finite-bank all-correct coordinate is 43.33% (Figure 5, left). Literal answer plurality reaches 78.33%, and sequence-log-probability selection reaches 77.50%. Accuracy from selecting the response with the highest mean token log probability instead falls from 75.56% to 65.83% as the bank grows (Figure 5, right). For this score, expanding the candidate bank from 1 to 80 therefore lowers submittedanswer accuracy despite raising Pass@k. The reference-assisted CompassVerifier diagnostic reaches 89.17%, 2.50 percentage points below Pass@80, but it has access to the gold answer and is not an inference-time result.

![](images/9ae5d4f191cd7ba883041933a4b54f4743e333f62d1de64f2e1b0910b9718437.jpg)

[Image: This line chart titled "(a) Discovery versus consistency" plots probability on the vertical axis against a "Sample budget k" on the horizontal axis, which scales logarithmically from 1 to 80. Two metrics are compared: "Pass@k (at least one correct)," represented by a blue line, and "All-correct@k," represented by an orange line. The blue "Pass@k" series exhibits a positive trend, rising from an initial probability of approximately 0.57 to over 0.8 as the sample budget increases to 80. Conversely, the orange "All-correct@k" series follows a negative trend, starting at the same initial value near 0.57 but declining to approximately 0.15 by the end of the scale. Both series include shaded confidence intervals that widen as the sample budget increases.]

(b) Agreement with the full-bank ranking  
![](images/25b1330ae9f379ad9ad498e582c1688c9423c8974226c1969984ceb3eb5e07f7.jpg)

[Image: This line chart displays the mean agreement of subset rankings with a full N=80 ranking against the sample budget $k$. The x-axis shows $k$ values ranging from 1 to 80 in powers of two, while the y-axis indicates agreement levels between 0.6 and 1.0. The purple line representing Spearman $\rho$ remains consistently high, starting near 0.97 and quickly plateauing near 1.0, whereas the teal line for Top-5 overlap shows a sharp increase from roughly 0.85 to 1.0 as $k$ increases from 1 to 8. Shaded regions surrounding each curve denote the central 95% ranges derived from repeated replays.]

![](images/4a45ad419c0da4afa5b7533c1f376d98cb1fa0e56b9cc33edd0684dc96c9a31c.jpg)

[Image: This line chart, titled "(c) Reducers on the strongest one-sample configuration," plots Accuracy or discovery probability on the y-axis against the Sample budget $k$ on the x-axis, which ranges from 1 to 80. The "Pass@k ceiling" and "CompassVerifier Best-of-N (reference-assisted)" series exhibit upward trends, rising from approximately 0.75 to over 0.9 as the sample budget increases. In contrast, the "Mean log-prob. / perplexity Best-of-N" curve shows a distinct decline, starting near 0.75 and dropping to roughly 0.66, with an annotation indicating a decrease from 75.56% to 65.83%. The other two methods, "Plurality" and "Sequence log-prob. Best-of-N," maintain relatively flat trajectories hovering around the 0.78 accuracy level throughout the range.]  
Figure 5: Candidate availability and reducer accuracy under repeated sampling. (a) Median exact Pass@k and $\mathrm { p a s s } ^ { k }$ across the 20 configurations; bands span the interquartile range of configurations. (b) Mean agreement of subset rankings with the N = 80 ranking; bands are central 95% ranges over 200 paired subset replays. (c) Reducers for Qwen3-30B-A3B-Thinking-2507, the strongest single-response configuration in this roster; bands are 95% prompt-bootstrap intervals. CompassVerifier sees the reference answer and is shown only as a reference-assisted diagnostic. Mean log probability and negative perplexity induce the same ordering, so one curve represents both.

## 4.3 Full trace collection on competition mathematics

This block contains 186 problems from five competition datasets distributed by MathArena (Dekoninck et al., 2026): AIME’26, HMMT Feb.’26, HMMT Nov.’25, CMIMC’25, and SMT’25 (MathArena, 2026a;b; 2025d;b;e).

The efort comparison comprises one Qwen3.6-35B-A3B (Qwen Team, 2026) bank and three gpt-oss-20b banks at low, medium, and high reasoning efort. Every trace records the full response, rule-based outcome, chosen token, and up to 20 token alternatives at every generation position.

Pass@k increases for all four banks (Figure 6). At k = 80, Pass@80 is 94.62% for Qwen3.6 and 72.58%, 91.94%, and 93.55% for gpt-oss low, medium, and high. The corresponding accuracies after reference-free pointwise selection are 86.56%, 58.06%, 75.81%, and 81.72%. The remaining 8.06–16.13 percentage-point gaps measure the share of questions for which a correct candidate is available but the reducer does not select it. Overlapping prompt-bootstrap intervals and diferences in response length preclude a total ordering of the generators. Among high-efort responses, 2,399 of 14,880 (16.12%) reach the common 81,920-token cap, compared with none at low efort.

![](images/8b6c265fe1efa0fb0b473896d633a5f92e4d8867be7c8bbab1ca9079e28820d4.jpg)

[Image: This figure presents four line charts plotting Accuracy against Sample budget $k$ for different generative models and effort levels. Panel (a) depicts Qwen3.6-35B-A3B, where 'Pass@k ceiling', 'Plurality', and 'LLM pointwise Best-of-N' all achieve high accuracy generally above 0.8. Panels (b) through (d) display results for 'gpt-oss-20b' under low, medium, and high effort conditions, showing a significant drop in performance relative to the ceiling in the low setting (annotated as a 14.5 pp gap) which narrows to 11.8 pp and 8.1 pp respectively.]  
Figure 6: Finite-bank scaling on the five 2025–2026 competition sets. Each panel compares the exact Pass@k ceiling with literal answer plurality and pointwise Best-of-N using the reference-free verifier described below. Arrows mark the k = 80 gap between Pass@80 and the better of the two observed reducers. Shading gives 95% prompt-bootstrap intervals conditional on the observed 80-response banks. Intermediate reducer points average 2,000 nested subset replays; k = 1 and k = 80 use exact endpoints. The horizontal axis counts generated candidates and excludes verifier computation.

## 4.4 Reference-assisted and reference-free verifier signals

We compute one reference-assisted score and one reference-free score. CompassVerifier-3B (OpenCompass) receives the question, reference answer, and candidate response and predicts A/B/C for correct, incorrect, or invalid responses (Liu et al., 2025c). We retain both its direct label distribution and a null-baseline-adjusted contextual distribution. The reference-dependent score is an outcome diagnostic and cannot be used for inference-time selection when gold answers are unavailable.

The reference-free score is a pointwise adaptation of the pairwise LLM-as-a-Verifier method (Kwok et al., 2026). Qwen3.6 receives one problem and one candidate response, with no reference answer, ground truth, Compass result, or other candidate. It scores problem understanding, reasoning validity, and conclusion support on an ordinal A–T scale. We map A through T to 20 through 1, compute the expected score from the returned, visible-mass-renormalized scoring-token probabilities, normalize each criterion to [0, 1], and average the three values. The score can rank candidates without a gold answer.

Against the rule-based outcome on 104,160 competition-mathematics responses, the trace-level ROC AUC is 0.983 for direct Compass A, 0.977 for contextual Compass A, and 0.871 for the pointwise score (Figure 7). The pointwise AUC is 0.744 on Qwen-generated responses and 0.876 on gpt-oss responses.

## 4.5 SuperGPQA

For SuperGPQA (M-A-P et al., 2025), we select 50 questions from each of 72 EvalScope fields, giving 3,600 questions (ModelScope Team, 2024). The four banks contain 80 responses per question from Qwen3.6 and gpt-oss at low, medium, and high efort, for $3 , 6 0 0 \times 4 \times 8 0 = 1$ ,152,000 responses.

For the gpt-oss high bank, mean response accuracy is 45.03%, Pass@80 is 81.94%, and $\mathrm { p a s s } ^ { 8 0 }$ is 9.47%. Of the 3,600 questions, 650 have no correct response and 341 are answered correctly in all 80 responses. Field-level response accuracy ranges from 21.33% in Aquaculture to 76.78% in Mathematics (Figure 8).

# 5 Conclusion

Test-time scaling encompasses a family of budgeted inference algorithms. Viewing these algorithms as operations over the implicit prefix tree distinguishes among single-trajectory deliberation, leaf-level sampling with terminal reduction, and prefix-level search. It also identifies the proposal, evidence map, decision rule, and causal stopping controller as distinct components of the inference process. Accordingly, the complete inference system is the scientifically meaningful unit of comparison.

This perspective clarifies how reasoning systems should be evaluated. End-to-end utility and candidatebank diagnostics answer diferent questions; shared-bank and end-to-end comparisons support diferent claims; compute accounting must include generation, evaluation, control, and decision; and uncertainty estimates must reflect the deployed inference protocol. Our framework also unifies repeated-sampling evaluation through the discovery–stability profile and distinguishes exact replay from distributional reproducibility. We analyze and publicly release 1,403,520 model attempts sampled from benchmarks covering broad knowledge, symbolic reasoning, and competition mathematics.

Our empirical study demonstrates the practical consequences of this system-level view. Model rankings change with the rubric, sampling budget, benchmark, and commitment standard; inference-time signals that predict correctness within individual trajectories need not reliably rank models; and strict answer extraction can conflate abstention with error. These results suggest that progress in test-time scaling should be assessed through reproducible inference systems with explicitly reported inference protocols, compute budgets, and uncertainties, rather than through checkpoint scores obtained under incompletely specified procedures.

# Acknowledgments

This research was supported in part by NSF awards 2117439, 2112606, and 2320952.

