# ByteRover: Agent-Native Memory Through LLM-Curated Hierarchical Context

Andy Nguyen<sup>1</sup>, Danh Doan<sup>1</sup>, Hoang Pham<sup>1</sup>, Bao Ha<sup>1</sup>, Dat Pham<sup>1</sup>, Linh Nguyen<sup>1</sup>, Hieu Nguyen<sup>1</sup>, Thien Nguyen<sup>1</sup>, Cuong Do<sup>1</sup>, Phat Nguyen<sup>1</sup>, Toan Nguyen<sup>1</sup>

<sup>1</sup>ByteRover https://www.byterover.dev

# Abstract

Memory-Augmented Generation (MAG) extends large language models with external memory to support long-context reasoning, but existing approaches universally treat memory as an external service that agents call into—delegating storage to separate pipelines of chunking, embedding, and graph extraction. This architectural separation means the system that stores knowledge does not understand it, leading to semantic drift between what the agent intended to remember and what the pipeline actually captured, loss of coordination context across agents, and fragile recovery after failures. In this paper, we propose ByteRover, an agent-native memory architecture that inverts the memory pipeline: the same LLM that reasons about a task also curates, structures, and retrieves knowledge. ByteRover represents knowledge in a hierarchical Context Tree—a file-based knowledge graph organized as Domain > Topic > Subtopic > Entry—where each entry carries explicit relations, provenance, and an Adaptive Knowledge Lifecycle (AKL) with importance scoring, maturity tiers, and recency decay. Retrieval uses a 5-tier progressive strategy that resolves most queries at sub-100 ms latency without LLM calls, escalating to agentic reasoning only for novel questions. Experiments on LoCoMo and LongMemEval demonstrate that ByteRover achieves state-of-the-art accuracy on LoCoMo and competitive results on LongMemEval while requiring zero external infrastructure—no vector database, no graph database, no embedding service—with all knowledge stored as human-readable markdown files on the local filesystem.

# 1 Introduction

Large Language Models (LLMs) have demonstrated remarkable capabilities across a wide range of tasks [Brown et al., 2020, Achiam et al., 2023, Wei et al., 2022], yet they remain fundamentally limited in their ability to maintain and reason over long-term context. These models process information within a finite attention window, and their internal representations do not persist across interactions, causing earlier details to be forgotten once they fall outside the active context [Brown et al., 2020, Beltagy et al., 2020]. Even within a single long sequence, attention efectiveness degrades with distance due to attention dilution, positional encoding limitations, and token interference, leading to the well-known “lost-in-the-middle” phenomenon [Liu et al., 2024, Press et al., 2022].

To address these limitations, Memory-Augmented Generation (MAG) systems have emerged as a promising direction for enabling LLMs to operate beyond the boundaries of their fixed context windows [Xu et al., 2025, Nan et al., 2025, Jiang et al., 2026a, Chhikara et al., 2025]. MAG equips an agent with an external memory module that continuously records interaction histories and allows the agent to retrieve and reintegrate past experiences when generating new responses. The paradigm has rapidly evolved from lightweight semantic stores to entity-centric, episodic, and hierarchical designs [Jiang et al., 2026b].

Despite this architectural diversity, current MAG systems share a common structural pattern: memory is an external service that agents call into. The agent serializes data, sends it to a separate pipeline (for chunking, embedding, entity extraction, or graph construction), receives an acknowledgment, and later queries the service to retrieve results. The pipeline that stores knowledge does not understand it—chunking is mechanical, embeddings encode surface similarity rather than semantic relationships, and the agent has no visibility into how its memories were organized or why certain relationships were created.

This external-service paradigm creates three failure modes that become critical for autonomous agents operating over long time horizons:

1. Semantic drift. The agent’s understanding of what it stored diverges from what the memory service actually captured. The agent intends to store a nuanced insight; the pipeline chunks and embeds it diferently, and the next retrieval returns a tangentially related fragment.

2. Lost coordination context. When multiple agents share an external memory service, they share data but not understanding. Agent A stores a finding with reasoning and rationale. Agent B retrieves the data but lacks the why—what reasoning led to the conclusion, what actions were expected to follow. The provenance is lost in the embedding.

3. Recovery fragility. When an autonomous agent crashes mid-task, it must reconstruct state by querying the memory service, interpreting results, and inferring where it left of. With stateful, file-based memory, the state is in the files—per-operation status, timestamps, and the knowledg structure itself tells the agent exactly what was completed.

To address these limitations, we propose ByteRover, an agent-native memory architecture that inverts the relationship between agent and memory. Instead of calling an external memory service, the same LLM that reasons about a task also curates knowledge into a hierarchical Context Tree—a file-based knowledge graph where each entry carries explicit relations, provenance, and lifecycle metadata. Memory operations (ADD, UPDATE, UPSERT, MERGE, DELETE) are tools in the agent’s toolkit, not API calls to an external service, enabling a stateful feedback loop where the agent sees per-operation results and adapts in real time.

Our contributions are summarized as follows:

1. We propose ByteRover, an agent-native memory architecture where the LLM itself curates knowledge through structured operations with explicit provenance and rationale, eliminating the separation between the “understanding” agent and the “storing” pipeline.

2. We introduce the Context Tree, a hierarchical file-based knowledge graph with an Adaptive Knowledge Lifecycle (AKL)—importance scoring, maturity tiers (draft → validated → core), and recency decay—that enables knowledge to naturally evolve over time.

3. We design a 5-tier progressive retrieval strategy that resolves most queries at sub-100 ms latency without LLM calls, combined with out-of-domain detection that explicitly signals when queries fall outside stored knowledge.

4. We demonstrate that ByteRover achieves state-of-the-art results on LoCoMo and competitive results on LongMemEval benchmarks while requiring zero external infrastructure—no vector database, no graph database, no embedding service—with all knowledge stored as humanreadable markdown files.

# 2 Background

## 2.1 Memory-Augmented Generation

Agentic memory extends retrieval-based generation by introducing persistent, writable memory that evolves across interactions [Jiang et al., 2026b]. Formally, at step t, the agent conditions on observations $O t$ and an external memory state $\mathcal { M } _ { t } \mathrm { : }$

$$
y _ {t} \sim f _ {\theta} \Bigl (\phi (o _ {t}, s _ {t}) \oplus \psi (\mathcal {M} _ {t}; q _ {t}) \Bigr),\tag{1}
$$

where $y _ { t }$ denotes the output, $s _ { t }$ is additional agent state, $\psi ( \mathcal { M } _ { t } ; q _ { t } )$ retrieves memory given query $q _ { t } .$ and ⊕ represents integration (e.g., prompt concatenation). Crucially, memory afects behavior through the explicit retrieval term ψ rather than updates to θ.

Two coupled processes are operated: inference-time recall (reading memory to condition decisions) and memory update (writing, consolidating, and forgetting to maintain a useful long term store). The memory module evolves via a feedback loop:

$$
o _ {t} = \operatorname{LLM} (q _ {t}, \operatorname{Retrieve} (q _ {t}, \mathcal {M} _ {t})),\tag{2}
$$

$$
\mathcal {M} _ {t + 1} = \mathrm{Update} (\mathcal {M} _ {t}, q _ {t}, o _ {t}).\tag{3}
$$

## 2.2 Taxonomy of Existing Approaches

Following the taxonomy introduced by Jiang et al. [2026b], existing MAG systems can be organized into four structural categories:

• Lightweight Semantic Memory. Independent textual units embedded in a vector space and retrieved via top-k similarity. No explicit structural relations [Liu et al., 2026].

• Entity-Centric and Personalized Memory. Organizes information around explicit entities using structured records or attribute-value pairs [Xu et al., 2025, Modarressi et al., 2023, Chhikara et al., 2025].

• Episodic and Reflective Memory. Adds temporal abstraction by organizing interactions into episodes or higher-level summaries [Nan et al., 2025].

• Structured and Hierarchical Memory. Imposes explicit organization over stored information via graphs [Jiang et al., 2026a, Rasmussen et al., 2025], hierarchical tiers [Kang et al., 2025a, Packer et al., 2023], or policy-optimized management.

## 2.3 The External Service Paradigm

Despite their architectural diversity, all systems in the taxonomy above share a common interaction pattern: the agent communicates with memory through an API boundary. The agent serializes data, the memory service processes it through its own pipeline (chunking, embedding, entity extraction, graph construction), and the agent later queries the service to retrieve results.

This pattern has a fundamental consequence: the system that stores knowledge does not understand it. The embedding model that creates vector representations operates independently of the agent’s reasoning. The entity extraction pipeline has its own notion of what matters. The agent has no visibility into how its memories were organized, why certain relationships were created, or whether the stored representation faithfully captures its intent.

ByteRover departs from this paradigm by making the agent itself the curator—the same LLM that reasons about a task decides what to store, where to place it, what it relates to, and why it matters.

# 3 The Context Tree

This section introduces the ByteRover architecture and its core data structure, the Context Tree.

## 3.1 Architectural Overview

ByteRover is organized into three logical layers, illustrated in Figure 1:

• Agent Layer. The LLM reasoning loop that produces both task outputs and memory operations. Memory tools (curate, query, search) are available as first-class tools alongside file $\mathrm { I / O } ,$ code execution, and other agent capabilities.

• Execution Layer. A sequential task queue that processes curate and query operations. Curation runs through a sandboxed environment where the LLM’s generated code has controlled access to the knowledge layer via a ToolsSDK interface. The sequential queue eliminates write-write conflicts without file-level locking.

• Knowledge Layer. The Context Tree (a hierarchical file structure of markdown entries), the MiniSearch full-text index, and the query cache. All storage is local filesystem—no external databases or services.

The key design principle is that memory operations are tools in the agent’s toolkit, not API calls to an external service. When the agent curates knowledge, it produces structured operations that execute within the agent process, with per-operation feedback enabling real-time error recovery. When the agent queries knowledge, results are returned from in-process caches and indexes before any LLM call is considered. Each project is served by a single agent process with its own Context Tree, managed by a per-project agent pool. When multiple clients (TUI, CLI, MCP) submit tasks to the same project, a sequential, deduplicated task queue serializes all operations, eliminating write-write conflicts without file-level locking. ByteRover exposes brv-query and brv-curate as MCP tools, enabling integration with any MCP-compatible agent framework. All knowledge is stored as human-readable markdown files on the local filesystem—version-controllable, portable, and requiring zero external infrastructure.

## 3.2 The Context Tree: Data Structure

The Context Tree is a hierarchical file-based knowledge graph organized as Domain $> T o p i c > S u b t o p i c > E n \mathrm { . }$ try. We formalize it as a directed graph $\mathcal { G } = ( \mathcal { N } , \mathcal { E } )$ where nodes $\mathcal { N }$ are knowledge entries (markdown files) and edges $\mathcal { E }$ are explicit cross-references declared via @domain/topic/file.md relation annotations.

### 3.2.1 Knowledge Entry Structure

Each entry $n _ { i } \in \mathcal N$ is a standalone markdown file with structured content (Equation 4, Appendix C):

$$
n _ {i} = \langle \mathcal {R} _ {i}, \mathcal {C} _ {i}, \mathcal {V} _ {i}, \mathcal {S} _ {i}, \mathcal {L} _ {i} \rangle ,\tag{4}
$$

![](images/e10287ce2f5c3550bf05ba3a0f5871dfa5cd8fc522d74f3980afa1bb73322fcf.jpg)

[Image: The image presents a system architecture flowchart divided into three main horizontal sections: Daemon, Agent Process, and Knowledge Layer. Inputs from TUI, CLI (via Socket.IO), and MCP connect to a Daemon layer housing a Task Queue and an Agent Pool, which initiates a separate "Agent Process" for each project. Within the Agent Process, an upper Agent Layer links an LLM Loop and a curate/search component to a lower Execution Layer containing a QueryExecutor and a CurateExecutor plus Sandbox. These components ultimately interact with a Knowledge Layer at the bottom, which utilizes a Context Tree, MiniSearch, and Cache stored on a local filesystem.]  
Figure 1: Architectural overview of ByteRover. Clients (TUI, CLI, MCP) connect via Socket.IO to a daemon that manages a per-project task queue and agent pool. Each agent process contains three logical layers: (1) an Agent Layer where curate and search\_knowledge are first-class tools in the LLM’s reasoning loop; (2) an Execution Layer with a query executor for 5-tier progressive retrieval and a sandboxed curation environment; and (3) a Knowledge Layer with the Context Tree, BM25 full-text index, and query cache, all backed by the local filesystem with no external infrastructure.

where $\mathcal { R } _ { i }$ denotes the relation set (explicit edges to other entries), $\mathcal { C } _ { i }$ is the raw concept (provenance: task, changes, sources, timestamp, author), $\nu _ { i }$ is the narrative (interpreted structure: dependencies, rules, examples, diagrams), $s _ { i }$ contains snippets (code, formulas, raw data), and $\mathcal { L } _ { i }$ is the lifecycle metadata.

### 3.2.2 Relation Graph and Symbol Tree

The edge set E is constructed from explicit @relation annotations in the Relations section of each entry. Unlike embedding-based implicit similarity, these edges represent author-stated semantic connections—the LLM that created the entry decided that these concepts are related and stated why.

A bidirectional reference index maintains both forward links (source → targets it references) and backlinks (target → sources that reference it), enabling graph traversal in both directions with O(1) lookup per entry.

A hierarchical symbol tree provides O(1) lookup from relative paths to knowledge entries and hosts the reference index above. The tree supports five symbol kinds: Domain (1), Topic (2), Subtopic (3), Context (4), and Summary (5). For query and curate operations, a lightweight representation of the tree structure is injected into the agent’s system prompt: either a directory listing of domain and topic names (up to 200 entries) or, when full-text search is available, a compact instruction to use the search tool. This gives the agent ambient awareness of what knowledge exists without dumping full contents.

### 3.2.3 Adaptive Knowledge Lifecycle (AKL)

Each entry carries lifecycle metadata $\mathcal { L } _ { i }$ that governs its evolution over time through an Adaptive Knowledge Lifecycle (AKL) mechanism:

• Importance score $\iota _ { i } \in [ 0 , 1 0 0 ] ;$ : Tracks the value of each entry over time. Access events contribute a +3 bonus; update events contribute +5. A daily decay factor of 0.995 prevents unbounded accumulation.

• Maturity tiers: Entries progress through three tiers based on importance, with hysteresis gaps to prevent rapid oscillation: draft → validated (promotion at $\iota \geq 6 5$ , demotion at $\iota < 3 5 ;$ gap of 30), validated → core (promotion at $\iota \geq 8 5$ , demotion at $\iota < 6 0 ;$ gap of 25).

• Recency decay: A time-dependent score $r _ { i } = \exp ( - \Delta t _ { i } / \tau )$ where $\Delta t _ { i }$ is the number of days since last update and $\tau = 3 0$ is the decay constant (∼21-day half-life).

The compound retrieval score (Equation 5) combines search relevance with lifecycle signals:

$$
\mathrm{Score} (n _ {i}, q) = w _ {r} \cdot \mathrm{BM25} (n _ {i}, q) + w _ {\iota} \cdot \hat {\iota} _ {i} + w _ {t} \cdot r _ {i},\tag{5}
$$

where $\hat { \iota } _ { i }$ is the normalized importance and $w _ { r } , w _ { \iota } , w _ { t }$ are tunable weights.

# 4 Agent-Native Operations

## 4.1 LLM-Curated Knowledge Operations

ByteRover supports five atomic curate operations (Table 1) that the LLM can compose:

<table><tr><td>Operation</td><td>Behavior</td></tr><tr><td>ADD</td><td>Create new entry; auto-generate context.md at each hierarchy level</td></tr><tr><td>UPDATE</td><td>Replace content of an existing entry</td></tr><tr><td>UPSERT</td><td>Add if new, update if exists (reduces pre-check overhead)</td></tr><tr><td>MERGE</td><td>Combine two entries intelligently; delete the source</td></tr><tr><td>DELETE</td><td>Remove a single entry or an entire subtree</td></tr></table>

Table 1: The five atomic curate operations. Every operation carries a reason field that serves as an audit trail.

### 4.1.1 Curation Pipeline

Curation follows a three-phase process:

1. Preprocessing. Source documents are read and validated (max 5 files, 40K characters each). PDFs are converted to text; code files are truncated to 2000 lines.

2. Pre-Compaction. An escalated compression strategy reduces input size through three levels: (L1) LLM summarization, (L2) aggressive LLM summarization at 0.6× token budget, (L3) deterministic binary-search prefix truncation (guaranteed convergence). This ensures curation always terminates regardless of input size.

<table><tr><td>Tier</td><td>Mechanism</td><td>Latency</td><td>Condition</td></tr><tr><td>0</td><td>Exact cache hit</td><td>~0 ms</td><td>Hash match + valid fingerprint</td></tr><tr><td>1</td><td>Fuzzy cache (Jaccard)</td><td>~50 ms</td><td>Jaccard ≥ θfuzzy</td></tr><tr><td>2</td><td>Direct MiniSearch</td><td>~100 ms</td><td>BM25 score ≥ θhigh, sufficient gap</td></tr><tr><td>3</td><td>Optimized LLM call</td><td>&lt;5 s</td><td>BM25 score ≥ θmed</td></tr><tr><td>4</td><td>Full agentic loop</td><td>8–15 s</td><td>All other queries</td></tr></table>

Table 2: The five retrieval tiers with their latency characteristics and escalation conditions.

3. Curation. The LLM agent runs in a sandboxed environment with access to the ToolsSDK—a controlled interface providing curate(), searchKnowledge(), readFile(), and other file operations. The agent reads sources, reasons about patterns and relationships, and produces structured curate operations with explicit provenance.

### 4.1.2 Stateful Feedback Loop

A critical diferentiator from external services is the stateful feedback loop. Each curate call returns per-operation status:

```json
{
    "applied": [
    {"type": "UPSERT", "path": "analysis/semi", "status": "success"},
    {"type": "MERGE", "path": "analysis/energy", "status": "failed",
    "message": "Source file not found"}
],
"summary": {"added": 0, "deleted": 0, "updated": 1, "merged": 0, "failed": 1}
}
```

The agent sees which operations succeeded, which failed, and why. It can reason about failures and adapt—skip the operation, retry with corrections, or flag the gap for later resolution. This feedback loop is impossible when memory is an external service returning HTTP status codes.

### 4.1.3 Atomic Writes and Crash Safety

All file operations use an atomic write-to-temp-then-rename pattern. If the process crashes midwrite, the Context Tree remains consistent—no partial entries or corrupted knowledge.

## 4.2 5-Tier Progressive Retrieval

Retrieval uses a tiered strategy (Table 2) that minimizes LLM calls, illustrated in Figure 2 and formalized in Algorithm 1.

Tiers 0–2 resolve queries without any LLM call, returning cached or high-confidence search results directly. Tier 3 pre-fetches relevant documents and passes them to a single optimized LLM call with constrained output (1,024 tokens, temperature 0.3). Tier 4 is the full agentic fallback: the agent enters a multi-turn reasoning loop where it calls tools (code\_exec, readFile) to navigate the Context Tree, with a higher token budget (2,048 tokens, temperature 0.5) and up to 50 iterations.

### 4.2.1 Search Engine

The search engine is MiniSearch—a lightweight full-text search library with BM25 ranking, fuzzy matching (0.2 character similarity threshold), and prefix search. Field boosting weights titles at 5×

![](images/1cb7808b24f9749bc1c31b71efd0163fdfb65a8bd442530008e4bda83c0a7450.jpg)

[Image: The image displays a hierarchical decision flowchart for processing a query $q$, categorized into four distinct tiers labeled Cache, MiniSearch, LLM, and Agent. The initial Cache tiers check for exact matches or fuzzy matches $\ge 0.6$ within milliseconds, while the subsequent MiniSearch tier evaluates search results for scores $\ge 0.85$ and dominance before returning data or rejecting out-of-distribution inputs. If these fast paths fail, the system proceeds to an LLM-based tier using pre-fetched context in under 5 seconds, or ultimately triggers a full agentic loop that takes 8–15 seconds.]  
Figure 2: The 5-tier progressive retrieval pipeline. Search is initiated in parallel with fingerprint computation. Tiers 0–1 resolve from cache without awaiting search. Tier 2 serves high-confidence results directly from MiniSearch. Only novel or ambiguous queries escalate to Tier 3 (single optimized LLM call with pre-fetched context) or Tier 4 (full agentic loop with tool access). Approximate latencies shown on right.

and paths at 1.5× over content.

Score normalization (Equation 6) maps raw BM25 scores to [0, 1) via:

$$
\hat {s} = \frac {s _ {\mathrm{raw}}}{1 + s _ {\mathrm{raw}}},\tag{6}
$$

yielding interpretable thresholds: strong (15) → 0.94, medium (8) → 0.89, moderate (4) → 0.80, weak (1) → 0.50.

### 4.2.2 Out-of-Domain Detection

When significant query terms (length ≥ 4 characters) do not match any entry in the knowledge base and the normalized score falls below a threshold $( \theta _ { \mathrm { O O D } } = 0 . 8 5 )$ , the system explicitly signals “this query appears outside the scope of stored knowledge.” This prevents hallucinated answers from tangential results—an essential property when agents are making decisions based on retrieved knowledge.
