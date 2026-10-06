# 5 CARA: COHERENT ADAPTIVE REASONING AGENTS

As described earlier, CARA (Coherent Adaptive Reasoning Agents) implements the reflect operation. Given the long-term memory bank built and maintained by TEMPR, CARA turns retrieved facts and observations into preference-conditioned reasoning and a layer of explicitly stored opinions that can change over time. CARA treats an agent’s behavioral profile as a first-class part of the system configuration rather than as a one-off prompt decoration. Each memory bank is associated with a configurable disposition profile (skepticism, literalism, empathy) and a concise background description, and CARA uses this profile when forming and updating opinions over the world and experience networks.

Concretely, CARA provides four key capabilities: disposition-profile integration, HINDSIGHT memory integration, opinion formation and reinforcement, and background merging with conflict resolu tion.

## 5.1 MOTIVATION

To motivate CARA, consider two configurations of the same agent discussing remote work.

In the first configuration, given a behavioral profile with low skepticism $( S = 1 )$ , flexible interpretation $( L = 2 )$ , and high empathy $( E = 5 )$ , an agent might form the opinion: “Remote work enables creative flexibility and spontaneous innovation.”

In the second configuration, given high skepticism $( S = 5 )$ , highly literal interpretation $( L = 5 )$ , and low empathy $( E = 1 )$ , the same facts might instead yield: “Remote work lacks the structure and accountability needed for consistent performance.”

Both configurations access identical factual information from the HINDSIGHT memory bank, but their behavioral profiles bias how they weight different aspects (viz. flexibility vs. structure) and what conclusions they draw. CARA provides a mechanism to specify such behavioral profiles and to systematically shape opinion formation and updating as a function of these configuration choices.

## 5.2 PREFERENCE MODEL

CARA first defines a preference space that can be parameterized and verbalized for prompting.

### 5.2.1 DISPOSITION PARAMETERS

We use a three-dimensional disposition space as an interpretable set of ordered preference dimensions. Let $\Theta = ( S , L , E , \beta )$ denote a behavioral profile where:

$$
S \in \{1, \dots , 5 \} \quad (\text { Skepticism }; 1 = \text { trusting }, 5 = \text { skeptical })\tag{18}
$$

$$
L \in \{1, \dots , 5 \} \quad (\text { Literalism }; 1 = \text { flexible }, 5 = \text { literal })\tag{19}
$$

$$
E \in \{1, \dots , 5 \} \quad (\text { Empathy }; 1 = \text { detached }, 5 = \text { empathetic })\tag{20}
$$

$$
\beta \in [ 0, 1 ] \quad (\text { Bias   strength:   controls   influence   of   preferences })\tag{21}
$$

The bias strength parameter $\beta$ controls how strongly the behavioral profile should shape opinion formation. When $\beta = 0$ , reasoning is primarily fact-based. When $\beta = 0 . 5$ , there is moderate influence from the behavioral profile. When $\beta = 1$ , there is strong preference-conditioned behavior.

Rationale for using Disposition Parameters. We adopt these dimensions because they offer a compact, interpretable parameterization of reasoning style (trusting vs. skeptical, flexible vs. literal, detached vs. empathetic), intuitive axes that can be verbalized in prompts $( \mathrm { e . g . }$ ., “skeptical but highly empathetic”), and a simple interface for users configuring different agent styles.

Intended Effects on Reasoning. CARA uses the behavioral profile to modulate prompts so that different configurations encourage different emphases when forming opinions. The mapping from preference values to reasoning behavior is achieved through natural language verbalization in system prompts. Higher Skepticism encourages more cautious evaluation of claims, greater emphasis on evidence quality, and reluctance to accept unsupported statements; lower Skepticism encourages more trusting and exploratory behavior. Similarly, higher Literalism encourages closer attention to exact wording and explicit instructions; lower Literalism encourages reading between the lines, inferring implicit goals, and using abstraction. Finally, higher Empathy encourages taking emotional context and interpersonal impact into account, using more supportive and face-saving language; lower Empathy encourages more blunt, task-first communication.

## 5.3 BANK PROFILE STRUCTURE

Each memory bank has an associated profile that encodes the agent’s identity and disposition configuration in a form suitable for prompting and reasoning. Formally, a bank profile is a tuple:

$$
P = (n, \Theta , h)\tag{22}
$$

where n is the agent’s name, $\Theta = ( S , L , E , \beta )$ is the behavioral profile, and h is a short background description written in the first person.

![](images/1927f036045fba0fd048ed95ae273ae7569e1ede2da8e5ded8c11ab66c9a1755.jpg)

[Image: This flowchart depicts an automated agent workflow beginning with an "Input Query" that initiates memory recall and context construction within a central processing block. Parallel to this, an "Agent Profile" is loaded based on specific dispositions (such as skepticism or empathy) and background details, which alongside the built context, conditions the subsequent "LLM Generation" phase. The system ultimately produces a "Final Response" while engaging in a feedback loop where the generated output updates the internal "Memory Store" by creating or adjusting stored opinions and observations.]  
Figure 4: CARA’s reflect loop. Given an input query, the agent recalls memories via TEMPR, builds context, loads the bank-specific profile (background and disposition), and performs dispositionconditioned generation, updating opinion and observation memories.

### 5.3.1 PREFERENCE DESCRIPTION GENERATION

The numeric behavioral profile Θ is verbalized into natural language so it can be injected into system messages. Let $\phi : \Theta \to$ String be a verbalization function that converts numeric values to descriptive text. For example:

ϕ(Θ) = “You are generally trusting, interpret language flexibly, and are highly empathetic ..."

(23)

This verbalization connects the numeric preference configuration to the LLM’s behavior by providing an explicit description of how the agent is intended to reason and communicate.

## 5.4 OPINION NETWORK AND OPINION FORMATION

### 5.4.1 OPINION STRUCTURE

Opinions are stored in the opinion network O, separate from world and bank facts. Each opinion is a self-contained memory that records both the judgment and the context in which it was formed. Formally, an opinion is a tuple:

$$
o = (t, c, \tau , b, \mathcal {E})\tag{24}
$$

where t is the opinion statement (including a brief rationale), $c \in [ 0 , 1 ]$ is the confidence score representing strength of conviction, τ is the timestamp when the opinion was formed, b is the bank identifier, and E is the set of entities mentioned in the opinion.

### 5.4.2 OPINION FORMATION PROCESS

Opinion formation sits at the interface between TEMPR and CARA (Figure 4). When a query calls for a subjective judgment, CARA performs the following steps (see Appendix A.2 for the complete opinion formation prompt template): 1) use TEMPR to retrieve relevant world facts and experiences (and any existing opinions) for the query $Q ,$ , where $\mathcal { F } _ { Q } = \mathop { \mathrm { R e c a l l } } ( B , Q , k )$ is the retrieved set; 2) construct a system message s that includes the bank’s name n, background h, and verbalized behavioral profile ϕ(Θ); 3) run a reflect step in which the LLM produces both a natural language answer r and candidate opinion updates, where the generation is conditioned on s, $\mathcal { F } _ { Q }$ , and the behavioral profile Θ; and 4) parse the structured output and store any new or updated opinions in the opinion network O.

![](images/65ac1780c80ba7d468a117eef9810d59d4b4a58237f30844c218ab2ed1a598c6.jpg)

[Image: The image presents two cards illustrating contrasting behavioral profiles, labeled "Trusting, Flexible, Empathetic Profile" with scores $(S=1, L=2, E=5)$ and "Skeptical, Literal, Detached Profile" with scores $(S=5, L=5, E=1)$. Each card provides a generated opinion on remote work; the first characterizes it as a net positive offering autonomy, while the second views it as a risk to consistency requiring structure. Distinct emphasis keywords are listed for each, highlighting concepts like "creative freedom" versus "accountability" to demonstrate how specific parameter combinations shape the content of the generated response.]  
Figure 5: Example of preference-conditioned opinion formation. Two agents with opposite behavioral profiles access identical facts about remote work but form different opinions based on their configured disposition parameters.

The behavioral profile Θ and its bias-strength parameter $\beta$ determine how strongly this reflect step is encouraged to lean into the configured style. For low bias values $( \beta \approx 0 )$ , system messages emphasize objectivity and downplay stylistic constraints. For intermediate values $( \beta \approx 0 . 5 )$ , they balance factual neutrality with preference-conditioned behavior. For high bias values $( \beta \approx 1 )$ , prompts explicitly encourage stronger, more opinionated language aligned with the specified preferences.

Each opinion formed in this way includes a confidence score $c \in [ 0 , 1 ]$ , which we interpret as belief strength. Values near 1.0 indicate very strong conviction, mid-range values indicate moderate or tentative beliefs, and low values indicate weak, easily revisable views. This scalar makes it possible to track not only what the agent believes, but also how firmly it holds those beliefs, which is important when opinions are later reinforced or revised as new evidence arrives.

Figure 5 illustrates how different behavioral profiles lead to systematically different opinions when presented with the same factual evidence.

## 5.5 OPINION REINFORCEMENT

So far, we have described how CARA forms new opinions. In a long-lived system, those opinions should also be able to evolve as new information is retained. When new facts arrive via TEMPR’s retain pathway, CARA updates any related opinions in three steps:

1) Identify Candidates. Use entity overlap and semantic similarity to find opinions that are plausibly related to the new facts. For each new fact f with entities $\mathcal { E } _ { f }$ and embedding $v _ { f }$ , we identify candidate opinions:

$$
\mathcal {O} _ {\text { cand }} = \{o \in \mathcal {O}: | \mathcal {E} _ {o} \cap \mathcal {E} _ {f} | > 0 \text {   or   } \text { sim } (v _ {o}, v _ {f}) > \theta \}\tag{25}
$$

where sim $( v _ { o } , v _ { f } )$ is the cosine similarity between the opinion and fact embeddings, and $\theta$ is a similarity threshold.

2) Assess the Evidence. For each candidate opinion $o \in \mathcal { O } _ { \mathrm { c a n d } } ,$ classify the relationship between the new facts and the current opinion. Let Assess $( o , f )$ be a function that returns one of {reinforce, weaken, contradict, neutral} based on LLM analysis of the relationship.

3) Apply an Update. Adjust the opinion’s confidence score (and, for strong contradictions or refinements, optionally its text) according to the assessed relationship. Let c be the current confidence and $c ^ { \prime }$ be the updated confidence. The update rule is:

```txt
Background Merging Example
Current Background:
“I was born in Colorado.”
New Snippet:
“You were born in Texas and have 10 years of startup experience.”
Merged Background:
“I was born in Texas and have 10 years of startup experience.”
```  
Figure 6: Example of background merging. The conflicting birthplace is resolved in favor of the new information, and the new work-history detail is added.

$$
c ^ {\prime} = \left\{ \begin{array}{l l} \min (c + \alpha , 1. 0) & \text { if   } \operatorname{Assess} (o, f) = \text { reinforce } \\ \max (c - \alpha , 0. 0) & \text { if   } \operatorname{Assess} (o, f) = \text { weaken } \\ \max (c - 2 \alpha , 0. 0) & \text { if   } \operatorname{Assess} (o, f) = \text { contradict } \\ c & \text { if   } \operatorname{Assess} (o, f) = \text { neutral } \end{array} \right.\tag{26}
$$

where $\alpha \in ( 0 , 1 )$ is a step size parameter. For contradicting evidence, we may also update the opinion text t to reflect the new nuance.

The update logic is designed to keep opinion trajectories stable but responsive. Small amounts of evidence lead to small changes, preventing opinions from oscillating in response to individual examples, while repeated reinforcement or strong contradictions can substantially shift the confidence. The behavioral profile can also influence how quickly opinions move (for example, a more cautious configuration may use a smaller α), although we leave detailed exploration of such settings to future work.

Overall, reinforcement ensures that opinions reflect both the system’s initial configuration (via the behavioral profile Θ) and its subsequent evidence, rather than being fixed at creation time or overwritten wholesale when new information appears.

## 5.6 BACKGROUND MERGING

In addition to opinions, an agent’s background description h evolves as users provide more biographi cal information. If handled naively, this can quickly lead to contradictions or unwieldy, concatenated prompts.

Over time, new background snippets may complement existing information (e.g., adding work history where none existed), conflict with prior statements (e.g., “born in Texas” vs. “born in Colorado”), or refine previous information (e.g., “works in tech” vs. “works as a machine learning engineer at a startup”).

To keep the background coherent, CARA uses an LLM-powered merging procedure. Given the current background h and a new snippet $h _ { \mathrm { n e w } }$ , we prompt the model to produce a revised background $h ^ { \prime }$ that 1) resolves direct conflicts in favor of the new information when appropriate, 2) appends non-conflicting details to enrich the description, 3) maintains a consistent first-person voice ${ ( ^ { 6 6 } \Gamma ^ { 5 } }$ rather than “You”), and 4) remains concise (e.g., targeting a length under a few hundred characters).

Formally, the merging function is:

$$
h ^ {\prime} = \mathbf {M e r g e} _ {\mathrm{LLM}} (h, h _ {\mathrm{new}})\tag{27}
$$

Figure 6 illustrates this process. As a preprocessing step, user-provided snippets are normalized into first person before merging, so that inputs such as “You are a creative engineer” become “I am a creative engineer.” This keeps the internal representation consistent with the way backgrounds are referenced in prompts. By maintaining a single, merged background per bank, CARA keeps identity information compact and coherent even as new biographical details accumulate over time.

## 5.7 PREFERENCE-CONDITIONED REASONING EXAMPLES

We conclude this section with brief examples showing how CARA produces distinct and evolving viewpoints using the same underlying memory.

### 5.7.1 EXAMPLE: OPINION EVOLUTION

CARA’s reinforcement mechanism also supports opinion change over time. Suppose a bank starts with the opinion:

$$
o _ {0} = \left(" \text { Python   is   the   best   general - purpose   language   for   data   science }", c _ {0} = 0. 7 0, \tau_ {0}\right)\tag{28}
$$

As new facts are retained via TEMPR, related evidence can strengthen or weaken this belief. For instance, a fact about Python’s dominant ecosystem in AI/ML might lead to a modest increase in confidence:

$$
o _ {1} = \left(" \text { Python   is   the   best   general - purpose   language   for   data   science }", c _ {1} = 0. 8 5, \tau_ {1}\right)\tag{29}
$$

Later facts about performance advantages and growing adoption of alternatives (e.g., Julia or Rust in certain domains) might decrease confidence and encourage a more qualified opinion:

$$
o _ {2} = \left(" \text { Python   is   strong   for   data   science   but   has   trade - offs }", c _ {2} = 0. 5 5, \tau_ {2}\right)\tag{30}
$$

In this way, opinions become trajectories rather than static labels. They start from an initial, preferenceconditioned formation step and are subsequently adjusted as new evidence accumulates.

Taken together, these mechanisms show how CARA turns the static memory structures provided by TEMPR into a configurable, preference-conditioned reasoning process. In Section 6, we combine TEMPR and CARA into the unified HINDSIGHT architecture and examine the end-to-end properties and empirical behavior of the full system.

# 6 PUTTING IT ALL TOGETHER: UNIFIED HINDSIGHT ARCHITECTURE

We have now described TEMPR, which implements Hindsight’s retain and recall operations (Section 4), and CARA, which implements the reflect operation (Section 5). In this section, we show how these components compose into a single end-to-end system and highlight the system-level properties that emerge from their interaction. At a high level, Hindsight turns raw conversational input into a structured memory bank and then uses that bank to support preference-conditioned reasoning over time.

## 6.1 INTEGRATION: RETAIN, RECALL, REFLECT

The Hindsight system integrates TEMPR and CARA into a unified architecture centered on three core operations. We summarize each operation here for completeness, using the same definitions introduced in Section 3.

Retain. The retain operation stores information into memory banks. Formally, given a memory bank B and input data D, the retain function is:

$$
\operatorname{Retain} (B, D) \to \mathcal {M} ^ {\prime} = \{\mathcal {W} ^ {\prime}, \mathcal {B} ^ {\prime}, \mathcal {O} ^ {\prime}, \mathcal {S} ^ {\prime} \}\tag{31}
$$

where M<sup>′</sup> is the updated four-network memory structure. The retain pipeline performs the following steps: 1) LLM-powered fact extraction with temporal ranges to convert D into a set of structured facts $\mathcal { F } \overset { \cdot } { = } \{ f _ { 1 } , \ldots , \dot { f } _ { n } \} ; 2 )$ entity recognition and resolution to map entity mentions to canonical entities $E ;$ 3) graph link construction to create edges of type temporal, semantic, entity, and causal in the memory graph $\mathcal { G } = ( V , E )$ ; 4) automatic opinion reinforcement for existing beliefs when new evidence arrives, where for each opinion $o \in \mathcal { O }$ , we identify related new facts and update the confidence score according to the reinforcement rules defined in Section 5; and 5) background merging to keep the bank profile coherent over time using the merging function $h ^ { \prime } = \mathop { \mathrm { M e r g e } _ { \mathrm { L L M } } } ^ { } ( h , h _ { \mathrm { n e w } } )$

Recall. The recall operation retrieves memories using multi-strategy search. Formally, given a memory bank B, query $Q .$ , and token budget k, the recall function is:

$$
\operatorname{Recall} (B, Q, k) \rightarrow \left\{f _ {1}, \dots , f _ {n} \right\}\tag{32}
$$

where $\textstyle \sum _ { i = 1 } ^ { n } | f _ { i } | \leq k$ and the returned facts are ordered by relevance. The recall pipeline performs the following steps: 1) four-way parallel retrieval (semantic, keyword, graph, temporal) to generate candidate sets $R _ { \mathrm { s e m } } , R _ { \mathrm { b m } 2 5 } , R _ { \mathrm { g r a p h } } , R _ { \mathrm { t e m p } } ;$ 2) Reciprocal Rank Fusion to combine ranked lists using

$$
\operatorname{RRF} (f) = \sum_ {R \in \left\{R _ {\text {sem}}, R _ {\text {bm25}}, R _ {\text {graph}}, R _ {\text {temp}} \right\}} \frac {1}{k + \operatorname{rank} _ {R} (f)}\tag{33}
$$

3) neural cross-encoder reranking for final precision using $\operatorname { C E } ( Q , f )$ scores; and $^ { 4 ) }$ token budget filtering to ensure $\begin{array} { r } { \sum _ { i = 1 } ^ { n } | f _ { i } | \le \overline { { k } } } \end{array}$ by greedily selecting the top-ranked facts until the budget is exhausted.

Reflect. The reflect operation generates preference-conditioned responses. Formally, given a memory bank B, query $Q ,$ , and preference profile Θ, the reflect function is:

$$
\operatorname{Reflect} (B, Q, \Theta) \to (r, \mathcal {O} ^ {\prime})\tag{34}
$$

where r is the generated response and $\mathcal { O } ^ { \prime }$ is the updated opinion network. The reflect pipeline performs the following steps: 1) use TEMPR to retrieve relevant memories from world, experience, opinion, and observation networks: $\mathcal { F } _ { Q } = \mathop { \mathrm { R e c a l l } } ( B , Q , k ) ; 2$ ) load the bank’s preference profile $\bar { \Theta } = ( S , L , E , \beta )$ and background h; 3) generate a response whose reasoning and tone are influenced by the configured preferences and bias-strength parameter $\beta ,$ , where the generation is conditioned on the system message $s = { \mathrm { V e r b a l i z e } } ( n , h , \Theta )$ and retrieved facts $\mathcal { F } _ { Q } ; \pmb { 4 } )$ form new opinions with confidence scores when appropriate, where for each new opinion $\dot { \boldsymbol { o } } = ( t , c , \tau , b , \mathcal { E } )$ , we add o to the opinion network $\mathcal { O } ;$ and 5) store opinions for future retrieval and reinforcement, updating $\mathcal { O } ^ { \prime } = \mathcal { O } \cup \{ o _ { 1 } , . . . , o _ { m } \}$

Together, these operations define a full loop: new experiences are retained into structured memory, recalled as needed for a given query, and reflected upon in a way that updates the agent’s beliefs and identity configuration.
