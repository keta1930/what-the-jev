# Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents

Minhua Lin<sup>1</sup>\*, Juncheng Wu<sup>2</sup>\*, Zijun Wang<sup>2</sup>, Zhan Shi<sup>3</sup>, Yisi Sang<sup>3</sup>, Bing He<sup>3</sup> Zewen Liu<sup>4</sup>, Tianxin Wei<sup>5</sup>, Zongyu Wu<sup>1</sup>, Zhiwei Zhang<sup>1</sup>, Dakuo Wang<sup>6</sup>, Xiang Zhang<sup>1</sup> Benoit Dumoulin<sup>3</sup>, Cihang Xie<sup>2</sup>, Yuyin Zhou<sup>2</sup>, Suhang Wang<sup>1</sup>, Hanqing Lu<sup>3</sup> <sup>1</sup>The Pennsylvania State University <sup>2</sup>UC Santa Cruz <sup>3</sup>Amazon <sup>4</sup>Emory University <sup>5</sup>UIUC <sup>6</sup>Northeastern University {mfl5681,szw494}@psu.edu; {jwu418}@ucsc.edu; {luhanqin}@amazon.com

# Abstract

LLM agents are increasingly deployed as systems built around editable external harnesses, including prompts, skills, memories and tools, that shape task execution without changing model parameters. Harness self-evolution adapts such agents by updating these harnesses from execution evidence. Yet it remains unclear whether a model’s base capability in tasksolving predicts its capabilities in harness selfevolution: which models produce useful harness updates, and which actually benefit from them? We analyze two harness self-evolution capabilities: (i) harness-updating, the capability to produce useful persistent harness updates from execution evidence; (ii) harness-benefit, the capability to benefit from updated harnesses during task solving. Our analysis reveals two findings. First, harness-updating isflat in base capability: models from different capability tiers produce harness updates that lead to surprisingly similar gains; even Qwen3.5-9B’s updates yield gains comparable to those of Claude Opus 4.6. Second, harness-benefit is non-monotonic in base capability: weak-tier models benefit little from updated harnesses, mid-tier models benefit most, and strong-tier models benefit less than mid-tier. We trace low gains at the weak tier to two failure modes: weak-tier models may fail to activate relevant harness artifacts, or activate them but fail to follow them faithfully. These findings suggest investing capability budget in the task-solving agent rather than the evolver, and targeting harness invocation and long-horizon instruction following in agent training. Our source code is publicly available at here.

# 1 Introduction

Large language models (LLMs) (Radford et al., 2018; Touvron et al., 2023) have become a general-purpose foundation for language understanding (Hendrycks et al., 2020), reasoning (Wang et al., 2025), and task solving (Zhou et al., 2025). Increasingly, they also power agentic systems that interact with external environments, call tools, operate software interfaces, and complete long-horizon tasks (Yang et al., 2024b; Merrill et al., 2026). In these settings, system behavior depends not only on the underlying model but also on an external agent harness: prompts (Wei et al., 2022), skills (Xia et al., 2026), memories (Yan et al., 2025), tools (Qin et al., 2024), etc., that shape how the model observes, reasons, acts, and recovers from errors. Improving an agentic system increasingly means refining not only the foundation model, but also the editable harness around it.

![](images/6512722e52974ca60e5dace2b94a8285375f3db6d4aa6237ebd77866d34be1aa.jpg)

[Image: The image displays a framework titled "Harness Self-Evolution," illustrating a workflow where a frozen Large Language Model operates alongside an external agent harness. This "Harness" component contains four distinct modifiable areas: Memory, Tools, Prompts, and Skills. At the bottom, a process starts with "Experiences" (visualized as a trajectory graph) passing through a "Diagnosis" step to an "Evolver Model." A feedback loop indicated by a curved arrow shows the Evolver Model generating updates that cycle back to refine the components within the Harness, allowing the system to adapt based on execution evidence.]  
Figure 1: Overview of harness self-evolution.

In current practice, harnesses are typically designed by hand. However, such manual design is brittle in deployment-time environments: task distributions shift, edge cases appear, and useful procedures are discovered only after the system interacts with real tasks. A natural response is to update the harness automatically from execution evidence: failures, feedback, trajectories, and successful procedures can be written back into the harness and reused on future tasks. We refer to this setting as harness evolution (Fig. 1): the model weights remain fixed, while the external agent harness is revised over time. Recent self-evolving agent methods (Madaan et al., 2023; Wu et al., 2025; Agrawal et al., 2026; Xia et al., 2026; Lin et al., 2026b) pursue this approach across diverse harness components and have shown end-task improvements over non-evolving baselines. In these works, harness updates are typically produced by an LLM from execution evidence; we refer to this update role as the evolver.

![](images/81d0d546a3a96040778c1352f0231bbdeea60c1557c5d3d673f5f079adb5e1d5.jpg)

[Image: The image displays a scatter plot titled "(A) harness-updating is flat in base capability," plotting "harness-updating (points)" on the y-axis against "Base capability (avg pass rate, %)" on the x-axis. Data points for various models, including Opus 4.6, Haiku 4.5, and Qwen3 series, are clustered tightly between y-values of 3 and 4.5, indicating minimal variance in performance gain regardless of base capability. A horizontal dashed blue line marks the mean improvement at 3.75 points, while a shaded blue region labeled "Small variation across models" visually emphasizes this consistency across the different data series.]

![](images/9f00e9fd7aee69247e42581c5ad4074b18c7a0ef232cd10a14559187cec1bf28.jpg)

[Image: This figure presents a scatter plot titled "harness-benefit is non-monotonic in base capability," plotting harness-benefit points against base capability percentages for various AI models. The data reveals a curved trend where "Mid-Tier models" like GPT-OSS-120B and Qwen3-235B achieve the highest harness benefits, while models at both the lower end (Owen3-32B) and higher end (Sonnet 4.6, Opus 4.6) show reduced benefits. To the right, a diagram explains these dynamics: weak models suffer from "Harness Activation Failure" or "Harness Adherence Failure," preventing them from utilizing updates effectively. Conversely, strong models reach a "performance ceiling" where further improvements are minimal regardless of harness usage. The plot visually groups these failure modes with dashed circles and arrows pointing to corresponding explanatory text boxes at the bottom.]  
Figure 2: Overview of our findings. (i) Harness-updating is flat in base capability. Models across capability tiers produce harness updates that yield similar gains. (ii) Harness-benefit is non-monotonic in base capability. Mid-tier models benefit most, while weak-tier models benefit little due to failures in harness activation and adherence.

Despite this rapid progress, evaluation of these methods still asks an end-to-end question: does a self-evolution method effectively improve agent performance? This question is important, but it hides the source of improvement. The gain may come from the evolver producing higher-quality harness updates, or from the task-solving agent using the updated harnesses more effectively during task solving. End-to-end scores cannot disentangle these contributions, leaving two practical questions open: which models produce useful harness up dates, and which models benefit mostfrom them?

To answer these questions, we analyze two evolution capabilities a model exercises in harness self-evolution across three agentic benchmarks and seven LLMs: harness-updating, the capability to produce useful harness updates from execution evidence; and harness-benefit, the capability to benefit from updated harnesses during task solving. A model exercises harness-updating as the evolver, and harness-benefit as the task-solving agent. We conduct comprehensive experiments by pairing seven LLMs, spanning open-source and closed-source families across capability tiers, as agents and evolvers on three representative agentic benchmarks. Our analysis reveals two systematic decouplings between harness-evolution capabilities and base capability, namely, a model’s task-solving capability without harness evolution (Fig. 2).

First, harness-updating is flat in base capability. When we fix the task-solving agent and vary the evolver model, models from different capability tiers produce harness updates that lead to surprisingly similar gains, and no evolver dominates across all substrates. Our case studies further show that even the Qwen3.5-9B evolver produces harness updates whose downstream gains match those of Claude Opus 4.6, despite a large gap in base capability.

Second, harness-benefit is non-monotonic across base-capability tiers. Mid-tier models (e.g., GPT-OSS-120B) benefit most from updated harness, and strong-tier models (e.g., Claude Opus 4.6) reach the performance ceiling and benefit less. The weak-tier end, however, is not explained by the same ceiling argument: with the largest headroom above their base capability, models like Qwen3-32B might be expected to benefit most, yet they benefit the least. Our in-depth analysis identifies two failure modes that explain this weak-tier gap: (i) harness activation failure: weak models often fail to invoke relevant harness artifacts (e.g., skills) during task-solving; and (ii) harness adherencefailure: even when the harness is loaded, weak modelsfail to adhere to it due to weak instructionfollowing over long-horizon tasks.

These findings translate into design guidance for harness self-evolution systems. (i) Allocate capability budget to the task-solving agent, not the evolver: the harness-updating gap across evolvers is at most 3.1 percentage points on any benchmark, so scaling up the evolver yields limited returns; post-evolution performance varies much more with the task-solving agent than with the evolver. (ii) Bake harness invocation into agent training: weaktier models often fail to load the harness at all (e.g., 25% load rate for Qwen3-32B against ≈ 96% for strong models), so harness invocation should be treated as a first-class learned skill. (iii) Strengthen long-horizon instruction following: even when loaded, weak-tier adherence decays across the trajectory over four times more steeply than strong models, making sustained instruction following a second key target for downstream agent training.

# 2 Related Work

Harness engineering. An LLM agent combines a frozen backbone with an external harness that mediates reasoning, tool use, memory access, and environment interaction (Yao et al., 2022; Yang et al., 2024b; Ning et al., 2026). Recent work treats the harness as a first-class design object, differing mainly in the type of artifact exposed to the agent. Prompts and instructions provide natural-language guidance (Zhou et al., 2022; Pan et al., 2026); tools expose external services and define how agents dis cover, invoke, and validate them (Hou et al., 2025; Qin et al., 2024; Liu et al., 2025; Lin et al., 2026a); memory stores prior observations, facts, and strate gies for later retrieval (Ouvang et al., 2025: Xu et al., 2026; Fang et al., 2026); skills package reusable procedures into callable modules (Li et al., 2026b; Liu et al., 2026); and code treats the harness itself as executable source that can be optimized by an agentic proposer (Lee et al., 2026). These works establish harnesses as editable agent state. Our work shifts the focus from harness representation to model capabilities in updating and benefiting from harnesses. More details are in Appendix A.1. Self-evolution of LLM agents. Beyond what the harness contains, a complementary line asks how it is updated from execution experience. Early sys tems adapt agents through episode- or task-level language feedback: verbal self-reflection (Shinn et al., 2023) and iterative self-feedback (Madaan et al., 2023) improve later attempts by feeding lessons back into context. More recent methods make persistent harness components the unit of self-evolution, updating prompts (Agarwal et al., 2024; Zhang et al., 2025b; Agrawal et al., 2026), memories (Wu et al., 2025: Zhang et al., 2025a: Lin et al., 2026c), skills (Xia et al., 2026; Alzubi et al., 2026; Yang et al., 2026), or tools (Chen et al., 2025; Li et al., 2026a) from execution traces. Col lectively, these methods show that writing execu tion experience back into the harness can improve downstream task performance. However, evalua tions in this line typically report the end-to-end gain of one update procedure paired with one tar get agent on one substrate (Li et al., 2026b; Jiang et al., 2026; Wei et al., 2025). Such scores conflate three sources of improvement: the agent’s base capability, the evolver’s harness-updating, and the agent’s harness-benefit. Our work complements these methods with a controlled analysis that varies task-solving agents and evolvers independently, measures harness-updating and harnessbenefit separately, and tests whether either tracks base capability. More details in Appendix A.2.

# 3 Harness-Evolution Capabilities

To explore the evolution capabilities in harness self-evolution, we consider harness self-evolution, which adapts an LLM agent by updating the external harness around a fixed model during task execution: the agent attempts a stream of tasks and the harness is updated based on the agent’s execution evidence. In this section, we formalize the harnessevolution protocol and define two evolution capabilities: harness-updating, the ability to produce useful harness updates, and harness-benefit, the ability to benefit from updated harnesses.

## 3.1 Preliminaries: Harness State and Evolver

Agent Harness. We use agent harness to denote the external, non-parametric context and infrastructure through which an LLM is deployed for task execution (Yao et al., 2022; Ning et al., 2026; Lee et al., 2026). Formally, at evolution step t, the LLM agent is defined as:

$$
A _ {t} = (f, H _ {t}),\tag{1}
$$

where $f$ is the agent’s model backbone and $H _ { t }$ is the harness state after step t. Following common harness self-evolution settings (Zhou et al., 2026; Lin et al., 2026b), we keep f fixed and only update editable components of $H _ { t }$ (e.g., prompts, skills, memories), and fix other components such as tool interfaces and execution policies.

Evolver. An evolver is the update procedure that converts the agent’s execution evidence into harness updates, where recent self-evolving agent systems (Yang et al., 2024a; Yuksekgonul et al., 2024; Xia et al., 2026; Agrawal et al., 2026) increasingly instantiate this procedure with LLM agents. Formally, given the previous harness $H _ { t }$ <sub>−1</sub> and the accumulated execution evidence $\mathcal { D } _ { t }$ at step t, the evolver e proposes a harness update and applies it to $H _ { t - 1 }$ to obtain the next harness:

$$
\begin{array}{c} \Delta H _ {t} = e (H _ {t - 1}, \mathcal {D} _ {t}), \\ H _ {t} = \mathrm{Apply} (H _ {t - 1}, \Delta H _ {t}). \end{array}\tag{2}
$$

where Apply denotes the commit operation to apply $\Delta H _ { t }$ to $H _ { t - 1 }$

## 3.2 Evolution Protocol

Following common harness self-evolution pipelines (Ouyang et al., 2025; Agrawal et al., 2026), we formalize the protocol as an iterative loop between task-solving and harness evolution. Starting from an initial harness $H _ { 0 }$ , the protocol iterates for $T$ steps. At each step, the agent runs on a batch of tasks, collects execution evidence, and the evolver updates the harness for the next step. Formally, given an agent $A _ { t - 1 } = \left( f , H _ { t - 1 } \right)$ and a task batch $\mathcal { X } _ { t }$ at step t, $A _ { t - 1 }$ attempts to solve each task $x \in \mathcal { X } _ { t }$ and output:

$$
(\tau_ {t, x}, y _ {t, x}) = \mathrm{Solve} (A _ {t - 1}, x)\tag{3}
$$

where $\tau _ { t , x }$ is the execution trajectory and $y _ { t , x }$ is the final output. The execution evidence $\mathcal { D } _ { t }$ is then:

$$
\mathcal {D} _ {t} = \{(x, \tau_ {t, x}, y _ {t, x}): x \in \mathcal {X} _ {t} \}.\tag{4}
$$

The evolver produces the updated harness $H _ { t }$ from $H _ { t - 1 }$ and $\mathcal { D } _ { t }$ as in Eq. 2, yielding the next agent $A _ { t } = \left( f , H _ { t } \right)$ . This loop repeats for $T$ steps, producing the final harness $H _ { T }$

## 3.3 Capability Metrics

To analyze which models produce useful harness updates and which models benefit from them, we formally define three metrics to measure both harness-evolution capabilities (i.e., harnessupdating and harness-benefit) along with each model’s base capability.

Base Capability and Evolution Gain. Given a task set $\textstyle { \bar { \mathcal { X } } } = \bigcup _ { t = 1 } ^ { T } \mathcal { X } _ { t }$ , the base capability of a model $f$ is the task-solving performance of the initial agent $A _ { 0 } = \left( f , H _ { 0 } \right)$ on $\mathcal { X } \mathrm { : }$ :

$$
M _ {\text { base }} (f) = J _ {\mathcal {X}} (f, H _ {0}),\tag{5}
$$

where $J _ { \mathcal { X } } ( f , H )$ is the scoring function that measures the performance of agent $( f , H )$ on $\mathcal { X }$ .

Given a model f and an evolver e, let $H _ { T } ^ { ( f , e ) }$ denote the final harness produced after evolution with $f$ as the agent and e as the evolver for $T$ steps starting from $H _ { 0 }$ . We further define the pairwise evolution gain as the improvement of a specific agent–evolver pairing $( f , e )$ over the agent’s task solving performance before evolution:

$$
\Delta (f, e) = J _ {\mathcal {X}} (f, H _ {T} ^ {(f, e)}) - M _ {\text { base }} (f).\tag{6}
$$

Harness-updating Capability. The harnessupdating capability of an evolver e is its ability to produce harness updates that improve agents task-solving. Formally, this is defined as the mean pairwise gain across an anchor agent set $\mathcal { F } ^ { \star }$ :

$$
\Delta_ {\text { update }} (e) = \frac {1}{| \mathcal {F} ^ {\star} |} \sum_ {f \in \mathcal {F} ^ {\star}} \Delta (f, e).\tag{7}
$$

Harness-benefit Capability. The harness-benefit capability of a model f is its maximum gain in tasksolving performance from harness self-evolution. In practice, we estimate this as the maximum pairwise gain across a fixed anchor evolver set ${ \mathcal { E } } ^ { \star }$ :

$$
\Delta_ {\text { benefit }} (f) = \max _ {e \in \mathcal {E} ^ {\star}} \Delta (f, e).\tag{8}
$$
