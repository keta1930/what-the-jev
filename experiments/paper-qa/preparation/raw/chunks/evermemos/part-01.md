# EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning

Chuanrui Hu<sup>1,2</sup>\* , Xingze Gao<sup>1,2</sup>\* , Zuyi Zhou<sup>1,2</sup>, Dannong Xu<sup>1,2</sup>, Yi Bai<sup>1,2</sup>, Xintong Li<sup>1,2</sup>, Hui Zhang<sup>1,2</sup>, Tong Li<sup>1,2</sup>, Chong Zhang<sup>2</sup>, Lidong Bing<sup>2†</sup> , Yafeng Deng<sup>1,2†</sup>

<sup>1</sup>EverMind <sup>2</sup>Shanda Group

{chuanrui.hu, xingze.gao, zuyi.zhou, dannong.xu, baiyi, xintong.li, zhanghui, litong02, zhangchong, lidong.bing, dengyafeng}@shanda.com

# Abstract

Large Language Models (LLMs) are increasingly deployed as long-term interactive agents, yet their limited context windows make it difficult to sustain coherent behavior over extended interactions. Existing memory systems for LLMs often store isolated records and retrieve fragments, limiting their ability to consolidate evolving experience and resolve conflicts. We introduce EverMemOS, a self-organizing memory operating system that implements an engram-inspired lifecycle for computational memory. First, Episodic Trace Formation converts dialogue streams into MemCells that capture episodic traces, atomic facts, and timebounded foresight. Second, Semantic Consolidation organizes MemCells into thematic MemScenes, distilling stable semantic structures and updating user profiles. Finally, Reconstructive Recollection performs MemSceneguided agentic retrieval to compose the necessary and sufficient context for downstream reasoning. Experiments on LoCoMo, Long-MemEval, and PersonaMem-v2 show that EverMemOS significantly outperforms state-ofthe-art methods on memory-augmented reasoning tasks. Our code is available at https: //github.com/EverMind-AI/EverMemOS.

# 1 Introduction

Large Language Models (LLMs) are increasingly deployed as long-term interactive agents rather than transient conversational tools (Yehudai et al., 2025; Ferrag et al., 2025). For providing better personalized services, LLM-based agents must maintain consistent personas and user models over extended interactions while continuously incorporating new constraints over extended timeframes, spanning days, months, or even years. To address this challenge, expanding context windows is a direct approach, but ultra-long contexts still degrade in performance (e.g., the “Lost-in-the-Middle” phenomenon) and incur prohibitive computational costs (Liu et al., 2024). Consequently, recent research has increasingly focused on constructing memory for LLMs that can both store past information and organize experiences into coherent, evolving structures that support long-horizon reasoning (Wu et al., 2025; Maharana et al., 2024).

![](images/05228c768f9a7b50f1c1a0b1ef1623ce733d7fc0e83019468677d2b418e09fcf.jpg)

[Image: The image is a vertical bar chart titled "Accuracy on LoCoMo Across Memory Systems," which compares performance metrics for five distinct approaches to memory management. The x-axis categorizes the methods as Mem0, MemU, MemOS, Zep, and EverMemOS (Ours), while the y-axis indicates accuracy percentages ranging from 0 to 100. Specific numerical values are displayed above each bar, illustrating a progressive increase in performance from 64.20 for Mem0 to the highest score of 93.05 for EverMemOS.]

Accuracy on LongMemEval Across Memory Systems  
![](images/70966760df0b4dac4a8921ee22319488b1f5824e0fbd55eae970854f653c3782.jpg)

[Image: This vertical bar chart compares the performance metrics of five memory-augmented systems labeled MemU, Zep, Mem0, MemOS, and EverMemOS (Ours). The chart displays specific numerical values for each method, with EverMemOS achieving the highest score of 83.00, followed by MemOS at 77.80. The other systems exhibit lower performance levels, with Mem0 recording 66.40, Zep at 63.80, and MemU showing the lowest value at 38.40. Distinct icons representing each system's architecture or function are embedded near the top of their respective bars.]  
Figure 1: Evaluation results of different memory methods for LLMs on two benchmarks (LoCoMo and Long-MemEval). All methods are based on GPT-4.1-mini.

Recently, a broad range of memory-augmented approaches have been proposed, including retrievalbased memory (Zhong et al., 2024; Packer et al., 2024), trainable memory (Zheng et al., 2024; Gong et al., 2024), and more recently Memory Operating Systems that unify storage, retrieval, filtering, and updating (Li et al., 2025; Kang et al., 2025). However, enabling long-term consistency in reasoning remains challenging. While these methods improve scalability and modularity, most of them treat memory as flat collections of isolated records. As a result, many failures stem not from missing information but from poor integration, where fragmented experiences are not consolidated into higher-level semantic structures. Without consolidation and ab straction, agents may retrieve relevant facts yet fail to detect conflicts, maintain stable user models, or reason consistently over time. Therefore, a key limitation of existing memory methods is the absence of an explicit mechanism to transform fragmented episodic experiences into coherent and stable knowledge structures that support long-horizon reasoning.

To address the above limitation, we propose EverMemOS, a unified and product-ready Memory Operating System that models memory as a dynamic lifecycle for long-term LLM-based agents. As shown in Figure 1, EverMemOS significantly outperforms the state-of-the-art memory methods for LLMs in experimental evaluation, relatively improving overall accuracy by 9.2% on LoCoMo and 6.7% on LongMemEval compared to the strongest baseline method. EverMemOS aims to transform fragmented episodic experiences into coherent and stable knowledge structures that support long-horizon reasoning through three phases. First, Episodic Trace Formation transforms the unbounded stream of interaction history into discrete, stable memory traces (termed MemCells). Second, Semantic Consolidation transforms MemCells into stable, scene-level structures (termed Mem-Scenes) that support coherent aggregation, such as maintaining consistent user profiles across interactions. Finally, Reconstructive Recollection, guided by the principle of necessity and sufficiency, actively composes only the grounded context required for a given query and supports long-horizon reasoning, rather than indiscriminately retrieving all potentially relevant records.

EverMemOS does not aim to simulate biological memory at the neural level. Instead, it draws on organizing principles from biological memory systems and translates them into a computational framework. Figure 2 illustrates the intuition behind EverMemOS. A fragment-based system may recall a user’s preference for IPA and recommend an alcoholic drink, failing to account for a newly introduced constraint that the user is taking antibiotics. In contrast, EverMemOS consolidates these experiences into a coherent representation of the user’s state, enabling the agent to safely recommend a non-alcoholic alternative. Although such foresight-oriented behaviors are not explicitly captured by existing benchmarks, they expose a fundamental limitation of fragment-based memory and motivate the system-level design of EverMemOS. Empirically, comprehensive experiments on three benchmarks for memory-augmented reasoning consistently indicate the superiority of EverMemOS, compared to the state-of-the-art methods.

![](images/8dff3331583ef2345377e41defbf86bd5f7b572ec44a44cfa7912477a9ecbc90.jpg)

[Image: This diagram contrasts two memory architectures, "Fragment-based Memory" and "EverMemOS," using a shared conversation history about movie nights and dental health. The top panel displays interaction history spanning last month, last week, and the current query, where a user mentions enjoying IPAs, then later taking antibiotics for a toothache, before asking for drink recommendations. The left workflow demonstrates fragment-based memory retrieving isolated episodes (IPA preference or toothache) independently, leading to a suggested response that recommends beer. In contrast, the right workflow illustrates EverMemOS utilizing semantic consolidation blocks like MemCell and MemScene to synthesize a user context with time-bounded foresight, ultimately generating a safe response that advises avoiding alcohol while suggesting mocktails.]  
Figure 2: Comparison of typical fragment-based memory and EverMemOS in an interactive chat scenario.

Our contributions are summarized as follows:

• System Design: We introduce EverMemOS, a unified and product-ready Memory Operating System for LLMs that reconceptualizes memory as a lifecycle, shifting from passive storage of records to structured organization of experience.

• Innovative Method: We propose a threephase method that can transform fragmented episodic experiences into coherent and stable knowledge structures that support longhorizon reasoning.

• Empirical Validation: Experimental results demonstrate that EverMemOS achieves state-of-the-art performance on multiple longcontext benchmarks for memory-augmented reasoning, validating the effectiveness of lifecycle-based memory organization.

# 2 Related Work

## 2.1 Memory Mechanisms in LLMs

Context Window Extension. Large language models (LLMs) are constrained by fixed-length context windows. Prior work extends context via sparse attention (Beltagy et al., 2020; Zaheer et al., 2020), recurrence (Dai et al., 2019; Bulatov et al., 2022), and length extrapolation (Chen et al., 2024, 2025). However, longer context does not guarantee effective utilization: the “Lost-in-the-Middle” phenomenon persists (Liu et al., 2024; Bulatov et al., 2023), suggesting context extension alone is insufficient for durable memory.

Retrieval-Augmented and Parametric Memory. Retrieval-augmented generation (RAG) (Lewis et al., 2020) externalizes memory to alleviate window limits, but its reliability depends on retrieval quality (Ram et al., 2023). Parametric approaches internalize information, yet often suffer from forgetting and instability (De Lange et al., 2022). Hybrid approaches (Wang et al., 2023; Packer et al., 2024) alleviate issues but lack a unified organizational principle for persistent memory.

## 2.2 Memory Systems

Early Computational Memory. Early differentiable memory systems (e.g., NTM/DNC/Key– Value memories) (Graves et al., 2014, 2016; Miller et al., 2016) introduced external memory interaction, but scale poorly and are ill-suited to modern autoregressive LLMs.

Memory in LLM Agents. As LLM-based agents evolve (Xi et al., 2023; Xia et al., 2024), memory systems have shifted toward persistent state integration. Recent systems introduce episodic (Wang and Chen, 2025), semantic (Shinn et al., 2024), and hierarchical task memory (Sun and Zeng, 2025). However, many designs still rely on fragmented text units and limited consolidation, which can degrade long-horizon performance (Packer et al., 2024).

Memory Operating Systems. Recent work formalizes memory management as a system-level runtime. Some focus on lifecycle and capacity, such as Nemori’s (Nan et al., 2025) predictiondriven updates and MemoryOS’s (Kang et al., 2025) hierarchical control. Others, like Mem0 (Chhikara et al., 2025) and $Z e p$ (Rasmussen et al., 2025), prioritize structured fact maintenance via knowledge graphs, while MemOS (Li et al., 2025) targets unified scheduling across memory types.

While these systems advance structural organization, they primarily focus on storage optimization or fact maintenance. EverMemOS distinguishes itself by implementing a three-phase memory lifecycle that transforms episodic traces into synthesized semantic structures for long-horizon reasoning.

# 3 EverMemOS

## 3.1 Framework Overview

Drawing inspiration from the biological engram lifecycle (Josselyn et al., 2015), EverMemOS follows a three-phase workflow (Figure 3): (1) Episodic Trace Formation encodes interaction streams into MemCells; (2) Semantic Consolidation organizes MemCells into MemScenes and updates user profiles; and (3) Reconstructive Recollection performs MemScene-guided retrieval under the principle of necessity and sufficiency.

## 3.2 Memory Primitives

At the core of EverMemOS is the MemCell, the atomic unit bridging low-level data and high-level semantics. Formally, a MemCell c is a tuple c = $( E , { \mathcal { F } } , P , M )$ , where:

• E (Episode): A concise third-person narrative of the event, serving as the semantic anchor.

$\mathcal { F } = \{ f _ { 1 } , \ldots , f _ { n } \}$ (Atomic Facts): Discrete, verifiable statements derived from E for highprecision matching.

• P (Foresight): Forward-looking inferences (prospections; e.g., plans and temporary states) annotated with validity intervals $[ t _ { s t a r t } , t _ { e n d } ]$ to support temporal awareness.

• M (Metadata): Contextual grounding including timestamps and source pointers.

This structure turns memory from a static record $( E , { \mathcal { F } } )$ into a temporally grounded representation that also supports Foresight (P).

## 3.3 Phase I: Episodic Trace Formation

Grounded in the engram concept (Josselyn et al., 2015), this first phase transforms the unbounded stream of interaction history $\mathcal { D } = \{ d _ { 1 } , \ldots , d _ { T } \}$ into discrete, stable memory traces (MemCells). This process adopts a three-step pipeline to distill semantic signal from noisy interaction data:

![](images/cf2a6691566783710f359766608575caa36b30f544ab89a6984ffbcb4c796ca6.jpg)

[Image: The image illustrates a three-phase architecture for managing conversational memory, starting with Phase I where interaction history is segmented into discrete "MemCells" comprising foresight, episodes, and atomic facts. Phase II involves semantic consolidation, where these cells undergo incremental clustering to form broader "MemScenes" that update a user profile with explicit and implicit traits. Finally, Phase III demonstrates reconstructive recollection, showing how chat and reasoning queries trigger scene matching and recall mechanisms to retrieve relevant historical data for context-aware agent responses.]  
Figure 3: The EverMemOS workflow mirrors an engram-inspired memory lifecycle: (1) Episodic Trace Formation segments continuous dialogue into MemCells with episodes, atomic facts, and time-bounded foresight. (2) Semantic Consolidation organizes MemCells into MemScenes and updates a user profile. (3) Reconstructive Recollection performs MemScene-guided retrieval to compose the necessary and sufficient context.

Contextual Segmentation To discretize continuous streams, a Semantic Boundary Detector processes interactions via a sliding window. Upon detecting a topic shift, accumulated turns are encapsulated as a raw episode history. We implement this step via LLM prompting; while boundary detection is not perfect, we find it robust in downstream evaluation (see Table 3).

Narrative Synthesis To resolve dialogue redundancy and ambiguity, the episode history is synthesized into a high-fidelity Episode (E). This rewriting process produces a concise, third-person narrative with resolved coreferences, establishing a stable semantic anchor.

Structural Derivation From E, the system extracts Atomic Facts (F) for precise matching and generates Foresight signals (P) with inferred validity intervals (e.g., distinguishing temporary "flu" from permanent "graduation"). Concretely, we prompt the LLM over the rewritten Episode E to output a constrained schema of Atomic Facts and Foresight signals with validity intervals [t , t ]. These components are bundled with metadata M to form the final MemCell c.

## 3.4 Phase II: Semantic Consolidation

Inspired by systems consolidation (McGaugh, 2000), EverMemOS employs an online mechanism that organizes MemCells into higher-order structures to transition from transient episodes to stable long-term knowledge.

Incremental Semantic Clustering EverMemOS organizes memory dynamically. When a new Mem-Cell c arrives, the system computes its embedding and retrieves the nearest MemScene centroid. If similarity exceeds a threshold τ, c is assimilated and the scene representation is incrementally updated; otherwise, a new MemScene is instantiated. This online process maintains thematic structure in real-time without batch reprocessing.

Scene-Driven Profile Evolution Scene-level consolidation can also update a compact User Profile from aggregated evidence. When a new Mem-Cell is assimilated into a MemScene, EverMemOS updates a concise scene summary and refreshes the user profile by prompting over these summaries (rather than individual turns), helping separate stable traits from temporary states. We maintain a compact profile of explicit facts (including timevarying measurements) and implicit traits, updated online from scene summaries with recency-aware updates and conflict tracking (Appendix B.3).

## 3.5 Phase III: Reconstructive Recollection

Building on theories of reconstructive memory (Schacter, 2008), retrieval in EverMemOS is modeled not as a static lookup but as an active Reconstruction process, guided by the principle of necessity and sufficiency. Given a query q, Ever-MemOS performs agentic retrieval grounded in MemScenes.

MemScene Selection We first compute relevance between the query and all MemCells by fusing dense and BM25 retrieval over their Atomic Facts F via Reciprocal Rank Fusion (RRF). We then score each MemScene by the maximum relevance among its constituent MemCells and select a small set of the highest-scoring MemScenes.

Episode and Foresight Filtering Within the selected MemScenes, we pool Episodes from their constituent MemCells and re-rank them to select a compact set for downstream inference. We then apply Foresight Filtering, retaining only timevalid Foresight whose validity intervals satisfy $t _ { n o w } \in [ t _ { s t a r t } , t _ { e n d } ]$ (discarding expired ones).

Agentic Verification and Query Rewriting The retrieved context is evaluated by an LLM-based verifier for sufficiency. If it is deemed insufficient, the system triggers a query rewriting step to supplement retrieval; otherwise, the context is passed to the downstream module. Prompt templates are provided in Appendix C.1.

Task Modes We consider two downstream settings that share the same retrieval pipeline: Memory-Augmented Reasoning and Memory-Augmented Chat. For Reasoning, we use the retrieved Episodes as context for benchmark evaluation. For Chat, the composed context additionally incorporates the User Profile and timevalid Foresight signals, filtered by the current time $t _ { n o w } \in [ t _ { s t a r t } , t _ { e n d } ] ;$ since these capabilities are not covered by existing reasoning benchmarks, we present them through qualitative case studies.
