# 7 EXPERIMENTS

We evaluate HINDSIGHT on two long-term conversational memory benchmarks to measure its ability to retain, recall, and reason over extended interactions. Our evaluation focuses on how well the system maintains coherent memory across many sessions and whether TEMPR and CARA together support accurate, preference-conditioned reasoning.

## 7.1 DATASETS

We use two benchmarks designed to test long-term memory in conversational agents.

### 7.1.1 LONGMEMEVAL

LongMemEval Wu et al. (2024) tests chat assistants on conversations that span many sessions and require recalling information from hundreds of thousands of tokens. The benchmark includes 500 questions that evaluate five core abilities:

• Information Extraction (IE): Retrieving basic facts from past conversations.

• Multi-session Reasoning (MR): Connecting information across different sessions.

• Temporal Reasoning (TR): Understanding when events occurred and their temporal relationships.

• Knowledge Update (KU): Handling updated or contradictory information over time.

• Abstention (ABS): Recognizing when information is not available rather than guessing.

The benchmark provides two conversation settings: the $\mathbf { S }$ setting with around 115,000 tokens spanning roughly 50 sessions, and the M setting with approximately 1.5 million tokens across about 500 sessions. Both settings test the same abilities but at different scales.

<table><tr><td>Statistic</td><td>LongMemEval</td><td>LoCoMo</td></tr><tr><td>Number of conversations</td><td>Varies (S/M)</td><td>50</td></tr><tr><td>Questions</td><td>500</td><td>Varies</td></tr><tr><td>Avg. turns per conversation</td><td>-</td><td>304.9</td></tr><tr><td>Avg. tokens per conversation</td><td>115k (S), 1.5M (M)</td><td>9,209.2</td></tr><tr><td>Avg. sessions per conversation</td><td>50 (S), 500 (M)</td><td>19.3</td></tr><tr><td>Max sessions</td><td>500</td><td>35</td></tr><tr><td>Multimodal</td><td>No</td><td>Yes (images)</td></tr><tr><td>Core abilities tested</td><td>5 (IE, MR, TR, KU, ABS)</td><td>Memory recall</td></tr></table>

Table 2: Statistics for LongMemEval and LoCoMo datasets.

### 7.1.2 LOCOMO

LoCoMo Maharana et al. (2024) evaluates very long-term conversational memory using 50 humanhuman conversations collected over multiple sessions. Each conversation averages 304.9 turns, 9,209.2 tokens, and 19.3 sessions, with some extending up to 35 sessions. The dataset includes multimodal information such as images shared during conversations, making it more realistic than text-only benchmarks. Questions test whether agents can recall personal details, preferences, past events, and context shared across distant sessions.

Table 2 summarizes statistics for both benchmarks.

## 7.2 EVALUATION METRICS

We use an LLM-as-a-judge approach to evaluate response quality (see Appendix A.4 for the complete judge prompt templates). For each test question, HINDSIGHT generates a response using its memory retrieval and reflection pipeline. We then present both the generated response and the ground truth answer to a separate judge LLM, which scores the response on correctness and completeness.

The judge assigns binary correctness scores (0 or 1) for factual accuracy, checking whether the response contains the correct information and does not introduce errors. For questions requiring multi-hop reasoning or temporal awareness, the judge also checks whether the response demonstrates appropriate use of retrieved memories and temporal context. For the abstention ability in LongMemEval, we measure whether HINDSIGHT correctly declines to answer when information is missing, rather than guessing or hallucinating facts.

## 7.3 EXPERIMENTAL SETUP

We evaluate HINDSIGHT using GPT-OSS-20b as the underlying LLM for both TEMPR’s fact extraction and CARA’s reflection operations. All experiments use the same model configuration to isolate the contribution of the memory architecture from model-specific improvements. For evaluation, we use GPT-OSS-120b as the judge LLM with temperature set to 0.0 to ensure consistent and deterministic scoring across all responses.

During retention, we process each conversation session through TEMPR’s extraction pipeline, which produces narrative facts, builds entity links, and updates the memory graph. For each test question, we retrieve memories using the four-way parallel recall mechanism (semantic, keyword, graph, temporal) with Reciprocal Rank Fusion and neural reranking. Retrieved memories are then passed to CARA’s reflection step, which generates the final response conditioned on the bank’s behavioral profile.

We configure memory banks with neutral behavioral profiles (disposition parameters skepticism, literalism, and empathy all set to 3) and low bias strength (0.2) for these experiments, since the benchmarks test factual recall rather than preference-conditioned reasoning. This setup allows us to measure the core memory and retrieval capabilities without introducing strong opinion formation. Token budgets for retrieval are set to <add> tokens for LongMemEval and <add> tokens for LoCoMo, balancing coverage and context efficiency. These budgets are well within the context windows of modern LLMs while providing enough retrieved information for multi-hop reasoning.

For the Hindsight (OSS-20B) configuration, both the memory stack (TEMPR and CARA) and the answer generation model are instantiated with GPT-OSS-20b. For the Hindsight (OSS-120B) and

<table><tr><td>Question Type</td><td>Full-context (GPT-4o)</td><td>Full-context (OSS-20B)</td><td>Zep (GPT-4o)</td><td>Supermemory (GPT-4o)</td><td>Supermemory (GPT-5)</td><td>Supermemory (Gemini-3)</td><td>Hindsight (OSS-20B)</td><td>Hindsight (OSS-120B)</td><td>Hindsight (Gemini-3)</td></tr><tr><td>single-session-user</td><td>81.4</td><td>38.6</td><td>92.9</td><td>97.1</td><td>97.1</td><td>98.6</td><td>95.7</td><td>100.0</td><td>97.1</td></tr><tr><td>single-session-assistant</td><td>94.6</td><td>80.4</td><td>80.4</td><td>96.4</td><td>100.0</td><td>98.2</td><td>94.6</td><td>98.2</td><td>96.4</td></tr><tr><td>single-session-preference</td><td>20.0</td><td>20.0</td><td>56.7</td><td>70.0</td><td>76.7</td><td>70.0</td><td>66.7</td><td>86.7</td><td>80.0</td></tr><tr><td>knowledge-update</td><td>78.2</td><td>60.3</td><td>83.3</td><td>88.5</td><td>87.2</td><td>89.7</td><td>84.6</td><td>92.3</td><td>94.9</td></tr><tr><td>temporal-reasoning</td><td>45.1</td><td>31.6</td><td>62.4</td><td>76.7</td><td>81.2</td><td>82.0</td><td>79.7</td><td>85.7</td><td>91.0</td></tr><tr><td>multi-session</td><td>44.3</td><td>21.1</td><td>57.9</td><td>71.4</td><td>75.2</td><td>76.7</td><td>79.7</td><td>81.2</td><td>87.2</td></tr><tr><td>Overall</td><td>60.2</td><td>39.0</td><td>71.2</td><td>81.6</td><td>84.6</td><td>85.2</td><td>83.6</td><td>89.0</td><td>91.4</td></tr></table>

Table 3: Results on LongMemEval benchmark (S setting, 500 questions). HINDSIGHT with OSS-120B achieves 89.0% overall accuracy, and with Gemini-3 Pro achieves 91.4%, outperforming all baseline systems including Supermemory with frontier models. The Full-context (OSS-20B) baseline shows the performance of the same base model without the HINDSIGHT memory architecture, demonstrating a +44.6% improvement with OSS-20B. Best result in each row shown in bold. All values shown as percentages.

Hindsight (Gemini-3) configurations, the Hindsight memory system itself (fact extraction, memory graph construction, and retrieval) is powered by GPT-OSS-120b. The Hindsight (Gemini-3) rows in both benchmarks use Gemini-3 Pro only as the final answer generator over the retrieved memories, while the underlying memory architecture and the LLM-as-a-judge remain based on GPT-OSS-120b.

Baseline results. We describe next how we benchmark HINDSIGHT against existing approaches.

For LongMemEval (Table 3), baseline scores for Full-context GPT-4o, Zep (GPT-4o), and the three Supermemory configurations (GPT-4o, GPT-5, Gemini-3 Pro) are taken directly from the Supermemory technical report and use their published GPT-4o LLM-as-a-judge setup.

For LoCoMo (Table 4), baseline scores for Backboard, Memobase, Zep, Mem0, Mem0-Graph, LangMem, and OpenAI are presented here as claimed on the official Backboard LoCoMo benchmark results. We treat these numbers as reported reference points rather than our independently reproduced baselines.

Our Hindsight results on both benchmarks are evaluated with a GPT-OSS-120B LLM-as-a-judge for all methods to ensure consistent scoring; in the Gemini-3 configuration, Gemini-3 is used only for answer generation, while memory retrieval and judging remain powered by GPT-OSS-120B.

Readers wishing to reproduce our results or re-evaluate HINDSIGHT can download our code and re-run benchmarks as described in Section 8. We provide access to our Github repository and an interactive results viewer.

## 7.4 RESULTS ON LONGMEMEVAL

Table 3 compares HINDSIGHT to full-context baselines and prior memory systems on the Long-MemEval S setting. The two Full-context baselines pass the entire conversation history to the model as raw context without any structured memory, while Zep and Supermemory pair dedicated memory layers with strong frontier models (GPT-4o, GPT-5, Gemini-3). In contrast, our primary configuration uses a smaller open-source 20B model (GPT-OSS-20B) for both retention and reflection, chosen to be deployable on a single high-end consumer GPU rather than only in large datacenter settings.

Despite this weaker base model, HINDSIGHT with OSS-20B achieves 83.6% overall accuracy, a +44.6 point gain over the Full-context OSS-20B baseline (39.0%), and even surpasses Full-context GPT-4o (60.2%). Relative to other memory systems, HINDSIGHT +OSS-20B matches or exceeds the performance of Zep+GPT-4o (71.2%) and Supermemory+GPT-4o (81.6%), demonstrating that the memory architecture, rather than sheer model size, is carrying much of the performance. The largest gains over the Full-context OSS-20B baseline appear exactly in the long-horizon categories LongMemEval was designed to stress: multi-session questions improve from 21.1% to 79.7% and temporal reasoning from 31.6% to 79.7%, and preference questions increase from 20.0% to 66.7%, indicating that TEMPR’s graph- and time-aware retrieval substantially mitigates context dilution at scale.

<table><tr><td>Method</td><td>Single-Hop</td><td>Multi-Hop</td><td>Open Domain</td><td>Temporal</td><td>Overall</td></tr><tr><td>Backboard</td><td>89.36</td><td>75.00</td><td>91.20</td><td>91.90</td><td>90.00</td></tr><tr><td>Memobase (v0.0.37)</td><td>70.92</td><td>46.88</td><td>77.17</td><td>85.05</td><td>75.78</td></tr><tr><td>Zep</td><td>74.11</td><td>66.04</td><td>67.71</td><td>79.79</td><td>75.14</td></tr><tr><td>Mem0-Graph</td><td>65.71</td><td>47.19</td><td>75.71</td><td>58.13</td><td>68.44</td></tr><tr><td>Mem0</td><td>67.13</td><td>51.15</td><td>72.93</td><td>55.51</td><td>66.88</td></tr><tr><td>LangMem</td><td>62.23</td><td>47.92</td><td>71.12</td><td>23.43</td><td>58.10</td></tr><tr><td>OpenAI</td><td>63.79</td><td>42.92</td><td>62.29</td><td>21.71</td><td>52.90</td></tr><tr><td>Hindsight (OSS-20B)</td><td>74.11</td><td>64.58</td><td>90.96</td><td>76.32</td><td>83.18</td></tr><tr><td>Hindsight (OSS-120B)</td><td>76.79</td><td>62.50</td><td>93.68</td><td>79.44</td><td>85.67</td></tr><tr><td>Hindsight (Gemini-3)</td><td>86.17</td><td>70.83</td><td>95.12</td><td>83.80</td><td>89.61</td></tr></table>

Table 4: Results on LoCoMo benchmark. Accuracy (%) by question type and overall for prior memory systems and our HINDSIGHT architecture with different backbone models. Backboard numbers are taken from their reported figures and could not be independently reproduced. HINDSIGHT with Gemini-3 Pro attains a very similar overall score and the best Open Domain performance. See Section 8 for links to our github code repository and an interactive results viewer for all HINDSIGHT runs.

Scaling the underlying model further amplifies these gains. With OSS-120B, HINDSIGHT reaches 89.0% overall accuracy, outperforming Supermemory with GPT-4o and GPT-5 (81.6% and 84.6%), and with Gemini-3 Pro it attains 91.4%, the best result across all systems and model backbones. Because the Full-context OSS-20B baseline uses the same base model as HINDSIGHT but with no structured memory, the consistent improvements across all question types provide direct evidence that the memory layer drives the observed performance rather than frontier-scale parameters alone.

## 7.5 RESULTS ON LOCOMO

Table 4 reports accuracy on LoCoMo. Across all backbone sizes, HINDSIGHT consistently outperforms prior open memory systems such as Memobase, Zep, Mem0, and LangMem, raising overall accuracy from 75.78% (Memobase) to 83.18% with OSS-20B and 85.67% with OSS-120B. With Gemini-3 as the answer generator, HINDSIGHT attains 89.61% overall accuracy and the highest Open Domain score (95.12%), effectively matching Backboard’s claimed 90.00% overall performance while doing so with a fully open-source memory stack, released evaluation code, and an interactive results viewer (Section 8). These results show that the gains from our memory architecture on LongMemEval transfer to realistic, multi-session human conversations.

# 8 CODE AVAILABILITY

We release our implementation of HINDSIGHT at https://github.com/vectorize-io/ hindsight . The repository provides (i) the full memory architecture, including retain/recall/reflect pipelines and the four-network memory representation; (ii) scripts and configuration files to run LongMemEval and LoCoMo with different backbones and judging setups; and (iii) utilities for fact extraction, graph construction, and analysis of retrieved memories. To facilitate inspection and comparison of runs, we also provide the HINDSIGHT Benchmarks Viewer at https://hindsight-benchmarks.vercel.app/, which hosts per-question results that users can drill into, retrieved memory contexts, model and judge configurations, and aggregate metrics for all HINDSIGHT variants reported in this paper.

# 9 CONCLUSION

We have introduced HINDSIGHT, an approach to treat agent memory as a first-class substrate for reasoning, rather than a thin retrieval layer around a stateless model. By organizing an agent’s longterm memory into world, bank, observation, and opinion networks and implementing retain, recall, and reflect as explicit operations, the architecture separates evidence from synthesized summaries and beliefs while remaining compatible with modern LLMs. Our experimental results demonstrate that this structure matters in practice and clearly leads to significant improvements in performance.

Looking ahead, we see several directions for extending this work. On the modeling side, learning to jointly optimize fact extraction, graph construction, and retrieval—–rather than treating them as fixed pipelines—–could further improve robustness and efficiency, especially in noisy, open-domain settings. A reinforcement learning loop would be ideal to explore the interplay between retain, recall, and reflect as done here.

On the application side, we plan to integrate HINDSIGHT with richer tool-use and workflow orchestration, exploring more diverse benchmarks than the conversational setting considered here. Finally, extending the opinion and belief layer to support controlled forgetting, time-aware belief revision, and privacy-aware memory management offers a path toward long-lived agents.

# REFERENCES

Qingyao Ai, Yichen Tang, Changyue Wang, Jianming Long, Weihang Su, and Yiqun Liu. Memorybench: A benchmark for memory and continual learning in llm systems. arXiv preprint arXiv:2510.17281, 2025.

Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building production-ready ai agents with scalable long-term memory. arXiv preprint arXiv:2504.19413, 2025.

Jen-tse Huang, Kaiser Sun, Wenxuan Wang, and Mark Dredze. Llms do not have human-like working memory. arXiv preprint arXiv:2505.10571, 2025.

Junming Liu, Yifei Sun, Weihua Cheng, Haodong Lei, Yirong Chen, Licheng Wen, Xuemeng Yang, Daocheng Fu, Pinlong Cai, Nianchen Deng, et al. Memverse: Multimodal memory for lifelong learning agents. arXiv preprint arXiv:2512.03627, 2025.

Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. Evaluating very long-term conversational memory of llm agents. arXiv preprint arXiv:2402.17753, 2024.

Charles Packer, Vivian Fang, Shishir\_G Patil, Kevin Lin, Sarah Wooders, and Joseph\_E Gonzalez. Memgpt: Towards llms as operating systems. 2023.

Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: a temporal knowledge graph architecture for agent memory. arXiv preprint arXiv:2501.13956, 2025.

Lianlei Shan, Shixian Luo, Zezhou Zhu, Yu Yuan, and Yong Wu. Cognitive memory in large language models. arXiv preprint arXiv:2504.02441, 2025.

Mohammad Tavakoli, Alireza Salemi, Carrie Ye, Mohamed Abdalla, Hamed Zamani, and J Ross Mitchell. Beyond a million tokens: Benchmarking and enhancing long-term memory in llms. arXiv preprint arXiv:2510.27246, 2025.

Zixuan Wang, Bo Yu, Junzhe Zhao, Wenhao Sun, Sai Hou, Shuai Liang, Xing Hu, Yinhe Han, and Yiming Gan. Karma: Augmenting embodied ai agents with long-and-short term memory systems. In 2025 IEEE International Conference on Robotics and Automation (ICRA), pp. 1–8. IEEE, 2025.

Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. Longmemeval: Benchmarking chat assistants on long-term interactive memory. arXiv preprint arXiv:2410.10813, 2024.

Yaxiong Wu, Sheng Liang, Chen Zhang, Yichao Wang, Yongyue Zhang, Huifeng Guo, Ruiming Tang, and Yong Liu. From human memory to ai memory: A survey on memory mechanisms in the era of llms. arXiv preprint arXiv:2504.15965, 2025.

Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-mem: Agentic memory for llm agents. arXiv preprint arXiv:2502.12110, 2025.

Sikuan Yan, Xiufeng Yang, Zuchao Huang, Ercong Nie, Zifeng Ding, Zonggen Li, Xiaowen Ma, Kristian Kersting, Jeff Z Pan, Hinrich Schütze, et al. Memory-r1: Enhancing large language model agents to manage and utilize memories via reinforcement learning. arXiv preprint arXiv:2508.19828, 2025.

Dianxing Zhang, Wendong Li, Kani Song, Jiaye Lu, Gang Li, Liuchun Yang, and Sheng Li. Memory in large language models: Mechanisms, evaluation and evolution. arXiv preprint arXiv:2509.18868, 2025a.

Zeyu Zhang, Quanyu Dai, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Jieming Zhu, Zhenhua Dong, and Ji-Rong Wen. A survey on the memory mechanism of large language model-based agents. ACM Transactions on Information Systems, 43(6):1–47, 2025b.
