# 4. Experiments

## 4.1. Basic Setups (Details in Appendix A)

We apply the proposed MCP-Persona benchmark to diverse LLM agents for comparative evaluation. We report three metrics. (1) Checkpoint Accuracy (Acc) is defined as the average checkpoint score within a task, where each checkpoint is scored by the LLM judge. (2) Success Rate at 0.8 (SR-0.8) measures the proportion of tasks whose Acc exceed 0.8. (3) Execution Accuracy (Exec-Acc) is defined as the average executor-verified checkpoint correctness over all human-specified execution steps within a task. All columns except the last three under Overall report Acc in Table 3.

Our benchmark includes two types of tasks: Single-Server tasks, which use tools from one personalized server, and Cross-Server tasks, which require coordinating tools across multiple personalized servers. In both settings, tool chains may also include information-seeking servers such as Amap.

Table 3. Performance of LLM agents on MCP-Persona. We report Acc except for the last two columns. The results highlight a significant challenge: even leading models struggle, achieving less than 50% accuracy, with Claude-Sonnet-4.5 delivering the best performance.

<table><tr><td rowspan="2">Model</td><td colspan="4">Single-Server</td><td colspan="3">Cross-Server</td><td colspan="3">Overall</td></tr><tr><td>Collaboration Platform</td><td>Content Management</td><td>Social Media</td><td>Email</td><td>Lark-Centric</td><td>Rednote -Centric</td><td>Hodgepodge</td><td>Acc</td><td>SR-0.8</td><td>Exec-Acc</td></tr><tr><td colspan="11">Proprietary Models</td></tr><tr><td>A\ Claude-Sonnet-4.5</td><td>39.94</td><td>19.76</td><td>47.04</td><td>43.63</td><td>40.81</td><td>42.37</td><td>12.50</td><td>38.66</td><td>10.40</td><td>41.50</td></tr><tr><td>GPT-5</td><td>43.50</td><td>22.57</td><td>42.64</td><td>47.17</td><td>37.67</td><td>34.66</td><td>12.50</td><td>36.99</td><td>6.94</td><td>41.45</td></tr><tr><td>A\ Claude-Opus-4.1</td><td>38.79</td><td>13.56</td><td>44.79</td><td>9.71</td><td>39.67</td><td>34.70</td><td>25.00</td><td>34.52</td><td>7.05</td><td>36.77</td></tr><tr><td>o4-mini</td><td>34.38</td><td>21.22</td><td>35.61</td><td>53.83</td><td>30.43</td><td>25.25</td><td>6.25</td><td>30.70</td><td>5.78</td><td>34.73</td></tr><tr><td>o3</td><td>26.41</td><td>14.55</td><td>32.78</td><td>41.08</td><td>34.64</td><td>26.05</td><td>37.50</td><td>29.79</td><td>5.20</td><td>30.27</td></tr><tr><td>GPT-4o</td><td>24.50</td><td>7.58</td><td>36.98</td><td>12.57</td><td>30.65</td><td>20.29</td><td>25.00</td><td>25.56</td><td>4.35</td><td>20.02</td></tr><tr><td>G Grok-4</td><td>17.80</td><td>11.82</td><td>39.43</td><td>5.71</td><td>26.78</td><td>19.79</td><td>37.50</td><td>24.58</td><td>6.68</td><td>22.49</td></tr><tr><td>Gemini-3-Pro</td><td>14.01</td><td>11.03</td><td>23.38</td><td>36.92</td><td>14.60</td><td>22.05</td><td>6.25</td><td>16.91</td><td>1.79</td><td>5.78</td></tr><tr><td>Gemini-2.5-Pro</td><td>22.58</td><td>22.24</td><td>26.22</td><td>20.92</td><td>18.23</td><td>11.76</td><td>6.25</td><td>20.68</td><td>0.66</td><td>13.38</td></tr><tr><td colspan="11">Open-Source Models</td></tr><tr><td>Qwen3-Max-Latest</td><td>24.36</td><td>11.67</td><td>47.98</td><td>11.71</td><td>30.95</td><td>15.79</td><td>18.75</td><td>27.54</td><td>5.75</td><td>29.23</td></tr><tr><td>Qwen3-235B-A22B</td><td>23.55</td><td>12.12</td><td>40.05</td><td>13.71</td><td>30.40</td><td>19.25</td><td>31.25</td><td>26.75</td><td>4.07</td><td>21.83</td></tr><tr><td>DeepSeek-V3</td><td>19.22</td><td>11.48</td><td>38.35</td><td>30.79</td><td>27.91</td><td>18.89</td><td>18.75</td><td>25.29</td><td>3.47</td><td>27.52</td></tr><tr><td>Qwen3-Coder</td><td>23.50</td><td>13.18</td><td>31.34</td><td>8.29</td><td>29.80</td><td>23.57</td><td>6.25</td><td>23.93</td><td>3.65</td><td>20.14</td></tr></table>

Table 4. Comparison of simulation fidelity on the Lark Server (50 samples). Tool-Traverse aligns significantly better with real-world tool behaviors than the documentation-only Vanilla baseline. TP/TN: True Positive/Negative; FP/FN: False Positive/Negative.

<table><tr><td rowspan="2">Method</td><td colspan="4">Confusion Matrix</td><td colspan="4">Behavioral Alignment (%)</td><td colspan="4">Response Similarity</td></tr><tr><td>TP</td><td>TN</td><td>FP</td><td>FN</td><td>Acc</td><td>Prec</td><td>Rec</td><td>F1</td><td>TF-IDF</td><td>ROUGE</td><td>BLEU</td><td>METEOR</td></tr><tr><td>Vanilla</td><td>12</td><td>17</td><td>8</td><td>13</td><td>58.0</td><td>60.0</td><td>48.0</td><td>53.3</td><td>0.2113</td><td>0.2258</td><td>0.2307</td><td>0.3214</td></tr><tr><td>Tool-Traverse</td><td>23</td><td>24</td><td>1</td><td>2</td><td>94.0</td><td>95.8</td><td>92.0</td><td>93.8</td><td>0.7391</td><td>0.7366</td><td>0.7412</td><td>0.8703</td></tr></table>

## 4.2. Performance Comparison on MCP-Persona

Main Results. (1) Across servers and settings, SOTA LLM agents still show limited reliability on MCP-Persona as none achieved an accuracy exceeding 50% in either checkpoint or execution evaluations. (2) Performances vary by tool family on single-server scenarios and degrades further with richer context and longer-horizon coordination. These results reveal common failure modes in tool use and demonstrate that our benchmark is a useful testbed for evaluating and improving agent capabilities.

Single-Server Breakdown. (1) Email tasks achieve the highest accuracy for most models due to simple operations and short dependency chains. (2) Tasks involving richer schemas or heterogeneous objects, such as social media and collaboration platforms, are more challenging, as they require handling cross-user interactions and implicit entity resolution. (3) Content-management tools perform worst, reflecting agents’ limited robustness when navigating and editing long documents under extended context budget.

Cross-Server Breakdown. We evaluate three cross-server scenarios: Lark-Centric, Rednote-Centric, and a Hodgepodge scenario spanning arbitrary combinations of the available applications. The hodgepodge subset proves to be the most challenging, consistently yielding the lowest accuracy across most models. This difficulty is attributable to its higher frequency of cross-server interactions and more complex dependency chains.

Metric Comparison. Overall, Exec-Acc is slightly higher than Acc, suggesting that human-annotated execution checkpoints are less noisy than LLM-segmented checkpoints. SR@0.8 remains low, indicating extreme difficulty in completing tasks end-to-end.

## 4.3. Validation of Tool Simulation Fidelity

To justify the effectiveness of our Tool-Traverse paradigm described in Section 3.1, we quantitatively verify that our code-based simulated tools $\mathcal { T } _ { s i m }$ exhibit behaviors and responses indistinguishable from real-world tools $\mathcal { T } _ { r e a l }$

Setups and Context Reconstruction. We evaluate all 14 tools from Lark using 50 authentic interaction traces (25 successful, 25 failed). A critical challenge in simulation is ensuring state consistency; a simulator might fail simply because it lacks a specific entity (e.g., user id) present in the environment, not because of flawed logic. To eliminate this confounding variable, we employ a Context Reconstruction strategy: we reverse-engineer the exact pre-condition state from each real-world trace and inject it into the simulator. This guarantees that $\mathcal { T } _ { s i m }$ and $\mathcal { T } _ { r e a l }$ operate on the exact same state snapshot, ensuring a fair comparison based solely on execution logic. We compare our approach against a Vanilla baseline, which simulates tools relying only on documentation without behavioral traversal data.

Table 5. Comparison with and without skill documentations on the Lark and Rednote subsets.

<table><tr><td rowspan="3">Model</td><td colspan="6">Lark Subset</td><td colspan="6">Rednote Subset</td></tr><tr><td colspan="2">Vanilla</td><td colspan="2">+ OpenClaw Skills</td><td colspan="2">+ Our Skills</td><td colspan="2">No Skills</td><td colspan="2">+ OpenClaw Skills</td><td colspan="2">+ Our Skills</td></tr><tr><td>Acc</td><td>Exec-Acc</td><td>Acc</td><td>Exec-Acc</td><td>Acc</td><td>Exec-Acc</td><td>Acc</td><td>Exec-Acc</td><td>Acc</td><td>Exec-Acc</td><td>Acc</td><td>Exec-Acc</td></tr><tr><td>GPT-5</td><td>37.50</td><td>64.29</td><td>42.50</td><td>71.43</td><td>45.00</td><td>80.36</td><td>42.19</td><td>31.25</td><td>35.94</td><td>25.00</td><td>43.75</td><td>31.25</td></tr><tr><td>A\ Claude-Sonnet-4.5</td><td>27.70</td><td>69.64</td><td>29.70</td><td>73.21</td><td>33.00</td><td>78.57</td><td>31.25</td><td>18.75</td><td>28.13</td><td>17.19</td><td>28.13</td><td>15.63</td></tr><tr><td>DeepSeek-V3</td><td>20.80</td><td>22.50</td><td>15.00</td><td>42.86</td><td>16.60</td><td>49.60</td><td>26.56</td><td>7.81</td><td>28.13</td><td>23.44</td><td>31.25</td><td>23.44</td></tr><tr><td>Qwen3-235B-A22B</td><td>20.20</td><td>37.30</td><td>21.30</td><td>49.80</td><td>29.30</td><td>43.10</td><td>25.00</td><td>18.75</td><td>28.13</td><td>15.63</td><td>35.94</td><td>23.44</td></tr><tr><td>Kimi-K2.5</td><td>31.40</td><td>69.20</td><td>30.40</td><td>77.70</td><td>34.10</td><td>78.30</td><td>40.63</td><td>39.06</td><td>40.63</td><td>32.81</td><td>42.19</td><td>40.63</td></tr></table>

![](images/fb108edc2677a07dde8078ff2b25b0123f88f7f585fc4d685d662bd633c4cf84.jpg)

[Image: This scatter plot displays "Checkpoint-Based Accuracy (%)" on the y-axis against "Average Token per Task (Log Scaled)" on the x-axis for various large language models. The vertical axis ranges from 20 to 40 percent, while the horizontal axis uses a logarithmic scale ranging from $10^3$ to $10^5$ tokens. High-performing models like Qwen3.5-Plus, GPT-5.5, and Claude-Sonnet-4.5 cluster in the upper-left quadrant, achieving accuracies above 35% with fewer tokens, whereas models like Qwen3-235B-A22B and GPT-4o appear in the lower-right with lower accuracy and higher token consumption. Other models such as Gemini-2.5-Pro and Gemini-3.1-Pro are located at the bottom left with the lowest accuracy percentages shown.]  
(a) Average token per task.

![](images/8d7097dc9d4316ec7844d0a0ea5277e11fc610e7fd999491d0150952de142ffe.jpg)

[Image: This scatter plot illustrates the trade-off between "Checkpoint-Based Accuracy (%)" on the vertical axis and "Average Cost per Task ($ Log Scaled)" on the horizontal axis for multiple large language models. The x-axis uses a logarithmic scale ranging from $10^{-2}$ to $10^1$, while the y-axis measures accuracy percentage from roughly 23% to 40%. Models are plotted as labeled circles, showing a general trend where high-cost options like Claude-Opus-4.1 and Qwen3.5-Plus achieve higher accuracy, whereas low-cost models like Gemini-2.5-Pro and DeepSeek-V3 cluster in the lower-left area with reduced accuracy.]  
(b) Average cost (\$) per task.

![](images/53be88b642130f53d216c7873889b3c98d9e1ae2da3d38a2c5b84b59d67e1855.jpg)

[Image: This scatter plot charts Benchmark-Based Accuracy (%) against Average Steps per Task for various generative AI models. The vertical axis scales from 20% to 40% accuracy, while the horizontal axis measures steps from 0 to 12. GPT-5.5 is positioned at the top with the highest accuracy near 40% and roughly 7 steps, whereas Gemini-2.5-Pro is in the bottom-left corner with approximately 21% accuracy and less than 2 steps. The data reveals a general trend where higher accuracy often correlates with a higher number of steps, though outliers like DeepSeek-V3 achieve nearly 30% accuracy with only about 2.5 steps.]  
(c) Average step length per task.  
Figure 3. Analysis of efficiency and performance trade-offs across various models, based on average token count, cost, and step length.

Table 6. Ablation study on the candidate tool settings.

<table><tr><td rowspan="2">Model</td><td colspan="2">All Tools</td><td colspan="2">Selected Tools</td></tr><tr><td>Acc</td><td>Exec-Acc</td><td>Acc</td><td>Exec-Acc</td></tr><tr><td>GPT-5</td><td>41.04</td><td>29.25</td><td>40.46</td><td>46.23</td></tr><tr><td>Gemini-2.5-Pro</td><td>20.23</td><td>13.68</td><td>22.54</td><td>11.79</td></tr><tr><td>Qwen3.5-Plus</td><td>40.46</td><td>43.87</td><td>42.20</td><td>47.64</td></tr><tr><td>MiniMax-M2.5</td><td>32.37</td><td>34.43</td><td>36.42</td><td>38.21</td></tr><tr><td>Kimi-K2.5</td><td>36.99</td><td>38.21</td><td>39.88</td><td>37.26</td></tr></table>

Results. As shown in Table 4, (1) Tool-Traverse significantly outperforms the baseline on all metric families. The Vanilla baseline achieves only 53.3% F1, with a particularly high False Negative rate, indicating it struggles to handle valid but complex inputs due to hallucinated constraints. (2) On response similarity, Tool-Traverse roughly triples both TF-IDF and METEOR. These gaps directly reflect that the baseline emits generic error templates rather than the server’s specific error codes and formats, whereas Tool-Traverse faithfully reproduces the nested response structure, a prerequisite for downstream agent reasoning to remain stable when run against $\mathcal { T } _ { s i m }$ in place of $\mathcal { T } _ { r e a l }$

## 4.4. Ablation Study on Skills and Tool Candidates

We conduct additional experiments to validate whether skills enhance performance on MCP-Persona. Specifically, we compare the most downloaded OpenClaw skills obtained from ClawHub with a manually refined version (denoted as Our Skill). The skills are tailored for Lark and Rednote respectively, and are tested on their designated subsets. The refined version features more detailed descriptions of tool functionalities and parameters, thereby enabling the agent to leverage the available tools more effectively. The results are presented in Table 5. Overall, incorporating skill descriptions tends to improve agent performance. In particular, the manually refined skills further enhance performance compared with the OpenClaw version, although the magnitude of improvement varies across different models.

We also compare two tool candidate selection settings: (1) using all available tools and (2) using only tools from the ground-truth servers. As shown in Table 6, reducing the number of candidate tools improves performance, especially in cases with longer contexts.

## 4.5. Token and Cost Analysis

Figure 3 illustrates the relationship between monetary cost, token consumption, and checkpoint-based accuracy. Notably, Notably, GPT-5 stands out as the most cost-effective model, reaching 36.99 accuracy at only \$0.09 per task on average, while Qwen3-Plus delivers the best trade-off among open-source alternatives. The results reveal no clear correlation between spending and performance, suggesting that model selection should prioritize accuracy-cost trade-offs rather than raw resource investment.

Table 7. Correlation analysis between human and LLM judgments, with misaligned ratios broken down by subset. Ckpt: Checkpoint.

<table><tr><td>Task Category</td><td>Misaligned Ckpt</td><td>Total Ckpt</td><td>Ratio (%)</td><td>Task Category</td><td>Misaligned Ckpt</td><td>Total Ckpt</td><td>Ratio (%)</td></tr><tr><td>Lark_Short</td><td>2</td><td>20</td><td>10.00</td><td>Instagram</td><td>2</td><td>29</td><td>6.90</td></tr><tr><td>Lark_Long</td><td>4</td><td>79</td><td>5.06</td><td>Slack</td><td>6</td><td>53</td><td>11.32</td></tr><tr><td>Rednote_Short</td><td>2</td><td>17</td><td>11.76</td><td>Lark_Rednote</td><td>11</td><td>119</td><td>9.24</td></tr><tr><td>Rednote_Long</td><td>3</td><td>59</td><td>5.08</td><td>Lark_Obsidian</td><td>4</td><td>50</td><td>8.00</td></tr><tr><td>Notion_Short</td><td>1</td><td>13</td><td>7.69</td><td>Lark_Notion</td><td>2</td><td>42</td><td>4.76</td></tr><tr><td>Notion_Long</td><td>2</td><td>24</td><td>8.33</td><td>Lark_Other</td><td>6</td><td>73</td><td>8.22</td></tr><tr><td>Obsidian_Short</td><td>1</td><td>17</td><td>5.88</td><td>Rednote_Obsidian</td><td>3</td><td>45</td><td>6.67</td></tr><tr><td>Obsidian_Long</td><td>3</td><td>21</td><td>14.29</td><td>Rednote_Notion</td><td>4</td><td>39</td><td>10.26</td></tr><tr><td>Email</td><td>7</td><td>51</td><td>13.73</td><td>Rednote_Other</td><td>7</td><td>81</td><td>8.64</td></tr><tr><td>Wecom</td><td>4</td><td>40</td><td>10.00</td><td>Hodgepodge</td><td>7</td><td>84</td><td>8.33</td></tr><tr><td>Reddit</td><td>1</td><td>14</td><td>7.14</td><td>Overall</td><td>82</td><td>970</td><td>8.45</td></tr></table>

## 4.6. Trajectory Error Analysis

By analyzing sampled failed traces, we have identified three recurring failure archetypes that account for most end-toend failures in our tool-using setting.

Under Exploration of Environment. In many real-world scenarios, users do not specify all necessary details or preferences in their instructions. Faced with implied information, weaker models often fail by producing a superficially plausible action, without sufficiently exploring the environment or verifying constraints to uncover the missing information.

Task: “...Additionally, please send a polite message to my supervisor, Song Ke, explaining my condition and requesting leave.”

Context: Song Ke’s user id: o9k5jtwo

The context contains Lark identity hints for Song Ke (i.e., user-id), but the instruction does not explicitly specify the platform. Instead of resolving Song Ke’s identity and sending the message via Lark, the agent sends a WeCom message to a hallucinated recipient and then terminates. As a result, the output appears on-topic but fails the task due to platform mismatch and missing recipient grounding.

Skipping Dependent Steps. A second recurring failure is skipping latent dependency steps implied by tool schemas.

Task: “...If everything looks fine, schedule the review meeting for next Monday from 10:00 AM to 12:00 PM in the main conference room. Also, have Zhao host the meeting since she...

Context: Zhao’s phone number: +86 13800138000

The intended workflow is to first resolve the platforminternal ID, user id, from Zhao’s phone number via the user batchGetId tool. The resolved user id is then passed to the calendarEvent create tool to schedule a meeting with Zhao as the host. However, weaker models often skip the resolution step, directly substituting the phone number for the user id or fabricating an ID, which causes execution errors or silent premature termination.

Over Long Context. Our context-tree design can induce progressive context stacking across turns, and certain tools (e.g., local document readers) can return voluminous payloads that sharply increase the tightening the in-context window. As trajectories rollout, the model’s ability to adhere to initial constraints and recall critical observations degrades, culminating in its failure to execute even rudimentary tasks.

## 4.7. Human-LLM Correlation Analysis

We conduct a correlation analysis based on checkpoint-level results of GPT-5 across all 173 tasks and 970 checkpoints. As shown in Table 7, the LLM-based judge is highly correlated with human judgment (91.5% alignment), largely due to our fine-grained breakdown of checkpoints. We also identify two primary causes for the remaining misalignments: (1) Model Capacity Limitation: Even advanced models occasionally struggle with complex logic or subtle context in specific tasks. (2) Over-Strictness: The judge model sometimes penalizes agents for using alternative tools, leading to a lower score despite successful execution.

# 5. Conclusion

In this work, we introduce MCP-Persona, a benchmark tailored for evaluating tool-augmented agents in realistic personalized settings. It is built upon 12 simulated MCP servers and 173 human-verified tasks, spanning a wide range of personal applications that previous work has long struggled to handle. Our experiments reveal that even SOTA agents fall short on personalized tool use, particularly in implicit grounding, multi-step state maintenance, and crosstool coordination. We hope MCP-Persona serves as a reproducible, privacy-preserving testbed that accelerates progress on personalization-aware agents and ultimately bridges the remaining gap between intelligent assistants and the nuanced, context-rich workflows of real users.

# Impact Statement

We acknowledge that the development of benchmarks for personalized tool use, while intended to spur innovation, carries risks of societal impact, particularly in high-stakes domains.

1. A primary concern is the potential for such systems to perpetuate and amplify existing societal biases. For instance, a personalized tool in a domain like finance or healthcare, if trained on historical data reflecting systemic inequities, might learn to offer suboptimal recommendations or fewer opportunities to individuals from marginalized groups. This could lead to discriminatory outcomes in loan applications, medical diagnoses, or legal case preparation.

2. Second, the very act of ”personalization” can create a risk of over-reliance and automation bias, where a user cedes their critical judgment to a system they perceive as being tailored to them. The personalization capabilities could be exploited by malicious actors for targeted phishing, social engineering, or automated spam.

3. Moreover, personalized agents that interact with sensitive services such as email, messaging platforms, or calendars raise significant privacy concerns. Improperly designed systems may expose personal data or introduce security vulnerabilities.

By creating a benchmark that prioritizes performance metrics like efficiency or task success rate, we risk incentivizing the development of powerful but inequitable models. Therefore, we stress that future research in this direction must be coupled with a rigorous focus on developing and integrating metrics for privacy, transparency, and accountability to mitigate these potential harms.
