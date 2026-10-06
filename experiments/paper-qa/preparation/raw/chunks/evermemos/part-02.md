# 4 Experiments

We evaluate EverMemOS on two long-horizon memory-augmented reasoning benchmarks (Lo-CoMo (Maharana et al., 2024) and Long-MemEval (Wu et al., 2025)), and report a profile study on PersonaMem-v2 (Jiang et al., 2025).

## 4.1 Experimental Setup

Benchmarks We evaluate memory-augmented reasoning on LoCoMo and LongMemEval. Lo-CoMo contains 1,540 questions over 10 ultra-long dialogues (∼9K tokens each), spanning single-hop, multi-hop, and temporal questions. LongMemEval (S-setting, ∼115k tokens per conversation) evaluates 500 questions requiring full-history parsing across core capabilities (e.g., updates and abstention). We additionally evaluate user profiling on PersonaMem-v2.

Baselines We compare EverMemOS against state-of-the-art memory systems: Zep (Rasmussen et al., 2025), Mem0 (Chhikara et al., 2025), MemOS (Li et al., 2025), MemoryOS (Kang et al., 2025), and MemU<sup>1</sup>. Fair comparison: We standardize the answer-generation backbone across methods while keeping each baseline’s official memory configuration unchanged; for Long-MemEval, we report baseline scores from the official MemOS leaderboard. Full settings are provided in Appendix A.1.

Evaluation Protocol We adopt the LLM-as-ajudge protocol, following MemOS: each answer is evaluated by GPT-4o-mini and two auxiliary judge models, and scores are averaged across the three judgments in a blind setting. We validate the reliability of this protocol against human annotations in Section A.2 (Appendix), showing high agreement (Cohen’s κ > 0.89).

Implementation Details EverMemOS uses GPT-4.1-mini (or GPT-4o-mini where specified) for all reasoning and memory operations. Retrieval uses hybrid dense+BM25 fusion (RRF) with reranking. Default retrieval hyperparameters are in

Appendix A.1. Unless otherwise specified, quantitative experiments use Memory-Augmented Reasoning. We provide a token-level cost breakdown by lifecycle phase in Appendix (Table 8).

## 4.2 Main Results

Main results on two benchmarks are reported in Tables 1-2. We make three observations:

(1) Lifecycle-driven performance gains. EverMemOS outperforms the strongest baseline on each benchmark overall, i.e., Zep on LoCoMo by 7.0% and 9.2%, and MemOS on LongMemEval by 6.7%. We attribute this to the shift from flat memory storage to a structured lifecycle, which consolidates fragmented experiences into usable knowledge before retrieval, providing a more robust context than isolated record matching.

(2) Structural consolidation aids complex reasoning that requires integrating dispersed evidence. We can observe significant gains on Lo-CoMo multi-hop (+19.7%) and temporal (+10.0%) tasks, as well as LongMemEval knowledge update (+20.6%), validating the effectiveness of Mem-Scenes. By clustering related episodes into coherent thematic units, EverMemOS presents the solver with a complete narrative context. This enables LLMs to naturally bridge dispersed evidence and resolve state conflicts that confuse other models relying on fragmented retrieval.

(3) EverMemOS offers a favorable accuracyefficiency trade-off. As shown in Figure 6 , EverMemOS attains high accuracy with moderate retrieval budgets. This efficiency confirms the utility of the Reconstructive Recollection phase, where the agentic sufficiency check ensures the context is composed of necessary and sufficient evidence, avoiding the noise accumulation common in fixedbudget retrieval.

## 4.3 Ablation Study

We conduct ablations on LoCoMo to isolate the contributions of MemScenes, MemCells, and episode segmentation.

Impact of Memory Architecture. To isolate the contribution of memory structure, we compare EverMemOS with three degraded variants: w/o EverMemOS (no external memory), w/o MemScene (flat retrieval over MemCells), and w/o MemCell (retrieval over raw dialogue). The backbone model and prompts are fixed, and only the memory representation and retrieval pipeline are varied.

![](images/84db5c8569c594b5d2b55654e8a1791a08c6dba962cc7ff4e7bf09508a32297a.jpg)

[Image: This horizontal bar chart visualizes accuracy results for the 'LoCoMo' task across four model configurations. The full system 'EverMemOS' achieves the highest performance at 93.05, while ablation variants 'w/o MemScene' and 'w/o MemCell' score 89.16 and 81.82, respectively. The baseline 'w/o EverMemOS' variant shows a drastically lower result of 0.52, separated visually by a break in the x-axis scale ranging from 0 to 100.]

![](images/db4efab0b52c40229d29bc589d93df90adaa6f10f523976768384d52446df29b.jpg)

[Image: This horizontal bar chart titled "LongMemEval" presents a comparison of accuracy percentages for four different system configurations. The top-performing bar, labeled EverMemOS, reaches an accuracy of 83.00%, followed closely by w/o MemScene at 79.60% and w/o MemCell at 71.20%. A significant outlier is present in the w/o EverMemOS category, which scores only 5.00%, necessitating a visual break in the x-axis scale to separate it from the higher values.]  
Figure 4: Ablation results (overall accuracy) on Lo-CoMo and LongMemEval.

![](images/1fc7a61f9cb8fa02e68626de2a9b585db5c05f17b77a20e7a1d2a41fa6243c73.jpg)

[Image: Line chart titled "LoCoMo" plotting Score (%) on the y-axis (ranging from 60 to over 90) against an x-axis variable (likely K) with discrete points at 1, 3, 5, 10, 15, 20, and 30. Two data series are displayed: Accuracy, represented by a solid teal line with circular markers, and Recall, represented by a dashed reddish-brown line with square markers. Both metrics exhibit a steep rise between x-values of 1 and 3, crossing near 88%, after which they plateau; Accuracy stabilizes slightly below 90% and Recall stabilizes slightly higher. A vertical gray line annotates the x-axis value of 10 with the label "K=10".]

![](images/9643738479c6c2032f84ebcffcd771f3fdebb8bf087fc41771f2167e1cf9b9ff.jpg)

[Image: This line chart titled "LongMemEval" plots "Score (%)" on the y-axis against "Scene Top-K" on the x-axis, featuring discrete values of 1, 3, 5, 10, 15, 20, and 30. A vertical grey line indicates the specific point K=10 on the horizontal axis. Two data series are presented: a lower solid teal line with circular markers and an upper dashed reddish-brown line with square markers. Both series demonstrate an upward trend, indicating improved scores as the Scene Top-K parameter increases, with the final values at K=30 reaching approximately 85% and just under 100% respectively.]  
Figure 5: Sensitivity analysis on the MemScene count (N).

As shown in Figure 4, performance degrades stepwise as structure is removed, revealing three corresponding capability losses. Removing Mem-Scenes eliminates scene-level organization, weakening cross-turn aggregation over related episodes. Removing MemCells further drops the stable semantic units (episodes/facts), forcing retrieval to rely on raw dialogue matching. Finally, removing external memory collapses long-horizon performance, indicating that many queries cannot be handled reliably within the context window alone.

Effectiveness of Episode Segmentation. We evaluate semantic episode segmentation against fixed heuristics and ground-truth boundaries under w/o MemScene to isolate boundary quality.

<table><tr><td>Method</td><td>Avg. Tokens</td><td>Single Hop</td><td>Multi Hop</td><td>Temporal</td><td>Open Domain</td><td>Overall</td></tr><tr><td colspan="7">GPT-4o-mini backbone</td></tr><tr><td>MemoryOS</td><td>5.2k</td><td>62.43</td><td>56.50</td><td>37.18</td><td>40.28</td><td>54.70</td></tr><tr><td>Mem0</td><td>1.0k</td><td>66.71</td><td>58.16</td><td>55.45</td><td>40.62</td><td>61.00</td></tr><tr><td>MemU</td><td>4.0k</td><td>72.77</td><td>62.41</td><td>33.96</td><td>46.88</td><td>61.15</td></tr><tr><td>MemOS</td><td>2.5k</td><td>81.45</td><td>69.15</td><td>72.27</td><td>60.42</td><td>75.87</td></tr><tr><td>Zep</td><td>1.4k</td><td>88.11</td><td>71.99</td><td>74.45</td><td>66.67</td><td>81.06</td></tr><tr><td>EverMemOS</td><td>2.5k</td><td>91.08 (↑3.4%)</td><td>86.17 (↑19.7%)</td><td>81.93 (↑10.0%)</td><td>66.67 (↑0.0%)</td><td>86.76 (↑7.0%)</td></tr><tr><td colspan="7">GPT-4.1-mini backbone</td></tr><tr><td>MemoryOS</td><td>5.5k</td><td>67.30</td><td>59.34</td><td>42.26</td><td>59.03</td><td>60.11</td></tr><tr><td>Mem0</td><td>1.0k</td><td>68.97</td><td>61.70</td><td>58.26</td><td>50.00</td><td>64.20</td></tr><tr><td>MemU</td><td>4.0k</td><td>74.91</td><td>72.34</td><td>43.61</td><td>54.17</td><td>66.67</td></tr><tr><td>MemOS</td><td>2.5k</td><td>85.37</td><td>79.43</td><td>75.08</td><td>64.58</td><td>80.76</td></tr><tr><td>Zep</td><td>1.4k</td><td>90.84</td><td>81.91</td><td>77.26</td><td>75.00</td><td>85.22</td></tr><tr><td>EverMemOS</td><td>2.3k</td><td>96.67 (↑6.4%)</td><td>91.84 (↑12.1%)</td><td>89.72 (↑16.1%)</td><td>76.04 (↑1.4%)</td><td>93.05 (↑9.2%)</td></tr></table>

Table 1: Main results on LoCoMo under two backbones. All metrics are accuracy (%), except Avg. Tokens. For EverMemOS, values in parentheses denote relative change (%) compared to the strongest baseline under the same backbone.

<table><tr><td>Method</td><td>Token</td><td>SS-User</td><td>SS-Asst</td><td>SS-Pref</td><td>Multi-S</td><td>Know. Upd</td><td>Temp. Reas</td><td>Overall</td></tr><tr><td>MemU</td><td>0.5k</td><td>67.14</td><td>19.64</td><td>76.67</td><td>42.10</td><td>41.02</td><td>17.29</td><td>38.40</td></tr><tr><td>Zep</td><td>1.6k</td><td>92.90</td><td>75.00</td><td>53.30</td><td>47.40</td><td>74.40</td><td>54.10</td><td>63.80</td></tr><tr><td>Mem0</td><td>1.1k</td><td>82.86</td><td>26.78</td><td>90.00</td><td>63.15</td><td>66.67</td><td>72.18</td><td>66.40</td></tr><tr><td>MemOS</td><td>1.4k</td><td>95.71</td><td>67.86</td><td>96.67</td><td>70.67</td><td>74.26</td><td>77.44</td><td>77.80</td></tr><tr><td>EverMemOS</td><td>2.8k</td><td>97.14 (↑1.5%)</td><td>85.71 (↑14.3%)</td><td>93.33 (↓3.5%)</td><td>73.68 (↑4.3%)</td><td>89.74 (↑20.6%)</td><td>77.44 (↑0.0%)</td><td>83.00 (↑6.7%)</td></tr></table>

Table 2: Main results on LongMemEval (accuracy, %). SS denotes single-session tasks; baselines are from the official MemOS results (Li et al., 2025). For EverMemOS, values in parentheses denote relative change (%) compared to the strongest baseline for that metric

![](images/09c687c1e0aa03370f833cf47033a2b560c4914c5d1f56a8c3b7efe0a9ea1b33.jpg)

[Image: This scatter plot displays Overall Accuracy (%) against Answer Token Usage, comparing the EverMemOS model against various baselines such as Mem0, MemOS, and Zep. The EverMemOS performance is tracked via a teal line marked with K values (1, 3, 5, 10, 30), showing a rapid accuracy increase to over 90% with low token usage (under 1,500) before plateauing near 93-94% as usage approaches 6,000. All baseline methods, represented by individual geometric markers, fall significantly below the EverMemOS trajectory, with Mem0 achieving the lowest accuracy around 64% and MemOS around 83%, highlighting EverMemOS's superior efficiency-performance trade-off.]  
Figure 6: Performance vs. cost frontier on LoCoMo by varying the retrieved episode count (K).

We compare three strategies: (1) Fixed Heuristics (fixed message count N = 10 or token thresholds N = 512, 1024); (2) Session (Oracle) (groundtruth session boundaries); and (3) EverMemOS (semantic segmentation with different backbones).

Table 3 shows that (i) semantic segmentation consistently outperforms fixed heuristics, especially coarse token chunking; (ii) it also outperforms Session (Oracle), suggesting sessions are not always optimal retrieval units; and (iii) results are robust across boundary-detection backbones (accuracy changes ≤0.7 points).

<table><tr><td rowspan="2">Segmentation Method</td><td colspan="2">Answer Model</td></tr><tr><td>GPT-4.1-mini</td><td>Qwen3-4B</td></tr><tr><td colspan="3">Heuristic Baselines</td></tr><tr><td>Fixed-Message-10</td><td>88.05</td><td>80.95</td></tr><tr><td>Fixed-Token-512</td><td>87.55</td><td>80.67</td></tr><tr><td>Fixed-Token-1024</td><td>84.52</td><td>75.19</td></tr><tr><td colspan="3">Semantic Segmentation</td></tr><tr><td>Session (Oracle)</td><td>87.66</td><td>80.63</td></tr><tr><td colspan="3">Default (EverMemOS)</td></tr><tr><td>w/ GPT-4.1-mini</td><td>89.16</td><td>83.07</td></tr><tr><td>w/ Qwen3-4B</td><td>89.78</td><td>82.73</td></tr></table>

Table 3: Comparison of boundary detection strategies. Session (Oracle) uses the ground-truth session partitions provided by LoCoMo.

## 4.4 Hyperparameter Analysis

We investigate the impact of retrieval scope via two hyperparameters: the number of retrieved MemScenes (N) and episodes (K). As shown in Figure 5, performance gains saturate around N = 10. Figure 6 further illustrates the efficiency– accuracy frontier governed by K. We therefore adopt N = 10 and K = 10 as the default configuration to balance performance with computational cost. Comprehensive sensitivity analysis is detailed in Appendix B.1.

![](images/02722a117e91f74ad06e70c99cc8f96c716d0f741c8011f3a3dde73f9ab5f413.jpg)

[Image: This figure illustrates three comparative case studies—Episodic Memory Recall, Longitudinal Profile Modeling, and Experience-Grounded Foresight—demonstrating the capabilities of the EverMemOS system versus a baseline without memory. Each case displays a timeline of user-assistant dialogues followed by a query and two contrasting responses. In Case 1, EverMemOS correctly recalls a specific medical diagnosis from previous logs, while the baseline offers generic sports injury advice. Case 2 and Case 3 similarly show EverMemOS leveraging historical data on physical measurements and past travel frustrations to provide personalized, context-aware recommendations, unlike the generic advice generated by the system without memory integration.]  
Figure 7: Case studies illustrating Profile, Foresight, and Episode capabilities in Memory-Augmented Chat.

<table><tr><td>Scenario</td><td>Ep.+Prof.</td><td>Prof.-only</td><td>Ep.-only</td></tr><tr><td>Consultation</td><td>51.03</td><td>47.33</td><td>44.44</td></tr><tr><td>Email (Personal)</td><td>53.85</td><td>46.15</td><td>46.15</td></tr><tr><td>Translation</td><td>50.00</td><td>46.15</td><td>38.08</td></tr><tr><td>Email (Professional)</td><td>53.79</td><td>41.38</td><td>45.17</td></tr><tr><td>Writing (Creative)</td><td>55.10</td><td>48.57</td><td>42.04</td></tr><tr><td>Writing (Professional)</td><td>45.56</td><td>44.79</td><td>40.15</td></tr><tr><td>Knowledge Query</td><td>63.68</td><td>62.94</td><td>54.73</td></tr><tr><td>Social Media</td><td>47.90</td><td>44.96</td><td>36.13</td></tr><tr><td>Chat</td><td>52.09</td><td>44.87</td><td>41.83</td></tr><tr><td>Overall</td><td>53.25</td><td>48.30</td><td>43.93</td></tr></table>

Table 4: Profile ablation on PersonaMem v2 (Jiang et al., 2025) (5,000 questions across 9 scenarios; accuracy, %).

## 4.5 Profile Study

We evaluate the effect of the consolidated user profile on PersonaMem-v2 (32k) (Jiang et al., 2025); results are not directly comparable across dataset versions due to differences in task setup and annotations. Table 4 shows that adding the User Profile to episodic evidence improves overall accuracy by 9.32 points over episodes-only (53.25 vs. 43.93), indicating that semantic consolidation provides complementary signal beyond episodic retrieval. We defer the full comparison against other memory systems on PersonaMem-v2 to Appendix A.4.

## 4.6 Case Study

Existing benchmarks primarily evaluate answerlevel accuracy/recall and do not capture several capabilities required for long-term conversational agents, such as conflict detection, profile stability, and experience-grounded foresight. To complement quantitative results, Figure 7 shows three representative cases: (Episode) reconstructing a concrete past injury episode (a Grade-II ankle sprain during badminton) rather than producing a generic explanation; (Profile) maintaining longitudinal stability and using sustained improvements (waist 104→96 cm with stable weight) for trajectoryconsistent goal setting; and (Foresight) leveraging previously observed failures (overcrowding and missing advance tickets) to make proactive recommendations for future travel. Together, these cases illustrate coherent, experience-aware behavior beyond what is measured by existing benchmarks.

# 5 Conclusion

In this paper, we introduced EverMemOS, a unified memory operating system for long-horizon LLM agents. By modeling an explicit memory lifecycle composed of episodic trace formation, semantic consolidation, and reconstructive recollection, EverMemOS achieves state-of-the-art performance on memory-augmented reasoning benchmarks, with particularly strong gains on multi-hop and temporal questions. We hope EverMemOS provides an extensible foundation for building more consistent and context-aware interactive agents.

# Limitations

We evaluate EverMemOS on text-only conversational benchmarks. Although the MemCell and MemScene abstraction is modality-agnostic, extending EverMemOS to multimodal or embodied settings is beyond the scope of this work. Ever-MemOS introduces LLM-mediated operations for memory construction and retrieval, increasing latency and computational cost relative to single-pass baselines. While many components can be cached, batched, or run asynchronously, improving end-toend efficiency remains future work. Finally, current benchmarks lack protocols for stress-testing ultralong timelines, so our evaluation does not fully isolate performance in such regimes. This motivates future benchmarks for long-term memory organization and consolidation.

# References

Iz Beltagy, Matthew E Peters, and Arman Cohan. 2020. Longformer: The long-document transformer. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics. Association for Computational Linguistics.

Atilim Gunes Bulatov, Valentin Khrulkov, Leyla Mirvakhabova, Alexey Markov, Artem Babenko, and Ivan Oseledets. 2022. Recurrent memory transformer. In Advances in Neural Information Processing Systems, pages 20230–20243.

Aydar Bulatov, Yuri Kuratov, and Mikhail S. Burtsev. 2023. Scaling transformer to 1m tokens and beyond with rmt. ArXiv, abs/2304.11062.

Guanzheng Chen, Xin Li, Zaiqiao Meng, Shangsong Liang, and Lidong Wang. 2024. Clex: Continuous length extrapolation for large language models. In International Conference on Learning Representations.

Guanzheng Chen, Xin Li, Michael Qizhe Shieh, and Lidong Bing. 2025. LongPO: Long context selfevolution of large language models through shortto-long preference optimization. In The Thirteenth International Conference on Learning Representations.

Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. 2025. Mem0: Building production-ready ai agents with scalable long-term memory. Preprint, arXiv:2504 19413

Zihang Dai, Zhilin Yang, Yiming Yang, Jaime Carbonell, Quoc V Le, and Ruslan Salakhutdinov. 2019. Transformer-XL: Attentive language models beyond a fixed-length context. In Proceedings of the 57th Annual Meeting ofthe Associationfor Computational Linguistics, pages 2978–2988. Association for Com putational Linguistics.

Matthias De Lange, Rahaf Aljundi, Marc Masana, Sarah Parisot, Xu Jia, Aleš Leonardis, Greg Slabaugh, and Tinne Tuytelaars. 2022. A continual learning survey: Defying forgetting in classification tasks. IEEE Transactions on Pattern Analysis and Machine Intel ligence, 44(7):3366–3385.

Mohamed Amine Ferrag, Norbert Tihanyi, and Merouane Debbah. 2025. From llm reasoning to autonomous ai agents: A comprehensive review. arXiv preprint arXiv:2504.19678.

Yue Gong and 1 others. 2024. M+: An efficient memory structure for large language models. arXiv preprint arXiv:2404.09337.

Alex Graves, Greg Wayne, and Ivo Danihelka. 2014. Neural turing machines. arXiv preprint arXiv:1410.5401.

Alex Graves, Greg Wayne, Malcolm Reynolds, Tim Harley, Ivo Keck, William O’Brien, Alistair Kritzman, Stanislav Illarionov, Edward Grefenstette, Tiago Wuthrich, and 1 others. 2016. Hybrid computing using a neural network with dynamic external memory. Nature, 538(7626):471–476.

Bowen Jiang, Yuan Yuan, Maohao Shen, Zhuoqun Hao, Zhangchen Xu, Zichen Chen, Ziyi Liu, Anvesh Rao Vijjini, Jiashu He, Hanchao Yu, Radha Poovendran, Gregory Wornell, Lyle Ungar, Dan Roth, Sihao Chen, and Camillo Jose Taylor. 2025. Personamem-v2: Towards personalized intelligence via learning implicit user personas and agentic memory. arXiv preprint arXiv:2512.06688.

Sheena A Josselyn, Stefan Köhler, and Paul W Frankland. 2015. Finding the engram. Nature Reviews Neuroscience, 16(9):521–534.

Jiazheng Kang, Mingming Ji, Zhe Zhao, and Ting Bai. 2025. Memory os of ai agent. arXiv preprint arXiv:2506.06326.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Yuxiang Kukliansky, Wen-tau Yih Chen, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2020. Retrievalaugmented generation for knowledge-intensive nlp tasks. In Advances in Neural Information Processing Systems, volume 33, pages 9459–9474.

Zhiyu Li, Shichao Song, Chenyang Xi, Hanyu Wang, Chen Tang, Simin Niu, Ding Chen, Jiawei Yang, Chunyu Li, Qingchen Yu, and 1 others. 2025. Memos: A memory os for ai system. arXiv preprint arXiv:2507.03724.

Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024. Lost in the middle: How language models use long contexts. Transactions ofthe Association for Computational Linguistics, 12:157–173.

Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei Fang. 2024. Evaluating very long-term conversational memory of llm agents. Preprint, arXiv:2402.17753.

James L McGaugh. 2000. Memory–a century of consolidation. Science, 287(5451):248–251.

Alexander Miller, Adam Fisch, Jesse Dodge, Amir-Hossein Karimi, Antoine Bordes, and Jason Weston. 2016. Key-value memory networks for directly reading documents. In Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing, pages 1400–1409. Association for Computational Linguistics.

Jiayan Nan, Wenquan Ma, Wenlong Wu, and Yize Chen. 2025. Nemori: Self-organizing agent memory inspired by cognitive science. Preprint, arXiv:2508.03341.

Charles Packer, Vivian Woodside, Neal Dhir, and Douwe Kiela. 2024. Memgpt: Towards llms as operating systems. In Advances in Neural Information Processing Systems.

Ori Ram, Eyal Shnarch, Jonathan Uziel, Lisa Haklay, and Amir Globerson. 2023. In-context retrieval augmented language models. Transactions of the Associationfor Computational Linguistics, 11:1316– 1331.

Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. 2025. Zep: A temporal knowledge graph architecture for agent memory. Preprint, arXiv:2501.13956.

Daniel L Schacter. 2008. Searching for memory: The brain, the mind, and the past. Basic books.

Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2024. Reflexion: Language agents with verbal reinforcement learning. In Advances in Neural Information Pro cessing Systems, volume 36.

Haoran Sun and Shaoning Zeng. 2025. Hierarchical memory for high-efficiency long-term reasoning in llm agents. arXiv preprint arXiv:2507.22925.

Weizhi Wang, Li Dong, Hao Cheng, Xiaodong Liu, Xifeng Yan, Jianfeng Gao, and Furu Wei. 2023. Longmem: Augmenting language models with longterm memory. In Advances in Neural Information Processing Systems, volume 36, pages 20292–20306.

Yu Wang and Xi Chen. 2025. Mirix: Multi-agent memory system for llm-based agents. arXiv preprint arXiv:2507.07957.

Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. 2025. Longmemeval: Benchmarking chat assistants on long-term interactive memory. Preprint, arXiv:2410.10813.

Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yi Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, and 1 others. 2023. The rise and potential of large language model based agents: A survey. arXiv preprint arXiv:2309.07864.

Chun Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. 2024. Agentless: Demystifying llm-based software engineering agents. ArXiv, abs/2407.01489.

Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan, and Michal Shmueli-Scheuer. 2025. Survey on evaluation of llmbased agents. arXiv preprint arXiv:2503.16416.

Manzil Zaheer, Guru Guruganesh, Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago Ontañón, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, and Amr Ahmed. 2020. Big Bird: Transformers for longer sequences. In Advances in Neural Information Processing Systems, pages 17283–17296.

Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, An Yang, Dayiheng Liu, Junyang Lin, Fei Huang, and Jingren Zhou. 2025. Qwen3 embedding: Advancing text embedding and reranking through foundation models. arXiv preprint arXiv:2506.05176.

Yuan Zheng and 1 others. 2024. Memoryllm: A framework for personalized and long-term dialogue generation. arXiv preprint arXiv:2401.17122.

W Zhong, L Guo, Q Gao, and 1 others. 2024. Memorybank: Enhancing large language models with long-term memory. In Proceedings ofthe AAAI Conference on Artificial Intelligence, volume 38, pages 19724–19731.
