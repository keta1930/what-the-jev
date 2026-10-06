TerminalBench-2 Harness Performance


# Meta-Harness: End-to-End Optimization of Model Harnesses

Yoonho Lee Stanford

Roshen Nair Stanford

Qizheng Zhang Stanford

Kangwook LeeKRAFTON

Omar Khattab MIT

Chelsea Finn Stanford

Project page w/ interactive demo: https://yoonholee.com/meta-harness/ Optimized harness: https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact

![](images/42fb1283a1bf37203f4c72cfaa6c7b74572671bad81cc8863e4e925699cf1672.jpg)

[Image: This line chart titled "Harness Optimizer Search Progress" plots Best Performance (%) on the y-axis against Harness Evaluations on the x-axis, ranging from 0 to 40. The red line representing Meta-Harness rises rapidly to exceed 55% performance within the first ten evaluations, significantly outperforming the teal TTT-Discover curve which peaks around 46% and the dark blue OpenEvolve curve which reaches approximately 43%. A dashed grey line indicates the performance baseline for the ACE method at roughly 40.5%, while fainter horizontal dotted lines mark lower baselines for "Few-shot" and "Zero-shot" scenarios at approximately 35% and 32%. The chart illustrates the search efficiency of Meta-Harness compared to existing optimizers and hand-designed benchmarks.]

![](images/ab0bfb0e4210a84c4397dfd3554b439882b46f0e1695c73c2c46475421a46837.jpg)

[Image: This bar chart compares the Pass Rate (%) of several software engineering agents, with the vertical axis scaling from 20 to 40 percent. The "Meta-Harness (ours)" system, highlighted in orange, achieves the highest pass rate of 37.6%, outperforming all other listed methods. The remaining five systems, categorized as "Human-written" and colored dark blue, display declining performance scores in descending order: Goose (35.5%), Terminus-KIRA (33.7%), Mini-SWE-Agent (29.8%), Terminus-2 (28.3%), and Claude Code (27.5%).]  
Figure 1: (Left) On text classification, Meta-Harness outperforms the best prior handdesigned harnesses (ACE) and existing text optimizers (TTT-Discover, OpenEvolve), match ing the next-best method’s final accuracy after just 4 evaluations. (Right) On TerminalBench-2, Meta-Harness outperforms all reported Claude Haiku 4.5 harnesses.


# Abstract

The performance of large language model (LLM) systems depends not only on model weights, but also on their harness: the code that determines what information to store, retrieve, and present to the model. Yet harnesses are still designed largely by hand, and existing text optimizers are poorly matched to this setting because they compress feedback too aggressively: they are memoryless, condition only on scalar scores, or restrict feedback to short templates or summaries. We introduce Meta-Harness, an outer-loop system that searches over harness code for LLM applications. It uses an agentic proposer that accesses the source code, scores, and execution traces of all prior candidates through a filesystem. On online text classification, Meta-Harness improves over a state-of-the-art context management system by 7.7 points while using 4× fewer context tokens. On retrieval-augmented math reasoning, a single discovered harness improves accuracy on 200 IMO-level problems by 4.7 points on average across five held-out models. On agentic coding, discovered harnesses surpass the best hand-engineered baselines on TerminalBench-2. Together, these results show that richer access to prior experience can enable automated harness engineering.


# 1 Introduction

Changing the harness around a fixed large language model (LLM) can produce a 6× performance gap on the same benchmark [47]. The harness—the code that determines what to store, retrieve, and show to the model—often matters as much as the model itself. This sensitivity has led to growing interest in harness engineering, the practice of refining the code around an LLM to improve the overall system’s performance [36; 21; 10; 9]. But despite its importance, harness engineering remains largely manual: practitioners inspect failures, adjust heuristics, and iterate on a small number of designs. In this paper, we ask whether this process itself can be automated.

![](images/1a1b4baaa2074832a338988a984b230211dea303a2dcf0945ac3562d3b47a87b.jpg)

[Image: This diagram illustrates a feedback loop for automating harness engineering through three numbered steps.

**Step 1**, labeled "Propose Harness Code," begins with an agent reading from a "Filesystem w/ All Experience" (represented by folders) and using that history to generate code, depicted by a robot icon thinking "Maximize." This process targets the creation of a "Harness," which evolves into a "Harness+LLM" block containing a neural network graphic.

**Step 2**, labeled "Evaluate," involves running the generated harness against a "Tasks" database (iconized as a cylinder). The evaluation process generates artifacts stored in a blue folder, specifically "Proposed Code," "Reasoning Traces," and an "Eval Score."

**Step 3**, labeled "Store all Logs to Filesystem," shows the output data from the evaluation folder feeding back into the initial file system, thereby closing the loop to inform future iterations of harness code generation.]  
Figure 2: Meta-Harness search loop. (1) An agent reads a filesystem containing all prior candidates’ source code, execution traces, and scores, and proposes a new harness. (2) We evaluate the proposed harness on evaluation tasks. (3) All logs (proposed code, reasoning traces, evaluation scores) are stored in the filesystem in a new directory, and the loop repeats.

<table><tr><td>Method</td><td>History</td><td>Log content</td><td>MTok/iter</td></tr><tr><td>OPRO [51]</td><td>Window</td><td>past (solution, score) pairs</td><td>0.002</td></tr><tr><td>TextGrad [53]</td><td>Last</td><td>textual feedback on current artifact</td><td>0.015</td></tr><tr><td>AlphaEvolve [35]</td><td>Window</td><td>program database + eval. scores</td><td>0.022</td></tr><tr><td>GEPA [1]</td><td>Summary</td><td>reflective feedback from rollout traces</td><td>0.008</td></tr><tr><td>Feedback Descent [26]</td><td>Summary</td><td>comparison + textual feedback</td><td>0.012</td></tr><tr><td>TTT-Discover [54]</td><td>Window</td><td>prev. solution fragment</td><td>0.026</td></tr><tr><td>Meta-Harness</td><td>Full</td><td>all logs and scores</td><td>10.0</td></tr></table>

Table 1: Comparison of text optimization methods and their settings. Each row represents a method collapsed across tasks. Mtok/iter is our best estimate of the full context generated from one evaluation of a text artifact in the largest setting considered in each paper. This paper considers settings that yield orders-of-magnitude more context per artifact evaluation.

A natural starting point is recent work on text optimization, since harness engineering also involves iteratively improving text and code artifacts using feedback from prior attempts [38; 39; 35; 26; 1]. However, these methods are poorly matched to harness engineering because they typically operate with short-horizon or heavily compressed feedback: some condition only on the current candidate [31; 51; 53], others rely primarily on scalar scores [35; 12], and others restrict feedback to short templates or LLM-generated summaries [1; 26]. This is a pragmatic scalability choice, not evidence that longer-range dependencies are uninformative. Harnesses act over long horizons: a single choice about what to store, when to retrieve it, or how to present it can affect behavior many reasoning steps later. Compressed feedback often removes the information needed to trace downstream failures to earlier harness decisions. Across the tasks studied by several representative text optimizers, the available context per optimization step ranges from only 100 to 30,000 tokens (Table 1), far below the diagnostic footprint of harness search. More broadly, work on retrieval and memory-augmented language models suggests that useful context should often be accessed adaptively rather than monolithically packed into a single prompt [28; 48; 37; 56].

We address this limitation with Meta-Harness, an agentic harness for optimizing harnesses via end-to-end search (Figure 2). Its proposer is a coding agent, i.e., a language-model-based system that can invoke developer tools and modify code. The choice of coding agent (rather than raw LLM) matters because the amount of experience quickly exceeds context limits, so the proposer must decide what to inspect and validate edits through direct interaction with the codebase. Its key design choice is to expose full history through a filesystem, enabling selective diagnosis of raw prior code and execution traces rather than optimization from compressed per-candidate summaries. For every previous candidate harness, the filesystem stores the source code, evaluation scores, and execution traces, which the proposer retrieves via standard operations such as grep and cat rather than ingesting them as a single prompt. In practice, the proposer reads a median of 82 files per iteration in our most demanding setting, referencing over 20 prior candidates per step (Appendix A). In the settings we study, a single evaluation can produce up to 10,000,000 tokens of diagnostic information, roughly three orders of magnitude beyond the largest feedback budgets used in prior text optimization settings (Table 1).

We evaluate Meta-Harness on online text classification, mathematical reasoning, and agentic coding. On online text classification, harnesses discovered by Meta-Harness improve over Agentic Context Engineering (ACE, Zhang et al. [59]) by 7.7 points while using 4× fewer context tokens, and match the next-best text optimizer’s final performance after 60 proposals with only four (Figure 1). On retrieval-augmented math reasoning, a single discovered harness improves accuracy on 200 IMO-level problems by 4.7 points on average across five held-out models. On TerminalBench-2, the discovered harness surpasses Terminus-KIRA and ranks #1 among all Haiku 4.5 agents.


# 2 Related Work

At a high level, Meta-Harness brings ideas from the broader literature on credit assignment and meta-learning [40; 46; 3; 17; 44; 2] in a new regime enabled by recent advances in coding agents. Rather than updating model weights, the system assigns credit at the harness level: it uses experience from past rollouts to deliberately reason about which steps and components are responsible for failures, then rewrites the external code that governs future behavior. More specifically, the method lies at the intersection of several recent research threads; it is most directly related to work on adaptive access to external context, executable code search, and text optimization.

External memory and adaptive access. Several prior works note the benefits of treating large knowledge sources or long inputs as external resources that a language model accesses adaptively, rather than consuming them in a single pass. Specifically, retrieval-augmented generation [28], interleaved retrieval and reasoning [48], memory-based agents [37], or recursive language models [56] are mechanisms for adaptive access to external context. Meta-Harness uses a similar access pattern, but in the more demanding setting of harness engineering, where the proposer selectively inspects a large external history of code, scores, and execution traces to improve context-management procedures themselves.

Executable code search. Recent methods search over executable code for functions, workflows, or agent designs. Early work proposes using large models as mutation and crossover operators in evolutionary program search [27]. Later methods evolve designated functions within fixed program scaffolds [39], use meta-agents to program new agents from prior dis coveries [20], or search over workflow graphs for agentic systems [58]. Another line of work searches over memory designs for continual-learning agents, where memory persists across task streams [57; 50]. In contrast, Meta-Harness searches over domain-specific harnesses, including prompt construction, retrieval, and state update strategies that reset between tasks. Its outer loop is deliberately minimal: instead of relying on a fixed scaffold, an archive of prior discoveries, or a persistent memory mechanism, it gives the proposer unrestricted filesystem access to prior experience. This lets the agent decide what information to inspect and enables search over full harness implementations rather than a predefined space of context-management procedures.

Text optimization methods. Meta-Harness is also closely related to methods such as ProTeGi, TextGrad, OPRO, GEPA, AlphaEvolve/OpenEvolve, and Feedback Descent, which iteratively improve prompts or other text artifacts using feedback from prior attempts [38; 31; 53; 51; 1; 35; 43; 26]. However, these methods are less well suited to harness engineering, where optimization targets a complete executable procedure, and the relevant environmental feedback is distributed across code, scores, and execution traces in a way that is hard to summarize up front. Rather than reacting only to aggregate scores or summaries, the proposer in Meta-Harness can reason over failed examples and their execution traces to propose targeted edits. See Table 1 for a comparison of problem scale considered in those papers and ours, and Figures 1 and 4 for a direct comparison with OpenEvolve, GEPA, and TTT-Discover in our problem setting.


# 3 Meta-Harness: A Harness for Optimizing Harnesses

This section describes Meta-Harness, our outer-loop procedure for searching over taskspecific harnesses. Meta-Harness is built on the idea that harness optimization benefits from allowing a proposer to selectively inspect prior code and execution traces via filesystem access, rather than optimizing from lossy summaries or an additional hand-designed search structure. At a high level, it repeatedly proposes, evaluates, and logs new harnesses.

Meta-Harness is itself a harness in the broad sense (hence the name), since it determines what information the proposer model sees during search. Unless otherwise noted, we use harness to refer to the task-specific programs being optimized.

Objective. A harness is a stateful program that wraps a language model and determines what context the model sees at each step. The goal is simple: find the harness that makes the underlying model perform best on the target task distribution. Formally, let M denote a fixed language model and $\mathcal { X }$ a task distribution. For a harness H and task instance $x \sim \mathcal { X } .$ we execute a rollout trajectory $\tau \sim p _ { M } ( H , x )$ . The harness constructs prompts for $M ,$ the model responds, and the harness updates its state after each interaction. A task-specific reward function $r ( \tau , x )$ scores the trajectory. The objective of harness optimization is to find the harness that maximizes the expected final reward:

$$
H ^ {*} = \underset {H} {\arg \max} \mathbb {E} _ {x \sim \mathcal {X}, \tau \sim p _ {M} (H, x)} r (\tau , x),
$$

When multiple objectives are relevant $( \mathrm { e . g . } ,$ , accuracy and context cost), we evaluate candidates under Pareto dominance and report the resulting frontier. In practice, this search has traditionally been carried out by human engineers and researchers, who iteratively refine prompts, context-management rules, and tool-use logic by hand.

Meta-Harness search loop. Meta-Harness uses a single coding-agent proposer with access to a growing filesystem D that serves as its feedback channel<sup>1</sup>. Here, a coding agent is a language-model-based system that can invoke developer tools and modify code. Unlike prior systems that externalize the improvement logic in a hand-designed search loop, Meta-Harness delegates diagnosis and proposal to the coding agent itself: it decides which prior artifacts to inspect, which failure modes to address, and whether to make a local edit or a more substantial rewrite. Equivalently, the proposer is not a raw next-token model operating on a fixed prompt assembled by the outer loop; it is an agent that retrieves information, navigates prior artifacts, and edits code as part of the search itself. Each evaluated harness contributes a directory containing its source code, scores, and execution traces (such as prompts, tool calls, model outputs, and state updates). The filesystem is typically far larger than the proposer’s context window, so the proposer queries it through terminal tools such as grep and cat rather than ingesting it as a single prompt. At each iteration, the proposer first inspects prior code, scores, and execution traces, then reasons about likely failure modes before generating a new harness.

Meta-Harness maintains a population H and a Pareto frontier over evaluated harnesses, but imposes no parent-selection rule: the proposer is free to inspect any prior harness and its execution trace when proposing new ones. We run evolution for a fixed number of iterations and perform a final test-set evaluation on the Pareto frontier. This simplicity is deliberate: by leaving diagnosis and edit decisions to the proposer rather than hard-coding search heuristics, Meta-Harness can improve automatically as coding agents become more capable. The proposer never sees test-set results; its only feedback comes from the search set, the subset of task instances used to evaluate candidate harnesses during search and generate the feedback signal for improvement, and from execution traces logged during those search runs.

Advantages of code-space search. Harness optimization occurs in code space, where small changes to retrieval, memory, or prompt-construction logic can affect behavior many steps later, making local search heuristics poorly matched to the problem. By inspecting execution traces, the proposer can often infer why a harness failed and which earlier design choices likely contributed to the failure, not just that it failed, as illustrated by the search trajectories in Appendices A and A.2. There, we see that the proposer reads broadly across prior code and logs, then uses those traces to identify confounded edits, isolate likely causal changes, and shift toward safer modifications after repeated regressions. The proposer can therefore modify the harness at the level of algorithmic structure, ranging from changes to retrieval, memory, or prompt-construction logic to full program rewrites, rather than filling in templates or applying predefined mutation operators. In practice, it often starts from a strong prior harness, but this is an emergent strategy rather than a hard-coded rule. Although the search space is large, representing harnesses as programs provides a natural regularization bias: coding models tend to propose coherent algorithms rather than brittle, hard-coded solutions, which biases the search toward reusable context-management procedures. This action space is closely aligned with the read–write–execute workflows on which frontier coding assistants are trained.

```txt
Algorithm 1 Meta-Harness outer loop over harnesses
1: Input: tasks X, LLM M, proposer P, iterations N
2: Initialize: population H ▷ Initial set of valid harnesses
3: Initialize: filesystem D ← ∅ ▷ stores code, scores, traces
4: for H ∈ H do
5: E_H ← Evaluate(H, M, X)
6: D ← D ∪ {(H, E_H)}
7: for t = 1 ... N do
8: Proposer P queries filesystem D ▷ inspects prior harnesses and scores
9: Proposer P proposes k new harnesses {H_1, ..., H_k}
10: for H in {H_1, ..., H_k} do
11: if H passes interface validation then
12: D ← D ∪ {(H, EVALUATE(H, M, X))}
13: return Pareto frontier of harnesses stored in D
```

Practical implementation. In our experiments, each harness is a single-file Python program that modifies task-specific prompting, retrieval, memory, and orchestration logic. In our experiments, the proposer P is Claude Code [4] with Opus-4.6. The proposer is guided by a minimal domain-specific skill that describes where to write new harnesses, how to inspect previous harnesses and their execution traces, and what files it can and cannot modify. The base model M varies by domain and is always frozen; see Section 4 for details. In our experiments, a typical run evaluates roughly 60 harnesses over 20 iterations. We provide additional tips for implementing Meta-Harness in a new domain in Appendix D.
