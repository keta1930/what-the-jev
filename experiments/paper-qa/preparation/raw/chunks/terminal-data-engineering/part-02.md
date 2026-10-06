# 5. Experiments  


## 5.1. Experimental Setup  


**Base Models.** We conduct experiments using pretrained models from the Qwen3 family (Yang et al., 2025). We use Qwen3-8B as our primary model for ablation studies, and we additionally experiment with Qwen3-14B and Qwen3-32B to verify that our findings scale with model size.  


**Training Details.** Unless specified otherwise, we use the following training hyperparameters: learning rate of 2e-5, weight decay of 1e-4, 2 epochs, maximum sequence length of 32,768 tokens, global batch size of 128, and micro-batch size of 1 per GPU, with AdamW optimizer ($\beta = 0.9$, 0.95), cosine learning rate scheduler with 10% warmup, and gradient clipping at 1.0. The 8B and 14B models are trained on 4 nodes with 8 GPUs per node (32 total GPUs) using sequence parallelism of 2. The 32B model is trained on 16 nodes (128 total GPUs). All experiments use CPU offloading.  


**Infrastructure.** We utilize Harbor (Shaw, 2025), the infrastructure framework from Terminal-Bench 2.0 (Team, 2025), to orchestrate large-scale trajectory generation in containerized environments. We extend Harbor to support Singularity (Kurtzer et al., 2017), enabling deployment on HPC clusters; while this introduces rare failures due to fakeroot overlay limitations, these are acceptable for synthetic data generation. For evaluation, we rely on Daytona (Daytona, 2025) to manage reliable, parallel execution in isolated cloud sandboxes.  


For SFT experiments, we use veRL (Sheng et al., 2024), an open-source framework designed for efficient LLM training.  


## 5.2. Main Results  


We evaluate Terminal-Task-Gen by benchmarking Nemotron-Terminal on Terminal-Bench 2.0 (TB2.0). As shown in Table 3, our models demonstrate substantial gains: Nemotron-Terminal-8B achieves $13.0 \pm 2.2$, a five-fold increase over Qwen3-8B ($2.47 \pm 0.5$). Remarkably, despite their modest scale, they rival significantly larger systems; Nemotron-Terminal-14B ($20.2 \pm 2.7$) outperforms the 120B GPT-OSS ($18.7 \pm 2.7$) and  


>Table 3: Terminal-Bench 2.0 (TB2.0) results
with Terminus 2 agent.  


| Model|Size|TB2.0|
| ---|---|---|
| Closed Source Models|Closed Source Models|Closed Source Models|
| GPT-5-Nano|–|$7.90 \pm 1.9$|
| GPT-5-Mini|–|$24.0 \pm 2.5$|
| GPT-5|–|$35.2 \pm 3.1$|
| GPT-5.1|–|$47.6 \pm 2.8$|
| GPT-5.2|–|$54.0 \pm 2.9$|
| Grok Code Fast 1|–|$14.2 \pm 2.5$|
| Grok 4|–|$23.1 \pm 2.9$|
| GLM 4.6|–|$24.5 \pm 2.4$|
| Gemini 2.5 Flash|–|$16.9 \pm 2.4$|
| Gemini 2.5 Pro|–|$32.6 \pm 3.0$|
| Gemini 3 Flash|–|$51.7 \pm 3.1$|
| Gemini 3 Pro|–|$56.9 \pm 2.5$|
| Claude Haiku 4.5|–|$28.3 \pm 2.9$|
| Claude Sonnet 4.5|–|$42.8 \pm 2.8$|
| Claude Opus 4.5|–|$57.8 \pm 2.5$|
| Open Source Models|Open Source Models|Open Source Models|
| Qwen3-8B|8B|$2.47 \pm 0.5$|
| Qwen3-14B|14B|$4.04 \pm 1.3$|
| Qwen3-32B|32B|$3.37 \pm 1.6$|
| Qwen3-Coder|480B|$23.9 \pm 2.8$|
| GPT-OSS (high)|20B|$3.10 \pm 1.5$|
| GPT-OSS (high)|120B|$18.7 \pm 2.7$|
| MiniMax M2|230B|$30.0 \pm 2.7$|
| MiniMax M2.1|230B|$29.2 \pm 2.9$|
| Kimi K2 Thinking|1T|$35.7 \pm 2.8$|
| DeepSeek-V3.2|685B|$38.2 \pm 2.9$|
| Ours|Ours|Ours|
| Nemotron-Terminal-8B|8B|$13.0 \pm 2.2$|
| Nemotron-Terminal-14B|14B|$20.2 \pm 2.7$|
| Nemotron-Terminal-32B|32B|$\mathbf{27.4 \pm 2.4}$|  


Gemini 2.5 Flash (16.9 ± 2.4), while Nemotron-Terminal-32B (27.4 ± 2.4) outperforms the 480B Qwen3-Coder (23.9 ± 2.8). This validates that high-quality trajectory data effectively bridges the gap between efficient models and massive frontier counterparts.  


Further analysis by task category (Table 4) confirms that our synthetic data unlocks critical capabilities where base models of all scales failed completely. While the Qwen3-14B and 32B models both scored 0.0 in Data Querying and Model Training, Nemotron-Terminal-32B surged to 60.0 and 50.0 respectively, representing a profound leap in functional utility. Similar transformations occur in Security (2.5 to 27.5), Data Processing (5.0 to 50.0), and Software Engineering (5.0 to 31.7) for the 32B variant, indicating that larger parameter count alone is insufficient for strong terminal capability. Furthermore, consistent gains in System Administration (6.7 to 31.1) and Debugging (0.0 to 33.3) demonstrate that our approach successfully instills domain-specific skills—such as complex file manipulation and command-line troubleshooting, which are effectively absent in the original models.  


>Table 4: Performance of models by Terminal-Bench category. TB2.0 scores for Qwen3 and Nemotron-Terminal models, broken down by category, showing where Nemotron-Terminal most improves over the Qwen3 baselines.  


| Category|Qwen3|Qwen3|Qwen3|Nemotron-Terminal|Nemotron-Terminal|Nemotron-Terminal|
| ---|---|---|---|---|---|---|
| Category|8B|14B|32B|8B|14B|32B|
| <b>Software& System</b>|<b>Software& System</b>|<b>Software& System</b>|<b>Software& System</b>|<b>Software& System</b>|<b>Software& System</b>|<b>Software& System</b>|
| Software Engineering (24)|1.70|6.70|5.00|9.20|18.3|31.7|
| System Administration (9)|13.3|6.70|6.70|22.2|28.9|31.1|
| Debugging (3)|0.00|0.00|0.00|20.0|40.0|33.3|
| Security (8)|0.00|0.00|2.50|12.5|17.5|27.5|
| File Operations (4)|0.00|0.00|0.00|0.00|10.0|5.00|
| <b>Data& Science</b>|<b>Data& Science</b>|<b>Data& Science</b>|<b>Data& Science</b>|<b>Data& Science</b>|<b>Data& Science</b>|<b>Data& Science</b>|
| Data Science (8)|2.50|7.50|0.00|7.50|17.5|27.5|
| Data Processing (4)|0.00|5.00|5.00|35.0|40.0|50.0|
| Data Querying (1)|0.00|0.00|0.00|20.0|40.0|60.0|
| Scientific Computing (7)|0.00|0.00|2.90|0.00|2.90|0.00|
| Mathematics (4)|0.00|0.00|0.00|0.00|0.00|0.00|
| <b>Machine Learning</b>|<b>Machine Learning</b>|<b>Machine Learning</b>|<b>Machine Learning</b>|<b>Machine Learning</b>|<b>Machine Learning</b>|<b>Machine Learning</b>|
| Machine Learning (3)|0.00|0.00|0.00|6.70|13.3|13.3|
| Model Training (4)|0.00|0.00|0.00|5.00|20.0|50.0|
| <b>Other</b>|<b>Other</b>|<b>Other</b>|<b>Other</b>|<b>Other</b>|<b>Other</b>|<b>Other</b>|
| Personal Assistant (1)|0.00|0.00|0.00|80.0|80.0|100|
| Games (1)|0.00|0.00|0.00|0.00|0.00|0.00|
| Video Processing (1)|0.00|0.00|0.00|0.00|0.00|0.00|
| Unknown (7)|5.70|8.60|8.60|34.3|34.3|34.3|
| <b>Overall</b>|2.50|4.00|3.40|13.0|20.2|27.4|  


## 5.3. Ablation on Dataset Components  


As demonstrated in Table 5, each data source provides complementary value. For dataset adapters, while individual splits like Math (5.39%) and Code (6.29%) underperform compared to SWE (7.02%), combining them leads to a significant performance jump to 9.66%, confirming that merging distinct domains yields further improvement than any single source alone. A similar pattern of robustness appears in synthetic tasks, where the skill-based data drives the primary gains (12.4%); although adding seed-based data does not increase the mean score, it successfully reduces variance and makes the model more robust.  


## 5.4. Filtering Strategies  


### Trajectory Filtering  


We investigate a few trajectory filtering strategies discussed in Section 4.4. For dataset adapters (Table 6), while we observe no significant difference on each subset, the no-filter setting yields the highest performance on the full set (9.66%) and is thus adopted. For synthetic tasks (Table 7), the impact is even more substantial: no filtering (12.4%) significantly surpasses both complete-only (6.74%) and success-only (5.06%) strategies.  


>Table 5: Qwen3-8B SFT results across training data sources. We show total samples and TB2.0 results from training on various subsets. For both dataset adapters and synthetic tasks, we achieve the strongest results from combining all data sources together.  


| Data Split|# Samples|TB2.0|
| ---|---|---|
| Dataset Adapters|Dataset Adapters|Dataset Adapters|
| Math|162,692|$5.39 \pm 1.65$|
| Code|31,960|$6.29 \pm 1.65$|
| SWE|31,661|$7.02 \pm 2.13$|
| All|226,313|$\mathbf{9.66 \pm 2.11}$|
| Synthetic Tasks|Synthetic Tasks|Synthetic Tasks|
| Seed-based|124,366|$6.18 \pm 1.91$|
| Skill-based|139,841|$12.4 \pm 2.38$|
| All|264,207|$\mathbf{12.4 \pm 2.29}$|  


>Table 6: Qwen3-8B ablations on dataset adapter filtering strategies. Because the dataset adapter subset does not include test cases, we compare no filtering to complete-only filtering and observe no significant performance difference.  


| Filter|# Samples|TB2.0|
| ---|---|---|
| Math|Math|Math|
| Complete-only|147,718|$7.19 \pm 1.87$|
| No filter|162,692|$5.39 \pm 1.65$|
| Code|Code|Code|
| Complete-only|20,169|$6.07 \pm 1.73$|
| No filter|31,960|$6.29 \pm 1.65$|
| SWE|SWE|SWE|
| Complete-only|29,053|$5.39 \pm 1.68$|
| No filter|31,661|$7.02 \pm 2.13$|
| All|All|All|
| Complete-only|196,940|$8.09 \pm 1.84$|
| No filter|226,313|$9.66 \pm 2.11$|  


This performance gap suggests that strict filtering is detrimental as it discards over half the available training data. Moreover, retaining unsuccessful trajectories appears to provide valuable supervision, exposing the model to realistic error states and recovery patterns that enhance overall robustness.  


>Table 7: Qwen3-8B ablations on synthetic task filtering. On the synthetic task subset, we experiment with no filtering, complete-only filtering, and success-only filtering. No filtering yields significantly better performance.  


| Filter|# Samples|TB2.0|
| ---|---|---|
| Complete-only|104,603|$6.74 \pm 2.20$|
| Success-only|83,448|$5.06 \pm 2.11$|
| No filter|264,207|$\mathbf{12.4 \pm 2.29}$|  


>Table 8: Impact of SFT sequence length and YaRN2 scaling on Qwen3-8B performance. We find that training and evaluating with default Qwen3 context settings yields the strongest performance.  


| SFT MaxLen|Eval MaxLen|SFTYaRN2|EvalYaRN2|TB2.0|
| ---|---|---|---|---|
| 32,768|40,960|||$13.0 \pm 2.2$|
| 32,768|65,536||$\checkmark$|$11.9 \pm 2.0$|
| 65,536|65,536|||$10.3 \pm 2.0$|
| 65,536|65,536|$\checkmark$|$\checkmark$|$11.9 \pm 2.1$|  


## 5.5. Long Context Training and Evaluation  


Terminal trajectories can vary significantly in their turn counts (Appendix A.1), which in turn induces large differences in token counts depending on task type and difficulty. As shown in Appendix A.1, most trajectories fit within the default maximum sequence length of Qwen3 models (32,768 tokens), but a nontrivial subset exceeds this limit and is truncated by SFT. Motivated by this, we investigate long-context training for Qwen3-8B.  


Specifically, we compare SFT with a 65,536-token context window without YaRN2 (Peng et al., 2023), SFT with YaRN2, and a baseline that only applies YaRN2 at evaluation time. Across these settings, we observe no significant performance differences (Table 8). Moreover, evaluating under the standard Qwen3-8B setup with a 40,960-token context window yields stronger results. Our results suggest that extending the context length slightly hurts performance; most high-quality supervision already fits within the standard window, while the long-tail trajectories tend to be noisy and less informative.  


## 5.6. Curriculum Learning  


We investigate two SFT curriculum strategies for data mixing: (1) a two-stage curriculum, where we first train on dataset adapters, followed by synthetic task data; and (2) a single-stage strategy, where we train on all  


datasets concurrently. As demonstrated in Table 9, the two-stage curriculum yields no performance advantage over simple mixed training. Consequently, we adopt the single-stage mixed training strategy for all other experiments in this paper.  


![9c46069899141fed2711fdde600e13e5.jpeg](images/10.png)

[Image: The image presents two line charts side-by-side evaluating the performance of Qwen3-8B and Qwen3-14B models across varying percentages of training data. The vertical axis measures Performance in percentage, while the horizontal axis marks Training Data Percentage at intervals including 1%, 2%, 5%, 10%, and 100%. Both models exhibit a consistent upward trend where mean performance increases with more data, with the Qwen3-14B model reaching approximately 20% performance at full dataset scale compared to roughly 13% for the Qwen3-8B model. Shaded regions surrounding the data points indicate the 95% Confidence Interval (CI) for the mean estimates.]  


>Figure 4: Impact of training data scale on model performance. Our scaling experiments show that TB2.0 performance increases with training data volume for both Qwen3-8B and Qwen3-14B.  


| Model|Strategy|TB2.0|
| ---|---|---|
| Qwen3-8B|mixed|$13.03 \pm 2.16$|
| Qwen3-8B|curriculum|$10.39 \pm 1.71$|  


>Table 9: Ablations on curriculum learning strategies. We compare a mixed single-stage strategy with a two-stage curriculum. The mixed strategy achieves the strongest performance.  


## 5.7. Scaling Experiments  


We investigate the impact of training data scale on model performance by fine-tuning Qwen3-8B and Qwen3-14B models on varying percentages of synthetic training data (0%, 1%, 2%, 5%, 10% and 100%). Both models demonstrate consistent performance improvements as training data increases (Figure 4). The larger 14B model not only achieves higher absolute performance across all data scales but also exhibits greater gains from additional training data. These results demonstrate that both model capacity and training data scale are critical factors for performance.  


# 6. Conclusion  


In this work, we address the data scarcity bottleneck in terminal agent training by introducing **Terminal-Task-Gen**, a scalable framework that synergizes large-scale dataset adaptation with targeted synthetic task generation. Our systematic study demonstrates that precise data engineering enables the efficient **Nemotron-Terminal** family to significantly outperform its Qwen3 base and rival larger frontier models on Terminal-Bench 2.0, proving that high-quality, diverse trajectories are more pivotal than sheer parameter scale. Looking ahead, we see significant potential in extending this foundation with Reinforcement Learning (RL), leveraging verifiable execution feedback to enable self-correction and optimal planning for long-horizon tasks. We release our models and most of our synthetic datasets, including the adapter and skill-based task subsets, to democratize research in autonomous terminal agents.  


# References  


[1] Wasi Uddin Ahmad, Sean Narenthiran, Somshubra Majumdar, Aleksander Ficek, Siddhartha Jain, Jocelyn Huang, Vahid Noroozi, and Boris Ginsburg. Opencodereasoning: Advancing data distillation for competitive coding. arXiv preprint arXiv:2504.01943, 2025. 5  


[2] Anthropic. Claude code: Best practices for agentic coding. https://www.anthropic.com/engineering/
claude-code-best-practices,Apr2025.1, 3  


[3] Anthropic. Introducing claude opus 4.5. https://www.anthropic.com/news/claude-opus-4-5,2025.
2  


[4] Antigma. Meet ante. https://antigma.ai/,2025.2, 3  


[5] Dan Austin. Terminal bench agentic data pipeline. https://github.com/Danau5tin/tbench-agentic-data-pipeline,2025.2, 3, 7  


[6] Ibragim Badertdinov, Alexander Golubev, Maksim Nekrashevich, Anton Shevtsov, Simon Karasik, Andrei Andriushchenko, Maria Trofimova, Daria Litvintseva, and Boris Yangel. Swe-rebench: An automated pipeline for task collection and decontaminated evaluation of software engineering agents. arXiv preprint arXiv:2505.20411, 2025. 5  


[7] Daytona. Daytona cloud: Secure and elastic infrastructure for running your AI-generated code. https://www.daytona.io,2025.8  


[8] DCAgent. bash_textbook_tasks_traces. https://huggingface.co/datasets/DCAgent/bash_textbook_tasks_traces,2025.2, 3  


[9] Google DeepMind. A new era of intelligence with gemini 3. https://blog.google/
products-and-platforms/products/gemini/gemini-3/,2025.2  


[10] ML Foundations Development. staqc-sandboxes-traces-terminus-2. https://huggingface.co/datasets/mlfoundations-dev/staqc-sandboxes-traces-terminus-2,2025.2, 3  


[11] ML Foundations Development. code-contests-sandboxes-traces-terminus-2. https://huggingface.co/datasets/mlfoundations-dev/code-contests-sandboxes-traces-terminus-2,2025.2, 3  


[12] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025. 5  


[13] Intelligent Internet. Ii-agent. https://ii.inc/web/blog/post/ii-agent,2025.2, 3  


[14] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. Livecodebench: Holistic and contamination free evaluation of large language models for code. arXiv preprint arXiv:2403.07974, 2024. 7  


[15] JetBrains. Junie cli: Llm-agnostic coding agent built for real-world development. https://junie.jetBrains.com/,2025.2, 3  


[16] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan. Swe-bench: Can language models resolve real-world github issues? arXiv preprint arXiv:2310.06770, 2023. 5, 7  


[17] Gregory M. Kurtzer, Vanessa Sochat, and Michael W. Bauer. Singularity: Scientific containers for mobility of compute. PloS One, 12(5):e0177459, 2017. doi: 10.1371/journal.pone.0177459. 8  


[18] Letta. Building the #1 open-source terminal-use agent using letta. https://www.letta.com/blog/terminal-bench,2025.2, 3  


[19] Aixin Liu, Aoxue Mei, Bangcai Lin, Bing Xue, Bingxuan Wang, Bingzheng Xu, Bochao Wu, Bowei Zhang, Chaofan Lin, Chen Dong, et al. Deepseek-v3. 2: Pushing the frontier of open large language models. arXiv preprint arXiv:2512.02556, 2025. 2, 7  


[20] Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xiubo Geng, Wenxiang Hu, Chongyang Tao, Jing Ma, Qingwei Lin, and Daxin Jiang. Wizardcoder: Empowering code large language models with evol-instruct. arXiv preprint arXiv:2306.08568, 2023. 3  


[21] MAA. Aime 2024 benchmark: Problems from the american invitational mathematics examination. https://huggingface.co/datasets/Maxwell-Jia/AIME_2024,2024.Benchmark of AIME 2024 problems for evaluating mathematical reasoning in language models. 7  


[22] MAA. Aime 2025 benchmark: Problems from the american invitational mathematics examination. https://ukgovernmentbeis.github.io/inspect_evals/evals/mathematics/aime2025/,2025.Benchmark of AIME 2025 problems for evaluating mathematical reasoning in language models. 7  


[23] Dirk Merkel. Docker: lightweight linux containers for consistent development and deployment. In Linux Journal, number 239. Belltown Media, 2014. 4  


[24] Mike A Merrill, Alexander G Shaw, Nicholas Carlini, Boxuan Li, Harsh Raj, Ivan Bercovich, Lin Shi, Jeong Yeon Shin, Thomas Walshe, E Kelly Buchanan, et al. Terminal-bench: Benchmarking agents on hard, realistic tasks in command line interfaces. arXiv preprint arXiv:2601.11868, 2026. 2, 3  


[25] MiniMax. Minimax m2 & agent: Ingenious in simplicity. https://www.minimax.io/news/minimax-m2,2025.2  


[26] Arindam Mitra, Luciano Del Corro, Guoqing Zheng, Shweti Mahajan, Dany Rouhana, Andres Codas, Yadong Lu, Wei-ge Chen, Olga Vrousgos, Corby Rosset, et al. Agentinstruct: Toward generative teaching with agentic flows. arXiv preprint arXiv:2407.03502, 2024. 3  


[27] Moonshot AI. Introducing kimi k2 thinking. https://moonshotai.github.io/Kimi-K2/thinking.html,Nov2025.2  


[28] Ivan Moshkov, Darragh Hanley, Ivan Sorokin, Shubham Toshniwal, Christof Henkel, Benedikt Schifferer, Wei Du, and Igor Gitman. Aimo-2 winning solution: Building state-of-the-art mathematical reasoning models with openmathreasoning dataset. arXiv preprint arXiv:2504.16891, 2025. 5  


[29] Mux. Terminal benchmarking. https://mux.coder.com/reference/benchmarking,2025.2, 3  


[30] Jack Nichols. How we scored #1 on terminal-bench (52%). https://www.warp.dev/blog/terminal-bench,2025.2, 3  


[31] OpenAI. Introducing swe-bench verified. https://openai.com/index/introducing-swe-bench-verified/,Aug2024.7  


[32] OpenAI. Introducing codex. https://openai.com/index/introducing-codex/,May2025.Overview of the Codex coding agent accessible via ChatGPT and related clients. 1, 3  


[33] OpenAI. Introducing gpt-5.2. https://openai.com/index/introducing-gpt-5-2/,2025.2  


[34] Bowen Peng, Jeffrey Quesnelle, Honglu Fan, and Enrico Shippole. Yarn: Efficient context window extension of large language models. arXiv preprint arXiv:2309.00071, 2023. 10  


[35] Xiaoxuan Peng, Xinyu Lu, Kaiqi Zhang, Taosong Fang, Boxi Cao, and Yaojie Lu. Litecoder-terminal: Lightweight terminal agents with <1k synthesized trajectories. https://huggingface.co/blog/Lite-Coder/litecoder-terminal-preview,2025.2, 3, 7  


[36] Alex Shaw. Harbor Framework, November 2025. URL https://github.com/laude-institute/harbor.
8  


[37] Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. arXiv preprint arXiv: 2409.19256, 2024. 8  


[38] Abhay Singhal, Leo Tchourakov, Daniel Flaherty, and Stepan Bedratiuk. Droid: The #1 software development agent on terminal-bench. Factory AI News, September 2025. URL https://factory.ai/news/terminal-bench.2, 3  


[39] Shivchander Sudalairaj, Abhishek Bhandwalsdar, Aldo Pareja, Kai Xu, David D Cox, and Akash Srivastava.
Lab: Large-scale alignment for chatbots. arXiv preprint arXiv:2403.01081, 2024. 3  


[40] The Terminal-Bench Team. Adapters. https://harborframework.com/docs/adapters,2025.2  


[41] The Terminal-Bench Team. Terminal-bench: A benchmark for ai agents in terminal environments, Apr 2025. URL https://github.com/laude-institute/terminal-bench.3, 4, 8  


[42] Boxin Wang, Chankyu Lee, Nayeon Lee, Sheng-Chieh Lin, Wenliang Dai, Yang Chen, Yangyi Chen, Zhuolin Yang, Zihan Liu, Mohammad Shoeybi, et al. Nemotron-cascade: Scaling cascaded reinforcement learning for general-purpose reasoning models. arXiv preprint arXiv:2512.13607, 2025. 5  


[43] Chengxing Xie, Bowen Li, Chang Gao, He Du, Wai Lam, Difan Zou, and Kai Chen. Swe-fixer: Training open-source llms for effective and efficient github issue resolution. arXiv preprint arXiv:2501.05040, 2025. 5  


[44] Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng, Pu Zhao, Jiazhan Feng, Chongyang Tao, and Daxin Jiang. Wizardlm: Empowering large language models to follow complex instructions. arXiv preprint arXiv:2304.12244, 2023. 3  


[45] Zhangchen Xu, Fengqing Jiang, Luyao Niu, Yuntian Deng, Radha Poovendran, Yejin Choi, and Bill Yuchen Lin. Magpie: Alignment data synthesis from scratch by prompting aligned llms with nothing. arXiv preprint arXiv:2406.08464, 2024. 3  


[46] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. arXiv preprint arXiv:2505.09388, 2025. 2, 3, 8  


[47] John Yang, Kilian Lieret, Carlos E Jimenez, Alexander Wettig, Kabir Khandpur, Yanzhe Zhang, Binyuan Hui, Ofir Press, Ludwig Schmidt, and Diyi Yang. Swe-smith: Scaling data for software engineering agents. arXiv preprint arXiv:2504.21798, 2025. 5  


