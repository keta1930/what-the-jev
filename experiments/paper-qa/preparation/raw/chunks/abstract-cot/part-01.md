# Thinking Without Words: Efficient Latent Reasoning with Abstract Chain-of-Thought

Keshav Ramji<sup>∗</sup>, Tahira Naseem & Ramón Fernandez Astudillo IBM Research AI

# Abstract

While long, explicit chains-of-thought (CoT) have proven effective on complex reasoning tasks, they are costly to generate during inference. Nonverbal reasoning methods have emerged with shorter generation lengths by leveraging continuous representations, yet their performance lags behind verbalized CoT. We propose Abstract Chain-of-Thought, a discrete latent reasoning post-training mechanism in which the language model produces a short sequence of tokens from a reserved vocabulary in lieu of a natural language CoT, before generating a response. To make previously unseen “abstract” tokens useful, we introduce a policy iteration-style warm-up loop that alternates between (i.) bottlenecking from a verbal CoT via masking and performing supervised fine-tuning, and (ii.) self-distillation by training the model to generate abstract tokens from the prompt alone via constrained decoding with the codebook. After warm-up, we optimize the generation of abstract sequences with warm-started reinforcement learning under constrained decoding. Abstract-CoT achieves up to 11.6× fewer reasoning tokens while demonstrating comparable performance across mathematical reasoning, instruction-following, and multi-hop reasoning, and generalizes across language model families. We also find an emergent power law distribution over the abstract vocabulary, akin to those seen in natural language, that evolves across the training phases. Our findings highlight the potential for post-training latent reasoning mechanisms that enable efficient inference through a learned abstract reasoning language.

# 1 Introduction

Large language models (LLMs) increasingly rely on long, explicit chains-of-thought (CoTs) to solve complex, multi-step reasoning problems. Despite its effectiveness, verbalized CoT (Wei et al., 2022; Kojima et al., 2022) is an expensive mechanism, increasing latency and cost at inference while bloating the length of traces during reinforcement learning (RL). Prior works also suggest that verbalized CoT can be unfaithful (Lanham et al., 2023; Turpin et al., 2023), while leveraging a different latent reasoning process that is not communicated. These drawbacks have motivated approaches to compress or internalize natural language CoT with more efficient intermediate representations (Cheng & Durme, 2024; Deng et al., 2024). Simultaneously, approaches focusing on pause or filler tokens (Goyal et al., 2024; Pfau et al., 2024) suggest that their addition facilitates deliberate internalized thinking through its activations. Furthermore, the findings of DeepSeek-R1-Zero (Guo et al., 2025) indicate that strong performance can be separable from human-readability, demonstrating gains even with language mixing in the CoTs. Recent works such as Coconut (Hao et al., 2025) have sought to enable reasoning mechanisms through continuous concept spaces, balancing efficiency and expressivity through principled methods for internalized recurrence.

In this work, we study a simple question: can we replace long verbalized rationales with a short sequence of discrete abstract tokens that functions as a latent scratchpad, while retaining the performance gains of CoT in response generation? We find that not only is this possible, but it can be achieved purely through post-training instruction-tuned models. We propose Abstract Chain-of-Thought (Abstract-CoT): instead of generating natural language reasoning, we induce the model to emit a bounded-length sequence of tokens from a reserved abstract vocabulary of distinguishable filler tokens. Abstract-CoT is designed to be token-efficient and non-verbal, producing short intermediate traces while offering an alternative to rationales generated in natural language.

![](images/e4431e6d0c91201ad131aab45cf946f846b0015c7ba1f306cd313e72168d1bbc.jpg)

[Image: `.
-   **Output Box (Green/Blue):** "Answer: $d = 120 \text{ km}$"

**Right Side: Abstract Chain-of-Thought**
-   **Header:** "Abstract Chain-of-Thought"
-   **Input Box (Blue):** Same question as the left side.
-   **Reasoning Box (Purple):**
    -   Starts with `<beginabstract>`.
    -   Displays two rows of small purple tokens with letters/abbreviations on them (e.g., E, C, AE, F, A, BB, D, G, BA, H, AC, B, AD, F). These represent the abstract vocabulary mentioned in the prompt text.
    -   Ends with `<endabstract>`.
-   **Output Box (Green/Blue):** "Answer: $d = 120 \text{ km}$"

**Overall Structure:**
-   Two parallel columns showing the same problem solved via different reasoning paths.
-   Arrows indicate the flow from Question -> Reasoning -> Answer.
-   A vertical dashed line separates the two approaches.

**Drafting the description:**
The image presents a side-by-side comparison of two reasoning methods: "Verbalized Chain-of-Thought" on the left and "Abstract Chain-of-Thought" on the right, both solving the same math word problem about a car traveling between points A and B. The left column details a natural language step-by-step derivation using equations, progressing from defining a variable `d` to solving for the distance ($d=120$ km). The right column replaces the textual reasoning steps with a sequence of abstract tokens (e.g., "E", "C", "AE") enclosed within `<beginabstract>` and `<endabstract>` tags, resulting in the identical final answer. Both methods utilize the same input question and yield the same result box at the bottom.

**Refining based on constraints:**
-   2-4 sentences? Yes.
-   Objective? Yes.
-   English? Yes.

**Final Polish:**
The image illustrates a comparative diagram between "Verbalized Chain-of-Thought" and "Abstract Chain-of-Thought" methods applied to a physics word problem involving travel speeds and time. On the left, the verbalized approach shows a multi-step mathematical derivation where steps define variables and set up an equation ($\frac{d}{60} + 0.5 + \frac{d}{80} = 4$) to find the distance $d$. On the right, the abstract approach replaces these natural language steps with a sequence of short alphanumeric tokens (like E, C, AE) bounded by XML-style tags. Both pipelines process the same initial question and conclude with the same final answer: $d = 120 \text{ km}$.
</think>

The image illustrates a comparative diagram between "Verbalized Chain-of-Thought" and "Abstract Chain-of-Thought" methods applied to a physics word problem involving travel speeds and time. On the left, the verbalized approach shows a multi-step mathematical derivation where steps define variables and set up an equation ($\frac{d}{60} + 0.5 + \frac{d}{80} = 4$) to find the distance $d$. On the right, the abstract approach replaces these natural language steps with a grid of short alphanumeric tokens (like E, C, AE) bounded by XML-style tags. Both pipelines process the same initial question and conclude with the same final answer: $d = 120 \text{ km}$.]  
Figure 1: Verbalized vs. Abstract Chain-of-Thought. Verbalized CoT (left) generates an explicit natural language rationale (Step 1 through Step 8) inside <think> · · · </think> tags before producing the answer. Abstract CoT (right) instead emits a short sequence of tokens from the reserved abstract vocabulary inside <beginabstract> · · · <endabstract> delimiters, achieving the same answer with substantially fewer reasoning tokens.

However, adding previously unseen tokens creates a cold-start problem, as their embeddings are randomly initialized and meaningless initially. While these tokens appear semantically uninformative, our recipe aims to learn to produce a sequence of these tokens, inducing new pathways between a prompt and a response. To this end, we adopt a twostage training recipe. The first stage is a policy iteration warm-up, alternating between verbal CoT guidance and direct on-policy generation of abstract token sequences. In the former, the final response only attends to the abstract tokens, not to the verbal CoT, forcing abstract token representations to learn useful information from the verbal CoT, serving as an information bottleneck. We then perform self-distillation by discarding the verbal CoTs and training only with on-policy-generated abstract sequences with the learned representations, and repeat this process iteratively. In the second stage, we apply reinforcement learning with a generative reward model to induce exploration over abstract token sequences and refine the abstract generation policy. Our findings demonstrate substantial gains in token efficiency while matching or outperforming verbalized chain-of-thought.

We summarize our contributions below:

1. Abstract Chain-of-Thought: We propose Abstract-CoT, a mechanism for reasoning through a vocabulary of reserved tokens introduced entirely in LLM post-training.

2. Warm-up via Policy Iteration: We warm up the embeddings of the reserved tokens by alternating bottlenecked SFT and self-distillation, yielding an abstract generator.

3. Warm-started RL for Abstract Policies: We optimize generation of abstract traces using GRPO, with constrained decoding to the abstract vocabulary.

4. Token Efficiency: Abstract-CoT reduces reasoning tokens up to 11.6× while matching verbalized CoT performance on MATH-500, AlpacaEval, and HotpotQA.

5. Abstract Reasoning Language: We observe power-law dynamics over the abstract vocabulary, indicating that meaningful concepts and re-use patterns are learned.

# 2 Related Work

## 2.1 Filler Tokens

Works on filler tokens augment the token sequence with special tokens that are semantically uninformative (not human-readable natural language), but expand the model’s effective computation in the forward pass. Goyal et al. (2024) introduce <pause> tokens, showing that explicitly allocating intermediate tokens to allow for ”thinking time” can improve reasoning. Mu et al. (2023) propose gist tokens which serve as a learned bottleneck, summarizing longer contexts into a small set of activations that can be cached and reused, introducing contextual ”slots” that can hold task-relevant information. Other works suggest that such tokens can be used to expand expressivity limits (Pfau et al., 2024; Merrill & Sabharwal, 2025; London & Kanade, 2025), and used to cache preceding context for long-context retrieval (Shah et al., 2025). Our work also relates to parameter-efficient methods that seek to optimize continuous prompt embeddings to steer generations (Lester et al., 2021; Li & Liang, 2021), and tokenspace interventions that add intermediate representations (Jang et al., 2025). While our abstract tokens are introduced specifically as a latent reasoning trace (rather than as prompt compression), they share a similar essence that a small number of lightweight extra positions can be trained to store or carry additional information, offering a new reasoning medium.

## 2.2 CoT Compression, Distillation, and Discrete Codebooks

Compression, distillation, and partially removing the textual rationale (often through staged curricula) are some of the key mechanisms used to target the verbosity and cost of verbalized CoT. Early works such as Hsieh et al. (2023) demonstrated that explicit stepby-step rationales can be distilled to smaller models. Recent methods include seeking to directly shorten verbalized CoT via multi-round refinement (Yan et al., 2025) and learning to skip intermediate reasoning tokens in a controllable fashion while retaining generation quality (Xia et al., 2025).

Approaches that compress parts of the rationale into a learned discrete or quantized representation are somewhat related to our discrete codebook. Su et al. (2025) combines latent tokens (learned via vector quantization) with remaining text tokens, inducing an efficiency interpretability trade-off. Complementary works perform step-wise compression of CoT into latent tokens (Zhang et al., 2025a) as well as gradually internalizing explicit steps into implicit computation (Deng et al., 2024) in a curriculum fashion. By contrast, our abstract tokens are not a quantized reconstruction of a teacher rationale, but are entirely in a newly introduced reserved vocabulary, with the model trained to use it as a compact reasoning language under constrained decoding. This allows the model to potentially explore other reasoning pathways, rather than being constrained to that of the teacher CoT.

## 2.3 Continuous and Hybrid Latent Reasoning

Some recent approaches seek to replace parts of the textual rationale with continuous thought states. Coconut (Hao et al., 2025) replaces some CoT tokens with continuous latent vectors derived from hidden states and trains the language model with a curriculum that gradually increases the latent segment and replaces verbalized CoT segments. CODI (Shen et al., 2025) similarly compresses CoT into a continuous space, using self-distillation to align latent trajectories with those induced by explicit rationales. System-1.5 reasoning (Wang et al., 2025) introduces dynamic shortcuts, traversing between language and latent spaces while aiming to reduce unnecessary verbal reasoning and retain controllability.

Related “soft” thinking approaches propagate intermediate representations by feeding distributions over embeddings as subsequent inputs (Xu et al., 2025; Zhang et al., 2025b). Recent works such as Butt et al. (2025) study training and optimization stability when such soft tokens are treated as decision variables through RL. Hybrid methods such as HybridCoT (Shen et al., 2026) explicitly interleave latent and text tokens to balance efficiency with partial interpretability. In our work, we suggest that it is possible to achieve the efficiency gains associated with latent reasoning while operating fully in the discrete token space.

## 2.4 Reinforcement Learning for Budget Control

A complementary direction focuses on controlling inference-time cost by explicitly optimizing the reasoning budget, which is often operationalized as the length of intermediate reasoning traces. Recent work applies RL to learn when to expend additional reasoning steps as opposed to answering early; for example, by learning adaptive chain-of-thought triggering policies under compute constraints (Lou et al., 2025), or by pruning or shortening intermediate reasoning via training-time objectives that directly reward efficiency (Hou et al., 2026). Other recent approaches optimize a length-accuracy trade-off with RL objectives, by allocating token budgets dynamically (Kleinman et al., 2025) or by explicitly optimizing for consistency with user-specified length constraints (Aggarwal & Welleck, 2025).

While our RL stage is most closely aligned with this line of work, it differs in the action space: instead of optimizing over free-form textual CoT length, we optimize over sequences constrained to a reserved discrete codebook. This enables control over the intermediate sequence while avoiding the brittleness of length control in open-ended natural language.

# 3 Latent Reasoning with Abstract Chain-of-Thought

## 3.1 Problem Setup and Notation

Let x, c, and y denote a prompt, gold verbal chain-of-thought (CoT), and the target answer, respectively. We assume training data $\mathcal { D } = \{ ( x _ { i } , c _ { i } , y _ { i } ) \} _ { i = 1 } ^ { N } .$ , where c<sub>i</sub> is only available during the first phase of warm-up. Let $\pi _ { \theta }$ be a causal decoder-only LLM with parameters θ and base vocabulary V. We extend the tokenizer with a set of M previously unseen (reserved) tokens in the abstract codebook, along with two delimiters <beginabstract> and <endabstract>, marking the abstract reasoning segment<sup>1</sup>:

$$
\mathcal {V} _ {\mathrm{abs}} = \left\{\langle \text {TOKEN\_A} \rangle , \langle \text {TOKEN\_B} \rangle , \dots , \langle \text {TOKEN\_Z} \rangle , \langle \text {TOKEN\_AA} \rangle , \dots \right\},
$$

Thus, an abstract chain-of-thought is a token sequence $z = ( z _ { 1 } , \dots , z _ { m } ) \in \mathcal { V } _ { a b s } ^ { m }$ , formatted as:

$$
\tilde {z} = \langle \text {   beginabstract   } \rangle z _ {1} z _ {2} \dots z _ {m} \langle \text {   endabstract   } \rangle
$$

We denote the maximum length of the abstract sequence by $m \le m _ { \mathrm { m a x } } ;$ at inference-time, the model receives x and must generate z˜ and y without access to c. Let Z denote the positions of the full abstract sequence z˜ (including <beginabstract> and <endabstract>), and let $\mathcal { Z } _ { \mathrm { a b s } } \subseteq \mathcal { Z }$ denote the positions of the m codebook tokens $z _ { 1 } , \dotsc , z _ { m } \in \mathcal { V } _ { \mathrm { a b s } }$

We view the abstract trace z as a discrete latent variable, mediating reasoning. Ideally, we would like to maximize the marginal likelihood:

$$
\log \pi_ {\theta} (y \mid x) = \log \sum_ {z \in \mathcal {V} _ {\mathrm{abs}} ^ {*}} \pi_ {\theta} (z \mid x) \pi_ {\theta} (y \mid x, z)\tag{1}
$$

for a sequence of length $\iota \leq m _ { \mathrm { m a x } } ,$ , but the sum over discrete traces is intractable. Therefore, Abstract Chain-of-Thought uses a bootstrapping procedure that alternates (i) proposing an abstract trace $z \in \mathcal { V } _ { \mathrm { a b s } } ^ { * }$ with verbal CoT guidance, and (ii) updating the model given the generated trace, followed by distillation to learn to directly propose traces from x alone.

## 3.2 Warm-Up via Policy Iteration

The abstract tokens start with randomly initialized embeddings, so the model initially cannot exploit the bottleneck in the absence of a prior that enforces specific concept mappings.

![](images/4e05680cbecd594a6934e468d309f6b7a942290d9d90490a08c14ed700b6fa48.jpg)

[Image: This figure outlines a two-part machine learning training framework, beginning with a "Policy Iteration Warm-up Loop" on the left that transitions into "Warm-Started Reinforcement Learning" on the right. The left component features a cyclic process comprising "Bottlenecked SFT," which aligns inputs with Abstract Chain-of-Thought (CoT) sequences using a block-structured attention mask, and "Self-Distillation," where an initial policy $\pi_\theta$ performs on-policy generation. The right component details "GRPO with Constrained Decoding," illustrating how an input splits into multiple rollouts (from 1 to $k$) of Abstract CoT and responses, which are subsequently processed by a Reward Model alongside a Gold Response.]  
Figure 2: Abstract Chain-of-Thought: The training recipe consists of two stages: (i.) a warm-up loop, consisting of a Bottlenecked SFT phase with guidance from a teacher Verbal CoT, and a Self-Distillation phase with on-policy abstract sequence generation, repeated iteratively, and (ii.) reinforcement learning using GRPO with constrained decoding for the rollouts, which rewards abstract sequences that lead to a high-quality response.

Therefore, we perform an abstract embedding warm-up with a policy iteration loop over iterations $t = 1 , \dots , T ;$ each iteration produces a dataset of abstract trajectories $\tilde { z } ^ { ( t ) }$ and updates θ via SFT. The training dataset D is staged over the iterations: $\mathcal { D } = \bigcup _ { t = 1 } ^ { T } \{ ( \mathcal { D } _ { t , 1 } , \mathcal { D } _ { t , 2 } ) \} )$

Constrained Decoding. We use $\pi _ { \theta } ^ { \mathrm { a b s } }$ to denote the policy restricted to an allowed token set $\mathcal { A } = \mathcal { V } _ { \mathrm { a b s } } \cup \{ \mathrm { < e n d a b s t r a c t > } \}$ which can be generated. At each step $i ,$ with context $h = x \cup$ {<beginabstract>} $\cup \ \tilde { z } _ { < i }$ , and $\textstyle \pi _ { \theta } ^ { \mathrm { a b s } } ( a \mid h ) = \frac { \pi _ { \theta } ( a \mid h ) \mathbf { 1 } [ a \in \mathcal { A } ] } { \sum _ { u \in \mathcal { A } } \pi _ { \theta } ( u \mid h ) }$ . We enforce a hard cap

$m _ { \mathrm { m a x } }$ of codebook tokens that may be generated; if $m = m _ { \mathrm { m a x . } }$ , we force the end delimiter to be generated, then allow the response to be produced without constrained decoding.

(1) Bottlenecked SFT with Abstract Tokens. Given $\left( x , c , y \right)$ , we construct $\tilde { z } ^ { ( t ) }$ using a policy $\phi _ { t }$ . In the first iteration, we use random initialization; with S steps in the verbal CoT, we sample a random number of abstract tokens per CoT step $( \mathrm { r a n d } ( 1 , \frac { | \ell | } { 2 } )$ for |ℓ| tokens in step $\ell \in S )$ and choosing the specific tokens uniformly at random from $\mathcal { V } _ { \mathrm { a b s } } .$ . We analyzed other initialization schemes (alphabetically cycling through the tokens, enforcing a power-law distribution), and found a uniform distribution over the tokens to be most effective. In subsequent iterations $( t \geq 2 ) .$ , abstract sequences are generated on-policy: $\tilde { z } ^ { ( t ) } \sim \pi _ { \theta } ^ { \mathrm { a b s } } ( \cdot \mid x , c )$ under constrained decoding.

We form a single concatenated training sequence $s = [ x \ ; c \ ; \tilde { z } \ ; y ]$ and define a blockstructured attention mask A that enforces an information bottleneck. Let indices be partitioned into prompt (X), verbal CoT (C), abstract sequence (Z) and answer (Y). The abstract tokens attend to the prompt and the verbal CoT; that is:

$$
\mathcal {A} _ {i, j} = 1 \forall i \in \mathcal {Z}, j \in \mathcal {X} \cup \mathcal {C} \cup \mathcal {Z} _ {\leq i}
$$

Crucially, the answer only attends to the prompt and the abstract tokens, not to the verbal CoT, with all other entries following standard causal masking:

$$
\mathcal {A} _ {i, j} = \left\{ \begin{array}{l l} 1 & i \in \mathcal {Y}, j \in \mathcal {X} \cup \mathcal {Z} \cup \mathcal {Y} _ {\leq i} \\ 0 & i \in \mathcal {Y}, j \in \mathcal {C} \end{array} \right.
$$

Concretely, this training procedure can be seen as implementing a discrete latent bottleneck; let $H _ { \mathcal { Z } _ { \mathrm { a b s } } }$ denote the hidden states at the abstract token positions $\mathcal { Z } _ { \mathrm { a b s } }$ produced from the prefix $[ x ; c ; \tilde { z } ]$ following masking of the verbal CoT. The only dependence of answer generation (y) on the verbal CoT (c) is through $H _ { \mathcal { Z } _ { \mathrm { a b s } } } ,$ , inducing conditional Markov structure:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Policy Iteration Warm-Up for Abstract-CoT

Require: Training data $\mathcal{D} = \{(x, c, y)\}$, abstract vocabulary $\mathcal{V}_{\text{abs}}$, iterations $T$

1: Initialize $\theta^{(0)}$ from base instruction-tuned model; add new token embeddings for $\mathcal{V}_{\text{abs}}$

2: for $t = 1$ to $T$ do

3: Data for current iteration: $\mathcal{D}_{t,1}, \mathcal{D}_{t,2} \subset \mathcal{D}^{(t)}$

4: Generate abstract traces $\tilde{z}^{(t)} \sim \phi_t (\cdot \mid x, c, \theta^{(t-1)})$ (random if $t=1$, else constrained decoding with $\phi_t = \pi_{\theta^{(t-1)}}$ for $(x, c, y) \in \mathcal{D}_{t,1}$

5: Update $\bar{\theta}^{(t)} \leftarrow \arg \min_{\theta} \mathbb{E}_{(x, c, y) \sim \mathcal{D}_{t,1}} [\mathcal{L}_{\text{SFT}}(\theta; x, c, \tilde{z}^{(t)}, y; A)]$

6: Distill: generate $\tilde{z}' \sim \pi_{\bar{\theta}^{(t)}}^{\text{abs}} (\cdot \mid x)$ for $(x, y) \in \mathcal{D}_{t,2}$

7: Starting from $\bar{\theta}^{(t)}$, update $\theta^{(t)} \leftarrow \arg \min_{\theta} \mathbb{E}_{(x, y) \sim \mathcal{D}_{t,2}} [\mathcal{L}_{\text{Distill}}(\theta; x, \tilde{z}', y)]$

8: end for

9: return $\theta^{(T)}$
</div>

$$
C \rightarrow H _ {\mathcal {Z} _ {\mathrm{abs}}} \rightarrow Y (\text { conditioned   on } X \text { and } Z)
$$

By the data processing inequality, any dependence between y and c must be bounded by the information that can be transmitted through the abstract segment:

$$
I (C; Y \mid X, Z) \leq I (C; H _ {Z _ {\mathrm{abs}}} \mid X, Z)\tag{2}
$$

Since $H _ { \mathcal { Z } _ { \mathrm { a b s } } }$ scales linearly with the abstract sequence length m, tuning $m _ { \mathrm { m a x } }$ affects the channel capacity from c to y during warm-up.

We then optimize a masked SFT objective that trains on the abstract sequence<sup>2</sup> and the answer while hiding the verbal CoT with bottleneck attention mask A:

$$
\mathcal {L} _ {\mathrm{SFT}} (\theta ; x, c, \tilde {z}, y) = - \sum_ {j \in (\mathcal {Z} _ {\mathrm{abs}} \cup \mathcal {Y})} \log \pi_ {\theta} \left(s _ {j} \mid s _ {<   j}; \mathcal {A}\right),\tag{3}
$$

(2) Self-Distillation Without Verbal CoT. The bottlenecked SFT stage exploits c to shape the hidden states at abstract-token positions, but our target policy ultimately should produce abstract tokens from the prompt alone; this motivated the loss computation on $\tilde { z } ^ { ( t ) }$ . We create a distillation dataset by generating $\tilde { z } \sim \pi _ { \theta } ^ { \mathrm { a b s } } ( \cdot \mid x )$ via constrained decoding (with $m \leq m _ { \mathrm { m a x } } )$ and pairing it with the gold answer y: $\mathcal { D } _ { \mathrm { d i s t i l l } } ^ { ( t ) } = \{ ( x _ { i } , \tilde { z } _ { i } , y _ { i } ) \} _ { i = 1 } ^ { N }$ . In the discrete latent bottleneck interpretation, the self-distillation and RL (Section 3.3) phases tune the model’s inference-time thinking budget. We train with standard causal SFT on $[ x ; \tilde { z } ; y ]$ where $s _ { j }$ spans the abstract and response tokens:

$$
\mathcal {L} _ {\text { Distill }} (\theta ; x, \tilde {z}, y) = - \sum_ {j \in (\mathcal {Z} _ {\text { abs }} \cup \mathcal {Y})} \log \pi_ {\theta} (s _ {j} \mid s _ {<   j})\tag{4}
$$

## 3.3 Reinforcement Learning from Warm-Start

After the warm-up stage, we optimize the abstract-token policy with RL; we refer to this as warm-started RL. In practice, this is implemented in a similar manner as the warm-up self-distillation phase: (1) generate z˜ under a guided-regex constraint, and (2) append <endabstract> and decode y unconstrained. Our default GRPO (Shao et al., 2024) updates include log-probabilities for both the abstract trace and the answer tokens, improving response quality after RL in addition to shaping the intermediate abstract sequence<sup>3</sup>. We use a generative reward model – specifically, gpt-oss-20b (OpenAI, 2025) – to score outputs in our experiments, for our recipe to generalize to non-verifiable, natural language settings.

For each prompt $x ,$ we sample a group of K trajectories $\{ ( \tilde { z } _ { k } , y _ { k } ) \} _ { k = 1 } ^ { K }$ by first drawing $\widetilde { z } _ { k } \sim \pi _ { \theta } ^ { \mathrm { a b s } } ( \cdot \mid x )$ , then $y _ { k } \sim \pi _ { \theta } ( \cdot \ | \ x , \tilde { z } _ { k } )$ , and computing rewards $\hat { R } _ { k } = \hat { R } ( x , \tilde { z } _ { k } , y _ { k } )$ . We define advantages:

$$
A _ {k} = \frac {\hat {R} _ {k} - \mathrm{mean} (\hat {R} _ {1 : K})}{\mathrm{std} (\hat {R} _ {1 : K}) + \epsilon}
$$

We update θ via applying GRPO to an action space over $\left( \tilde { z } , y \right)$

$$
\begin{array}{r l} & {\mathcal {J} (\theta) = \mathbb {E} _ {x} \bigg [ \frac {1}{K} \sum_ {k = 1} ^ {K} A _ {k} \Big (\sum_ {t \in \mathcal {Z} _ {\mathrm{abs}}} \log \pi_ {\theta} ^ {\mathrm{abs}} (z _ {k, t} \mid x, z _ {k, <   t}) + \sum_ {t \in \mathcal {Y}} \log \pi_ {\theta} (y _ {k, t} \mid x, \tilde {z} _ {k}, y _ {k, <   t}) \Big)} \\ & {- \beta \operatorname{KL} \Big (\pi_ {\theta} ^ {\mathrm{abs}} (\tilde {z} \mid x) \pi_ {\theta} (y \mid x, \tilde {z}) \left\| \pi_ {\theta_ {\mathrm{ref}}} ^ {\mathrm{abs}} (\tilde {z} \mid x) \pi_ {\theta_ {\mathrm{ref}}} (y \mid x, \tilde {z})\right) \bigg ].} \end{array}\tag{5}
$$

where $\pi _ { \theta _ { \mathrm { r e f } } }$ is the reference policy (the warm-started model). KL regularization is applied over both the abstract and the response distributions.

