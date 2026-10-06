# 5 Experiments

We conduct comprehensive experiments to evaluate both the reasoning efectiveness and system properties of ByteRover over state-of-the-art baselines (Tables 3–5).

## 5.1 Experimental Setup

Datasets. We evaluate on two widely adopted long-term conversational benchmarks: (1) Lo-CoMo [Maharana et al., 2024], which contains ultra-long conversations (average length of ∼20K tokens across 35 sessions) designed to assess long-range temporal and causal retrieval; and (2) LongMemEval S [Wu et al., 2025], the full-scale variant of LongMemEval with 500 questions spanning six memoryability categories, average context length exceeding 100K tokens across ∼48 sessions per question, designed to stress-test memory retention and scalability under realistic interaction horizons.

```txt
Algorithm 1 5-Tier Progressive Retrieval
Require: Query q, Cache C, Search Index I, Agent A
Ensure: Response R, Tier τ
1: h ← Hash(q)
2: if h ∈ C and Fingerprint(C[h]) = Fingerprint(G) then
3: return C[h], τ = 0 {Exact cache hit}
4: end if
5: q' ← arg max_{c∈C} Jaccard(q, c)
6: if Jaccard(q, q') ≥ θ_fuzzy then
7: return C[q'], τ = 1 {Fuzzy cache hit}
8: end if
9: D ← MiniSearch(I, q) {BM25 + fuzzy + prefix}
10: if Score(D₁) ≥ θ_high and Gap(D₁, D₂) ≥ θ_gap then
11: return DirectResponse(D), τ = 2 {High-confidence search}
12: end if
13: if Score(D₁) ≥ θ_med then
14: C_pre ← Prefetch(D)
15: return LLM(q, C_pre), τ = 3 {Optimized single LLM call}
16: end if
17: return A.AgenticLoop(q), τ = 4 {Full multi-turn reasoning}
```

Baselines. On LoCoMo, we evaluate six memory systems under a unified protocol using our benchmark harness with identical judge configuration, enabling direct comparison: Mem0 [Chhikara et al., 2025], Zep [Rasmussen et al., 2025], Hindsight [Latimer et al., 2025], HonCho,<sup>1</sup> Memobase,<sup>2</sup> and OpenAI Memory (ChatGPT). These systems span the spectrum from structured fact extraction (Mem0, Memobase) to graph-based memory architectures (Zep, Hindsight) and commercial assistants (OpenAI Memory, HonCho).

On LongMemEval-S, we include our own evaluations of Hindsight and HonCho alongside published results from Chronos [Sen et al., 2026], SmartSearch [Derehag et al., 2026], Memora [Xia et al., 2026], TiMem [Li et al., 2026], Zep, and a full-context baseline, cited from their respective publications. Results marked with † use diferent backbone and judge configurations; see Table 4 for details.

Metrics. We adopt LLM-as-a-Judge [Zheng et al., 2023] as the primary metric, where a judge model evaluates each generated answer against the ground truth and returns a binary correctness label. For our own evaluations, we use Gemini 3 Flash as the judge with a separate justifier model (Gemini 3.1 Pro) that synthesizes an answer from retrieved context before scoring. Both models run at temperature 0.0. The judge uses a token budget of 8,192 with thinking disabled, while the justifier uses 32,768 tokens with low thinking budget. Full hyperparameter details are provided in

<table><tr><td>Method</td><td>Single-Hop</td><td>Multi-Hop</td><td>Open-Domain</td><td>Temporal</td><td>Overall</td></tr><tr><td>HonCho</td><td>93.2</td><td>84.0</td><td>77.1</td><td>88.2</td><td>89.9</td></tr><tr><td>Hindsight</td><td>86.2</td><td>70.8</td><td>95.1</td><td>83.8</td><td>89.6</td></tr><tr><td>Memobase</td><td>70.9</td><td>46.9</td><td>77.2</td><td>85.1</td><td>75.8</td></tr><tr><td>Zep</td><td>74.1</td><td>66.0</td><td>67.7</td><td>79.8</td><td>75.1</td></tr><tr><td>Mem0</td><td>67.1</td><td>51.2</td><td>72.9</td><td>55.5</td><td>66.9</td></tr><tr><td>OpenAI Memory</td><td>63.8</td><td>42.9</td><td>62.3</td><td>21.7</td><td>52.9</td></tr><tr><td>BYTEROVER (ours)</td><td>97.5</td><td>93.3</td><td>85.9</td><td>97.8</td><td>96.1</td></tr></table>

Table 3: LLM-as-Judge accuracy (%) on LoCoMo (4 categories, 1,982 questions). All systems evaluated under identical conditions using our benchmark harness with Gemini 3 Flash as the judge.

Appendix B.

Evaluation prompts. To enable direct, apples-to-apples comparison with Hindsight [Latimer et al., 2025], we reuse their publicly available evaluation prompts.<sup>3</sup> Specifically, the judge prompts— including the default LoCoMo preamble and all five LongMemEval category-specific preambles (standard, temporal-reasoning, knowledge-update, and preference)—are adopted without modification, ensuring that scoring criteria are identical across systems. The LoCoMo justifier prompt is likewise reused verbatim. For the LongMemEval justifier, we adapt Hindsight’s prompt to reflect ByteRover’s single-layer knowledge representation: where Hindsight instructs the model to crossreference atomic facts against raw source chunks (a two-layer retrieval output), our variant replaces this with guidance for interpreting key facts with session-level timestamps, matching the Context Tree’s curated entry format. All other instructions—date calculation rules, counting-question disambiguation, recommendation handling, and question-type-specific guidelines—remain unchanged from the original.

## 5.2 Overall Comparison on LoCoMo

ByteRover achieves the highest overall accuracy at 96.1%, outperforming the next-best system (HonCho, 89.9%) by 6.2 percentage points. The gains are particularly pronounced on multi-hop questions (+9.3 over HonCho), which require synthesizing information across distant sessions— a task where the Context Tree’s explicit inter-entry relations provide navigable paths that flat memory stores lack. On temporal queries, ByteRover reaches 97.8%, benefiting from structured timestamps embedded in each entry’s metadata that enable precise temporal grounding. The sole category where ByteRover does not lead is open-domain, where Hindsight achieves 95.1% versus 85.9%. Open-domain questions frequently require commonsense reasoning that extends beyond the conversation corpus, an area where retrieval-augmented approaches can excel by leveraging the backbone LLM’s parametric knowledge.

## 5.3 Generalization on LongMemEval-S

ByteRover achieves the highest overall accuracy at 92.8%, surpassing Chronos-Low (92.6%, GPT-4o backbone) while remaining below Chronos-High (95.6%, Claude Opus 4.6 backbone), which benefits from a substantially more capable generation model. The strength profile is distinctive:

<table><tr><td>Method</td><td>KU</td><td>SSU</td><td>SSA</td><td>SSP</td><td>TR</td><td>MS</td><td>Overall</td></tr><tr><td> $Chronos^†$ </td><td>96.2</td><td>94.3</td><td>100.0</td><td>80.0</td><td>90.2</td><td>91.7</td><td>92.6</td></tr><tr><td>Hindsight</td><td>94.9</td><td>97.1</td><td>96.4</td><td>80.0</td><td>91.0</td><td>87.2</td><td>91.4</td></tr><tr><td>HonCho</td><td>94.9</td><td>94.3</td><td>96.4</td><td>90.0</td><td>88.7</td><td>85.0</td><td>90.4</td></tr><tr><td> $SmartSearch^†$ </td><td>93.6</td><td>100.0</td><td>85.7</td><td>96.7</td><td>82.7</td><td>84.2</td><td>88.4</td></tr><tr><td> $Memora^†$ </td><td>97.4</td><td>98.6</td><td>78.6</td><td>83.3</td><td>89.5</td><td>78.2</td><td>87.4</td></tr><tr><td> $TiMem^†$ </td><td>87.7</td><td>96.3</td><td>85.7</td><td>55.3</td><td>73.4</td><td>72.8</td><td>79.0</td></tr><tr><td> $Zep^†$ </td><td>83.3</td><td>92.9</td><td>80.4</td><td>56.7</td><td>62.4</td><td>57.9</td><td>71.2</td></tr><tr><td> $Full-context^†$ </td><td>78.2</td><td>81.4</td><td>94.6</td><td>20.0</td><td>45.1</td><td>44.3</td><td>60.2</td></tr><tr><td>BYTEROVER (ours)</td><td>98.7</td><td>98.6</td><td>98.2</td><td>96.7</td><td>91.7</td><td>84.2</td><td>92.8</td></tr></table>

Table 4: LLM-as-Judge accuracy (%) on LongMemEval-S (500 questions). KU = Knowledge Update, SSU = Single-Session User, SSA = Single-Session Assistant, SSP = Single-Session Preference, TR = Temporal Reasoning, MS = Multi-Session. Hindsight and HonCho evaluated with our harness (Gemini 3 Flash judge). <sup>†</sup>Results from respective papers; backbone and judge configurations difer.

<table><tr><td>Metric</td><td>LoCoMo</td><td>LongMemEval-S</td></tr><tr><td>Context tree size</td><td>272 docs</td><td>23,867 docs</td></tr><tr><td>Total queries</td><td>1,982</td><td>500</td></tr><tr><td>Cold query latency p50</td><td>1.2 s</td><td>1.6 s</td></tr><tr><td>Cold query latency p95</td><td>1.4 s</td><td>2.3 s</td></tr><tr><td>Cold query latency p99</td><td>1.7 s</td><td>2.5 s</td></tr></table>

Table 5: Operational latency profile. Cold query latency measures end-to-end time from process invocation through response delivery, excluding answer justification and evaluation.

ByteRover leads on knowledge update (98.7%), temporal reasoning (91.7%), and single-session preference (96.7%, tied with SmartSearch), categories that reward precise fact retrieval and temporal grounding—capabilities directly served by the Context Tree’s structured entries and timestampaware indexing. The weakest category is multi-session (84.2%), which requires cross-session synthesis over long horizons and represents the primary area for improvement. Notably, Chronos achieves 91.7% on multi-session, suggesting that its event-ordering approach may better capture inter-session dependencies.

## 5.4 Operational Profile

Despite a substantially larger context tree on LongMemEval-S (23,867 documents vs. 272 on Lo-CoMo), median query latency remains low at 1.6 s, suggesting that the tiered retrieval architecture efectively bounds search cost as the corpus grows. The tight percentile spread (p50-to-p99 gap of 0.5 s on LoCoMo, 0.9 s on LongMemEval-S) indicates consistent performance without long-tail degradation.

## 5.5 Ablation Study

To assess the contribution of individual components, we conduct an ablation study on LongMemEval-S by selectively disabling three key query-time mechanisms. Ablation experiments are conducted on LongMemEval-S, where the larger corpus (23,867 documents) provides a more demanding test of retrieval-side components; LoCoMo results (Table 3) serve as a generalization test on a smaller corpus.

<table><tr><td>Configuration</td><td>KU</td><td>SSU</td><td>SSA</td><td>SSP</td><td>TR</td><td>MS</td><td>Overall</td><td> $\Delta$ </td></tr><tr><td>w/o Tiered Retrieval</td><td>69.2</td><td>71.4</td><td>76.8</td><td>83.3</td><td>61.7</td><td>47.4</td><td>63.4</td><td>-29.4</td></tr><tr><td>w/o OOD Detection</td><td>98.7</td><td>98.6</td><td>98.2</td><td>96.7</td><td>89.5</td><td>85.0</td><td>92.4</td><td>-0.4</td></tr><tr><td>w/o Relation Graph</td><td>98.7</td><td>98.6</td><td>98.2</td><td>96.7</td><td>89.5</td><td>85.0</td><td>92.4</td><td>-0.4</td></tr><tr><td>BYTEROVER (Full)</td><td>98.7</td><td>98.6</td><td>98.2</td><td>96.7</td><td>91.7</td><td>84.2</td><td>92.8</td><td>—</td></tr></table>

Table 6: Ablation study on LongMemEval-S (500 questions). Each row disables one query-time component while keeping the curated Context Tree unchanged. Category abbreviations follow Table 4.

w/o Tiered Retrieval. All queries are routed to the full agentic loop (Tier 4), bypassing Tiers 0– 3 and the separate justifier model (see §4.2 for the distinction between tiers). This ablation produces the largest accuracy drop (−29.4 pp, from 92.8% to 63.4%). Multi-session questions sufer most severely (84.2% → 47.4%), followed by temporal reasoning (91.7% → 61.7%). The result demonstrates that the tiered architecture is not merely a latency optimization: the lower tiers surface precise, high-confidence content that the justifier can faithfully synthesize, whereas unconstrained agentic reasoning over a 23,867-document corpus compounds retrieval errors with generation errors.

w/o OOD Detection. Disabling the out-of-domain rejection gate produces only a modest overall decline (−0.4 pp, from 92.8% to 92.4%), with the efect concentrated in temporal reasoning (91.7% → 89.5%, −2.2 pp). Four categories (KU, SSU, SSA, SSP) are completely unafected, indicating that OOD detection primarily guards against temporal and multi-session queries where partial matches from unrelated sessions could otherwise mislead the justifier. The small magnitude suggests the curated Context Tree already provides strong topical coherence, limiting the opportunities for OOD errors.

w/o Relation Graph. Removing explicit cross-entry relations produces the same overall decline as disabling OOD detection (−0.4 pp, 92.4%), with an identical per-category profile: temporal reasoning drops by 2.2 pp (91.7% → 89.5%) while multi-session improves slightly (84.2% → 85.0%). The identical scores to the OOD ablation suggest that, on LongMemEval-S’s question distribution, relation edges and OOD gates address overlapping failure modes—both primarily afect queries that require disambiguating temporally adjacent sessions. The relation graph’s contribution may be more pronounced on benchmarks with explicit multi-hop reasoning demands (e.g., LoCoMo’s multi-hop category, where relations provide navigable paths across conversation boundaries).

Components not ablated. Three mechanisms—Adaptive Knowledge Lifecycle (AKL), the curation feedback loop, and escalated compression—operate exclusively during the write path (curation). Since the curated Context Tree is held constant across all ablation conditions, their contribution can not be isolated through query-time ablation on a static benchmark. Evaluating these components would require re-curation under degraded conditions, which we leave to future work.

# 6 Conclusion

We introduced ByteRover, an agent-native memory architecture that inverts the conventional MAG paradigm: instead of delegating knowledge storage to an external service, the same LLM that reasons about a task curates knowledge into a hierarchical Context Tree with explicit relations, provenance, and lifecycle management. By making memory operations first-class tools in the agent’s reasoning loop, ByteRover enables a stateful feedback loop that eliminates semantic drift, preserves coordination context across agents, and supports graceful recovery from failures.

The 5-tier progressive retrieval strategy resolves most queries at sub-100 ms latency without LLM calls, while the Adaptive Knowledge Lifecycle enables knowledge to naturally evolve—reinforcing frequently accessed entries and decaying stale ones. Empirical results on LoCoMo and LongMemEval demonstrate that ByteRover achieves competitive or state-of-the-art accuracy while requiring zero external infrastructure, with all knowledge stored as human-readable markdown files on the local filesystem.

# 7 Limitations

While ByteRover demonstrates strong architectural properties, it has several limitations that warrant discussion.

First, the write path is expensive. LLM-curated knowledge requires reasoning per curation event, which is slower and more costly than mechanical chunking and embedding. For use cases where write throughput is critical (e.g., real-time ingestion of high-frequency data streams), the curation overhead may be prohibitive.

Second, novel queries are slower than vector search. When queries miss the cache and index (Tier 3–4), ByteRover requires an LLM call that a vector similarity search does not. The design assumes that agents ask many variations of a smaller set of questions, so the cache absorbs most of the load. When this assumption does not hold, retrieval latency increases.

Third, curation quality depends on backbone model capability. This is a shared limitation across all MAG systems [Jiang et al., 2026b], but ByteRover’s deeper reliance on LLM reasoning for both storage and retrieval amplifies the impact of backbone sensitivity. Open-weight models with higher format error rates may produce lower-quality knowledge entries.

Fourth, the file-based storage may face scaling challenges at very large knowledge bases. The in-memory MiniSearch index and sequential task queue are designed for knowledge bases of up to ∼10K entries. Beyond this scale, sharding strategies or alternative indexing backends may be needed.

Finally, the sequential task queue limits write throughput under heavy concurrent load. While this is rarely a bottleneck in practice (curation is an infrequent, high-cost operation), deployments with many agents writing simultaneously may experience queuing delays.

# References

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.

Iz Beltagy, Matthew E Peters, and Arman Cohan. Longformer: The long-document transformer. arXiv preprint arXiv:2004.05150, 2020.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. Advances in Neural Information Processing Systems, 33:1877–1901, 2020.

Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building production-ready ai agents with scalable long-term memory. arXiv preprint arXiv:2504.19413, 2025.

Jesper Derehag, Carlos Calva, and Timmy Ghiurau. Smartsearch: How ranking beats structure for conversational memory retrieval. arXiv preprint arXiv:2603.15599, 2026.

Bernal Jiménez Gutiérrez, Yiheng Shu, Sizhe Qi, Weijian Zhou, and Yu Su. From rag to memory: Non-parametric continual learning for large language models. In International Conference on Machine Learning, 2025.

Chuanrui Hu, Xingze Gao, Zuyi Zhou, Dannong Xu, Yi Bai, Xintong Li, Hui Zhang, Tong Li, Chong Zhang, Lidong Bing, et al. Evermemos: A self-organizing memory operating system for structured long-horizon reasoning. arXiv preprint arXiv:2601.02163, 2026.

Dongming Jiang, Yi Li, Guanpeng Li, and Bingzhe Li. Magma: A multi-graph based agentic memory architecture for ai agents. arXiv preprint arXiv:2601.03236, 2026a.

Dongming Jiang, Yi Li, Songtao Wei, Jinxin Yang, Ayushi Kishore, Alysa Zhao, Dingyi Kang, Xu Hu, Feng Chen, Qiannan Li, and Bingzhe Li. Anatomy of agentic memory: Taxonomy and empirical analysis of evaluation and system limitations. arXiv preprint arXiv:2602.19320, 2026b.

Ziyan Jiang, Xueguang Ma, and Wenhu Chen. Longrag: Enhancing retrieval-augmented generation with long-context llms. arXiv preprint arXiv:2406.15319, 2024.

Jiazheng Kang, Mingming Ji, Zhe Zhao, and Ting Bai. Memory os of ai agent. arXiv preprint arXiv:2506.06326, 2025a.

Jikun Kang, Wenqi Wu, Filippos Christianos, Alex James Chan, Fraser David Greenlee, George Thomas, Marvin Purtorab, and Andrew Toulis. Lm2: Large memory models. arXiv preprint arXiv:2502.06049, 2025b.

Chris Latimer, Nicolo Boschi, Andrew Neeser, Chris Bartholomew, Gaurav Srivastava, Xuan Wang, and Naren Ramakrishnan. Hindsight is 20/20: Building agent memory that retains, recalls, and reflects. arXiv preprint arXiv:2512.12818, 2025.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33:9459–9474, 2020.

Kai Li, Xuanqing Yu, Ziyi Ni, Yi Zeng, Yao Xu, Xin Zhang, Jitao Li, Xiaogang Sang, Xuelei Duan, Xiaogang Wang, et al. Timem: Temporal-hierarchical memory consolidation for long-horizon conversational agents. arXiv preprint arXiv:2601.02845, 2026.

Jiaqi Liu, Yaofeng Su, Peng Xia, Siwei Han, Zeyu Zheng, Cihang Xie, Mingyu Ding, and Huaxiu Yao. Simplemem: Eficient lifelong memory for llm agents. arXiv preprint arXiv:2601.02553, 2026.

Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. Transactions of the Association for Computational Linguistics, 12:157–173, 2024.

Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of llm agents. arXiv preprint arXiv:2402.17753, 2024.

Ali Modarressi, Ayyoob Imani, Mohsen Fayyaz, and Hinrich Schütze. RET-LLM: Towards a general read-write memory for large language models. arXiv preprint arXiv:2305.14322, 2023.

Jiayan Nan, Wenquan Ma, Wenlong Wu, and Yize Chen. Nemori: Self-organizing agent memory inspired by cognitive science. arXiv preprint arXiv:2508.03341, 2025.

Charles Packer, Vivian Fang, Shishir G Patil, Kevin Lin, Sarah Wooders, and Joseph E Gonzalez. Memgpt: Towards llms as operating systems. arXiv preprint arXiv:2310.08560, 2023.

Joon Sung Park, Joseph C O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology, pages 1–22, 2023.

Ofir Press, Noah A Smith, and Mike Lewis. Train short, test long: Attention with linear biases enables input length extrapolation. In International Conference on Learning Representations, 2022.

Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: A temporal knowledge graph architecture for agent memory. arXiv preprint arXiv:2501.13956, 2025.

Sahil Sen, Elias Lumer, Anmol Gulati, and Vamse Kumar Subbiah. Chronos: Temporal-aware conversational agents with structured event retrieval for long-term memory. arXiv preprint arXiv:2603.16862, 2026.

Zheng Wang, Shu Teo, Jieer Ouyang, Yongjun Xu, and Wei Shi. M-rag: Reinforcing large language model performance through retrieval-augmented generation with multiple partitions. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1966–1978, 2024.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. Advances in Neural Information Processing Systems, 35:24824–24837, 2022.

Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. Longmemeval: Benchmarking chat assistants on long-term interactive memory. In International Conference on Learning Representations, 2025.

Menglin Xia, Xuchao Zhang, Shantanu Dixit, Paramaguru Harimurugan, Rujia Wang, Victor Ruhle, Robert Sim, Chetan Bansal, and Saravan Rajmohan. Memora: A harmonic memory representation balancing abstraction and specificity. arXiv preprint arXiv:2602.03315, 2026.

Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-MEM: Agentic memory for llm agents. In Advances in Neural Information Processing Systems, volume 38, 2025.

Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. Advances in Neural Information Processing Systems, 36:46595–46623, 2023.

Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language models with long-term memory. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pages 19724–19731, 2024.

# A Related Work

We organize related work along the progression from context-window extension to retrieval-augmented generation and finally to memory-augmented generation, then discuss the external-service paradigm that ByteRover departs from.

Context-Window Extension. A direct line of work extends the efective context length of Transformers by modifying attention or positional extrapolation. Longformer [Beltagy et al., 2020] introduces sparse attention patterns, while ALiBi [Press et al., 2022] enables length extrapolation by injecting distance-aware linear biases into attention scores. More recently, LM2 [Kang et al., 2025b] proposes a decoder-only architecture augmented with auxiliary memory. While these approaches improve long-range coverage, they do not address the continual, evolving, and write-back nature of agent memory.

Retrieval-Augmented Generation. RAG [Lewis et al., 2020] augments an LLM with external retrieval over a fixed corpus. LongRAG [Jiang et al., 2024] studies integration with long-context LLMs, while M-RAG [Wang et al., 2024] uses multiple partitions for fine-grained retrieval. However, standard RAG typically assumes a static knowledge base, whereas agentic settings require memory that is continuously updated [Gutiérrez et al., 2025].

Memory-Augmented Generation. MAG systems maintain a time-variant memory that evolves via a feedback loop [Zhong et al., 2024, Park et al., 2023]. Recent work spans multiple architectural categories [Jiang et al., 2026b]: graph-structured memory (MAGMA [Jiang et al., 2026a], Zep [Rasmussen et al., 2025]), hierarchical tiers (MemGPT [Packer et al., 2023], MemoryOS [Kang et al., 2025a], EverMemOS [Hu et al., 2026]), entity-centric stores (A-MEM [Xu et al., 2025], Mem0 [Chhikara et al., 2025]), and episodic/reflective designs (Nemori [Nan et al., 2025]). All of these operate as external services that agents call into. ByteRover departs from this paradigm by embedding memory operations directly in the agent’s reasoning loop.

Benchmarks and Evaluation. LoCoMo [Maharana et al., 2024] evaluates long-term conversational memory across 35 sessions with temporal and causal reasoning questions. LongMemEval [Wu et al., 2025] stress-tests memory retention at context lengths exceeding 100K tokens. Recent analysis [Jiang et al., 2026b] reveals that many benchmarks risk context saturation—fitting within modern 128K+ windows—and that lexical metrics (F1, BLEU) systematically diverge from semantic correctness, motivating the use of LLM-as-a-Judge evaluation [Zheng et al., 2023].

# B Hyperparameter Configuration

# C Context Tree Entry Example

Figure 3 shows a complete knowledge entry as stored on disk in the Context Tree.

<table><tr><td>Module</td><td>Parameter</td><td>Value</td></tr><tr><td rowspan="4">Search Index</td><td>MiniSearch version</td><td>v7</td></tr><tr><td>Fields</td><td>title (5×), content (1×), path (1.5×)</td></tr><tr><td>Max retrieval results</td><td>32</td></tr><tr><td>Max content length</td><td>8,000 chars</td></tr><tr><td rowspan="3">Search Config</td><td>Fuzzy ratio</td><td>0.2</td></tr><tr><td>Prefix matching</td><td>enabled</td></tr><tr><td>Score normalization</td><td>s/(1+s)</td></tr><tr><td rowspan="3">Direct Response</td><td>High confidence threshold</td><td>0.93</td></tr><tr><td>Minimum score</td><td>0.85</td></tr><tr><td>Minimum gap (top vs #2)</td><td>0.08</td></tr><tr><td rowspan="2">OOD Detection</td><td>Minimum relevance score</td><td>0.6</td></tr><tr><td>Unmatched term threshold</td><td>0.85</td></tr><tr><td rowspan="3">Lifecycle</td><td>Importance decay (daily)</td><td> $0.995^{\Delta t}$ </td></tr><tr><td>Recency decay</td><td> $e^{-\Delta t/30}$ </td></tr><tr><td>Maturity thresholds</td><td>draft &lt; 35, core ≥ 85</td></tr><tr><td rowspan="2">Curation</td><td>Max files per operation</td><td>5</td></tr><tr><td>Max chars per file</td><td>40,000</td></tr><tr><td rowspan="2">Compression</td><td>Level 1 (LLM)</td><td>Normal summarization</td></tr><tr><td>Level 2 (Aggressive)</td><td>0.6× token budget</td></tr><tr><td rowspan="2">Cache</td><td>Query cache TTL</td><td>0 (disabled)</td></tr><tr><td>Fingerprint cache TTL</td><td>0 (disabled)</td></tr><tr><td rowspan="2">Inference</td><td>LLM Backbone (curate/query)</td><td>Gemini 3 Flash</td></tr><tr><td>Temperature</td><td>0.0</td></tr><tr><td rowspan="4">Judge</td><td>Model</td><td>Gemini 3 Flash</td></tr><tr><td>Max tokens</td><td>8,192</td></tr><tr><td>Thinking budget</td><td>0 (disabled)</td></tr><tr><td>Prompts</td><td>Hindsight (verbatim)</td></tr><tr><td rowspan="4">Justifier</td><td>Model</td><td>Gemini 3.1 Pro</td></tr><tr><td>Max tokens</td><td>32,768</td></tr><tr><td>Thinking budget</td><td>low</td></tr><tr><td>Prompts</td><td>Hindsight (adapted for LongMemEval)</td></tr></table>

Table 7: Hyperparameter configuration for ByteRover and evaluation pipeline.

![](images/236bb617d56acd473c0fe3f1e6b203f664869ea68af74e2d0ec79a98024bd6e0.jpg)

[Image: The image displays a markdown document titled "Auth-Billing Circular Dependency" positioned within a technical documentation directory labeled "module_boundaries". The document includes YAML frontmatter containing metadata such as tags (architecture, tech-debt), timestamps indicating creation in February 2026, and hyperlinks to related assessment files. The main body outlines a triangular dependency cycle among auth, billing, and user-management modules, specifically identifying `src/auth/middleware.ts` and `src/billing/subscriptionCheck.ts` as the source files for this conflict. It further defines rules classifying circular dependencies with runtime imports as high severity and those limited to types as low severity.]  
Figure 3: A complete knowledge entry in the Context Tree, showing the YAML frontmatter with lifecycle metadata, explicit relation annotations, raw concept (provenance), and narrative (interpreted structure).
