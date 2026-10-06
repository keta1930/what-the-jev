# G Data, Experiments, and Reproducibility

We release 1,403,520 attempts across repeated mathematics, signal-rich mathematics, and field-balanced SuperGPQA, with 80 attempts per model–question pair. Table 3 shows that the 3,600-question field-balanced SuperGPQA collection accounts for most released attempts, whereas the two mathematics collections cover 306 questions across nine tasks, so the aggregate release count combines collections with very diferent question and task coverage. A response is one model completion, and a bank comprises the responses from one model configuration on a fixed question set.

<table><tr><td>Collection</td><td>Model cfgs.</td><td>Tasks</td><td>Questions</td><td>Attempts</td></tr><tr><td>Repeated mathematics</td><td>20</td><td>4</td><td>120</td><td>192,000</td></tr><tr><td>Signal-rich mathematics</td><td>4</td><td>5</td><td>186</td><td>59,520</td></tr><tr><td>Field-balanced SuperGPQA</td><td>4</td><td>1</td><td>3,600</td><td>1,152,000</td></tr><tr><td>Total</td><td>-</td><td>-</td><td>-</td><td>1,403,520</td></tr></table>

Table 3: Coverage of the public response collections.

## G.1 Data sources

Across the benchmark sources in Table 4, question-set scale ranges from 30-question competition sets to 12,032 MMLU-Pro questions; the block-level estimates therefore rest on markedly diferent numbers of questions.

<table><tr><td>Block</td><td>Source</td><td>Questions</td></tr><tr><td>Broad</td><td>MMLU-Pro (TIGER-Lab, 2024; Wang et al., 2024)</td><td>12,032</td></tr><tr><td>Broad</td><td>BBH (SaylorTwift, 2024; Suzgun et al., 2023)</td><td>6,511</td></tr><tr><td>Repeated math</td><td>AIME&#x27;24 (Jia, 2024)</td><td>30</td></tr><tr><td>Repeated math</td><td>AIME&#x27;25 (Zhang &amp; Math-AI, 2025)</td><td>30</td></tr><tr><td>Repeated math</td><td>HMMT&#x27;25 (MathArena, 2025c)</td><td>30</td></tr><tr><td>Repeated math</td><td>BrUMO&#x27;25 (MathArena, 2025a)</td><td>30</td></tr><tr><td>Signal-rich math</td><td>Five MathArena-hosted sets</td><td>186</td></tr><tr><td>Broad extension</td><td>SuperGPQA (M-A-P Team, 2025; M-A-P et al., 2025)</td><td>3,600</td></tr></table>

Table 4: Question sources and sizes.

The signal-rich study combines all 186 questions from AIME’26, HMMT Feb.’26, HMMT Nov.’25, CMIMC’25, and SMT’25 (MathArena, 2026a;b; 2025d;b;e). Its results use our evaluation protocol.

## G.2 Metrics, reducers, and uncertainty

For a question with N responses, let c be the number marked correct by the benchmark adapter. The exact without-replacement coordinates used throughout are

$$
\text {Pass@} k = 1 - \frac {\binom {N - c} {k}}{\binom {N} {k}}, \qquad \qquad \text {pass} ^ {k} = \frac {\binom {c} {k}}{\binom {N} {k}}.\tag{9}
$$

The first asks whether a size-k subset contains at least one correct candidate; the second asks whether every candidate in that subset is correct. They describe a bank and do not specify which response a system submits.

We evaluate submitted-answer accuracy by replaying reducers on subsets of the same bank. Budgets are $k \in \{ 1 , 2 , 4 , 8 , 1 6 , 3 2 , 6 4 , 8 0 \}$ . A counter-derived seed gives each question a reproducible random permutation, and prefixes form nested uniform subsets without replacement. In the 20-configuration study we enumerate all 80 singleton choices and use 200 paired subset replays for each $k > 1$ . The signal-rich mathematics study uses 2,000 replays for $1 < k < 8 0$ , an exact average over all singletons at $k = 1$ , and the full bank at $k = 8 0$ Ties are resolved by the earliest candidate in the seeded random order. A reducer’s $k = 8 0$ value is therefore exact conditional on that fixed tie-breaking order, not an average over every possible permutation.

The reported intervals resample questions after integrating over subset replays. Experiment 2 uses 2,000 percentile bootstrap replicates; the signal-rich mathematics analysis uses 10,000. These intervals are conditional on the observed 80-response banks. They measure sensitivity to the question composition, not the additional variability that would arise from generating a new bank. Pooled summaries are item-weighted micro-averages. For SuperGPQA, field-balanced summaries give each of the 72 constructed fields equal weight because every field contributes 50 questions.

The available signals constrain which analyses a bank supports: Table 5 maps each diagnostic or reducer to its required inputs and distinguishes reference-free reducers from Compass Best-of-N, which requires a benchmark reference and is used only diagnostically.

<table><tr><td>Reducer or statistic</td><td>Required signals</td><td>Interpretation</td></tr><tr><td>Pass@k, passk</td><td>Binary outcome</td><td>Exact bank diagnostic</td></tr><tr><td>String plurality</td><td>Extracted answer</td><td>Deployable terminal reducer; literal strings</td></tr><tr><td>Sequence/mean log probability</td><td>Chosen-token log probabilities</td><td>Deployable confidence heuristic</td></tr><tr><td>Normalized-likelihood vote</td><td>Answer string and response likelihood</td><td>Deployable weighted terminal vote</td></tr><tr><td>Pointwise Best-of-N</td><td>Reference-free Qwen score</td><td>Deployable after paying verifier cost</td></tr><tr><td>Compass Best-of-N</td><td>Question, reference, and candidate</td><td>Reference-assisted diagnostic only</td></tr></table>

Table 5: Inputs and roles of the reported analyses. “Deployable” here means that the reducer does not require a benchmark reference answer; its compute is still additional to candidate generation.

## G.3 Broad knowledge and symbolic reasoning

Protocol. The broad block evaluates 27 model configurations on all 12,032 MMLU-Pro and 6,511 BBH questions (Wang et al., 2024; Suzgun et al., 2023). MMLU-Pro uses final-option exact match, whereas BBH uses its flexible extractor.

Generation is zero-shot, with temperature 0.6, $\mathrm { t o p } { - } p = 0 . 9 5$ , frequency penalty 0.1, a 32,768-token cap, and a fixed seed.

Response counts. The 27 configurations produce 500,661 responses across the two suites. This block lacks token-level probabilities and structured finish reasons, so it supports neither likelihood-based reducers nor reliable termination analysis. The configuration orderings in Table 6 difer between MMLU-Pro and BBH, so the suite-specific exact-match columns are retained as separate descriptive results rather than pooled into one ranking.

<table><tr><td>Configuration</td><td>MMLU-Pro</td><td>BBH</td></tr><tr><td>Bespoke-Stratos-32B</td><td>67.37</td><td>75.41</td></tr><tr><td>Bespoke-Stratos-7B</td><td>46.68</td><td>51.50</td></tr><tr><td>DeepSeek-R1-Distill-Llama-8B</td><td>29.42</td><td>64.57</td></tr><tr><td>DeepSeek-R1-Distill-Qwen-1.5B</td><td>3.13</td><td>25.97</td></tr><tr><td>DeepSeek-R1-Distill-Qwen-14B</td><td>48.85</td><td>77.88</td></tr><tr><td>DeepSeek-R1-Distill-Qwen-32B</td><td>46.02</td><td>81.68</td></tr><tr><td>DeepSeek-R1-Distill-Qwen-7B</td><td>6.68</td><td>53.11</td></tr><tr><td>FuseO1-DeepSeekR1-QwQ-32B-Preview</td><td>45.05</td><td>81.22</td></tr><tr><td>FuseO1-DeepSeekR1-QwQ-SkyT1-32B-Preview</td><td>44.96</td><td>82.20</td></tr><tr><td>FuseO1-DeepSeekR1-QwQ-SkyT1-Flash-32B-Preview</td><td>44.52</td><td>81.45</td></tr><tr><td>FuseO1-DeepSeekR1-Qwen2.5-Instruct-32B-Preview</td><td>46.62</td><td>82.14</td></tr><tr><td>LIMO</td><td>65.61</td><td>74.41</td></tr><tr><td>Light-R1-14B-DS</td><td>38.23</td><td>74.09</td></tr><tr><td>Light-R1-32B</td><td>55.60</td><td>74.44</td></tr><tr><td>Light-R1-7B-DS</td><td>7.68</td><td>54.57</td></tr><tr><td>OlympicCoder-32B</td><td>50.78</td><td>57.79</td></tr><tr><td>OlympicCoder-7B</td><td>40.88</td><td>56.89</td></tr><tr><td>OpenR1-Qwen-7B</td><td>15.97</td><td>31.45</td></tr><tr><td>OpenThinker-32B</td><td>66.62</td><td>75.26</td></tr><tr><td>OpenThinker-7B</td><td>47.45</td><td>52.22</td></tr><tr><td>QwQ-32B</td><td>70.47</td><td>58.45</td></tr><tr><td>Qwen2.5-32B-Instruct</td><td>67.10</td><td>56.52</td></tr><tr><td>Sky-T1-32B-Flash</td><td>60.29</td><td>79.14</td></tr><tr><td>Sky-T1-32B-Preview</td><td>59.48</td><td>79.67</td></tr><tr><td>Sky-T1-7B</td><td>15.08</td><td>39.35</td></tr><tr><td>TinyR1-32B-Preview</td><td>58.32</td><td>77.39</td></tr><tr><td>s1.1-32B</td><td>64.23</td><td>41.48</td></tr></table>

Table 6: Broad-block exact match in percent. BBH uses its flexible extractor. The columns are separate descriptive results and are not averaged.

Empty BBH extractions remain in the denominator and are scored incorrect.

## G.4 Twenty configurations on 2024–2025 mathematics

Grid and models. The four sets are AIME’24, AIME’25, HMMT’25, and BrUMO’25, with 30 questions each. HMMT’25 and BrUMO’25 are distributed through MathArena, but the four-set combination is not itself a MathArena benchmark. Twenty configurations generate 80 responses for each of 120 questions, yielding 192,000 responses.

Generation. Generation uses temperature 0.6, top-p = 0.95, one completion, and a 32,768-token cap. Realized-token log probabilities and ranks are available at every generation position, but full next-token distributions are not. These signals support sequence-likelihood, mean-log-probability, and realized-rank summaries, but not entropy or other full-distribution methods. All non-gpt-oss configurations use the common boxed-answer instruction. Within the three gpt-oss efort configurations, that instruction is present for 80% of the AIME’24 and AIME’25 attempts and absent from the BrUMO’25 and HMMT’25 attempts. Comparisons involving these configurations therefore combine model, task, and prompt-interface diferences.

CompassVerifier-7B. CompassVerifier-7B assigns an outcome score whose $\mathrm { A / B / C }$ labels mean correct, incorrect, and invalid (Liu et al., 2025c); we use the probability assigned to A. Scores or parsed answers that are unavailable are excluded without imputation. Because the verifier sees the gold answer, we use it only as a reference-assisted diagnostic.

<table><tr><td>Configuration</td><td>Acc.@1</td><td>Pass@8</td><td>Pass@80</td></tr><tr><td>Qwen3-30B-A3B-Thinking-2507</td><td>75.56</td><td>85.83</td><td>91.67</td></tr><tr><td>Qwen3-4B-Thinking-2507</td><td>66.55</td><td>80.40</td><td>87.50</td></tr><tr><td>Phi-4-reasoning-plus</td><td>65.56</td><td>84.19</td><td>91.67</td></tr><tr><td>gpt-oss-20b high</td><td>63.99</td><td>83.94</td><td>90.83</td></tr><tr><td>gpt-oss-20b medium</td><td>63.65</td><td>86.49</td><td>93.33</td></tr><tr><td>AceReason-Nemotron-1.1-7B</td><td>60.74</td><td>74.70</td><td>80.83</td></tr><tr><td>Phi-4-reasoning</td><td>59.97</td><td>82.81</td><td>90.83</td></tr><tr><td>OpenThinker2-32B</td><td>59.75</td><td>76.77</td><td>82.50</td></tr><tr><td>FuseO1-DeepSeekR1-QwQ-SkyT1-Flash-32B-Preview</td><td>58.52</td><td>74.05</td><td>81.67</td></tr><tr><td>Light-R1-14B-DS</td><td>58.27</td><td>74.09</td><td>81.67</td></tr><tr><td>NVIDIA-Nemotron-Nano-9B-v2</td><td>54.72</td><td>72.12</td><td>79.17</td></tr><tr><td>LIMO-v2</td><td>53.45</td><td>73.33</td><td>82.50</td></tr><tr><td>gpt-oss-20b low</td><td>47.39</td><td>72.39</td><td>85.00</td></tr><tr><td>EXAONE-4.0-1.2B</td><td>44.29</td><td>67.78</td><td>83.33</td></tr><tr><td>OpenR1-Distill-7B</td><td>43.68</td><td>65.66</td><td>78.33</td></tr><tr><td>OpenThinker3-1.5B</td><td>43.38</td><td>62.13</td><td>75.00</td></tr><tr><td>OpenReasoning-Nemotron-1.5B</td><td>40.73</td><td>62.07</td><td>78.33</td></tr><tr><td>DeepSeek-R1-Distill-Qwen-1.5B</td><td>25.30</td><td>47.47</td><td>64.17</td></tr><tr><td>Sky-T1-32B-Flash</td><td>25.27</td><td>43.95</td><td>55.83</td></tr><tr><td>Bespoke-Stratos-7B</td><td>18.39</td><td>36.22</td><td>54.17</td></tr></table>

Table 7: Complete fixed-roster results for the 2024–2025 mathematics block, in percent. Acc.@1 averages the 80 response outcomes per question; Pass@k is the exact without-replacement discovery statistic.

Across the complete roster in Table 7, Pass@80 exceeds Acc.@1, the mean single-response accuracy, for every configuration; the full-bank discovery statistic nevertheless does not define submitted-answer accuracy.

<table><tr><td>Qwen3-30B-A3B-Thinking-2507</td><td>k=1</td><td>k=8</td><td>k=80</td></tr><tr><td>Pass@k</td><td>75.56</td><td>85.83</td><td>91.67</td></tr><tr><td>passk</td><td>75.56</td><td>61.50</td><td>43.33</td></tr><tr><td>String plurality</td><td>75.56</td><td>77.74</td><td>78.33</td></tr><tr><td>Sequence-log-probability Best-of-N</td><td>75.56</td><td>78.45</td><td>77.50</td></tr><tr><td>Mean-log-probability Best-of-N</td><td>75.56</td><td>74.56</td><td>65.83</td></tr><tr><td>Compass Best-of-N (reference-assisted)</td><td>75.51</td><td>84.23</td><td>89.17</td></tr></table>

Table 8: Selected repeated-mathematics results in percent, pooled over 120 questions. The k = 1 reducer values enumerate all singletons; k = 8 uses 200 paired subset replays; $k = 8 0$ is the full bank. Negative perplexity is identical to mean-log-probability selection.

For Qwen3-30B-A3B-Thinking-2507, Table 8 shows an availability–selection gap at k = 80: Pass@80 is 91.67%, whereas the best deployable terminal reducer shown, string plurality, reaches 78.33%. The leading configuration’s Acc.@1 has a 95% prompt-bootstrap interval of [68.81, 82.18]. Across the 20 configurations, the mean Spearman correlation between subset and full-bank accuracy rankings is 0.967 at k = 1 and 0.992 at $k = 8$ . This stability describes the present roster; it is not a general sample-size guarantee.

## G.5 Signal-rich competition mathematics

Generators and prompts. The generators are Qwen3.6-35B-A3B and gpt-oss-20b (Qwen Team, 2026; OpenAI, 2025b). Each receives the problem in a zero-shot prompt that requests step-by-step reasoning and a boxed final answer; no reference or evaluator signal is shown. Boxed answers are checked for numeric or symbolic equivalence (ModelScope Team, 2024).

Qwen uses temperature 1, top-p = 0.95, top-k = 20, and presence penalty 1.5. GPT-OSS uses temperature 1, top-p = 1, no top-k truncation, and no presence penalty. Both use one completion and an 81,920-token generation cap.

Efective efort and sampling. Each model–efort condition contains 186 × 80 = 14,880 responses. The four analyzed banks are Qwen and gpt-oss at low, medium, and high efort. Three additional gpt-oss runs used medium efort and serve only as diagnostics; they are not pooled with the analyzed medium bank. Their Acc.@1 values range from 63.08% to 63.47%, compared with 62.80% for the analyzed medium bank.

Token-level signals. We observe realized-token log probabilities and ranks and at most 20 alternatives per completion step. Ranks and probability mass beyond the first 20 alternatives are unavailable, and the recorded probabilities precede decoding penalties and truncation.

## G.6 Verifier implementations and diagnostics

CompassVerifier scores final-answer outcomes with access to the reference answer. The pointwise Qwen evaluator instead scores problem understanding, reasoning validity, and conclusion support without a reference; its score is used for reference-free Best-of-N (Table 9).

<table><tr><td></td><td>CompassVerifier-3B (OpenCompass)</td><td>Pointwise Qwen adaptation</td></tr><tr><td>Input</td><td>Problem, reference answer, candidate response</td><td>Problem and one candidate response; no reference or other candidate</td></tr><tr><td>Judgment</td><td>A/B/C final-answer outcome; reasoning explicitly ignored</td><td>Problem understanding, reasoning validity, and conclusion support</td></tr><tr><td>Score</td><td>Direct A/B/C softmax; null-adjusted contextual A/B/C softmax</td><td>Expected A-T ordinal score per criterion, then mean</td></tr><tr><td>Role</td><td>Reference-assisted outcome diagnostic</td><td>Reference-free Best-of-N evidence</td></tr><tr><td>Main caveat</td><td>Gold access and neither distribution is calibrated</td><td>Ordinal, not calibrated; Qwen evaluates its own Qwen traces</td></tr></table>

Table 9: The two verifier pipelines. The pointwise pipeline is inspired by LLM-as-a-Verifier (Kwok et al., 2026) but is not its pairwise tournament. CompassVerifier follows the released outcome-verifier prompt and scoring formulation (Liu et al., 2025c).

CompassVerifier-3B (OpenCompass). The oficial prompt supplies the problem, standard answer, and candidate. It asks for A (correct), B (incorrect), or C (invalid), instructs the verifier to compare final answers, and explicitly says to ignore errors in the reasoning when the final answer is correct (Liu et al., 2025c). From the label log probabilities $( \ell _ { A } , \ell _ { B } , \ell _ { C } )$ , the direct score is

$$
p _ {\mathrm{direct}} (z) = \mathrm{softmax} _ {z \in \{A, B, C \}} (\ell_ {z}).
$$

The contextual variant subtracts a null-prompt baseline before normalizing; let $\ell _ { z } ^ { \mathrm { s l o t } }$ and $\ell _ { z } ^ { \mathrm { n u l l } }$ denote the label log probabilities under the populated and null prompts:

$$
p _ {\mathrm{ctx}} (z) = \operatorname{softmax} _ {z \in \{A, B, C \}} \left(\frac {\ell_ {z} ^ {\mathrm{slot}} - \ell_ {z} ^ {\mathrm{null}}}{1 . 5}\right).
$$

This adjustment is a diagnostic used by our pipeline; it is not a calibrated correctness probability or the production label of CompassVerifier.

For inputs exceeding the context window, only the middle of the candidate is shortened, preserving its prefix and sufix as well as the question and reference.

Reference-free pointwise Qwen evaluator. The corpus-wide score adapts the expected-score idea of LLM-as-a-Verifier to one candidate at a time (Kwok et al., 2026). Qwen critiques problem understanding, reasoning validity, and conclusion support, then assigns an A–T ordinal distribution to each criterion. Unlike the cited pairwise method, this evaluator ranks candidates directly without a tournament or Bradley–Terry aggregation.

Let $q _ { j } ( L )$ be the resulting distribution for criterion $j ,$ with $v ( A ) = 2 0 , \ldots , v ( T ) = 1$ . We compute

$$
r _ {j} = \frac {\sum_ {L = A} ^ {T} q _ {j} (L) v (L) - 1}{1 9}, \qquad s _ {\mathrm{point}} = \frac {1}{3} \sum_ {j = 1} ^ {3} r _ {j}.
$$

The score is in [0, 1], but the construction is ordinal rather than probabilistic calibration, and low-mass letters may be censored by the returned token probabilities. Qwen judging Qwen-generated responses is self evaluation; judging gpt-oss responses is cross-model evaluation. The reported selection curves and intervals condition on the observed verifier scores and do not include evaluator-rerun variability.

Verifier signals on 104,160 MathArena-sourced competition-math traces  
![](images/88d3ba97e6615d2a53d37f8e8bae1d78c61f2770e82cbc5cf243e5495fc6b490.jpg)

[Image: The image displays six plots evaluating model verifiers and generators across three different scoring contexts. The top row (panels a-c) presents conditional empirical Cumulative Distribution Functions (CDFs) for 'Incorrect' (orange) versus 'Correct' (green) traces, reporting AUC scores of 0.983 for Compass direct A, 0.977 for Compass contextual A, and 0.871 for the pointwise rubric score. The bottom row (panels d-f) plots Empirical exact-rule accuracy against mean score bins in equal-count bins for two generators: Qwen3.6 (blue) and gpt-oss (yellow). While all scenarios show a positive correlation between score and accuracy, panel (d) and (e) demonstrate that the Qwen3.6 generator achieves higher exact-rule accuracy at lower mean scores compared to gpt-oss, whereas panel (f) shows both models converging near perfect accuracy as scores approach 1.0.]  
Figure 7: Verifier signals against the independent rule-based outcome on 104,160 competitionmath traces. The figure compares direct and contextual Compass A scores with the reference-free pointwise Qwen score through conditional distributions and equal-count score bins. The lower panels separate Qwen-generated self-evaluations from gpt-oss cross-model evaluations. Compass sees the reference answer; pointwise Qwen does not. The binned empirical correctness curves describe ranking behavior on this fixed response set and should not be interpreted as calibration guarantees.

Against the rule-based outcome, the descriptive trace-level ROC AUC is 0.983 for direct Compass A, 0.977 for contextual Compass A, and 0.871 for the pointwise score. The pointwise AUC is 0.744 on Qwen-generated traces and 0.876 on gpt-oss traces. This split does not identify a causal self-evaluation efect because the generator families also difer in prompts, output distributions, and base accuracy. A pooled AUC would conceal the observed diference between generators.

Scaling results. Table 10 reports the four canonical banks. String plurality groups literal extracted strings rather than mathematically equivalent forms. Pointwise Best-of-N uses only the reference-free score; Compass scores are excluded from these deployed-selection results.

<table><tr><td>Canonical bank</td><td>Acc.@1</td><td>Pass@8</td><td>Pass@80</td><td>Str.-Plur.@80</td><td>Pnt.-BoN@80</td><td>Caps</td></tr><tr><td>Qwen3.6</td><td>83.12</td><td>91.70</td><td>94.62</td><td>89.25</td><td>86.56</td><td>675</td></tr><tr><td>gpt-oss low</td><td>32.90</td><td>56.14</td><td>72.58</td><td>45.70</td><td>58.06</td><td>0</td></tr><tr><td>gpt-oss medium</td><td>62.80</td><td>85.99</td><td>91.94</td><td>80.11</td><td>75.81</td><td>32</td></tr><tr><td>gpt-oss high</td><td>73.03</td><td>88.12</td><td>93.55</td><td>85.48</td><td>81.72</td><td>2,399</td></tr></table>

Table 10: Finite-bank and shared-bank results on the 186 MathArena-sourced competition questions, in percent. Caps count responses that reach 81,920 tokens out of 14,880. Pnt.-BoN is pointwise Best-of-N.

At k = 80, the 95% prompt-bootstrap intervals for Pass@80 are [90.86, 97.85], [66.13, 79.03], [87.63, 95.70], and [89.78, 96.77] in table order. Pointwise Best-of-N intervals are [81.72, 91.40], [51.08, 65.05], [69.35, 81.72], and [75.81, 87.10]. Several intervals overlap. Mean completion counts per response are 34,382 tokens for Qwen and 1,781, 12,341, and 37,264 for gpt-oss low, medium, and high. These costs exclude prompt tokens and verifier computation. The high-efort cap rate is 16.12%, so the efort comparison is inseparable from the shared length limit.

## G.7 Field-balanced SuperGPQA extension

SuperGPQA contains 26,529 multiple-choice questions across 285 graduate disciplines (M-A-P et al., 2025). Our 3,600-question sample includes 50 items from each of 72 EvalScope fields, preventing large fields from dominating the result (ModelScope Team, 2024). The zero-shot prompt requests step-by-step reasoning and a final option letter, which is extracted for binary scoring. The four generation banks are Qwen3.6 and gpt-oss at low, medium, and high efort, with 80 responses per question. Sampling and verification follow the signal-rich mathematics protocol. The pointwise rubric is generalized to factual or technical accuracy, logical coherence, and completeness. Together, the four banks contain 3,600 × 4 × 80 = 1,152,000 responses.

For the gpt-oss high bank, the 288,000 responses have mean accuracy 45.03%. Exact Pass@80 is 81.94%, while pass<sup>80</sup> is 9.47%. Of the 3,600 questions, 650 are never answered correctly and 341 are answered correctly in all 80 responses. Field-level response accuracy ranges from 21.33% in Aquaculture to 76.78% in Mathematics. Figure 8 reports finite-bank scaling and field variation from the 3,600 by 80 binary matrix. These values are descriptive of the equal-field construction, not estimates under SuperGPQA’s original field frequencies.

(a) Exact finite-bank scaling  
![](images/ecc878c3112dc130e5f87c244d7ee22c46033dd57b4366f86bf183874f3c60ff.jpg)

[Image: This line chart illustrates exact finite bank scaling, plotting the fraction of questions on the y-axis against the sample budget, k, on a logarithmic x-axis ranging from 1 to 80. The blue data series, labeled "Pass@k", exhibits an upward trend starting at approximately 45% and reaching just over 80% at k=80. The orange data series, labeled "All-correct@k", follows a downward trajectory from the same starting point of roughly 45% down to approximately 10% at k=80.]

(b) Heterogeneity across 72 fields  
![](images/0c0e2b7007e962b6c58b55be1727d5d326db73ba869c5d309dae38b34649a452.jpg)

[Image: This scatter plot displays performance metrics for 72 distinct fields, plotting 'Single-sample accuracy' on the horizontal axis against 'Pass@80' on the vertical axis. Each data point represents a field, with its color corresponding to the 'All-correct@80' percentage shown on the vertical color bar to the right, ranging from dark purple to yellow. Annotated points highlight specific domains such as Mathematics in the top right corner with high scores on both axes, and Chemistry near the bottom center with lower Pass@80 values relative to its single-sample accuracy. A dashed diagonal line extends upwards from the bottom right area of the graph.]  
GPT-high; EvalScope rule correctness only. Shading: 95% prompt bootstrap interval.

Figure 8: SuperGPQA scaling and field heterogeneity for the gpt-oss high bank. The left panel gives exact finite-bank discovery and stability over 3,600 questions. In the right panel, each point is one of 72 equally sized fields: the axes compare single-response accuracy with Pass@80, and color shows the all-correct@80 coordinate. This figure uses only the rule-based correctness matrices; it does not substitute an LLM verifier for the benchmark outcome.