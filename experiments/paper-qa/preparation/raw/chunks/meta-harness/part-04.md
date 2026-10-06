# B Discovered Harnesses

Meta-Harness discovers executable inference-time procedures specific to the problem setup at hand. These harnesses are structured, domain-specific policies, often with nontrivial control flow such as routing, filtering, and conditional context construction, selected solely by whether they improve search-set performance. This section presents compact, method-style abstractions of representative harnesses that summarize the main behaviors and controlflow decisions that drive inference-time behavior. For reference, the full implementation for each discovered harness is on the order of 100–1000 lines of code.

![](images/904a963b60c738ee7b813f9b0f69e6f3d2e88fa5465c25ab05f983b3ac0a8560.jpg)

[Image: This flowchart illustrates the logic of a Text Classification Harness, beginning with a "Query + memory" input that branches into two retrieval pathways. On the left, the system retrieves top-5 similar examples to perform a "Draft call," establishing an initial label $D$ that subsequently guides the retrieval of confirmers and challengers on the right branch. This information undergoes a "Verification call" to decide whether to keep or revise the label $D$. The workflow concludes by converging into a "Final label" node at the bottom.]  
Figure 5: Draft-verification classification harness. The first call produces a draft label from a short retrieved context. The second call retrieves evidence for and against that draft and returns the final prediction.

## B.1 Text Classification Harness

In online text classification, Meta-Harness discovers a family of memory-based harnesses rather than a single canonical policy. Table 9 reports the Pareto frontier of non-dominated variants from the main search, all selected solely by search-set performance. We highlight two representative endpoints here: Meta-Harness (Draft Verification), the lowest-context frontier point, and Meta-Harness (Label-Primed Query), the highest-accuracy frontier point used in the main text.

Overview. Both harnesses maintain a growing memory of past labeled examples and build prompts from that memory at inference time. What differs is the control flow used to interrogate the memory. Meta-Harness (Draft Verification) uses two short calls and explicitly tests the model’s first guess against retrieved counterexamples, while Meta-Harness (Label-Primed Query) spends a larger single-call budget on making the label space and local decision boundaries explicit. Figures 5 and 6 summarize these two programs.

Meta-Harness (Draft Verification). The corresponding discovered file is draft verificat ion.py. This lightweight variant turns prediction into a two-call procedure. It first retrieves the 5 most similar labeled examples and makes a draft prediction. It then re-queries the same memory conditioned on that draft label, retrieving 5 confirmers with the same label and 5 challengers with different labels, and asks the model whether to maintain or revise its initial answer. The key discovered behavior is that the second retrieval depends on both the query and the draft prediction, so the harness can surface counterexamples targeted at the model’s current guess rather than only generic near neighbors. If too few labeled examples have been accumulated, the program falls back to a standard single-call few-shot prompt.

• Stage 1: Draft. Retrieve the 5 nearest labeled examples and ask for an initial prediction.

• Stage 2: Verification. Condition retrieval on the draft label, then show both supporting and challenging examples before making the final prediction.

• Cold start. If fewer than 5 labeled examples are available, skip the two-stage procedure and use a standard single-call few-shot prompt.

• Why it is cheap. Both calls use short retrieved contexts, so the overall context cost stays near the low end of the frontier even with two model invocations.

![](images/b77f715a7551ab7cdf9e0a4b83a34acdfc09b7a133bbba2eecf81f5df8b086bf.jpg)

[Image: This diagram depicts a workflow for constructing a single prompt to determine a "Final label" based on "Query + memory". The process initiates by branching into a "Label primer" component for all valid labels and a "TF-IDF retrieval" path that creates both a "Coverage block" containing the best example per label and "Contrastive pairs" featuring similar examples with different labels. These three distinct streams—the label primer, the coverage block, and the contrastive pairs—converge at an intermediate step to "Assemble one prompt with primer, coverage, and contrastive pairs", which then outputs the final label.]  
Figure 6: Label-primed query-anchored classification harness. The program builds a single prompt that exposes the label space, then populates it with query-relevant coverage examples and local contrastive pairs.

Meta-Harness (Label-Primed Query). The corresponding discovered file is label prime d query anchored.py. This strongest variant uses a single larger call built from three parts. It begins with a label primer listing the valid output labels, then constructs a coverage section with one query-relevant example per label, and finally adds query-anchored contrastive pairs that place highly similar examples with different labels side by side. The coverage block exposes the full label space, while the contrastive block sharpens local decision boundaries around the current query. In code, the harness implements this with TF-IDF retrieval over past labeled examples and a query-anchored pairing rule that chooses contrasting examples from the same local neighborhood.

• Label primer. List the valid output labels before showing any examples, so the model sees the full answer space up front.

• Coverage block. For each known label, retrieve the most query-relevant labeled example and include one representative example per class.

• Contrastive block. Build pairs of highly similar examples with different labels, so the prompt exposes local decision boundaries around the current query.

• Retrieval rule. Use TF-IDF similarity and query-anchored partner selection rather than label-agnostic nearest neighbors.

## B.2 Math Retrieval Harness

This subsection describes the retrieval harness discovered by Meta-Harness for mathematical reasoning (Section 4.2). The final harness is a compact four-route BM25 program whose structure emerged through search rather than being manually specified after the fact. All design choices below—the routing predicates, reranking terms, deduplication thresholds, and per-route example counts—were selected by the outer loop across 40 iterations of evolution.

<table><tr><td rowspan="2" colspan="2">Variant</td><td colspan="3">Datasets</td><td colspan="2">Avg metrics</td></tr><tr><td>USPTO ↑</td><td>Symptom ↑</td><td>LawBench ↑</td><td>Avg ↑</td><td>Ctx ↓</td></tr><tr><td>Meta-Harness</td><td>(Draft Verification)</td><td>18.0</td><td>85.4</td><td>17.0</td><td>40.1</td><td>5.4</td></tr><tr><td>Meta-Harness</td><td>(Error-Annotated)</td><td>9.0</td><td>87.7</td><td>24.0</td><td>40.2</td><td>22.3</td></tr><tr><td>Meta-Harness</td><td>(CoT Replay)</td><td>13.0</td><td>88.2</td><td>25.0</td><td>42.1</td><td>23.3</td></tr><tr><td>Meta-Harness</td><td>(Cluster Coverage)</td><td>12.0</td><td>86.8</td><td>33.0</td><td>43.9</td><td>31.2</td></tr><tr><td>Meta-Harness</td><td>(Cascade Retrieval)</td><td>12.0</td><td>86.8</td><td>36.0</td><td>44.9</td><td>39.2</td></tr><tr><td>Meta-Harness</td><td>(RRF + Contrastive)</td><td>18.0</td><td>89.6</td><td>35.0</td><td>47.5</td><td>41.4</td></tr><tr><td>Meta-Harness</td><td>(Relevance + Contrastive)</td><td>18.0</td><td>90.6</td><td>36.0</td><td>48.2</td><td>43.9</td></tr><tr><td>Meta-Harness</td><td>(Label-Primed Query)</td><td>14.0</td><td>86.8</td><td>45.0</td><td>48.6</td><td>45.5</td></tr></table>

Table 9: Pareto-optimal discovered variants from the main text-classification search, trading off average accuracy against context cost. The selected system in the main text is Meta-Harness (Label-Primed Query). Ctx denotes average additional characters in input context (thousands).

![](images/5ddf58f1d0871f669c22e5afd4f3880ebf13bab7186f1ca7813c71a9c34e0812.jpg)

[Image: The image contains three scatter plots titled "Val vs Test Accuracy by Dataset (gpt-oss-120b)," each plotting Validation Accuracy (%) on the x-axis against Test Accuracy (%) on the y-axis. The subplots display results for three specific datasets: LawBench, Symptom2Disease, and USPTO, with a dashed diagonal line representing equal values for both metrics. While a cloud of light pink dots indicates general performance distribution, specific experimental variants such as "Zero-shot," "Few-shot," and "ACE" are distinctly marked with colored geometric shapes and text labels.]  
Figure 7: Search-set vs. test accuracy per dataset for discovered text-classification strategies. Each pink dot is a discovered strategy; baselines are labeled. The dashed diagonal is y=x.

Overview. At inference time, the harness assigns each problem to exactly one of four routes: combinatorics, geometry, number theory, or a default route for algebra and other problems. The gates are implemented as lightweight lexical predicates over the problem statement, including keyword sets and a small number of regex features for geometry notation. The harness does not aggregate outputs across routes: once a route is selected, only that route retrieves examples for the final prompt. All routes use BM25 as the underlying retrieval mechanism over the filtered corpus described above. The BM25 index uses a math-aware tokenizer that preserves LaTeX tokens $\scriptstyle ( \mathbf { e . g . } , \lor r a c , \cdot \{ 2 \} )$ as atomic units. The selected harness is a merge of two successful search lineages, autonomously combined by the proposer during search: one contributed a stronger geometry route based on raw BM25, while another contributed a stronger combinatorics route based on deduplication and difficulty reranking. Figure 8 gives a compact flowchart view of the final program.

• Combinatorics: fetch 20 BM25 candidates, deduplicate to 8, rerank by lexical score and difficulty, then return the top 3. This is the main route where the harness explicitly trades off diversity against hard-problem matching.

• Geometry: return 1 hard NuminaMath reference together with 2 raw BM25 neighbors. Search consistently prefers raw structural matches here over difficulty reranking.

• Number theory: fetch 12 BM25 candidates and rerank using lexical score, difficulty, and a small bonus for solutions that state a technique early. This favors examples whose proof strategy is explicit.

• Default: fetch 10 BM25 candidates, rerank by lexical score and difficulty, and choose an adaptive number of examples based on how concentrated the top retrieval scores are.

![](images/9e8ae0248149ee6a9674a94fc9f38fed04fe9835380f3c266f8a2f4c8c63b9a4.jpg)

[Image: This flowchart illustrates a multi-stage retrieval architecture beginning with an input "Query" directed to a "Lexical router" that utilizes keyword and regex cues. The router distributes the query to four distinct parallel processing paths based on category: Combinatorics, Geometry, Number theory, and Algebra/Other. Each path specifies unique retrieval configurations, such as using BM25@20 for Combinatorics or 1 fixed reference plus 2 BM25 results for Geometry, before converging into a final step to "Build final prompt." The specific parameters include varying retrieval counts (e.g., keep 3, Adaptive K) and whether reranking is applied for each domain.]  
Figure 8: Discovered math retrieval harness. A lexical router assigns each query to one of four subject-specific retrieval policies. The selected policy retrieves examples, which are inserted into the final prompt.

## B.3 TerminalBench-2 Harness

The discovered TerminalBench-2 harness builds on Terminus-KIRA [25], inheriting its native tool calling (replacing Terminus 2’s ICL-based JSON parsing), 30KB output cap, and multiperspective completion checklist. The main modification discovered by Meta-Harness is environment bootstrapping: before the agent loop begins, the harness runs a compound shell command to gather a snapshot of the sandbox environment and injects it into the initial prompt. The proposer’s hypothesis, recorded verbatim from the search log, was:

```txt
Hypothesis: “Injecting an environment snapshot (OS, installed languages, package managers, /app contents) before the first LLM turn will reduce wasted exploration episodes by 3--5 turns on dependency-heavy tasks”
Changes: “Added _gather_env_snapshot() that runs a single compound shell command to collect working directory, /app listing, available languages (python, gcc, node, java, rustc, go), package managers (pip, apt) [... ] and injects as [Environment Snapshot] block”
```

The snapshot includes: the working directory, a listing of /app (truncated to 20 entries for large directories), available programming languages and their versions (Python, GCC, G++, Node, Java, Rust, Go), installed package managers (pip, apt-get), and available memory. This eliminates the 2–4 exploratory turns that agents typically spend discovering what tools and files are available, allowing the model to begin productive work immediately. The bootstrapping command is guarded by a 15-second timeout and fails silently, so it does not break the agent in unusual environments. The full implementation adds roughly 80 lines on top of Terminus-KIRA. Figure 9 summarizes the harness structure.

Per-task analysis. Compared to Terminus-KIRA, the discovered harness gains on 7 of 89 tasks, with the largest improvements on protein-assembly and path-tracing. The gaining tasks share a common property: they require domain-specific tooling whose availability cannot be assumed in advance (bioinformatics libraries, rendering pipelines, chess engines, cryptographic utilities, CoreWars simulators). Without the bootstrap, the agent spends its first 2–4 turns probing the environment; on tasks with tight turn budgets or where early wrong assumptions cascade, those wasted turns can be the difference between pass and fail. This suggests that the bootstrap’s value is largest when the environment is non-obvious, and the task requires the agent to match its strategy to what is actually installed.

![](images/d32ba46d2cd5c220bed30f678cfbcd606c0cd654772608587a520c01c6c258b5.jpg)

[Image: The image displays a vertical flowchart detailing an automated task execution workflow. It begins with a "Task instruction" leading into an "Env bootstrap" stage that configures environment variables such as pwd, files, languages, and memory. The sequence proceeds through an "Initial prompt" containing the task and snapshot, an "Agent loop" with native tool calling and a 30KB output cap, and concludes with a "Multi-perspective completion checklist". A decision point follows the checklist where a "pass" outcome leads to "Task complete", while a "fail" outcome loops back to the "Agent loop".]  
Figure 9: Discovered TerminalBench-2 harness. The harness inherits Terminus-KIRA’s native tool calling, output cap, and completion checklist (green). The environment bootstrap (red) is the component discovered by Meta-Harness: it gathers a sandbox snapshot before the agent loop begins, eliminating early exploratory turns.


# C Dataset Details

## C.1 OOD Text Classification Datasets

• SciCite is a 3-way citation-intent classification benchmark introduced by Cohan et al. [14]. Each example consists of a citation context from a scientific paper, labeled by the citation’s rhetorical role, such as background, method, or result. The task tests whether a model can infer why one paper cites another from the local scientific context.

• FiNER-139 is a financial numeric entity recognition benchmark introduced by Loukas et al. [29]. It consists of word-level annotations from financial filings with 139 fine-grained XBRL entity types, making it substantially more fine-grained than standard sentencelevel classification tasks. The benchmark tests whether a model can identify and classify numeric financial entities from context.

• Amazon Reviews is the English portion of the Multilingual Amazon Reviews Corpus introduced by Keung et al. [22]. In our setting, it is used as a 5-way review rating prediction task, where the label corresponds to the review’s star rating. This benchmark evaluates general-domain sentiment and rating prediction from product review text.

• Financial PhraseBank is a 3-way financial sentiment benchmark introduced by Malo et al. [32]. It consists of sentences from financial news and related economic text labeled as positive, neutral, or negative with respect to market sentiment. The task evaluates domain-specific sentiment classification in finance.

• GoEmotions is a fine-grained emotion classification benchmark introduced by Demszky et al. [15]. It contains English Reddit comments annotated with 27 emotion categories plus a neutral category, and is commonly treated as a 28-way classification task. The benchmark tests nuanced affect recognition beyond coarse positive-negative sentiment.

• Banking77 is a fine-grained intent classification benchmark introduced by Casanueva et al. [11]. It contains online banking user utterances labeled with 77 intents, covering a wide range of customer service requests. The task evaluates single-domain intent detection with a large label space.

• AG News is a 4-way news topic classification benchmark commonly associated with the text classification setup of Zhang et al. [60]. Examples are labeled with broad news categories such as world, sports, business, and science/technology. It is a standard general-domain benchmark for topic classification.

• SciTail is a science-domain textual entailment benchmark in which the task is to predict whether a hypothesis is entailed by a premise sentence in a science-focused inference setting [24].

• TweetEval (Hate) is the hate-speech subset of the TweetEval benchmark introduced by Barbieri et al. [7]. It is a binary tweet classification task for detecting hateful versus non-hateful content within a unified social-media evaluation suite. This benchmark tests robust classification in noisy, short-form social media text.

## C.2 Math Retrieval Corpus

Table 10 lists the datasets composing the retrieval corpus used in Section 4.2. The raw sources contain more problems than the final corpus; several filtering steps were applied before merging. NuminaMath-1.5 was filtered to competition-math subsets (AMC/AIME, olympiad references, number theory, inequalities, and related sources), discarding lowerquality web-scraped entries. OpenMathReasoning was deduplicated to one solution per problem (retaining the solution with the highest pass rate on an independent verifier), and problems whose source matched any evaluation benchmark family (IMO, AIME, HMMT, SMT, USAMO, Putnam) were removed before deduplication. The entire corpus was then decontaminated against all evaluation benchmarks and the search set used during harness search, using exact prefix matching followed by fuzzy Jaccard similarity (threshold 0.8); any corpus problem matching an eval problem under either criterion was discarded. Solutions from OpenMathReasoning and DeepMath are truncated to 5,000 characters to limit retrieval context length. At runtime, the selected harness further restricts retrieval to entries with non-empty solutions shorter than 4,000 characters. Retrieved solutions are truncated again to 3,000 characters when inserted into the prompt. For the geometry route, the harness also constructs a separate hard-reference index from NuminaMath problems with difficulty greater than 6.

## C.3 Math IMO-level Test Set

The main text aggregates results over 200 IMO-level problems drawn from IMO-AnswerBench, IMO-ProofBench, ArXivMath December 2025, and ArXivMath January 2026. The 200-problem evaluation set consists of a stratified 100-problem subset of IMO-AnswerBench, together with all problems from the other three benchmarks. This perbenchmark breakdown is useful because the four datasets mix answer-style, proof, and research-style problems, which are aggregated together in the main paper for brevity. When included, the table in this section should report each benchmark separately for both Base and Meta-Harness across the five held-out models.

<table><tr><td>Dataset</td><td>Problems</td><td>Sol. Len</td><td>Proof</td></tr><tr><td>OpenMathReasoning</td><td>281,743</td><td> $5,000^{\dagger}$ </td><td>34%</td></tr><tr><td>DeepMath-103K</td><td>103,021</td><td> $5,000^{\dagger}$ </td><td>0%</td></tr><tr><td>NuminaMath-1.5</td><td>129,520</td><td>1,376</td><td>13%</td></tr><tr><td>PolyMath</td><td>11,083</td><td>363</td><td>0%</td></tr><tr><td>Omni-MATH</td><td>4,289</td><td>829</td><td>0%</td></tr><tr><td>FineProofs-SFT</td><td>4,275</td><td>3,977</td><td>100%</td></tr><tr><td>AIME 1983–2024</td><td>933</td><td>—</td><td>0%</td></tr><tr><td>Putnam-AXIOM</td><td>492</td><td>888</td><td>100%</td></tr><tr><td>Total</td><td>535,356</td><td> $5,000^{\dagger}$ </td><td>22%</td></tr></table>

<sup>†</sup> Truncated at 5,000 characters; actual solutions are longer.

Table 10: Datasets in the math retrieval corpus (535K problems total). Sol. Len is the median solution length in characters. Proof indicates whether the dataset contains prooftype problems (by answer or problem type field).

<table><tr><td>Dataset</td><td>Problems</td></tr><tr><td>IMO-AnswerBench</td><td>100</td></tr><tr><td>IMO-ProofBench</td><td>60</td></tr><tr><td>ArXivMath Dec. 2025</td><td>17</td></tr><tr><td>ArXivMath Jan. 2026</td><td>23</td></tr><tr><td>Total</td><td>200</td></tr></table>

Table 11: Breakdown of the 200-problem IMO-level evaluation set.


# D Practical Implementation Tips

Meta-Harness is largely domain-agnostic: we expect it to apply in any setting where a language model is wrapped by a task-specific harness. Applying it in a new domain, however, requires operating in a relatively new regime of LLM-assisted coding, where the proposer conditions on long-horizon histories of prior runs and writes programs whose effects may only become visible many steps later. In getting this workflow to work reliably, we found a small set of practical choices that mattered consistently across the three domains studied in this paper. The guidelines below are not themselves scientific claims about the method; they are engineering lessons from building and running the system, which we hope will make it easier for future work to apply Meta-Harness in other domains.

• Write a good skill. The skill text is the primary interface for steering the search, and its quality is the strongest lever on whether the loop works. The proposer receives a natural language skill [5] that defines its role, the directory layout, CLI commands, and output format. In practice, the skill should constrain outputs and safety-relevant behavior, not the proposer’s diagnosis procedure: it should specify what is forbidden, what artifacts to produce, and what objectives to optimize, while leaving the model free to inspect scores, traces, and prior code as needed. Our intuition from inspecting logs from Meta-Harness runs is that after enough iterations, the accumulated traces often shape the proposer’s behavior more than the skill itself. In our experience, iterating on the skill text had a larger effect on search quality than changing iteration count or population size. Expect to run a few short evolution runs (3–5 iterations each) specifically to debug and refine the skill before committing to a full run.

• Start with a baseline harness and a search set that is hard for it. Write a simple baseline (e.g., few-shot prompting), then construct the search set by either filtering for examples that the baseline gets wrong or selecting a diverse subset of difficult instances. The search has little to optimize if the baseline already saturates the evaluation. Keep the search set small enough for roughly 50 full evaluations per run (50–100 examples in our classification experiments, 88 problems for math retrieval); a fast, discriminative eval is more valuable than a large one.

• Log everything in a format that is easy to navigate. Evaluation code should write code, scores, and execution traces in a form that the proposer can query reliably. In practice, this means using machine-readable formats such as JSON, organizing artifacts hierarchically, choosing reasonable and consistent file names, and adopting naming schemes that make simple tools such as regex search work well.

• Make logs queryable through a small CLI (optional, but helpful). Each harness gets a directory containing source code, scores, and execution traces, but as the history grows, raw filesystem access alone becomes cumbersome. A short CLI that lists the Pareto frontier, shows top-k harnesses, and diffs code and results between pairs of runs can make the experience store much easier to use, and querying such CLIs is closely aligned with the workflows on which coding agents are trained. If relevant offline experience exists (rollouts from other models, solved problem corpora, relevant papers), converting it into the same directory structure can also help warm-start exploration and ground new ideas. This layer helps the proposer save tokens it may have wasted on navigation.

• Lightweight validation before expensive benchmarks. Write a small validation test that imports the module, instantiates the class, and calls both methods on a tiny set of examples. Harnesses proposed during the search should pass this test before being fully evaluated. A simple test script can catch most malformed or nonfunctional candidates in seconds and keep the cost of failures near zero.

• Automate evaluation outside the proposer. Running evals is simple enough that it is not worth making the proposer do it. A separate harness should score candidates and write results to the filesystem.


# E Extended Related Work

This appendix expands the brief discussion in Section 2 and situates Meta-Harness relative to several neighboring lines of work that we could not cover in detail in the main text. A recurring distinction is that Meta- Harness optimizes executable harness implementations and provides the proposer with selective access to prior code, scores, and execution traces via the filesystem.

AlphaEvolve / OpenEvolve. AlphaEvolve [35] and OpenEvolve [43] evolve code via LLM-guided mutations with structured feedback: the proposer receives a program database with scalar scores (4–22K tokens per step; Table 1) and applies fixed mutation strategies to tournament-selected parents. These methods are designed for algorithm discovery and optimization (mathematical conjectures, scheduling heuristics, hardware kernels), where the search target is a single stateless function with a clean scalar objective, and mutations are local. Harness engineering is a different regime: harnesses are stateful programs that accumulate experience across many examples, and a single design choice (e.g., what to store in memory) can cascade through an entire evaluation sequence. Meta-Harness addresses this by giving an unstructured coding agent full filesystem access, letting it selectively read any prior candidate’s source code, execution traces, and scores.

GEPA. GEPA [1] is the closest text optimizer in terms of feedback richness, providing rollout traces per candidate. It is designed for prompt optimization on tasks with short feedback loops (math problems, instruction-following, code optimization), where each rollout is a single LLM call or a short pipeline. In this regime, per-candidate reflection works well: one prompt, one answer, one score. Harness engineering requires reasoning across many examples and many candidates simultaneously: understanding why a retrieval strategy works for one class of problems but degrades on another requires comparing execution traces across the full population. GEPA operates on one candidate at a time (2–8K tokens per step; Table 1), with a fixed critique format that must anticipate what information is relevant. Meta-Harness gives the proposer access to all prior candidates simultaneously and lets the agent decide what to examine.

Prompt orchestration frameworks. Several systems provide structured abstractions for composing multi-stage LLM programs. LMQL [8], LangChain [13], and DSPy [23] make prompt engineering more systematic by providing higher-level interfaces for prompt templates, control flow, and modular LLM pipelines. These frameworks help developers specify and organize LLM programs, but they still typically require manual design of retrieval policies, memory updates, and orchestration logic. Meta-Harness operates at a different level: it searches over the implementation of these policies in executable code, treating the harness itself as the optimization target.
