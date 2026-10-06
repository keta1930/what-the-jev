# ALSO: Adversarial Online Strategy Optimization for Social Agents

Xiang Li <sup>1</sup> Liping Yi <sup>1</sup> Mingze Kong <sup>2</sup> Min Zhang <sup>3</sup> Zhongxiang Dai <sup>2</sup> QingHua Hu <sup>1</sup>

# Abstract

Social simulation provides a compelling testbed for studying social intelligence, where agents interact through multi-turn dialogues under evolving contexts and strategically adapting opponents. Such environments are inherently non-stationary, requiring agents to dynamically adjust their strategies over time. However, most Large Language Model (LLM) based social agents rely on static personas, while existing approaches for enhancing social intelligence, such as offline reinforcement learning or external planners, are ill-suited to these settings, typically assuming stationarity and incurring substantial training overhead. To bridge this gap, we propose ALSO (Adversarial onLine Strategy Optimization), the first framework for online strategy optimization in multi-agent social simulation. ALSO advances social adaptation through two key contributions. (1) ALSO formulates multi-turn interaction as an adversarial bandit problem, where combinations of static personas and dynamic strategy instructions are treated as arms, providing a principled solution to non-stationarity without relying on environmental stability assumptions. (2) To predict rewards and generalize sparse feedback in multi-turn di alogues, ALSO introduces a lightweight neural surrogate to predict rewards from interaction histories, enabling sample-efficient exploration and continuous online adaptation. Experiments on the Sotopia benchmark demonstrate that ALSO consistently outperforms static baselines and existing optimization methods in dynamic environments, validating the effectiveness of adversarial online strategy optimization for building robust social agents.

![](images/78570f4401d0b1ee036feddc892507bb1e0362568d60af159e924360d55f3c7b.jpg)

[Image: The image displays a conceptual diagram of a negotiation task involving two opposing personas: a conservative "Chief Risk Officer" aiming to "play it safe" and an aggressive "Fintech Founder" aiming to "win fast." Both agents are situated within "Online Learning Loops" depicted by circular blue arrows connecting their thought bubbles to a central interaction table where "Strategy Cards" are being exchanged. Below the table, large grey arrows indicate "Observation & Reward (Feedback)" pathways that feed back into the agents' learning loops, visualizing a continuous cycle of adaptation based on the interaction. Small gear icons near the feedback arrows symbolize the underlying algorithmic processes optimizing the agents' strategies in this dynamic environment.]  
Figure 1. Online social interaction between agents with personas and adaptive strategies, where feedback multi-turn dialogue drives continuous strategy optimization under evolving behaviors.

# 1. Introduction

Modeling social intelligence (Mathur et al., 2024) is a central pursuit in Artificial Intelligence research. The advent of Large Language Models (LLMs) has substantially advanced this field by endowing agents with human-like communication (Spitale et al., 2023) and planning capabilities (Wu et al., 2024a; Park et al., 2023). This progress has positioned LLM-based social simulation as a powerful framework for studying emergent social behaviors in large-scale and goaloriented interactions (Epstein, 2012; Wang et al., 2024a). In such simulations, agent behavior is typically governed by a persona, a formalized profile encapsulating personality traits, occupations, and background stories (Reiss, 2023; Salinas & Morstatter, 2024; Bisbee et al., 2024).

While static personas provide foundational identity, they alone are insufficient for eliciting adaptive social intelligence. It is important to distinguish between persona and strategy: a persona defines who an agent is, whereas a strategy specifies how the agent acts to navigate interactions and achieve goals. Empirical studies demonstrate that relying solely on static personas often yields stereotypical and homogeneous behaviors, failing to capture the diversity required for robust social simulation (Taubenfeld et al., 2024; Hwang et al., 2025; Zeng et al., 2025; Venkit et al., 2026). This homogeneity is further reinforced by the “alignment tax” of Reinforcement Learning from Human Feedback (RLHF), which suppresses behavioral variance in favor of safety (Kirk et al.). Without evolving strategies to complement identity, agents struggle to adapt to dynamic opponents, resulting in rigid and suboptimal interaction patterns (Li et al., 2023; Wang et al., 2024b; Zeng et al., 2025).

To enhance social adaptability, recent work has explored automated prompt optimization (APO) for refining agent instructions (Zhou et al., 2022a; Guo et al., 2024; Lin et al., 2024b; Opsahl-Ong et al., 2024a), which can be interpreted through multi-armed bandit formulations. However, both offline approaches and online variants (Yang et al., 2023; Lin et al., 2024a; Wu et al., 2024b) fundamentally rely on stationarity assumptions, where each prompt induces a stable reward distribution evaluated on fixed validation sets. Such assumptions break down in social simulation, as feedback from multi-turn interactions with strategically adapting counterparts whose behaviors co-adapt with the agent’s strategy choices, inducing persistent reward shifts and strong temporal coupling. This dynamic feedback loop renders standard stochastic bandit models inadequate for social strategy instruction optimization.

To bridge this gap, we propose ALSO (Adversarial Online Strategy Optimization), an online framework that casts social strategy adaptation as an adversarial multi-armed bandit problem to enable principled optimization under nonstationarity, as shown in Figure 1. Rather than assuming stationary rewards, ALSO explicitly models the co-evolving and strategically adaptive nature of social interactions with two designs. (1) In ALSO, each arm corresponds to a strategy instruction sampled from a generated strategy set (e.g., cooperation, competition, deception, rational bargaining). At each interaction round, the selected strategy is combined with the agent’s persona to form the final prompt context, ensuring that dynamic adaptation remains grounded in consistent identity. Based on this adversarial bandit formulation, ALSO instantiates a robust online optimization procedure inspired by EXP3 (Lattimore & Szepesvari, 2020) with´ smoothing to hedge against shifting opponent behaviors. (2) Standard bandit methods treat arms independently and fail to exploit semantic relationships among strategy instructions. To address this limitation, ALSO introduces a lightweight neural surrogate model that leverages interaction histories to predict rewards and generalize sparse feedback across semantically related strategies. This enables sample-efficient online optimization under sparse multi-turn feedback.

Overall, ALSO forms a closed-loop online system that iteratively selects strategies, interacts under persona-conditioned prompts, and updates both the bandit policy and surrogate model from feedback. We evaluate ALSO on Sotopia, a comprehensive LLM-based social simulation benchmark spanning seven dimensions of social intelligence. Across diverse settings, ALSO consistently outperforms static persona agents and existing optimization baselines, achieving a +16.60% overall improvement and +83.79% substantial gains on relationship outcomes.

Contributions. We make the following contributions:

• We introduce the first online strategy learning framework for LLM-based multi-agent social simulation, enabling dynamic adaptation beyond static personadriven behavior in evolving environments.

• We formulate social strategy optimization as an adversarial bandit problem with surrogate reward modeling, providing a principled solution to non-stationary and strategically adaptive interactions.

• We conduct extensive evaluations on the Sotopia benchmark, demonstrating consistent improvements over static agents and existing optimization baselines across diverse social settings.

# 2. Related work

## 2.1. Social Intelligence

Social intelligence, distinct from abstract and mechanical intelligence, refers to the ability to manage interpersonal relations and social contexts (Thorndike, 1920; Strang, 1930; Thorndike & Stein, 1937). In computational settings, Artificial Social Intelligence emphasizes modeling and responding to the mental and behavioral dynamics of interacting partners, including both humans and artificial agents (Sap et al., 2022; Gweon et al., 2023; Mathur et al., 2024). Recent advances in Large Language Models (LLMs) provide a strong foundation for building socially capable agents (Hoppler et al., 2022; Lee et al., 2024; Anthis et al., 2025).

Early social evaluation frameworks (e.g., Social IQa (Sap et al., 2019) and SocialBench (Chen et al., 2024)) focused on static multiple-choice settings, which fail to capture the dynamic and non-stationary nature of social interaction. This limitation motivated dynamic simulation-based benchmarks, including SOTOPIA (Zhou et al., 2024) and AgentSense (Mou et al., 2025), which assess agents in openended multi-turn environments with continuously evolving goals and social relations.

Existing methods for enhancing social intelligence generally follow two paradigms. The first category focuses on offline optimization. Sotopia-π (Wang et al., 2024b) improves performance through data-centric refinement, while Sotopia-RL (Yu et al., 2025) and SDPO (Kong et al., 2025a) address credit assignment and preference optimization in multi-turn dialogues. Adaptive Mode Learning (AML) (Wang et al., 2025a) further promotes diverse social reasoning patterns.

The second category augments inference through offlinetrained external planners. Methods such as Sotopia-

Ω (Zhang et al., 2025), DAT (Li et al., 2024), and EPO (Liu et al., 2025) learn auxiliary planning models from generated data to provide high-level strategic guidance at test time. While these approaches highlight the importance of strategies in social interaction, they embed strategic behaviors either within model parameters or fixed planners.

As a result, introducing new strategies or adapting to evolving social dynamics typically requires data recollection and retraining. This limitation motivates our ALSO, which enables dynamic and sample-efficient strategy adaptation through online optimization without offline retraining.

## 2.2. Prompt Optimization

Prompt Optimization (PO) provides an efficient mechanism for adapting agent behavior without parameter fine-tuning by treating strategies as optimizable instructions (Wang et al., 2025b). Early PO methods primarily fall into two categories: LLM-as-Optimizer approaches such as APE (Zhou et al., 2022b), OPRO (Yang et al., 2023), and Instinct (Lin et al., 2024c), which iteratively generate and refine prompts, and evolutionary methods including EvoPrompt (Guo et al., 2024) and PromptBreeder (Fernando et al., 2024), which explore instruction spaces via mutation and selection.

Despite their effectiveness in static tasks, most PO methods rely on offline oracles, such as fixed validation sets, to evaluate and rank candidate strategies (Opsahl-Ong et al., 2024b; Kong et al., 2025b). This offline paradigm assumes stationary reward distributions and fails to capture the coupled, evolving dynamics of social interaction, where optimal strategies shift in response to adaptive opponents. Consequently, existing PO frameworks are ill-suited for online social simulation, motivating the need for adversarial and online strategy optimization as pursued in ALSO.

# 3. Problem Formulation

We consider a multi-agent social simulation environment and formulate online social strategy learning as sequential strategy selection under non-stationary interactions.

## 3.1. Multi-Agent Social Simulation Environment

We consider a general multi-agent social simulation framework in which LLMs act as interactive agents. The agent set is denoted by $\mathcal { N } = \{ 1 , 2 , \dots , N \}$ , where each agent $i \in \mathcal N$ is characterized by a persona $b _ { i } \in B$ and a private socia goal $g _ { i } \in \mathcal { G }$ . The scenario S specifies the social context, including environmental settings and interaction constraints.

The simulation proceeds in discrete dialogue rounds indexed by $l = 1 , \ldots , L$ At round l, the active agent i forms an observation o<sup>i</sup> by conditioning on the scenario, interaction history $\mathcal { H } _ { l - 1 }$ , its persona, and its goal:

$$
o _ {l} ^ {i} = \operatorname{Prompt} (\mathcal {S}, \mathcal {H} _ {l - 1}, b _ {i}, g _ {i}).\tag{1}
$$

The agent then samples an action $a _ { l } ^ { i }$ based on $o _ { l } ^ { i }$ from the LLM:

$$
a _ {l} ^ {i} \sim \operatorname{LLM} (o _ {l} ^ {i}).\tag{2}
$$

The environment updates the state and augments the history as $\mathcal { H } _ { l } = \mathcal { H } _ { l - 1 } \cup \{ a _ { l } ^ { i } \}$

After L dialogue rounds, an LLM-based evaluator assesses agent performance along M social dimensions:

$$
\{d _ {m} ^ {(i)} \} _ {m = 1} ^ {M} = \mathrm{LLM} _ {\mathrm{eval}} (\mathcal {S}, \mathcal {H} ^ {(L)}, b _ {i}, g _ {i}),\tag{3}
$$

which are aggregated into a scalar reward:

$$
r _ {i} = \frac {1}{M} \sum_ {m = 1} ^ {M} \phi_ {m} (d _ {m} ^ {(i)}).\tag{4}
$$

However, a key different of social simulation from this setting is its inherent non-stationary arising from strategically adaptive agents. Let ${ \bf A } _ { l } = ( a _ { l } ^ { ( 1 ) } , \dots , a _ { l } ^ { ( \bar { N } ) } )$ denote the joint action set at step l, and $\mathbf { a } _ { l } ^ { - i }$ the actions of all agents except agent i. Let $R ( s _ { l } , a _ { l } ^ { ( i ) } , \mathbf { a } _ { l } ^ { - i } )$ denote the instantaneous turnlevel reward function under state s<sub>l</sub> and joint actions set. The expected step/turn level reward for agent i is given by

$$
\mathbb {E} \left[ r _ {l} ^ {(i)} \mid s _ {l}, a _ {l} ^ {(i)} \right] = \sum_ {\mathbf {a} _ {l} ^ {- i} \in A ^ {- i}} R \left(s _ {l}, a _ {l} ^ {(i)}, \mathbf {a} _ {l} ^ {- i}\right) \prod_ {j \neq i} \pi_ {j} \left(a _ {j} \mid s _ {l}\right),\tag{5}
$$

where $\pi _ { j }$ denotes the evolving policy of agent j.

In practice, agents only observe the realized $r _ { i } ,$ , while the underlying expected reward $\mathbb { E } [ r _ { l } ^ { ( i ) } \mid s _ { l } , a _ { l } ^ { ( i ) } ]$ remains implicit and shifts continuously as opponent policies $\pi _ { j }$ evolve. This creates a fundamental learning challenge:

$$
r _ {i} = \mathbb {E} [ r _ {l} ^ {(i)} \mid s _ {l}, a _ {l} ^ {(i)} ] + \epsilon_ {t}, \quad \text { where } \epsilon_ {t} \text { is   non - stationary },\tag{6}
$$

where $\epsilon _ { t }$ captures both stochastic noise from LLM generation and distributional shift induced by co-evolving opponent policies. This motivates casting the strategy learning problem as adversarial online optimization (Section 3.2), where no stationarity of the reward signal is assumed.

## 3.2. Online Social Strategy Learning Problem

We model social strategy adaptation by discretizing the strategy space into a finite set of K strategic instructions (e.g., cooperation and competition), each corresponding to a bandit arm. Each instruction encodes high-level behavioral principles over goal orientation and interaction style, forming an interpretable strategy space for online learning. In this formulation, the agent’s action at each turn is to select an arm, i.e., choose a strategy instruction to guide its behavior throughout the social interaction. This directly casts online strategy selection under evolving social dynamics as an adversarial multi-armed bandit problem.

![](images/fa0845d9e59510fa2625ad67f84d905665a55eb30351ca8f8e5bcd02e469831b.jpg)

[Image: The image presents a comparative diagram featuring three vertical panels that illustrate a transition from rigid social simulation to an adaptive strategy framework. The left panel, titled "Social Simulation (Rigid Price DeadLock)," depicts two agents with static personas engaging in a failed negotiation over price, resulting in no deal. The center panel, labeled "ALSO (Adversarial Online Strategy Optimization)," details the underlying architecture which uses Strategy Space and Context inputs to drive Surrogate Reward Prediction and Adaptive Strategy Selection via an Adversarial Bandit. The right panel demonstrates the "Adaptive Strategy Instruction" in action, showing agents successfully negotiating a $75 deal through updated communication strategies, achieving a "Success" outcome compared to the initial failure.]  
Figure 2. Overview of ALSO for adaptive social strategy learning in LLM-based multi-agent social simulation. Static persona-driven agents exhibit rigid interactions and fail to achieve social goals (left), while ALSO leverages adversarial online strategy selection with surrogate reward modeling to dynamically adapt strategies and enable successful social outcomes (center–right).

Objective. Over rounds $t = 1 , \dots , T$ (each corresponding to a complete L-turn social simulation episode), agent i selects a strategy arm $k _ { t } \in [ K ]$ and receives an trun-level reward $r _ { k _ { t } } ^ { ( t ) } \in [ 0 , 1 ]$ from the evaluator (Eq. (4)). A natural target objective is to minimize the cumulative pseudo-regret

$$
\bar {R} _ {T} = \mathbb {E} \left[ \max _ {k \in [ K ]} \sum_ {t = 1} ^ {T} r _ {k} ^ {(t)} - \sum_ {t = 1} ^ {T} r _ {k _ {t}} ^ {(t)} \right],\tag{7}
$$

which measures performance relative to the best fixed strategy in hindsight. In our setting, however, the reward process is induced by co-evolving multi-agent interactions and an LLM evaluator; thus, ALSO adopts adversarial online learning as a design rationale for robustness rather than claiming a formal regret guarantee.

# 4. Methodology

This section presents ALSO, our adversarial online approach to strategy optimization in LLM-based multi-agent social simulations, as displayed in Figure 2.

## 4.1. Problem Setting

We formalize dynamic strategy instruction optimization in two-agent $( N = 2 )$ LLM-based social simulations. Each agent $i \in \{ 1 , 2 \}$ augments its original persona $b _ { i } ^ { 0 }$ with one of K predefined social strategies $\Sigma = \{ \sigma _ { 1 } , \dots , \sigma _ { K } \}$ (details in Appendix B.2).

In the original framework, the agent’s action is generated using a fixed persona:

$$
a _ {t} ^ {(i)} \sim \operatorname{LLM} \bigl (\mathcal {S}, \mathcal {H} _ {t - 1}, b _ {i} ^ {0}, g _ {i} \bigr).\tag{8}
$$

In ALSO, we dynamically augment the persona at each turn t by appending a selected strategy instruction $\sigma _ { k _ { t } } ^ { ( i ) }$ from the strategy space Σ. This creates an enhanced persona

$$
b _ {i} ^ {(t)} = b _ {i} ^ {0} \oplus \sigma_ {k _ {t}} ^ {(i)},\tag{9}
$$

where ⊕ denotes textual concatenation. The resulting persona $b _ { i } ^ { ( t ) }$ incorporates both the agent’s original identity (demographics, personality, values, etc.) and the high-level behavioral guidance provided by the strategy (e.g., collaborative problem-solving, firm bargaining, or strategic withholding). The LLM then generates the next action conditioned on this augmented context:

$$
a _ {t} ^ {(i)} \sim \operatorname{LLM} \bigl (\mathcal {S}, \mathcal {H} _ {t - 1}, b _ {i} ^ {(t)}, g _ {i} \bigr).\tag{10}
$$

This augmentation allows the LLM to adapt its responses based on the chosen strategy (e.g., collaboration or information withholding) without retraining the model.

Non-stationarity. In social simulation, the reward process is inherently non-stationary: the counterpart agent adapts to the ego agent’s behavior, and the dialogue state evolves over turns. Therefore, we do not assume rewards are i.i.d. or drawn from a fixed distribution across optimization iterations; instead, we adopt an adversarial online learning perspective as a design rationale for robust strategy selection under distribution shift.

Feedback. After each round, we use an LLM evaluator to provide per-turn rewards $r _ { t } ^ { ( i ) } = \rho ( s _ { t } , a _ { t } ^ { ( i ) } )$ over M dimensions, which are normalized by $\phi _ { m }$ (Table 4), following prior LLM-evaluator-based social simulation work such as Sotopia-Ω (Zhang et al., 2025) and AML (Wang et al., 2025b). We use the resulting scalar reward (after aggregation/normalization) as the bandit feedback in Algorithm 1.

## 4.2. ALSO: Adversarial Online Strategy Optimization

To address strategy optimization in a large, discrete space under non-stationary social dynamics, we propose ALSO. ALSO follows an adversarial online learning design: it makes no stationarity assumptions about rewards, uses randomized selection to remain robust to shifting partner behaviors, and incorporates a recency mechanism to track drift. Concretely, ALSO combines an exponential-weights selector with a lightweight neural surrogate that generalizes sparse feedback across strategies. The LLM policy remains frozen; only the surrogate network is trained online.

The core logic of ALSO is organized into the following phases (including a preprocessing step): We denote by $a _ { t }$ the focal agent’s utterance and by $o _ { t }$ the counterpart response; $\mathcal { H } ^ { ( t ) }$ is the dialogue history up to turn t.

Arm Space (Alg. 1, Line 1–2). Before online interaction begins, we precompute an embedding for each augmented persona obtained by appending a candidate strategy to the base persona for computer efficiency. Concretely, for each $k \in [ K ]$ , we form $b ^ { ( k ) } = b ^ { 0 } \oplus \sigma _ { k }$ and compute $\mathbf { b } _ { k } = g ( b ^ { ( k ) } )$ . These embeddings are fixed across turns and serve as the strategy-specific representation used by the surrogate.

Context Encoding & Prediction (Alg. 1, Lines 5–6). At the beginning of each interaction turn t, the optimal strategy depends on the dialogue state. We use the frozen embedding model $g ( \cdot )$ to encode the dialogue history $\mathcal { H } ^ { ( t - 1 ) }$ into a context vector $\mathbf { c } ^ { ( t ) }$ . For each candidate strategy $\sigma _ { k } \in \Sigma .$ , we concatenate the precomputed augmented-persona embedding $\mathbf { b } _ { k }$ with $\mathbf { c } ^ { ( t ) }$ to form $\mathbf { x } _ { k } ^ { ( t ) }$ . A trainable value network $f _ { \theta } ( \cdot )$ predicts the expected reward $\hat { v } _ { k } ^ { ( t ) }$ for all arms:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Adversarial Online Strategy Optimization
Require: Strategy space $\Sigma = \{\sigma_1, \ldots, \sigma_K\}$ (candidate strategy instructions), base persona $b^0$ (fixed persona text), frozen embedding model $g(\cdot)$, trainable value network $f_\theta$, learning rate $\eta &gt; 0$, decay factor $\lambda \in (0,1]$, batch size $B$
Ensure: Sequence of selected strategies $\{\sigma_{k_t}\}_{t=1}^T$ (the strategy chosen at each turn $t$)
1: Precompute augmented-persona embeddings:
2: For all $k$, form $b^{(k)} \leftarrow b^0 \oplus \sigma_k$ and compute $\mathbf{b}_k \leftarrow g(b^{(k)})$
3: Initialize: $S_k^{(0)} \leftarrow 0$ for all $k$; replay buffer $\mathcal{D} \leftarrow \emptyset$; history $\mathcal{H}^{(0)} \leftarrow \emptyset$
4: for turn $t = 1$ to $T$ do
5: Context encoding: $\mathbf{c}^{(t)} \leftarrow g(\mathcal{H}^{(t-1)})$
6: Value prediction: compute $(\mathbf{x}_k^{(t)}, \hat{v}_k^{(t)})$ for all $k$ via Eq. 11
7: Strategy selection: compute $\pi^{(t)}$ and sample $k_t$ via Eq. 12
8: Interaction &amp; feedback: form augmented persona $b^{(t)} \leftarrow b^0 \oplus \sigma_{k_t}$ and execute $b^{(t)}$ to generate focal-agent action $a_t$; observe counterpart response $o_t$ and reward $r_t$; update $\mathcal{H}^{(t)} \leftarrow \mathcal{H}^{(t-1)} \cup \{a_t, o_t\}$
9: Surrogate update: add $(\mathbf{x}_{k_t}^{(t)}, r_t)$ to $\mathcal{D}$; sample a minibatch of size $B$ from $\mathcal{D}$ and update $f_\theta$ via MSE
10: Score smoothing: update $S_k^{(t)}$ for all $k$ via Eq. 13
11: end for
</div>

$$
\mathbf {x} _ {k} ^ {(t)} = [ \mathbf {b} _ {k}; \mathbf {c} ^ {(t)} ], \qquad \hat {v} _ {k} ^ {(t)} = f _ {\theta} (\mathbf {x} _ {k} ^ {(t)}).\tag{11}
$$

This provides a data-efficient inductive bias in early online learning, where only a small number of interactions are available.

Strategy Selection (Alg. 1, Lines 7). We maintain a cumulative score $S _ { k }$ for each arm and sample strategies from an exponential-weights distribution:

$$
\pi_ {k} ^ {(t)} \propto \exp \bigl (\eta   S _ {k} ^ {(t - 1)} \bigr), \qquad k _ {t} \sim \text { Categorical } (\pi^ {(t)}).\tag{12}
$$

Randomized selection is essential in the adversarial setting, where a greedy policy can be exploited or can overfit to transient dynamics.

Interaction & Surrogate Update (Alg. 1, Lines 8–9). After sampling $\sigma _ { k _ { t } }$ and observing the per-turn reward $r _ { t } .$ , we store $( \mathbf { x } _ { k _ { t } } ^ { ( t ) } , r _ { t } )$ in a replay buffer D and update $f _ { \theta }$ by minimizing an MSE loss. The surrogate improves sample efficiency by transferring supervision to semantically related strategies.

Score estimation. In classical EXP3, the exponentialweights sampling distribution is constructed from per-arm cumulative rewards. In our online social simulation setting, however, we only observe feedback for the selected strategy at each turn, and many candidate strategies (or their paraphrased variants) may never be played. This makes direct per-arm reward accumulation highly sample-inefficient, especially when the effective arm space is large. Motivated by prior prompt optimization work, we therefore use a lightweight neural surrogate $f _ { \theta }$ over pretrained embeddings to estimate scores for all arms from the current dialogue context. This provides dense score estimates to construct the exponential-weights distribution, and propagates sparse feedback across semantically related strategies while keeping the base LLM frozen.

Score Smoothing (Alg. 1, Lines 10). To explicitly track non-stationarity, we apply an exponential decay factor $\lambda \in \mathsf { \Gamma } ( 0 , 1 ]$ (set to λ = 0.9 in all experiments) so that recent evidence dominates historical estimates. This keeps $S _ { k } ^ { ( t ) }$ responsive to partner shifts while preventing outdated interactions from dominating the strategy distribution:

$$
S _ {k} ^ {(t)} = \lambda S _ {k} ^ {(t - 1)} + \hat {v} _ {k} ^ {(t)}.\tag{13}
$$

