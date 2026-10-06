## A Ablations

### A.1 Scaling Abstract Vocabulary Size

![](images/47c4f40d7f8e8e73bdec45b3944ab0af68e03a8a601cef72668100002ababfd3.jpg)

[Image: The image presents a line chart plotting "MATH-500 Accuracy" on the y-axis against "Vocabulary Size M (log2 scale)" on the x-axis, which ranges from 1 to 512. A horizontal dashed blue line represents the "Base model" accuracy constant at 82.5. The "PI-3 + RL" data series (purple circles) demonstrates the highest performance, increasing from approximately 80.5 to nearly 91.5 as vocabulary size increases. Other configurations like "PI-3" (green) and "PI-2" (orange) follow an upward trend, surpassing the base model significantly at larger vocabulary sizes, while "Cold-start RL" (red) remains consistently below the base model line.]  
Figure 5: MATH-500 abstract vocabulary scaling ablation across stages of the Abstract-CoT pipeline, compared against cold-start RL, the base model performance, and the pause token baseline $( M \stackrel { \cdot } { = } 1$ variant with greater data). The results show clear and consistent scaling trends across warm-up stages and warm-started RL, plateauing at larger vocabulary sizes, while cold-start flattens out much earlier and does not surpass the base model performance.

![](images/fbd414be51c919a3dc881508162aa3f8bccdca4b89e3d329586ca357af05069b.jpg)

[Image: The line chart plots AlpacaEval Win-rate against Vocabulary Size M on a logarithmic scale, ranging from 1 to 512. It compares several model configurations, including three stages of Policy Iteration (PI-1, PI-2, PI-3), PI-3 combined with Reinforcement Learning (PI-3 + RL), and a Cold-start RL baseline against a static Base model line and a Pause token data point. The PI-3 + RL series demonstrates the strongest performance, rising sharply to a peak win-rate over 60 at a vocabulary size of 64. While the PI-3, PI-2, and PI-1 series also show positive scaling trends surpassing the base model, the Cold-start RL series underperforms the base model across all vocabulary sizes.]  
Figure 6: AlpacaEval abstract vocabulary scaling ablation. The results show clearer differentiation than MATH-500, with $M = 6 4$ achieving the highest score with PI-3 and $\mathrm { P I } { - } 3 + \mathrm { R I }$ , and cold-start RL again underperforming the base model while surpassing PI-1.

We ablate the behavior of Abstract-CoT when scaling the size of $\mathcal { V } ^ { \ast }$ , with values ranging from $M = 1 \left( 2 ^ { 0 } \right)$ to $M = 5 1 2 \left( 2 ^ { 9 } \right)$ ), across stages of training (3× Policy Iteration warm-up, GRPO) as well as with cold-start GRPO with randomly initialized embeddings for the abstract tokens. Aside from analyzing the value of a larger vocabulary on benchmark performance across MATH-500, AlpacaEval, and HotpotQA, this allows us to study trends in the frequency distributions between cold-started and warm-started RL. Since the M = 1 case trivially invokes the same token every time, we start from M = 2. Note that for the distribution plots, the y-axes have been scaled to illustrate the variation in token frequency.

![](images/03738c78c7c0e0210934dd8cfd88461539447594916f2e6ade61b85134535a3f.jpg)

[Image: The image displays a line chart plotting HotpotQA F1 scores versus Vocabulary Size $M$ on a logarithmic scale ranging from 1 to 512. Multiple methods are compared, including 'PI-3 + RL', 'PI-3', 'PI-2', 'PI-1', and 'Cold-start RL', in addition to a horizontal dashed 'Base model' reference line situated at an F1 score of 51. The 'PI-3 + RL' series demonstrates the strongest performance, rising continuously to a peak F1 score of approximately 59 at M=64 before slightly declining. In contrast, the 'Cold-start RL' series consistently underperforms the others, maintaining scores between 47 and 49 across all vocabulary sizes. While most curves show improvement as vocabulary size scales up to 64, they generally plateau or decrease afterward.]  
Figure 7: HotpotQA abstract vocabulary scaling ablation. The results again show clearly differentiable scaling curves, with PI-3 and PI-3 + RL exhibiting near-linear improvement from M = 1 to M = 64, followed by a decline. On the other hand, cold-start lags behind even PI-1, further supporting the value of the warm-up stage.

The results in Figures 5- 7 demonstrate that across all three benchmarks, scaling the size of the vocabulary improves performance, yet eventually saturates and slightly declines. This trend holds across all methods, though cold-start RL appears to consistently underperform the base model’s performance out-of-the-box regardless of vocabulary size – in fact, it underperforms PI-1 on HotpotQA for all sizes and on MATH-500 for the tested values of M ≥ 16. On the basis of these scaling analyses, M = 64 was chosen as the best configuration.

#### A.1.1 Frequency Distribution Across RL Training

Figures 8-16 demonstrate the change in token frequency after the policy iteration warm-up (RL step 0) to after RL training, depicted by the subfigures on the left, and the frequency distribution by token rank after RL, given by the subfigures on the right. As shown in Figure 4, RL training shapes the distribution of token usage, resulting in a power law-like distribution that is more evident at larger vocabulary sizes. We observe that using a max sequence length of 128 during training, as we scale the vocabulary size, there are more tokens in the tail that are relatively unused, despite the initial stage of warm-up involving a uniform schedule of abstract token selection. This suggests that the model learns to re-use certain tokens for frequently re-appearing concepts, while reserving others for more rare concepts.

![](images/b6f8d4d681d61c28c598b6f0101d7053f67d9eaeea91c0eb2c9c2918b4ccdee0.jpg)

[Image: This line chart plots Token Frequency on the vertical axis against RL Step on the horizontal axis, illustrating the performance of a model with a 2-token vocabulary. A dark blue curve tracks a token starting at a frequency of roughly 0.61, which gradually rises to reach 0.7 by the final step. Simultaneously, a lighter blue curve tracks a second token beginning near 0.4 that stabilizes briefly before declining to a frequency of 0.3.]

![](images/55198e73b4808853fbf54dd7336c05c0bf7ea4f2a46d7639f53928df4f4ebd6f.jpg)

[Image: This bar chart illustrates the "Token Frequency at Final Step" across two categories labeled on the x-axis as "Token Rank (final step)" with values 1 and 2. The first category (Rank 1) is represented by a dark blue bar reaching a y-value of 0.7, while the second category (Rank 2) is represented by a light blue bar reaching a y-value of 0.3. The visual data indicates a significant disparity in frequency, where the top-ranked token occurs more than twice as often as the second-ranked token.]  
Figure 8: Scaling ablation with M = 2 abstract token vocabulary.

![](images/7251a4ebd54397372c89ebfcca440b5b105e66ff656478d3b0b25bbd69d8c80f.jpg)

[Image: This line chart illustrates Token Frequency against RL Steps for a scaling ablation experiment utilizing an M = 2 abstract token vocabulary. The horizontal axis ranges from 0 to roughly 3750 steps, while the vertical axis scales from 0.0 to 0.4. Multiple data series are plotted, dominated by a dark blue line that rises continuously from approximately 0.31 to 0.45, while three other lines remain clustered lower between 0.15 and 0.25, showing generally flat or downward trends.]

![](images/628ffd752e5fd61294b50d157855ceac9d609bfb50dec8a57827e9863868d49c.jpg)

[Image: Vertical bar chart illustrating 'Token Frequency at Final Step' across four 'Token Rank' categories. The y-axis scales from 0.0 to 0.4, showing a clear downward trend in frequency as the token rank increases. The first token rank exhibits the highest frequency at approximately 0.44, followed by ranks 2, 3, and 4 with frequencies declining to roughly 0.22, 0.18, and 0.16 respectively.]  
Figure 9: Scaling ablation with M = 4 abstract token vocabulary.

![](images/c00a349701e6db3a2944745f174c8651577157cc0c67629aab4b7c111859bede.jpg)

[Image: This line chart illustrates the Token Frequency over RL Steps for an experiment using a 4-token vocabulary. A primary dark blue line dominates the plot, rising from roughly 0.12 to a peak above 0.20 near step 2000 before stabilizing around 0.21. A secondary light blue line trends upward later in the training, peaking near 0.15 at step 3000, while an orange line shows a steady, gradual increase to approximately 0.12. The remaining multiple trajectories are clustered at the bottom of the graph, generally fluctuating between frequencies of 0.05 and 0.07.]

![](images/65681e8a646901943e68ddc4b72e2ed2788869a3a70589dac0cfdf634f379f4e.jpg)

[Image: This vertical bar chart illustrates the token frequency at the final step across 16 distinct token ranks. The y-axis, labeled "Token Frequency at Final Step," ranges from 0.00 to roughly 0.22, showing that Rank 1 has the highest frequency at slightly above 0.20. As the token rank increases along the x-axis, the frequency generally decreases, with Ranks 2 and 3 dropping to approximately 0.12 and subsequent ranks falling further until they approach zero by Rank 16.]  
Figure 11: Scaling ablation with M = 16 abstract token vocabulary.

![](images/459888a460177a0a66a4c4c249fa13fcb60a6414fbc9d80190ce7eabcdf2e625.jpg)

[Image: Line chart displaying Token Frequency on the y-axis (ranging from 0.00 to 0.12) versus RL Step on the x-axis (ranging from 0 to approximately 3750). A dark blue line exhibits the steepest growth, rising from approximately 0.03 to over 0.11 by the final plotted steps. Several other lines, including orange and light blue traces, show moderate upward trends, while the majority of the multicolored lines remain clustered near the bottom, fluctuating mostly below 0.04. Based on the surrounding text referencing "scaling ablation," this plot likely tracks the usage frequency of specific tokens or token groups during a reinforcement learning training process.]

![](images/795fe1630c56837aa6b8b16a0376deffef4eecbad2c8791b38e8f2c0a60aa27d.jpg)

[Image: The image presents a bar chart illustrating 'Token Frequency at Final Step' relative to 'Token Rank (final step)'. The vertical axis measures frequency from 0.00 to 0.12, while the horizontal axis lists token ranks up to 121. The data reveals a dominant spike at rank 1, where the blue bar exceeds a frequency of 0.11, followed by a sharp decay where subsequent ranks quickly drop below 0.02. For higher ranks beyond 20, the bars remain consistently short and multicolored, hovering near a frequency of roughly 0.01.]  
Figure 14: Scaling ablation with M = 128 abstract token vocabulary.

![](images/a1e0a9d23281fc7ad493b63a576cd09ad7fd4439e29d1e545d44d62a048f2148.jpg)

[Image: Line chart showing Token Frequency on the y-axis versus RL Step on the x-axis for a scaling ablation study with an M=128 abstract token vocabulary. The top dark blue trajectory begins at approximately 0.22 frequency and exhibits a significant upward trend after step 3000, reaching above 0.30. A secondary light blue line shows steady growth from 0.17 to 0.22, while an orange line peaks around step 2000 before declining. Several lower-frequency lines in green, red, and pink remain below 0.10 throughout the timeline, with most showing either fluctuation or a general downward trend.]

![](images/2ec45750b8832fe7d8280ca039280a361a013f5eee74bc4215d09aad1fbff301.jpg)

[Image: This vertical bar chart plots "Token Frequency at Final Step" on the y-axis against "Token Rank (final step)" ranging from 1 to 8 on the x-axis. The data shows a decreasing trend in frequency as the token rank increases, with the first bar (Rank 1) reaching the highest value of approximately 0.33. Subsequent bars show lower frequencies, dropping to roughly 0.23 for Rank 2 and continuing down to approximately 0.03 for Rank 8. Each rank is represented by a distinct colored bar, transitioning from dark blue to pink.]  
Figure 10: Scaling ablation with M = 8 abstract token vocabulary.

![](images/b7affce5d22a0cef619e597f26b82f5f885cd97a55a914062eab5640c98b39aa.jpg)

[Image: This line chart plots "Token Frequency" on the vertical axis against "RL Step" on the horizontal axis, which extends from 0 to approximately 3750. A single dark blue line exhibits a distinct upward trend, increasing from a frequency of roughly 0.16 to 0.26, while a dense cluster of multicolored lines remains confined to the lower range, fluctuating between 0.00 and 0.10. The figure, labeled as a scaling ablation with an $M = 8$ abstract token vocabulary, illustrates how token distribution diverges over training steps, with one token becoming significantly more dominant than the rest.]

![](images/5cf6da08fd41c5c62edeb52826679acf92bb2f0b3ab34d4c29520e6e752e2214.jpg)

[Image: This vertical bar chart displays the frequency of abstract tokens at the final step, plotted against their ranking. The x-axis indicates the Token Rank, incrementing from 1 to 31, while the y-axis represents Token Frequency at Final Step with a scale from 0.00 to 0.25. The data shows a highly skewed distribution where the first token (blue bar) dominates with a frequency slightly above 0.25. There is a rapid decay in frequency for subsequent tokens, with the second bar dropping to 0.10 and higher ranks tapering off near zero.]  
Figure 12: Scaling ablation with $M = 3 2$ abstract token vocabulary.

![](images/40df0927cfcf175c91490711c6c0da92d319a24f2710b3c42d409cb674e90f98.jpg)

[Image: The image presents two plots analyzing token frequency dynamics, likely related to a scaling ablation study. The left panel is a line chart plotting Token Frequency against RL Step, where a distinct dark blue line rises steadily to approximately 0.08 while numerous other colored lines remain clustered below 0.04. The right panel is a bar chart depicting Token Frequency at the Final Step across Token Ranks from 1 to 241, revealing a heavily skewed distribution where the highest-ranking token dominates with a frequency near 0.075 before rapidly decaying.]  
Figure 15: Scaling ablation with M = 256 abstract token vocabulary.

![](images/85c615ec492630ceadef7f7d9c1c0cf34c5b945f5b46789e4ae6de90f1ae184a.jpg)

[Image: The image displays two plots illustrating token frequency dynamics using a vocabulary size of 256. The left plot is a line chart tracking "Token Frequency" against "RL Step," where a single dominant dark blue line increases from approximately 0.02 to just over 0.04, while other lines remain clustered at lower values. The right plot shows a vertical bar chart of "Token Frequency at Final Step" sorted by "Token Rank," revealing a steep distribution where the top-ranked token reaches nearly 0.04 and frequencies for subsequent ranks drop off sharply.]  
Figure 16: Scaling ablation with $M = 5 1 2$ abstract token vocabulary.

#### A.1.2 Cold-Start RL Frequency Distribution

For comparison, we include the frequency distribution with $M = 6 4$ for cold-start RL training in Figure 17. The starting frequency is uniform probability $\textstyle { { \bigl ( } { \frac { 1 } { M } } { \bigr ) } }$ given the embeddings are randomly initialized. We find a distribution that less closely resembles a power law compared to the warm-started RL. This demonstrates the efficacy of the warm-up toward its goal of embedding learning for the new vocabulary, creating a distribution of token usage that is further shaped through RL. On-policy generation, which happens in the self-distillation phase as well as the bottlenecked SFT stage with t > 1, allows the model to learn the relationship between successful sequences and a teacher (gold) response. By contrast, though cold-start RL quickly learns to use the token which ends up with the highest frequency (<TOKEN\_T>)), several other tokens are eventually used with similar frequency while other tokens are very rarely used. It is possible that further scaling training compute – specifically, rollouts and RL episodes – could have a similar effect as a warm-up phase.

![](images/7a44ad871fe1de004283485ba22fdeb8b9f7ba537a3cce34a59325067e081806.jpg)

[Image: The image displays a line chart plotting "Token Frequency" on the y-axis against "RL Step" on the x-axis, spanning approximately 0 to 3,500 steps. A single dark blue line demonstrates a strong positive trend, starting near 0.07 and steadily increasing to surpass 0.14 by the final step, indicating the emergence of a highly frequent token. Conversely, a light blue line plateaus around 0.08 to 0.09, while a large cluster of multicolored lines remains concentrated at low frequencies between 0.01 and 0.05, illustrating that most other tokens are utilized with significantly less frequency.]

![](images/af7073e86794989d3be5af73f045300739504351f0f023e3b2aee037c0a2c0ca.jpg)

[Image: The image displays a bar chart illustrating "Token Frequency at Final Step" on the vertical axis against "Token Rank (final step)" on the horizontal axis. The data shows a highly skewed distribution where the token at rank 1 has the highest frequency, exceeding 0.14, represented by a tall blue bar. Frequencies drop sharply for the next few ranks, with the second highest value reaching approximately 0.05 around rank 4, followed by a gradual decay where most remaining tokens have frequencies below 0.02.]  
Figure 13: Scaling ablation with M = 64 abstract token vocabulary. Note that this is the same as Figure 4, included in the appendix for comparison to the other vocabulary sizes.

![](images/d4d320560e1c0f074a3bba30dc1e93e94494c79f924ffaa76ea9768a77d7a7fd.jpg)

[Image: Line chart displaying Token Frequency against RL Steps for an experiment involving a vocabulary size of $M=64$. A single dark blue line exhibits the highest frequency, peaking near 0.10 around step 1000 and stabilizing between 0.08 and 0.09. Several other colored lines show intermediate frequency levels ranging between 0.04 and 0.08, while a large number of fainter lines remain clustered near the bottom axis below 0.02.]

![](images/c624f13d5754ba037c63fed0d04a6999db6ab3c42dfb2770ee379e6ef3b926c3.jpg)

[Image: This bar chart illustrates the distribution of token frequency at the final step relative to their rank. The vertical axis measures frequency from 0.00 to 0.08, while the horizontal axis marks token ranks up to 61. The data reveals a strong inverse correlation, with the top-ranked tokens showing the highest frequencies—peaking near 0.08 for rank 1—and frequencies decaying sharply as the rank number increases. By rank 21, frequencies have dropped below 0.01, continuing to taper off toward zero for higher ranks.]  
Figure 17: Cold-start RL in the scaling ablation with M = 64 abstract token vocabulary.

### A.2 Scaling Model Size: Qwen3-32B

While we have studied the transferability of our method across model families (Qwen, Granite), it is also valuable to examine whether the method scales to larger model sizes. Thus, we study the performance of Abstract-CoT with Qwen3-32B, in comparison to baselines consistent with those reported in Table 1. SFT training was performed with 8×NVIDIA H100 GPUs, and RL training was performed on 32×NVIDIA H100 GPUs. As with Qwen3-8B, the "thinking mode" is disabled.

The findings corroborate those in Table 1: Abstract-CoT outperforms verbalized CoT (SFT + RL) on AlpacaEval and HotpotQA while using 2.7× and 4.4× fewer tokens, respectively, while nearly matching performance on MATH-500 with 11.0× fewer tokens. The 32B model appears to be slightly more verbose in its reasoning traces and response tokens than its 8B counterpart, resulting in slight increases in average tokens for all settings.

### A.3 CoT Truncation Analysis

While verbal chain-of-thought generates a large number of thinking tokens within its delimiters, truncating reasoning trace to a short length serves as a form of inference-time budget control and a mechanism to analyze the "compactness" of Abstract-CoT sequences.

<table><tr><td rowspan="2">Method</td><td colspan="2">MATH-500</td><td colspan="2">AlpacaEval</td><td colspan="2">HotpotQA</td></tr><tr><td>Accuracy</td><td>Tokens</td><td>Win-rate</td><td>Tokens</td><td>F1</td><td>Tokens</td></tr><tr><td>Baseline</td><td>86.8</td><td>1278</td><td>60.5</td><td>361</td><td>54.4</td><td>598</td></tr><tr><td>Pause Tokens</td><td>82.6</td><td>156</td><td>53.9</td><td>240</td><td>52.1</td><td>176</td></tr><tr><td>Stepwise Internalization</td><td>90.6</td><td>163</td><td>61.3</td><td>261</td><td>56.6</td><td>165</td></tr><tr><td>SFT (no CoT)</td><td>89.0</td><td>427</td><td>60.8</td><td>372</td><td>55.1</td><td>372</td></tr><tr><td>SFT (CoT)</td><td>93.4</td><td>1706</td><td>63.3</td><td>545</td><td>58.3</td><td>734</td></tr><tr><td>SFT+RL</td><td>95.0</td><td>1832</td><td>65.2</td><td>608</td><td>60.9</td><td>797</td></tr><tr><td>Abstract-CoT (RL-only)</td><td>84.4</td><td>137</td><td>58.9</td><td>232</td><td>53.8</td><td>156</td></tr><tr><td>Abstract-CoT (Warm-up)</td><td>90.2</td><td>195</td><td>62.7</td><td>277</td><td>58.6</td><td>216</td></tr><tr><td>Abstract-CoT (Warm-up + RL)</td><td>94.6</td><td>167</td><td>65.6</td><td>229</td><td>62.1</td><td>180</td></tr></table>

Table 4: Results on MATH-500 (accuracy), AlpacaEval (win-rate) and HotpotQA (F1) with Qwen3-32B, demonstrating efficiency gains and strong performance consistent with the trends exhibited with other models, highlighting the scalability of Abstract-CoT.

Prior works have sought to extend CoT lengths for reasoning tasks to analyze budget control, such as appending "Wait" to its generation to continue reasoning (Muennighoff et al., 2025). We limit the model to k tokens by truncation: for Abstract-CoT, this means halting the CoT after k tokens and appending the <endabstract> delimiter prior to response generation. The complete set of results across benchmarks and for k = {32, 48, 64} are included in Table 5.

<table><tr><td>Method</td><td>Full CoT</td><td>64 Tokens</td><td>48 Tokens</td><td>32 Tokens</td></tr><tr><td colspan="5">MATH-500</td></tr><tr><td>Verbal CoT (SFT+RL)</td><td>92.6</td><td>84.8</td><td>84.0</td><td>80.9</td></tr><tr><td>Abstract-CoT (PI-3+RL, M=64)</td><td>90.8</td><td>87.1</td><td>86.4</td><td>84.6</td></tr><tr><td colspan="5">AlpacaEval</td></tr><tr><td>Verbal CoT (SFT+RL)</td><td>58.4</td><td>55.2</td><td>54.7</td><td>53.4</td></tr><tr><td>Abstract-CoT (PI-3+RL, M=64)</td><td>60.6</td><td>57.0</td><td>56.1</td><td>55.5</td></tr><tr><td colspan="5">HotpotQA</td></tr><tr><td>Verbal CoT (SFT+RL)</td><td>58.1</td><td>53.1</td><td>52.8</td><td>51.0</td></tr><tr><td>Abstract-CoT (PI-3+RL, M=64)</td><td>58.6</td><td>54.8</td><td>54.0</td><td>52.4</td></tr></table>

Table 5: Truncation sensitivity across benchmarks for Qwen3-8B. “Normal” denotes the untruncated setting. For verbal CoT, truncation is applied to the natural-language chain-ofthought; for Abstract-CoT, truncation is applied to the abstract trace.

The key findings noted in Section 4.3 are reflected across benchmarks: both methods clearly decrease, with a similar amount on AlpacaEval and HotpotQA, while there is a sizable discrepancy with MATH-500. AlpacaEval has the smallest drop due to having the fewest thinking tokens and more response tokens to start, as reflected in Table 1. Notably, the smoothness of degradation with Verbal CoT appears to be consistent with the number of thinking tokens produced. Benchmarks like MATH-500 with more tokens saw a sharper drop, whereas AlpacaEval had a smaller decline, with HotpotQA in between.

### A.4 Permutation Testing Analysis

As discussed in Section 4.3, we conducted a permutation analysis to study the behavior of Abstract-CoT compared to Verbal CoT in its compositional power induced through RL. Recall that while the warm-up phase is intended to learn embeddings corresponding to the new abstract vocabulary, the RL phase is designed to learn sequences of abstract tokens that result in high-quality responses, as determined by a generative reward model. To this end, learning to effectively use the abstract vocabulary through constrained decoding should make the model more sensitive to CoT perturbations, making it less permutation-invariant.

For each prompt in the evaluation set, we first generate a {Verbal, Abstract} CoT. Then, for verbal CoT experiments, we randomly permute the steps in the CoT based on the newline delimiter, and then induce the model to produce a response. For Abstract-CoT, we randomly permute the tokens in the generated sequence, given the absence of such delimiters therein.

The complete set of results across MATH-500, AlpacaEval, and HotpotQA is included in Table 6. All 3 benchmarks exhibit a similar trend: both methods clearly decrease with permuted CoT, and the verbal CoT degrades by more than Abstract-CoT, but Abstract-CoT is still affected by a substantial amount. Consistent with the intuition above, RL training leads to greater degradation due to learning token sequences that produce better responses, and augmenting the CoT muddles the context, resulting in worse generations. Encouragingly, this appears to be reflected in Abstract-CoT, suggesting that further scaling training improves the model’s ability to use the abstract vocabulary, leading to behavior resembling natural language even more closely.

<table><tr><td>Method</td><td>Direct</td><td>Permuted</td><td>Change (Δ)</td></tr><tr><td colspan="4">MATH-500</td></tr><tr><td>Verbal CoT (SFT)</td><td>89.8</td><td>81.8</td><td>-8.0</td></tr><tr><td>Verbal CoT (SFT+RL)</td><td>92.6</td><td>81.6</td><td>-11.0</td></tr><tr><td>Abstract-CoT (PI-3)</td><td>87.4</td><td>83.2</td><td>-4.2</td></tr><tr><td>Abstract-CoT (PI-3+RL)</td><td>90.6</td><td>82.8</td><td>-7.8</td></tr><tr><td colspan="4">AlpacaEval</td></tr><tr><td>Verbal CoT (SFT)</td><td>57.0</td><td>51.9</td><td>-5.1</td></tr><tr><td>Verbal CoT (SFT+RL)</td><td>58.4</td><td>50.4</td><td>-8.0</td></tr><tr><td>Abstract-CoT (PI-3)</td><td>55.6</td><td>51.9</td><td>-3.7</td></tr><tr><td>Abstract-CoT (PI-3+RL)</td><td>60.3</td><td>54.3</td><td>-6.0</td></tr><tr><td colspan="4">HotpotQA</td></tr><tr><td>Verbal CoT (SFT)</td><td>54.8</td><td>48.7</td><td>-6.1</td></tr><tr><td>Verbal CoT (SFT+RL)</td><td>58.1</td><td>47.6</td><td>-10.5</td></tr><tr><td>Abstract-CoT (PI-3)</td><td>53.3</td><td>48.0</td><td>-5.3</td></tr><tr><td>Abstract-CoT (PI-3+RL)</td><td>57.9</td><td>49.2</td><td>-8.7</td></tr></table>

Table 6: Permutation ablation on Qwen3-8B. For verbal CoT, we use turn-level permutation; for Abstract-CoT, we use fully random token permutation.

