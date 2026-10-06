# 4 TEMPR: RETAIN AND RECALL

As described earlier, TEMPR (Temporal Entity Memory Priming Retrieval) implements HINDSIGHT’s retain and recall operations. It is responsible for turning raw conversational transcripts into a structured, temporal, entity-aware memory graph, and for retrieving variable amounts of relevant information for downstream reasoning. We first describe how TEMPR retains information by organizing memories, extracting narrative facts, and constructing an entity-aware graph. We then describe how it recalls information using a four-way parallel retrieval architecture with fusion and neural re-ranking. The neural components used in this pipeline, including the embedding model for semantic retrieval, the cross encoder reranker, and the downstream LLM, can all be treated as configurable modules rather than fixed backbones.

## 4.1 RETAIN: BUILDING A TEMPORAL ENTITY MEMORY GRAPH

### 4.1.1 MEMORY ORGANIZATION

As introduced in Section 3, HINDSIGHT organizes memories into four networks to separate objective information, subjective beliefs, and synthesized summaries. TEMPR instantiates this design by storing each extracted fact in exactly one network and attaching it to the shared memory graph. Each fact $f$ is assigned a type $\ell ( f ) \in \{ \mathrm { w o r l d }$ , experience, opinion, observation} that determines its target network.

Each memory is stored as a self-contained node that combines natural language, vector representations, and temporal metadata. Formally, a memory unit is a tuple:

$$
f = (u, b, t, v, \tau_ {s}, \tau_ {e}, \tau_ {m}, \ell , c, x)\tag{1}
$$

![](images/e51e643785034d4c7fda28d1cb138335ece2fcb358158af65b6481045ccd5b99.jpg)

[Image: The image displays two comparative text boxes illustrating different data extraction approaches for handling narrative content. The top box, titled "Fragmented Extraction (Avoided)," lists five separate bullet points that isolate individual statements made by characters named Alice and Bob regarding playlist suggestions. The bottom box, titled "Narrative Extraction (Used)," presents a single paragraph that combines these isolated details into a cohesive summary of their discussion and final decision. This visual example contrasts atomized facts against a unified narrative structure, illustrating potential methods for processing the text field $t$ within the defined schema.]  
Figure 3: Comparison of fragmented versus narrative fact extraction. TEMPR uses narrative extraction to create comprehensive, self-contained facts that preserve context and reasoning across multiple conversational turns.

where u is a unique identifier, b is the bank identifier, t is the narrative text, $v \in \mathbb { R } ^ { d }$ is the embedding vector, $\tau _ { s }$ and $\tau _ { e }$ define the occurrence interval, $\tau _ { m }$ is the mention timestamp, ℓ is the fact type, $c \in [ 0 , 1 ]$ is an optional confidence score (for opinions), and x contains auxiliary metadata such as context, access count, and full-text search vectors.

These fields allow TEMPR to treat each memory as a single unit for storage, graph construction, and retrieval, while supporting both semantic and lexical search as well as temporal and opinion-aware reasoning.

### 4.1.2 LLM-BASED NARRATIVE FACT EXTRACTION

TEMPR uses an open-source LLM to convert conversational transcripts into narrative facts and associated metadata. Compared to rule-based or sentence-level pipelines, this approach lets us extract self-contained facts that preserve cross-turn context and reasoning.

Chunking Strategy. We use coarse-grained chunking, extracting 2–5 comprehensive facts per conversation. Each fact is intended to cover an entire exchange rather than a single utterance, be narrative and self-contained, include all relevant participants, and preserve the pragmatic flow of the interaction. Fig. 3 illustrates this approach. Instead of storing five fragmented facts, we store a single narrative fact that makes downstream retrieval and reasoning less sensitive to local segmentation decisions.

Extraction Pipeline. The extraction model is prompted to produce structured output containing the narrative text of each fact, normalized temporal information (including ranges), participants and their roles, a fact type indicating the target network, and a set of mentioned entities (see Appendix A.1 for the complete prompt template and Appendix A.5 for the structured output schema). Internally, we decompose this into the following steps: 1) coreference resolution over the conversation to identify entity mentions and their referents; 2) temporal expression normalization and range extraction to convert relative time references (“last week”, “in March”) into absolute timestamps $( \tau _ { s } , \tau _ { e } )$ 3) participant attribution to determine who did or said what in the conversation; 4) preservation of explicit reasoning or justifications when present in the dialogue; 5) fact type classification to assign $\ell ( f ) \in \{ \mathrm { w o r l d }$ , experience, opinion, observation} based on the nature of the statement; and 6) entity extraction to identify PERSON, ORGANIZATION, LOCATION, PRODUCT, CONCEPT, and

OTHER entity types. Before embedding, we augment each fact with a human-readable time reference derived from the normalized timestamps, which improves temporal awareness during retrieval and reranking.

### 4.1.3 ENTITY RESOLUTION AND LINKING

Entity resolution links memories that refer to the same underlying entity, enabling multi-hop reasoning over the memory graph.

Recognition and Disambiguation The LLM used for fact extraction (described above) also identifies entity mentions during fact extraction. We then map mentions to canonical entities using a combination of string and name similarity (e.g., Levenshtein distance), co-occurrence patterns with other entities, and temporal proximity of mentions. Let M be the set of all entity mentions and E be the set of canonical entities. The resolution function $\rho : M \to E$ maps each mention $m \in M$ to a canonical entity $e \in E$ by maximizing a similarity score:

$$
\rho (m) = \underset {e \in E} {\arg \max} \left[ \alpha \cdot \operatorname{sim} _ {\mathrm{str}} (m, e) + \beta \cdot \operatorname{sim} _ {\mathrm{co}} (m, e) + \gamma \cdot \operatorname{sim} _ {\text { temp }} (m, e) \right]\tag{2}
$$

where sim ${ \bf \delta l _ { S t r } } ,$ sim $^ { 1 } \mathrm { c o } \cdot$ and $\mathrm { s i m } _ { \mathrm { t e m p } }$ are string similarity, co-occurrence similarity, and temporal proximity scores respectively, and $\alpha , \beta , \gamma$ are weighting coefficients.

Entity Link Structure Each canonical entity $e \in E$ induces edges of type entity between all memories that mention it. Formally, for any two memory units $f _ { i }$ and $f _ { j }$ that both mention entity e, we create a bidirectional link:

$$
e _ {i j} = (f _ {i}, f _ {j}, w = 1. 0, \ell = \text { entity }, e)\tag{3}
$$

These entity links enable graph traversal to surface indirectly related facts. For example, conversations about the same person across distant time spans that would be difficult to retrieve with vector or keyword search alone can be discovered through entity links.

### 4.1.4 LINK TYPES AND GRAPH STRUCTURE

In addition to entity links, the memory graph $\mathcal { G } = ( V , E )$ contains three other edge types. Let V be the set of all memory units and $\dot { E }$ be the set of directed edges. Each edge $e \in E$ is a tuple $( f _ { i } , f _ { j } , w , \ell )$ where $f _ { i } , f _ { j } \in V$ are memory units, $w \in [ 0 , 1 ]$ is a weight, and ℓ is the link type.

1) Temporal Links. For any two memories $f _ { i }$ and $f _ { j }$ with temporal metadata, we create a temporal link if they are close in time. The weight decays as temporal distance increases:

$$
w _ {i j} ^ {\mathrm{temp}} = \exp \left(- \frac {\Delta t _ {i j}}{\sigma_ {t}}\right)\tag{4}
$$

where $\Delta t _ { i j }$ is the time difference between $f _ { i }$ and $f _ { j }$ , and $\sigma _ { t }$ is a decay parameter.

2) Semantic Links. For any two memories $f _ { i }$ and $f _ { j }$ with embeddings $v _ { i } , v _ { j } \in \mathbb { R } ^ { d }$ , we create a semantic link if their cosine similarity exceeds a threshold $\theta _ { s }$ :

$$
w _ {i j} ^ {\text {sem}} = \left\{ \begin{array}{l l} \frac {v _ {i} \cdot v _ {j}}{\| v _ {i} \| \| v _ {j} \|} & \text {if} \frac {v _ {i} \cdot v _ {j}}{\| v _ {i} \| \| v _ {j} \|} \geq \theta_ {s} \\ 0 & \text {otherwise} \end{array} \right.\tag{5}
$$

3) Causal Links. Causal relationships are extracted by the LLM and represent cause-effect relationships. These links are upweighted during traversal to favor explanatory connections. Let ${ \mathcal { C } } \subseteq V \times V$ be the set of causal relationships identified by the LLM. For $( f _ { i } , f _ { j } ) \in \mathcal { C }$ , we create a causal link with weight $w _ { i j } ^ { \mathrm { c a u s a l } } = 1 . 0$ and type $\ell \in$ {causes, caused\_by, enables, prevents}.

Together, entity, temporal, semantic, and causal links support multi-hop discovery across the memory graph, allowing TEMPR to surface information that is related by identity, time, meaning, or explanation rather than by surface form alone.

### 4.1.5 THE OBSERVATION PARADIGM

Observations provide structured, objective summaries of entities that sit on top of raw narrative facts.

Motivation and Design. For simple entity-centric queries (e.g., “Tell me about Alice”), retrieving all underlying facts can be inefficient and redundant. Instead, we maintain synthesized profiles (observations) that summarize salient properties of each entity and can be referenced directly in responses (see Appendix A.3 for the complete observation generation prompt). Let $F _ { e } \subset V$ be the set of all facts that mention entity e. An observation $o _ { e }$ is generated by applying an LLM-based summarization function:

$$
o _ {e} = \mathrm{Summarize} _ {\mathrm{LLM}} (F _ {e})\tag{6}
$$

where the LLM is instructed to produce a concise, preference-neutral summary.

Observations vs. Opinions. Observations and opinions differ along several dimensions that matter for reasoning. Observations are generated without behavioral profile influence, whereas opinions are explicitly shaped by the bank’s disposition behavioral parameters (skepticism, literalism, empathy). Observations provide objective summaries of entities (e.g., roles, attributes), while opinions capture subjective evaluations and judgments. Observations do not carry confidence scores, but opinions include a confidence score $c \in [ 0 , 1 ]$ representing belief strength. Observations are produced via background synthesis and regenerated when underlying facts change, whereas opinions are formed during reflection and updated via reinforcement.

Background Processing. Observation generation and regeneration run asynchronously to maintain low-latency writes while gradually improving the quality of entity-centric summaries. When new facts mentioning entity e are retained, a background task is triggered to recompute $o _ { e }$ based on the updated set $F _ { e }$

## 4.2 RECALL: AGENT-OPTIMIZED RETRIEVAL ARCHITECTURE

Given the memory graph described above, TEMPR must retrieve variable amounts of relevant context for a query while respecting the downstream LLM’s context window. Unlike conventional search systems that expose a fixed top-k interface, our setting requires an agent-optimized retrieval layer. The caller can trade off latency and coverage, and the system must exploit both the graph structure and temporal metadata of memories.

To accomplish the above objective, TEMPR combines several complementary retrieval strategies into a single pipeline with Reciprocal Rank Fusion and neural reranking. The result is a recall mechanism that can surface both directly and indirectly related memories (via entities, time, and causal links), and present them in a form that fits within a specified token budget.

### 4.2.1 AGENT-OPTIMIZED RETRIEVAL INTERFACE

Rather than exposing a fixed top-k interface, TEMPR lets the caller specify how much context to retrieve and how much effort to spend finding it. Formally, the retrieval function is:

$$
\operatorname{Recall} (B, Q, k) \to \left\{f _ {1}, \dots , f _ {n} \right\}\tag{7}
$$

where $B$ is the memory bank, Q is the query, and k is a token budget aligned with the downstream LLM’s context window. An optional cost or latency budget may also be specified to cap how aggressively to expand search. The returned set satisfies:

$$
\sum_ {i = 1} ^ {n} | f _ {i} | \leq k\tag{8}
$$

where $| f _ { i } |$ denotes the token count of fact $f _ { i } .$ This allows agents to request “just enough” memory for simple questions, or to spend more budget on broader, multi-hop recall when the task is complex.

### 4.2.2 FOUR-WAY PARALLEL RETRIEVAL

To populate the candidate set for a query, TEMPR runs four retrieval channels in parallel, each capturing a different notion of relevance. Let Q be the query with embedding $v _ { Q } \in \mathbb { R } ^ { \bar { d } }$ and text $t _ { Q }$

Semantic Retrieval (Vector Similarity) The semantic retrieval channel performs vector similarity search using cosine similarity between the query embedding $v _ { Q }$ and memory embeddings. Let $\dot { V }$ be the set of all memory units in the target network. The semantic score for each memory f with embedding $v _ { f }$ is:

$$
s _ {\text { sem }} (Q, f) = \frac {v _ {Q} \cdot v _ {f}}{\| v _ {Q} \| \| v _ {f} \|}\tag{9}
$$

We use an HNSW-based pgvector index to efficiently retrieve the top-k memories by semantic score:

$$
R _ {\text { sem }} = \underset {S \subseteq V, | S | = k} {\arg \max} \sum_ {f \in S} s _ {\text { sem }} (Q, f)\tag{10}
$$

This channel is responsible for capturing conceptual similarity and paraphrases, and typically provides high recall on meaning-level matches even when surface forms differ.

Keyword Retrieval (BM25) In parallel, we run a lexical channel using a full-text search with BM25 ranking over a GIN index on the memory text. Let $\mathbf { B M } 2 5 ( t _ { Q } , f )$ denote the BM25 score for query text $t _ { Q }$ and memory $f .$ . The top-k keyword matches are:

$$
R _ {\mathrm{bm25}} = \underset {S \subseteq V, | S | = k} {\arg \max} \sum_ {f \in S} \operatorname{BM25} (t _ {Q}, f)\tag{11}
$$

This channel excels at precise matching of proper nouns and technical terms $( \mathrm { e . g . }$ , specific API names or dataset identifiers) and complements the semantic channel by recovering items that might be underrepresented or ambiguous in the embedding space.

Graph Retrieval (Spreading Activation) The third channel exploits the memory graph $\mathcal { G } = ( V , E )$ via spreading activation. Beginning with the top semantic hits as entry points, we perform breadth-first search with activation propagation. Let $A ( f , t )$ denote the activation of memory $f$ at step t. Initially, $A ( f , 0 ) = s _ { \mathrm { s e m } } ( Q , f )$ for entry points and ${ \ddot { A } } ( { \dot { f } } , 0 ) = 0$ otherwise. At each step, activation propagates along edges:

$$
A (f _ {j}, t + 1) = \max _ {(f _ {i}, f _ {j}, w, \ell) \in E} [ A (f _ {i}, t) \cdot w \cdot \delta \cdot \mu (\ell) ]\tag{12}
$$

where $\delta \in ( 0 , 1 )$ is a decay factor and $\mu ( \ell )$ is a link-type multiplier. Causal and entity edges have $\mu ( \ell ) > 1$ , while weak semantic or long-range temporal edges have $\mu ( \ell ) \leq 1$ . This process surfaces memories that are not obviously similar to the query text but are connected through shared entities, nearby events, or causal chains.

Temporal Graph Retrieval When a temporal constraint is detected in the query, we invoke a temporal graph retrieval channel backed by a hybrid temporal parser. We first run a rule-based analyzer that uses two off-the-shelf date parsing libraries with multilingual support to normalize explicit and relative expressions (for example, “yesterday”, “last weekend”, or “June 2024”) into a date range. This heuristic path handles the majority of queries at low latency. For queries that cannot be resolved heuristically, we fall back to a lightweight sequence-to-sequence model (here, we use google/flan-t5-small), which converts the remaining temporal expressions into a concrete date range $[ \tau _ { \mathrm { s t a r t } } , \tau _ { \mathrm { e n d } } ]$ . We then match against the occurrence intervals of memories:

$$
R _ {\mathrm{temp}} = \left\{f \in V: [ \tau_ {s} ^ {f}, \tau_ {e} ^ {f} ] \cap [ \tau_ {\mathrm{start}}, \tau_ {\mathrm{end}} ] \neq \emptyset \right\}\tag{13}
$$

Graph traversal is restricted to memories in $R _ { \mathrm { t e m p } } ,$ prioritizing events that actually occurred in the requested period. Each memory is scored by temporal proximity to the query range:

$$
s _ {\mathrm{temp}} (Q, f) = 1 - \frac {| \tau_ {\mathrm{mid}} ^ {f} - \tau_ {\mathrm{mid}} ^ {Q} |}{\Delta \tau / 2}\tag{14}
$$

where $\tau _ { \mathrm { m i d } } ^ { f }$ and $\tau _ { \mathrm { m i d } } ^ { Q }$ are the midpoints of the fact’s occurrence interval and the query range, and $\Delta \tau = \tau _ { \mathrm { e n d } } - \tau _ { \mathrm { s t a r t } }$ is the query range duration.

Running these four channels in parallel yields a diverse set of candidates: semantically similar memories, exact lexical matches, graph-neighbor memories connected via entities and causal links, and time-constrained events aligned with the query’s temporal intent.

### 4.2.3 RECIPROCAL RANK FUSION (RRF)

After parallel retrieval, TEMPR merges the four ranked lists using Reciprocal Rank Fusion. Let $R _ { 1 } , R _ { 2 } , R _ { 3 } , R _ { 4 }$ denote the ranked lists from the four channels. For each candidate memory $f ,$ let $r _ { i } ( f )$ denote its rank in list $R _ { i }$ (with $r _ { i } ( f ) = \infty$ if $f \notin R _ { i } )$ . The fused score is:

$$
\operatorname{RRF} (f) = \sum_ {i = 1} ^ {4} \frac {1}{k + r _ {i} (f)}\tag{15}
$$

where $k$ is a small constant $( { \bf e . g . } , k = 6 0 )$ . Intuitively, each strategy contributes a larger amount when it places $f$ near the top of its list, and items that appear high in multiple lists accumulate more evidence.

RRF has several advantages over score-based fusion in this setting. Because it is rank-based, it does not rely on raw scores being calibrated across systems. It is also robust to missing items. If a candidate does not appear in a particular list, that strategy simply contributes nothing rather than penalizing it. Finally, memories that are consistently retrieved across different channels naturally rise to the top, reflecting multi-evidence support.

### 4.2.4 NEURAL CROSS-ENCODER RERANKING

After RRF fusion, TEMPR applies a neural cross-encoder reranker to refine precision on the top candidates. We use cross-encoder/ms-marco-Mini $\scriptstyle { \mathbf { { M } } } \mathbf { { - } } \mathbf { { L } } \mathbf { { - } } 6 - \mathbf { v } 2 ,$ which jointly encodes the query and each candidate memory and outputs a relevance score. Let $\operatorname { C E } ( Q , f )$ denote the cross-encoder score. The final ranking is:

$$
R _ {\text { final }} = \operatorname{argsort} _ {f \in R _ {\mathrm{RRF}}} \mathrm{CE} (Q, f)\tag{16}
$$

Compared to purely embedding-based similarity, the cross-encoder can model rich query-document interactions learned from supervised passage-ranking data, rather than relying on independent vector representations. In our setting, we also include formatted temporal information in the input text, allowing the reranker to incorporate simple temporal cues when deciding which memories are most relevant.

### 4.2.5 TOKEN BUDGET FILTERING

In the final stage, TEMPR enforces the caller’s token budget so that the selected memories fit within the downstream LLM’s context window. Starting from the reranked list $R _ { \mathrm { f i n a l } }$ , we iterate over candidates in order and include each memory’s text until the cumulative token count reaches the specified k:

$$
R _ {\text { output }} = \left\{f _ {1}, \dots , f _ {n}: \sum_ {i = 1} ^ {n} | f _ {i} | \leq k \text {   and   } \sum_ {i = 1} ^ {n + 1} | f _ {i} | > k \right\}\tag{17}
$$

where $f _ { i } \in R _ { \mathrm { f i n a l } }$ are ordered by relevance. This simple packing step ensures that the model receives as much relevant information as possible without exceeding its context capacity.
