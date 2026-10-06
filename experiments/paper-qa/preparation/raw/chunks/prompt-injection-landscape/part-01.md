# The Landscape of Prompt Injection Threats in LLM Agents: From Taxonomy to Analysis

Peiran Wang UCLA

Xinfeng Li NTU

Chong Xiang NVIDIA

Jinghuai Zhang UCLA

Xiaofeng Wang NTU

Ying Li UCLA

Lixia Zhang UCLA

Yuan Tian UCLA

# Abstract

The evolution of Large Language Models (LLMs) has resulted in a paradigm shift towards autonomous agents, necessitating robust security against Prompt Injection (PI) vul nerabilities where untrusted inputs hijack agent behaviors. This SoK presents a comprehensive overview of the PI land scape, covering attacks, defenses, and their evaluation prac tices. Through a systematic literature review and quantitative analysis, we establish taxonomies that categorize PI attacks by payload generation strategies (heuristic vs. optimization) and defenses by intervention stages (text, model, and exe cution levels). Our analysis reveals a key limitation shared by many existing defenses and benchmarks: they largely overlook context-dependent tasks, in which agents are au thorized to rely on runtime environmental observations to determine actions. To address this gap, we introduce AGENTPI, a new benchmark designed to systematically evaluate agent behavior under context-dependent interaction settings. Using AGENTPI, we empirically evaluate representative defenses and show that no single approach can simultaneously achieve high trustworthiness, high utility, and low latency. Moreover, we show that many defenses appear effective under existing benchmarks by suppressing contextual inputs, yet fail to gen eralize to realistic agent settings where context-dependent reasoning is essential. This SoK distills key takeaways and open research problems, offering structured guidance for future research and practical deployment of secure LLM agents.

# 1 Introduction

Recent advances have enabled Large Language Model (LLM) agents to interact with external tools and environments, substantially expanding their capabilities [27, 73, 82]. However, the LLM agents are vulnerable to Prompt Injection (PI) attacks, in which untrusted inputs manipulate the backbone LLM’s output to hijack the agent behavior [45, 56]. Such at tacks can lead to severe consequences, including unauthorized remote computer use [71], sensitive data leakage [25], etc.

Thus, many works (78 papers we collected until Oct. 20, 2025) have been proposed to study such threats. On the attack side, for example, optimization-based techniques utilize fuzzing [84] or gradient guidance [45, 55] to generate stealthy payloads, yet they often face challenges regarding query efficiency or require white-box access. On the defense side, some detection approaches employing external LLMs [48,66] show promise in identifying payload segments, but they introduce additional computational overhead. Similarly, isolation works [78, 79] aim to contain threats by separating control and data flow, although they may severely compromise the agent’s utility in complex tasks.

Given the rapid growth of this field, a SoK is crucial to understand the landscape. This SoK aims to: (1) bridge knowledge gaps by analyzing PI attack and defense approaches; (2) offer critical insights into the core paradigms, strengths, and limitations of current work; (3) propose promising open problems to motivate future research directions. In this paper, we first establish a taxonomy of existing PI attacks grounded in attack payload generation methods. The taxonomy provides a trend analysis of payload generation, attack threat models, attacker capability, and payload visibility. We found that attacks have gradually evolved from impractical attacks under white-box, base LLM victim settings to more practical settings under black-box, LLM agent victim settings.

Next, we provide a taxonomy of existing PI defenses categorized by defense intervention stages. This taxonomy provides a comparative analysis of intervention stages, defense capability, explainability, and costs, revealing a multifaceted landscape. Furthermore, we identify several takeaways and open problems to motivate future research from this taxonomy. We identified that there is no definitive “perfect” defense to meet the high trustworthiness (security+explainability), high utility, and low latency simultaneously. For instance, the LLM-involved methods lack reliability in terms of explainability [66, 74], while human-involved methods bring additional latency costs [65, 79]. We propose several important research directions to advance PI, including the integration of availability defenses, fine-grained access control for attention probe for explainability, etc. We also identify a key limita tion shared by existing defenses: they lack consideration of context-dependent tasks.

To address the lack of consideration on context-dependent tasks, we propose AGENTPI benchmark. Real-world agents frequently rely on runtime environmental observations, such as following configuration files [33, 80] or executing conditional logic (e.g. “If-Else” structure) [74]. This reliance creates context-dependent tasks and an attack surface for context-aware attacks, in which adversaries manipulate en vironmental inputs to corrupt reasoning. However, existing benchmarks [21, 86, 89] predominantly focus on tasks fully specified by prompts. This focus inadvertently favors defenses that isolate or reject contextual inputs, leading to an overestimation of their utility in realistic scenarios where context is essential for planning. To bridge this gap, AGENTPI systematizes 5 context-dependent tasks and their corresponding attacks.

Finally, to validate our taxonomy and theoretical analysis, we conducted comprehensive experiments on 8 defenses, ranging from text-level filters to execution-level monitors. We evaluated these mechanisms using a multi-dimensional metric system that quantifies the trade-offs between security effectiveness (attack success rate), agent utility, and computational cost (time and tokens). Our empirical analysis reveals that there is currently no tested defense that simultaneously achieves high trustworthiness, high utility, and low latency. Specifically, we find that while execution-level defenses can enforce strict action boundaries, they often incur prohibitive computational overhead, up to 3x the baseline cost, or resort to aggressive “early refusal” strategies that render the agent unusable for complex tasks. Conversely, text-level defenses, while efficient, fail to provide robust security guarantees against sophisticated payload manipulations.

In summary, we have the following key contributions:

• Systematic taxonomy of attacks and defenses: We pro vide a comprehensive taxonomy and comparative analysis of 78 papers, encompassing both attacks and defenses. We categorize attacks based on payload generation methodolo gies (heuristic vs. optimization) and defenses by interven tion stages (text, model, and execution levels). This system atization offers a unified view of the evolving PI landscape, from manual templates to automated injections, and the corresponding mitigation strategies.

• The AGENTPI benchmark and empirical evaluation: To address the critical lack of evaluation on context-dependent tasks, we introduce AGENTPI benchmark, designed to assess defenses’ performance in such tasks. We evaluate 8 defenses and identify a fundamental trilemma among trustworthiness, utility, and latency.

• Insights and future roadmap: We explore the latest research trends, identify key challenges, and propose future directions based on 9 takeaways and 4 open problems. Through quantitative and qualitative analysis, we highlight gaps in current works where there is no “perfect” defense to meet high trustworthiness, high utility, and low latency, and extract open problems to guide future research in PI.

# 2 Preliminary and Problem Setup

In this section, we first define the system model of LLM agents in §2.1. Then, we present the definition of prompt injection in LLM agents in §2.2.

## 2.1 LLM Agents

To provide a system model for this paper, we first introduce the typical execution loop of the LLM agentic system, with 6 iterative steps as illustrated in Fig. 1:

1 Receive prompts. Firstly, LLM agents receive system prompts defined by the agentic developer and the user prompts written by the users.

2 Retrieve RAG (optional). Some of the agents are integrated with the Retrieval-Augmented Generation (RAG) database to fetch relevant, up-to-date data from external knowledge sources before generating the response.

3 Reasoning (optional). Next, the agents go through a chain-of-thought process to reason about the plans or the next step to execute. This step is optional, since some agent developers tend to use function calling [53].

4 Generate tool call. Then, based on previous context memory, the backbone LLM of the agents generates the next step’s tool call (the tool name and tool parameters).

5 Tool execution. The tool call is forwarded to the executive environments bound with the LLM agents to execute.

6 Tool observation return (loop back to 2 ). At last, the environment returns tool execution results (called tool observation) to the LLM agents, integrating into the context memory, and looping back to 2 .

## 2.2 Prompt Injection in LLM Agents

Input to the LLM agents. Within this loop, the LLM agents take inputs from various sources, along with their influence on the actions of LLM agents. Unlike computer programs, which provide isolated input interfaces for diverse inputs, LLM agents manage all the inputs in a single context memory. Different inputs are segmented with separators (e.g., “[SYS-TEM]”, “[DATA]”, etc.) in the context memory. We categorize the input into 3 types as shown in Fig. 1:

1 Trusted prompt input. The system prompt and user prompt constitute the basic input of an LLM agent. Among them, the system prompt is defined by the agentic developer, while the user prompt is issued by the user. The prompts are generally considered trusted in LLM agents.

2 Untrusted tool observation. Another type of input is tool observation, originating from the tool execution process within the environment. Since the executive environment is not fully controlled by the agent, the tool observation is considered to be the untrusted input.

![](images/0135063fb0a851314a2b4bf9f2dadba22806a67bc23d03fe9999d6b4ab073c31.jpg)

[Image: The image displays a system architecture where a Backbone LLM processes Input Text derived from System and User Prompts (1) and RAG/Training Data (3). Processed information flows through a Reasoning module (3) to generate Tool Calls (4), which interact with an Environment containing diverse tools such as Websites, Email, and Files (2). The system includes a feedback mechanism where Tool Observations (6) are returned as new Input Text, creating a cycle involving Context Memory. Red circled numbers identify specific nodes like the File interface and Reasoning block, corresponding to potential supply-chain or untrusted input vectors described in the text.]  
Figure 1: Overview of the LLM agent execution loops and inputs to the agent.

3 Supply-chain dataset input. In addition to the 2 common-seen input types, the supply-chain data, including the retrieval content of RAG and the training dataset, are also considered. Most works treat these inputs as trusted; however, some threat models account for attack surfaces from the 2 data sources [63, 90, 91]. Thus, we label these 2 inputs as partially trusted.

These inputs have different trust levels and co-exist in a single context memory of the LLM agent to affect its behaviors.

Principles of prompt injection. The prompt injection vulnerability arises from the lack of privilege isolation between different trust levels’ inputs. Despite textual delimiters, the model processes the context as a unified semantic sequence, creating ambiguity where untrusted inputs can mimic trusted input to manipulate the agent’s behaviors. This results in attention competition: adversarial payloads manipulate the self attention mechanism, shifting attention weights away from system prompts toward malicious inputs [29, 93]. Furthermore, this leads to unauthorized privilege escalation, enabling the hijacking of the agent’s control flow.

# 3 Taxonomy of Attacks

Selection methodology. We conducted a systematic literature search focused on prompt injection attacks using two search queries: “prompt injection attacks” and “LLM agent attacks”. The search was performed on Google Scholar manually, and excluding result papers about jailbreaking LLM agents, general LLM agent safety, etc. The selection process ended on Oct. 20, 2025, with 37 prompt injection attack papers selected. In addition, during our selection, the attack papers on general LLM and specific LLM applications (LLM translation, etc.) instead of agents are selected as well, since the attacks can be integrated into LLM agents as well.

Taxonomy methodology. We systematically categorized the collected prompt injection attack papers based on the payload generation methods. We identified two types: heuristic-based and optimization-based in §3.1.

Analysis methodology. After systematic taxonomy analysis, we discuss the core attack paradigm across all attacks, including the threat models (attack surfaces, victims, and goals), the attacker capabilities, and the visibility of payloads in §3.2.

## 3.1 Attack Payload Generation

We systematize the collected 37 prompt injection attack papers based on their payload generation methodologies, as summarized in Table 1. We categorize these methods into two paradigms: heuristic-based approaches, which rely on manual design or semantic exploitation strategies (23 out of 37 works) to generate payloads, and optimization-based approaches, which employ automated algorithms to search for optimal payloads (14 out of 37 works).

Heuristic Heuristic-based attacks exploit the intrinsic instruction-following bias of LLMs, typically treating the target agent as a black box. We categorize these works (23 out of37 papers) into 3 subtypes:

(1) Manual template. As the most prevalent category (16 papers), these attacks involve manually constructing adversarial prompts that exploit priority conflicts in the attention mechanism, where the model prioritizes recent or authoritativesounding instructions over system prompts. While early techniques focused on direct overrides, recent works demonstrate that such templates have evolved into stealthy IPI embedded within agent memory or log files to trigger action hijacking [56, 91]. Furthermore, this vector extends to the supply chain, where attackers poison training datasets with backdoor triggers to permanently compromise model alignment [9, 63].

(2) LLM generation. To address the inefficiency of manual crafting, researchers employ “LLM-against-LLM” frameworks (3 papers). Unlike optimization-based methods that iteratively search for payloads, these approaches leverage the generative capabilities of a Red-team LLM to generate adversarial instructions based on heuristic rules [16, 18].

(3) Structural encoding. These attacks (4 papers) target the cognitive gap between the model’s tokenizer and its semantic processing. Instead of relying on natural language, adversaries encode payloads into non-semantic formats, such as Base64, ASCII art, or structured file layouts, that bypass semantic safety filters while remaining executable. Recent studies validate that such structural injections can manipulate logic in PDF parsing or web search tools, highlighting the insufficiency of semantic-only defenses [14, 35, 61].

Table 1: Systematization of prompt injection attacks, categorized into optimization and heuristic as illustrated in §3.1.

<table><tr><td>Category</td><td>Method§3.1</td><td>Surface§3.2</td><td>Victim§3.2</td><td>Goal§3.2</td><td>Capability§3.2</td><td>Visibility§3.2</td><td>Ref.</td></tr><tr><td rowspan="14">Optimization</td><td rowspan="6">Gradient</td><td></td><td>:Base</td><td>:Goal Hijack</td><td>:Gradients</td><td>:Semantics</td><td>[45]</td></tr><tr><td></td><td>:Base</td><td>:Fingerprint</td><td>:Logits</td><td>:Semantics</td><td>[28]</td></tr><tr><td></td><td>:Base</td><td>:Goal Hijack</td><td>:Gradients</td><td>:Semantics</td><td>[57]</td></tr><tr><td></td><td>:Evaluator</td><td>:Score Tamper</td><td>:Logits</td><td>:Semantics</td><td>[64]</td></tr><tr><td></td><td>:Finetuned</td><td>:Defend Bypass</td><td>:Attention</td><td>:Semantics</td><td>[55]</td></tr><tr><td></td><td>:RAG</td><td>:Goal Hijack</td><td>:Gradients</td><td>:Context</td><td>[90]</td></tr><tr><td rowspan="6">Genetic</td><td></td><td>:Base</td><td>:Goal Hijack</td><td>:Query-free</td><td>:Semantics</td><td>[88]</td></tr><tr><td></td><td>:Base</td><td>:Goal Hijack</td><td>:Success Boolean</td><td></td><td>[84]</td></tr><tr><td></td><td>:Tabular</td><td>:Goal Hijack</td><td>:Shadow Agent</td><td>:Context</td><td>[23]</td></tr><tr><td></td><td>:Defense</td><td>:Defend Bypass</td><td>:Defender Feedback</td><td>:Semantics</td><td>[44]</td></tr><tr><td></td><td>:General</td><td>:Goal Hijack</td><td>:Logits</td><td>:Context</td><td>[85]</td></tr><tr><td></td><td>:Search</td><td>:Rank Tamper</td><td>:Rankings</td><td>:Semantics</td><td>[52]</td></tr><tr><td rowspan="2">Sampling</td><td></td><td>:Base</td><td>:Goal Hijack</td><td>:Reward Signal</td><td>:Semantics</td><td>[77]</td></tr><tr><td></td><td>:Base</td><td>:Goal Hijack</td><td>:Surrogate Activations</td><td>:Semantics</td><td>[41]</td></tr><tr><td rowspan="23">Heuristic</td><td rowspan="16">Manual Template</td><td></td><td>:Memory</td><td>:Action Hijack</td><td>:Memory Output</td><td>:Context</td><td>[91]</td></tr><tr><td></td><td>:Multi</td><td>:Agent Hijack</td><td>:Consensus State</td><td>:Context</td><td>[17]</td></tr><tr><td></td><td>:Multi</td><td>:Agent Hijack</td><td>:Message Passing</td><td>:Context</td><td>[37]</td></tr><tr><td></td><td>:General</td><td>:C:Data Leakage</td><td>:Tool Output</td><td></td><td>[2]</td></tr><tr><td></td><td>:Finance</td><td>:Goal Hijack</td><td>:Output Text</td><td></td><td>[3]</td></tr><tr><td></td><td>:Hacker</td><td>:Action Hijack</td><td>:Logs</td><td>:Context</td><td>[56]</td></tr><tr><td></td><td>:Medical</td><td>:Misinformation</td><td>:Text Output</td><td></td><td>[12]</td></tr><tr><td></td><td>:CoT</td><td>:A:CoT DoS</td><td>:Reasoning Trace</td><td></td><td>[81]</td></tr><tr><td></td><td>:Translator</td><td>:Task Hijack</td><td>:Translation</td><td></td><td>[68]</td></tr><tr><td></td><td>:Coding</td><td>:Action Hijack</td><td>:Execution</td><td>:Vision</td><td>[46]</td></tr><tr><td></td><td>:Product</td><td>:C:Data Leakage</td><td>:Exfiltration Log</td><td>:Context</td><td>[62]</td></tr><tr><td></td><td>:Hacker</td><td>:Action Hijack</td><td>:Shell Access</td><td>:Encoding</td><td>[51]</td></tr><tr><td></td><td>:Reviewer</td><td>:Score Tamper</td><td>:Review Output</td><td>:Vision</td><td>[94]</td></tr><tr><td></td><td>:Evaluator</td><td>:Score Tamper</td><td>:Score Output</td><td>:Encoding</td><td>[50]</td></tr><tr><td></td><td>:Base</td><td>:Defend Bypass</td><td>:Training Data</td><td></td><td>[63]</td></tr><tr><td></td><td>:Base</td><td>:Defend Bypass</td><td>:Training Access</td><td></td><td>[9]</td></tr><tr><td rowspan="3">LLM Generation</td><td></td><td>:CoT</td><td>:A:CoT DoS</td><td>:Output Length</td><td>:Semantics</td><td>[16]</td></tr><tr><td></td><td>:RAG</td><td>:C:Data Leakage</td><td>:Leak Success</td><td>:Context</td><td>[18]</td></tr><tr><td></td><td>:Evaluator</td><td>:C:Defend Bypass</td><td>:Score Consistency</td><td></td><td>[43]</td></tr><tr><td rowspan="4">Structural Encoding</td><td></td><td>:Reviewer</td><td>:Score Tamper</td><td>:Review Score</td><td>:Vision</td><td>[14]</td></tr><tr><td></td><td>:Reviewer</td><td>:Score Tamper</td><td>:Grading Score</td><td></td><td>[24]</td></tr><tr><td></td><td>:Browser</td><td>:C:Data Leakage</td><td>:Web Request</td><td>:Encoding</td><td>[61]</td></tr><tr><td></td><td>:Reviewer</td><td>:Score Tamper</td><td>:Review Score</td><td>:Context</td><td>[35]</td></tr></table>

(1) For the attack surface: : direct prompt injection; : indirect prompt injection; : prompt injection from supply chain. (2) For the victim: LLM; : LLM-integrated application; : LLM agent. (3) For the access: : black-box; : white-box. (4) For the perceptibility: Y: visible payloads; X: invisible payloads; Vision: invisible in vision; Context: invisible via merging in context; Encoding: invisible via encoding; Semantics: invisible via adversarial optimization of semantics.

Optimization Optimization-based attacks automate the search for adversarial suffixes or token combinations that maximize the likelihood of malicious generation. These methods (14 out of37 papers) are categorized by their access requirements into gradient-based (white-box) and genetic/samplingbased (black-box) approaches.

(1) Gradient. Requiring white-box access to model weights (6 papers), these methods compute the gradient of the loss function with respect to input tokens. Inspired by Greedy Co ordinate Gradient (GCG) attacks, they iteratively update the payload to minimize model resistance. Applications include generating universal adversarial suffixes to bypass perplexity filters, fingerprinting LLMs via injection response patterns, and crafting neural execution triggers to evade sanitization layers [28, 45, 57].

(2) Genetic and (3) sampling. To operate under black-box constraints (8 papers), researchers utilize evolutionary algorithms or sampling techniques driven by query feedback. Genetic approaches evolve a population of prompts to bypass distributional detectors or manipulate tabular agents [23, 88]. Alternatively, Reinforcement Learning (RL) and MCMC sam pling frameworks model the attack as a reward maximization problem, generating transferable injections that bypass instruction hierarchies without direct gradient access [41, 77].

Takeaway I. Misalignment between attack payload generation and defense evaluation. Our analysis highlights a critical “evaluation gap”: while optimization-based attacks now constitute 14 out of37 works, existing defenses and benchmarks continue to evaluate security primarily against heuristic templates. This misalignment creates a “false sense of security”, where defenses appear robust against manual patterns but remain untested against automated-generated payloads.

## 3.2 Attack Paradigms

In this section, we discuss the core attack paradigm across all attacks, including the threat models (surfaces, victims, and goals), the attacker capabilities, and the visibility of payloads.

Threat model. Mapping the threat landscape to the execution loop in §2.1, we categorize attacks into three vectors: Direct Prompt Injection (DPI) (malicious user inputs), Indirect Prompt Injection (IPI) (adversarial instructions embedded in external resources), and Supply-chain Prompt Injection (SPI) (payloads within RAG or training datasets). Our anal ysis reveals a significant expansion in the attack surface: while foundational studies address DPI (17 works), the majority of agent-specific research now prioritizes IPI (20 works). At the same time, attack victims have gradually shifted from base LLM to researching specific LLM applications and LLM agents. Consequently, attacker goals have shifted from safety violations to I integrity compromise (30 out of 37 works), manifesting primarily as action or goal hijacking. Notably, C confidentiality attacks (4 works) [2, 18, 61, 62] increasingly converge with hijacking for data exfiltration, while A availability vectors (2 works) [16, 81] specifically target reasoning mechanisms (e.g., CoT DoS).

Attacker capabilities. We categorize capabilities by system access, where a minority of studies (9 works) assume white-box access to model parameters, leveraging : gradients for adversarial suffixes [45, 57, 90], : logits for fingerprinting [28, 64], or : training data for poisoning [9, 63]. Conversely, the majority (28 out of 37) operate under black-box constraints, optimizing against visible : text/score outputs [50, 68] or restricted : success boolean signals [18, 84]. Notably, agentic systems introduce environmental side-channels, enabling state inference via : logs [56], : memory output [91], or : execution effects [46, 51] without direct model access.

Attack visibility We classify payloads into Yvisible and Xinvisible categories, identifying a paradigm shift where the majority of research (27 out of 37 works) focuses on invis ibility to evade detection. While early heuristics employed Yvisible payloads with explicit natural language triggers (10 works), adversaries have pivoted to stealthier vectors: semantics invisibility (11 works) utilizes optimization to craft non-meaningful suffixes [45]; context invisibility (10 works) conceals payloads within massive context windows via poi soned sources like RAG [90] or logs [56]; encoding invisibility (3 works) exploits parsing gaps via non-standard formats (e.g., Base64) [61]; and vision invisibility (3 works) embeds imperceptible instructions into visual inputs transparent to humans but legible to agents [94].

Takeaway II. The paradigm shift to more practical attacks. The threat landscape has transitioned from theoretical safety violations to practical integrity compromises, where adversaries prioritize high-stakes action hijacking over simple toxic generation. This evolution is characterized by a migration from direct, visible overrides to stealthy, environment-driven vectors, specifically IPI and invisible optimization, that exploit the agent’s context processing rather than relying on white-box model access.

![](images/90a8a641c84eaec042f6eae15ae44ecf50472be5f4fe9c70277a2047eaca0884.jpg)

[Image: This flowchart depicts a recursive agent architecture centered on a "Backbone LLM" connected to "Context Memory." A "User Prompt" initiates the process as "Input Text," which the LLM processes to generate "Output Text." This output triggers a "Tool Call" within an external "Environment," resulting in a "Tool Observation" that is fed back into the "Input Text" stream to close the loop. The diagram uses green "T" tags to denote textual data and blue "E" tags to represent environmental interactions.]  
Figure 2: We map the taxonomy of defenses to 3 different levels: (1) T Text-level: Stateless defenses focusing on the backbone LLMs’ input and output; (2) M Model-level: Internal defenses focusing on the model parameters or inference internal representation (IR); (3) E Execution-level: Stateful defenses focusing on the consequences and causality of actions within the environments.

