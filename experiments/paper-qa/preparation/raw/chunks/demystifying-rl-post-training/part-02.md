# 5 Results: Unpacking Learning Dynamics

## 5.1 The Coverage Principle

The coverage principle proposes that pre-training enables post-training primarily by assigning nonnegligible probability mass to high-quality data (Chen et al., 2025). To test this empirically, we manipulated base model priors through SFT+ and SFT- phases, resulting in models that exhibit differing probabilities of producing the target string τ, which are shown in Table 1a.

When training these models utilizing a standard sparse reward, we indeed find that the base model’s probability of producing the desired behavior has a strong effect on the success of RL post-training. Models artificially injected with the target quote (SFT+) demonstrated quick convergence and easily maximized the sparse reward. Conversely, models lacking coverage completely failed to learn (SFTand the unmodified Qwen3-8B Base). Because the target quote was absent from the reference policy, it was never generated during the RL phase, trapping the agent in a state of zero reward. This failure provides empirical evidence to support the coverage principle: without initial probability mass, RL with sparse rewards does not succeed in learning a new behavior outside of the base model’s original distribution (see Figure 6 in the Appendix for Qwen2-7B learning curves).

Furthermore, unmodified base models highlight the strict threshold of sparse RL. While Qwen2-7B (≈ 3.5% prior) eventually converged after a 40- step exploration plateau, smaller models with lower priors, like Qwen3-1.7B, (≈ 0.5% prior) failed entirely. With rewards so sparse, hitting the correct sequence by chance was statistically improbable under sparse optimization (Figure 2a).

We observe the same exploration bottleneck in our mathematical reasoning task (Table 2). Evaluating Qwen2.5-7B-Instruct on AIME Problem 4 with a sparse reward reveals similar behavior. Models injected with the correct derivation (SFT+) quickly converged (∼85% exact match), while the unmodified Base model stalled near 10%. Because the complete reasoning chain was unlikely under the base distribution, it was rarely sampled during exploration, leaving the model with almost no positive learning signal. This confirms that the Coverage Principle governs real-world RLVR: without sufficient initial probability mass on complete reasoning trajectories, sparse optimization stalls.

<table><tr><td>Model</td><td>SFT+</td><td>Base</td><td>SFT-</td></tr><tr><td>Qwen3-8B</td><td>42.8%</td><td>0.00%</td><td>0.00%</td></tr><tr><td>Qwen2-7B</td><td>28.75%</td><td>3.52%</td><td>0.00%</td></tr><tr><td>Qwen3-1.7B</td><td>14.04%</td><td>0.48%</td><td>0.00%</td></tr><tr><td>Qwen2-1.5B</td><td>7.96%</td><td>0.31%</td><td>0.00%</td></tr></table>

(a) Pre-RL probabilities.

<table><tr><td>Model</td><td>SFT+</td><td>Base</td><td>SFT-</td></tr><tr><td>Qwen3-8B</td><td>100.0%</td><td>0.00%</td><td>0.00%</td></tr><tr><td>Qwen2-7B</td><td>99.6%</td><td>99.9%</td><td>0.00%</td></tr><tr><td>Qwen3-1.7B</td><td>98.7%</td><td>10.0%</td><td>0.00%</td></tr><tr><td>Qwen2-1.5B</td><td>92.5%</td><td>0.71%</td><td>0.00%</td></tr></table>

(b) Post-RL probabilities (sparse rewards).  
Table 1: Probability of producing the target quote before and after RL post-training, (eval = 10,000 samples).

<table><tr><td>Configuration</td><td>SFT+</td><td>Base</td><td>SFT-</td></tr><tr><td>No Reward</td><td>26.6%</td><td>3.92%</td><td>0.00%</td></tr><tr><td>Sparse Reward</td><td>85.9%</td><td>10.2%</td><td>0.00%</td></tr><tr><td>Dense Reward</td><td>86.7%</td><td>92.2%</td><td>0.00%</td></tr></table>

Table 2: Probability of correctly solving AIME Problem 4 before and after RL post-training on Qwen2.5-7B-Instruct (eval = 128 samples).

## 5.2 Dense Reward Shaping: Beyond Pass@k

A prevailing assumption in recent alignment literature is that RL post-training cannot formulate new behaviors, but rather strictly upweights the existing “pass@k” capabilities of the base model, acting merely as a selector rather than a driver of novel behavior (Yue et al., 2025). Our next experiment challenges this assumption, by testing if providing the model with sufficiently dense yet accurate rewards can enable learning new behaviors.

Target string generation. We first experiment in our sequence-generation sandbox, by replacing the binary success metric with a dense Levenshtein distance reward to provide the model with intermediate gradient signals based on structural proximity to the target. Figure 2a shows learning curves for the Qwen3-1.7B model trained with both sparse and dense rewards. Despite the base model possessing a marginal ≈ 0.5% base probability of producing τ, with post-training failing under standard sparse rewards, the dense signal successfully guided the model out of failure, pulling its final match rate to nearly 50%. However, as in classical RL we find that reward shaping has its limits; the SFT+ model trained with dense rewards underperforms the sparse variant in absolute string matching performance, likely because the Levenshtein distance does not sufficiently incentivize producing the exact target string over close approximations.

RLVR reasoning. We then assess if these results replicate for more complex reasoning tasks, testing whether dense rewards provided through a PRM can overcome base model exploration bottlenecks on an AIME mathematical problem. As Figure 2b shows, when optimizing with standard sparse rewards on this task, the base reasoning model failed to meaningfully improve, flat-lining at a match rate of approximately 10% (see Table 2). By contrast, introducing the dense reward radically altered the learning dynamics. With exponentially increasing dense rewards for correctly reaching each step of the reasoning problem, the Base model’s exact match rate jumped to over 90%. It even slightly outperformed the artificially inflated SFT+ model, which plateaued around 85% under both reward types. Qualitative analysis of the Base model’s generated trajectories reveals that the dense reward successfully guided the model to combine disparate, partial reasoning steps into novel, valid solution paths that differed from the original SFT+ ground truth. This shows that RLVR can achieve complex generalization, provided the reward signal is granular enough to credit intermediate logic.

![](images/a235d39568c91ec8fdd0a3eb5cae2d29267c1c3ed39af6f18ed7664afce31f57.jpg)

[Image: The image is a line chart titled "RL Reward Curves Raw Qwen3-1.7B" that plots Reward on the y-axis (ranging from 0.0 to 1.0) against Steps on the x-axis (extending past 120). The chart displays six distinct curves representing three model configurations—BASE, SFT+, and SFT-—each trained with either Dense (solid lines) or Sparse (dashed lines) rewards. The SFT+ model utilizing dense rewards demonstrates the highest performance, showing a sharp increase in reward starting around step 40 and fluctuating near the maximum value of 1.0. In contrast, the sparse reward variants (represented by dashed lines) for all configurations remain stagnant near zero, while the BASE model with dense rewards achieves a moderate upward trend reaching approximately 0.6.]  
(a) Qwen3-1.7B, movie quote

![](images/d15fb1a797f1660d1b96bcfec549b8904aa17762684fc380756830c2ba6cde4b.jpg)

[Image: This line chart displays raw RL reward curves over approximately 50 steps for three model conditions: BASE, SFT+, and SFT-, each tested with both dense and sparse reward functions. The y-axis represents the Reward value ranging from 0.0 to roughly 0.9, while the x-axis indicates Steps. The solid green line (SFT+ Dense) and solid blue line (BASE Dense) show the most successful performance, rising to exceed a reward of 0.8. In contrast, the dashed orange line (SFT- Sparse) remains flat near zero, indicating a lack of learning or active penalization under those specific conditions. The solid orange line (SFT- Dense) fluctuates around a reward of 0.5 to 0.6, demonstrating some level of partial learning despite penalties.]  
(b) Qwen2.5-7B-Instruct, AIME  
Figure 2: Overlay of sparse vs. dense learning dynamics. RL learning curves for (a) Qwen3-1.7B on the movie quote task; (b) Qwen2.5-7B-Instruct on the AIME task. Both figures show an example of how dense rewards can successfully guide the model to learn a behavior with very low probability in the base model, which it is not possible to learn with sparse rewards.

The SFT- reasoning experiments also highlight an interesting nuance about partial learning. While the heavily penalized SFT- model achieved a 0% exact match rate under both sparse and dense rewards, tracking its trajectory revealed that under the dense reward, its average reward climbed steadily to approximately 0.6 (Figure 2b). This indicates that even when a policy is actively suppressed from reaching the final correct answer, a dense reward allows it to re-learn through iteratively building on intermediate reasoning milestones.

Taken together, these results demonstrate that the limitations often attributed to RLVR—such as the inability to move beyond pass@k priors—are not inherent flaws of RL post-training, but rather artifacts of the exploration bottleneck caused by sparse, binary reward functions.

![](images/eb8d8e560527c487541b3b50306fed1e4d614e75a4c6b0f34c1a8b6265ffdc9b.jpg)

[Image: The image displays a line chart titled "Avg accuracy (MATH + AMC)" plotting performance over "global step" on the x-axis and "acc@1" on the y-axis. Two data series are presented: a blue line representing "Narrow (DeepScaleR)" and an orange line for "Broad (WildChat)". The Narrow model demonstrates a general increasing trend, finishing at an accuracy of 0.547, while the Broad model shows more volatility and ends at a lower value of 0.496.]  
Figure 3: Acc@1 on the MATH and AMC datasets after training on narrow and broad D; training on narrow D yields higher accuracy.

## 5.3 Prompt Distribution: Broad vs. Narrow

Qwen family. Figure 3 show the effects of training on spurious (random) rewards, with both the narrow prompt distribution of Shao et al. (2025), and the broad distribution. The narrow distribution replicates the original results, showing that the capabilities of Qwen models can actually increase with random rewards. However, when switching to a broad prompt distribution, we see minimal improvements on the MATH benchmark, and degraded performance on AMC. This is supported by tracking the entropy through training (Figure 4). Under the narrow distribution, entropy remains low through training, while under the broad distribution, it jumps at the first step and remains high.

![](images/c78dff7cc6e37fbf38fd93f4031dbc75e05d15db04ec81a8cb63efe3049eae7b.jpg)

[Image: Line chart titled "Entropy over Training" plotting Average Entropy against Training Steps from 0 to 1000. Three data series are displayed: "Base" (blue), "SFT" (orange), and "DPO" (green). The "Base" model begins with high entropy around 1.7, spikes to approximately 2.15 between steps 200 and 300, and stabilizes near 2.0. In contrast, both "SFT" and "DPO" start with low entropy near 0.6; "SFT" jumps to roughly 1.5 after step 400, while "DPO" rises later to about 1.4 after step 500, eventually plateauing below the "Base" trajectory.]  
(a) Broad distribution: entropy

![](images/4e3557ed89778dd0f0cbc7c616f7e83b82a6675f18ebd03629d321dc564abafa.jpg)

[Image: This line chart displays model performance during SFT Training, plotting 'Log Likelihood' and 'Entropy' on the left y-axis and 'Eval Score (%)' on the right y-axis against 'Training Step' on the x-axis. The evaluation metrics for GSM8K (green), MMLU (purple), and IFEval (orange) maintain high stability between 60% and 90% until approximately step 400, where they experience a simultaneous, sharp decline toward 0%. In contrast, the Entropy metric (red) exhibits a sharp spike upwards to roughly 1.5 at step 400, while Log Likelihood (blue) plummets from -0.6 to below -1.5, creating a distinct inverse correlation with the evaluation scores at that specific training interval.]  
(b) Broad distribution: capabilities

![](images/a15909d63527495cf42a51d737e3d12ecb73a86fb305b8efd208392a7cbeb226.jpg)

[Image: This dual-axis line chart, titled "SFT Narrow D Training," plots training metrics and evaluation scores against training steps from 0 to 800. The left y-axis represents "Log Likelihood / Entropy" ranging from -1.00 to 0.50, while the right y-axis represents "Eval Score (%)" from 0 to 100. Key data series include `log_likelihood` (blue diamonds), which steadily decreases from approximately -0.75 to -1.00, and `GSM8K` (green circles), which shows a sharp decline from roughly 0.4 to -0.5 after step 200. Other series such as `IFEval` (orange triangles), `MMLU` (purple markers), and a red series with square markers remain relatively stable at higher values throughout the training process.]  
(c) Narrow distribution  
Figure 4: Effect of training OLMo models on spurious (random) rewards). (a) Average entropy on broad D (10k prompts). Each training stage (Base → SFT → DPO) delays entropy increase onset, showing increasing resilience. (b) Broad D SFT model—entropy spike at step ∼400 coincides with collapse of all eval metrics (GSM8K, MMLU, IFEval), confirming global unlearning. (c) Narrow D SFT model (100 math prompts)—entropy decreases, MMLU and IFEval are preserved, but GSM8K collapses, showing targeted corruption of the training domain.

OLMo family. Figure 4 shows the effect of posttraining the OLMo family of models (base, SFT, and DPO) on spurious rewards. Under a broad prompt distribution D, we see that the entropy of the models increases (Fig. 4a), and that this increase at step ∼400 for the SFT model corresponds to a sharp decrease in capabilities, as measured with the GSM8K, MMLU, and IFEval benchmarks (Fig. 4b). Notably, log likelihood decreases and entropy increases uniformly across all three domains (math, code, instruction following), with no generalization gap. This indicates the unlearning is global: random rewards on a broad D effectively reward any response to any prompt, erasing the model’s learned distribution.

Under a narrow D (100 math-only prompts), the dynamics differ strikingly. As shown in Figure 4c, entropy decreases slightly across all domains, indicating the model’s distribution is tightening rather than dispersing. However, this increased certainty does not mean improved performance: GSM8K drops from 86% to ∼32% by step 400, while MMLU (∼65%→62%) and IFEval (∼79%→77%) remain largely intact. Damage is domain-specific: random rewards corrupt the training domain while preserving capabilities in unsampled domains.

The breadth of D, as well as the base model’s distribution, determine both the scope of degradation, and whether degradation occurs. A broad D causes widespread unlearning. A narrow D increases certainty about the responses the base model was already likely to produce, which can either lead to performance improvement or targeted corruption, depending on the base model’s initial accuracy. Although a narrow D uses fewer examples with more repetition, this repetition is exactly what drives the policy to collapse toward its prior. Neither setting creates new capabilities. Qwen’s gains under a narrow D fit this explanation: the same targeted sharpening that harms GSM8K performance in OLMo 3 instead reinforces the correct math reasoning paths already present in Qwen. This suggests that spurious rewards improve performance only when the prompt distribution is narrow and the base model is already strongly biased toward the target domain, a restricted setting that does not apply to most of RL post-training.

# 6 Conclusion

In this work, we deconstructed the mechanics of RL post-training for LLMs to explain how components of the post-training algorithm—the base model distribution, prompt distribution, and reward structure—affect optimization outcomes. By isolating the components of the RLVR pipeline within a controlled sequence-generation sandbox, we explain, empirically verify, or provide a counterpoint to existing post-training results in the literature. In particular, we show that standard sparse RL is unable to surpass the base model’s initialization lim its. When a target behavior lacks sufficient baseline coverage, the model cannot sample it, making optimization untenable. However, we show that this is not a hard and fast limitation of RL post-training as a technique; a sufficiently dense and accurate reward function can enable learning new behaviors with vanishing support in the base model, a finding that contradicts a popular position in the literature (Yue et al., 2025; Shao et al., 2025; Wu et al.; Zhao et al., 2025; Wu et al., 2025). Furthermore, we show the effect of “spurious rewards” depends entirely on the post-training prompt distribution.

Training with random rewards on a broad prompt distribution leads to an increase in model entropy and a corresponding catastrophic decrease in capabilities. By clarifying these interacting mechanics, we hope this work can serve as a resource to the NLP community and those looking to sharpen their understanding of the mechanics of RL posttraining, and help move the field beyond treating RL as a “black box” toward a more controlled and interpretable optimization process.

# Acknowledgments

This research was supported by the UW-Amazon Science Gift Hub, UW-Tsukuba Amazon NVIDIA Cross Pacific AI Initiative (XPAI), Sony Research Award, Tinker Research Grants, Character.AI, DoorDash, Open Philanthropy, Coefficient Giving, Toyota Research Institute, the Schmidt AI2050 Fellows program, and the NSF CISE RI program, award #2550849. This material is based upon work supported by the Defense Advanced Research Projects Agency and the Air Force Research Laboratory, contract number(s): FA8650-23-C-7316. Any opinions, findings and conclusions, or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of AFRL or DARPA. This work was supported by NSF grants CNS-2112471, IIS-2229876, CCF-2505865, and DMS-2502281.

# References

Ömer Faruk Akgül, Rajgopal Kannan, Willie Neiswanger, and Viktor Prasanna. 2026. Rethinking rl for llm reasoning: It’s sparse policy selection, not capability learning. arXiv preprint arXiv:2605.06241.

Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, and 32 others. 2022. Constitutional ai: Harmlessness from ai feedback. Preprint, arXiv:2212.08073.

Fan Chen, Audrey Huang, Noah Golowich, Sadhika Malladi, Adam Block, Jordan T. Ash, Akshay Krishnamurthy, and Dylan J. Foster. 2025. The coverage principle: How pre-training enables post-training. Preprint, arXiv:2510.15020.

Xuxin Cheng, Kexin Shi, Ananye Agarwal, and Deepak Pathak. 2023. Extreme parkour with legged robots. Preprint i

Maxime Chevalier-Boisvert, Bolun Dai, Mark Towers, Rodrigo de Lazcano, Lucas Willems, Salem Lahlou, Suman Pal, Pablo Samuel Castro, and Jordan Terry. 2023. Minigrid & miniworld: Modular & customizable reinforcement learning environments for goaloriented tasks. Preprint, arXiv:2306.13831.

Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei. 2023. Deep reinforcement learning from human preferences. Preprint, arXiv:1706.03741.

Cristian Danescu-Niculescu-Mizil and Lillian Lee. 2011. Chameleons in imagined conversations: A new approach to understanding coordination of linguistic style in dialogs. In Proceedings ofthe Workshop on Cognitive Modeling and Computational Linguistics, ACL 2011.

Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, and Sergey Levine. 2018. Diversity is all you need: Learning skills without a reward function. arXiv preprint arXiv:1802.06070.

Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, and 175 others. 2025. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. Nature, 645(8081):633–638.

Jian Hu, Xibin Wu, Zilin Zhu, Xianyu, Weixun Wang, Dehao Zhang, and Yu Cao. 2024. Openrlhf: An easyto-use, scalable and high-performance rlhf framework. arXiv preprint arXiv:2405.11143.

Natasha Jaques, Shixiang Gu, Dzmitry Bahdanau, José Miguel Hernández-Lobato, Richard E. Turner, and Douglas Eck. 2017. Sequence tutor: Conservative fine-tuning of sequence generation models with kl-control. Preprint, arXiv:1611.02796.

Magnus Jørgenvåg, David Kaczér, Lasse Ruttert, Marvin Gülhan, Lucie Flek, and Florian Mai. 2026. Reinforcement learning amplifies emergent misalignment from harmless rewards. arXiv preprint arXiv:2605.31328.

Devvrit Khatri, Lovish Madaan, Rishabh Tiwari, Rachit Bansal, Sai Surya Duvvuri, Manzil Zaheer, Inderjit S. Dhillon, David Brandfonbrener, and Rishabh Agarwal. 2025. The art of scaling reinforcement learning compute for llms. Preprint, arXiv:2510.13786.

Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman, Lester James V. Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, Yuling Gu, Saumya Malik, Victoria Graf, Jena D. Hwang, Jiangjiang Yang, Ronan Le Bras, Oyvind Tafjord, Chris Wilhelm, Luca Soldaini, and 4 others. 2025. Tulu 3: Pushing frontiers in open language model post-training. Preprint, arXiv:2411.15124.

Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. 2023. Let’s verify step by step. Preprint, arXiv:2305.20050.

Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, and Ryan Lowe. 2022. Training language models to follow instructions with human feedback. Preprint, arXiv:2203.02155.

Neel Rajani, Aryo Pradipta Gema, Seraphina Goldfarb-Tarrant, and Ivan Titov. 2025. Scalpel vs. hammer: Grpo amplifies existing capabilities, sft replaces them. arXiv preprint arXiv:2507.10616.

Yi Ren and Danica J. Sutherland. 2025. Learning dynamics of llm finetuning. Preprint, arXiv:2407.10490.

Amrith Setlur, Chirag Nagpal, Adam Fisch, Xinyang Geng, Jacob Eisenstein, Rishabh Agarwal, Alekh Agarwal, Jonathan Berant, and Aviral Kumar. 2024. Rewarding progress: Scaling automated process verifiers for llm reasoning. Preprint, arXiv:2410.08146.

Rulin Shao, Shuyue Stella Li, Rui Xin, Scott Geng, Yiping Wang, Sewoong Oh, Simon Shaolei Du, Nathan Lambert, Sewon Min, Ranjay Krishna, Yulia Tsvetkov, Hannaneh Hajishirzi, Pang Wei Koh, and Luke Zettlemoyer. 2025. Spurious rewards: Rethinking training signals in rlvr. Preprint, arXiv:2506.10947.

David Silver, Aja Huang, Chris J Maddison, Arthur Guez, Laurent Sifre, George Van Den Driessche, Ju lian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, et al. 2016. Mastering the game of go with deep neural networks and tree search. nature, 529(7587):484–489.

Nisan Stiennon, Long Ouyang, Jeff Wu, Daniel M. Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford, Dario Amodei, and Paul Christiano. 2022. Learning to summarize from human feedback. Preprint, arXiv:2009.01325

Sijun Tan, Michael Luo, Justin Wong, Colin Cai, Xiaoxiang Shi, William Yuan Tang, Manan Roongta, Tianjun Zhang, Li Erran Li, Raluca Ada Popa, and Ion Stoica. 2026. Deepscaler: Effective RL scaling of reasoning models via iterative context lengthening.

OLMo Team, Allyson Ettinger, Amanda Bertsch, Bailey Kuehl, David Graham, David Heineman, Dirk Groen eveld, Faeze Brahman, Finbarr Timbers, Hamish Ivison, Jacob Morrison, Jake Poznanski, Kyle Lo, Luca Soldaini, Matt Jordan, Mayee Chen, Michael Noukhovitch, Nathan Lambert, Pete Walsh, and 49 others. 2025. Olmo 3. In Technical Report, 2025.

Rishabh Tiwari, Aditya Tomar, Udbhav Bamba, Monishwaran Maheswaran, Heng Yang, Michael W. Mahoney, Kurt Keutzer, and Amir Gholami. 2026. Reward under attack: Analyzing the robustness and hackability of process reward models. Preprint, arXiv:2603.06621.

Oriol Vinyals, Igor Babuschkin, Wojciech M Czarnecki, Michaël Mathieu, Andrew Dudzik, Junyoung Chung, David H Choi, Richard Powell, Timo Ewalds, Petko Georgiev, et al. 2019. Grandmaster level in starcraft ii using multi-agent reinforcement learning. nature, 575(7782):350–354.

Fang Wu, Aaron Tu, Weihao Xuan, Heli Qi, Xu Huang, Qingcheng Zeng, Shayan Talaei, Yijia Xiao, Peng Xia, Xiangru Tang, et al. 2025. Position: The hidden costs and measurement gaps of reinforcement learning with verifiable rewards. arXiv preprint arXiv:2509.21882.

Fang Wu, Weihao Xuan, Ximing Lu, Mingjie Liu, Yi Dong, Zaid Harchaoui, and Yejin Choi. The invisible leash: Why rlvr may or may not escape its origin, 2026. URL https://arxiv. org/abs/2507.14843.

Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. 2025. Kungfubot: Physics-based humanoid whole-body control for learning highlydynamic skills. Preprint, arXiv:2506.12851.

Wanli Yang, Hongyu Zang, Junwei Zhang, Wenjie Shi, Du Su, Jingang Wang, Xueqi Cheng, and Fei Sun. 2026. Beyond reasoning: Reinforcement learning unlocks parametric knowledge in llms. arXiv preprint arXiv:2605.07153.

Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, and Gao Huang. 2025. Does reinforcement learning really incentivize reasoning capacity in llms beyond the base model? Preprint, arXiv:2504.13837.

Rosie Zhao, Alexandru Meterez, Sham Kakade, Cengiz Pehlevan, Samy Jelassi, and Eran Malach. 2025. Echo chamber: Rl post-training amplifies behaviors learned in pretraining. arXiv preprint arXiv:2504.07912.

Wenting Zhao, Xiang Ren, Jack Hessel, Claire Cardie, Yejin Choi, and Yuntian Deng. 2024. Wildchat: 1m chatgpt interaction logs in the wild. Preprint, arXiv:2405.01470

# A Resource Details

## A.1 Computational Specifications

All experiments were run on either NVIDIA A100 80GB GPU or NVIDIA L40s 48GB. For the Math reasoning task, an NVIDIA A100 80GB GPU was used for the main experiments, while an NVIDIA L40s 48GB was used for the PRM LLM-as-a-Judge.

## A.2 LLM Usage

LLMs were used in the development of the code base/experiments, specifically modifying behavior to adapt to resource limitations, as well as simplify experiment pipeline for generating results.

