# The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement

Yi Duan<sup>1,2∗</sup>, Ying Liu<sup>1,2∗</sup>, Zirui Tang<sup>1,2∗</sup>, Haodong Chen<sup>1,2∗</sup>, Jun Zhou<sup>1,2∗</sup>, Yumou Liu<sup>1,2</sup>, Bangrui Xu<sup>1,2</sup>, Yukai Wu<sup>1,2</sup>, Sidi Chen<sup>1,2</sup>, Yuhan Zhou<sup>1,2</sup>, Haoyu Wang<sup>1,2</sup>, Xiaoyou Yu<sup>1,2</sup>, Shaokun Han<sup>1,2</sup>, Xuzhou Zhu<sup>1,2</sup>, Le Zhou<sup>1,2</sup>, Bolin Lu<sup>1,2</sup>, Wei Zhou<sup>1,2</sup>, Jiachen Liu<sup>9</sup>, Nuozhou Fang<sup>2</sup>, Jiaxin Tian<sup>2</sup>, Ruoyu Chen<sup>4</sup>, Yuxuan Li<sup>5</sup>, Kai Zuo<sup>6</sup>, Kaiyan Zhang<sup>10</sup>, Qianyu Yang<sup>8</sup>, Zijie Wang<sup>8</sup>, Jiantao Qiu<sup>7</sup>, Conghui He<sup>7</sup>, Guoliang Li<sup>3</sup>, Bowen Zhou<sup>7,3</sup>, Zhiyuan Liu<sup>3</sup>, Zhoufutu Wen<sup>8</sup>, Jihua Kang<sup>4</sup>, Xuanhe Zhou<sup>1,2†</sup>, Fan Wu<sup>1,2</sup>

<sup>1</sup>Shanghai Jiao Tong University <sup>2</sup>Theseus Labs <sup>3</sup>Tsinghua University <sup>4</sup>ByteDance <sup>5</sup>ModelBest <sup>6</sup>Super Intelligence Team, Xiaohongshu Inc. <sup>7</sup>Shanghai AI Lab <sup>8</sup>Humanlaya <sup>9</sup>Agent-Native Research Lab <sup>10</sup>Frontis.AI

# Abstract

Recursive self-improvement (RSI) enables AI systems to turn experience and feedback into persistent changes that improve both their capabilities and the process of future improvement. We first use the Headroom-Closed Index (HCI) to reveal the problems of existing LLMs, then introduce the RSI concept and its development roadmap: from improvement-execution autonomy, improvement-strategy autonomy, experience-acquisition autonomy, and environment-adaptation autonomy, to recursive meta-improvement. Next we examine RSI across scenarios (e.g., scientific discovery, embodied intelligence, software engineering), highlighting their distinct requirements and development speeds. Drawing on diverse industry practices and preliminary empirical evidence, we connect RSI research with practical systems and identify key challenges to achieving genuine RSI.

Project Page: https://theseus-labs-rsi.github.io/ GitHub Repository: https://github.com/theseus-labs-rsi/awesome-rsi

TL;DR Like human evolution, AI evolution will unfold through a vast and extraordinary history. Everything AI has achieved so far is but a drop in the ocean.  
![](images/24e3a3cf6fc8b96beee52f434f85e06f3a2222800770dccb36a2ed8b15016193.jpg)

[Image: This document displays a structured chart categorizing various AI agents, tools, and research frameworks across nine domains such as AI Research, Robotics, and Enterprise AI, arranged by horizontal levels from L1 Execution to L5 Meta Improvement. Vertical sections delineate specific operational workflows including "In-Task Iteration," "Execution Automation," "Strategy Search," "Experiment-Based Refinement," "Data Pipeline Automation," and "Deployment Automation," listing entities like LangSmith, Anthropic, and Sakana.ai within the relevant tiers. Color-coded markers indicate the primary research focus for each entry, while dashed boundaries group related methods like SFT, RLHF, and Evolutionary Search alongside their corresponding implementation stages. A detailed legend on the far right explains the color coding for different adaptation mechanisms, distinguishing between strategies like "Search & Optimization," "Verification & Selection," and "Online & Meta-Level Adaptation."]  
Figure 1 Overview of the five RSI autonomy levels and representative systems. Autonomy progressively expands from executing prescribed improvements (L1), to selecting improvement strategies (L2), acquiring future learning experience (L3), adapting through deployment and environmental feedback (L4), and ultimately improving mechanisms that govern subsequent improvement (L5). See system details in Appendix B.

# Contents

1 Introduction 3
1.1 Scaling Burdens in Model Development 3
1.2 From Development Burden to RSI 3
1.3 Challenges for RSI 4
1.4 An Autonomy-Centered Framework 4
1.5 Application Domains 5
1.6 Industrial Evidence 6
1.7 Differences from Existing Surveys 6

2 Background and Preliminaries 7
2.1 Uneven Capability Progress in Modern Foundation Models 7
2.2 Conceptual Foundations of Recursive Self-Improvement 9
2.3 Scope of Evidence 12

3 RSI Across Autonomy Levels 12
3.1 B0: In-Task AI Improvement 12
3.2 L1: Autonomy over Improvement Execution 14
3.3 L2: Autonomy over Improvement Strategies 18
3.4 L3: Autonomy over Future Learning Experience 22
3.5 L4: Autonomy in Deployment and Environmental Adaptation 26
3.6 L5: From Environmental Adaptation to Meta-Improvement 31
3.7 Cross-Level Synthesis 35

4 RSI Across Applications 36
4.1 S1: RSI for Science 36
4.2 S2: RSI for Embodied Intelligence 36
4.3 S3: RSI for Software Engineering 37
4.4 S4: RSI for Healthcare 37

5 Industry Landscape and Preliminary Practices 37
5.1 Theseus: Environment–Data–Model Co-Evolution for RSI Intelligence 37
5.2 Lark: Building the Data Foundation for Reliable Enterprise-Level RSI 39
5.3 Xiaohongshu: Dual-Timescale RSI for Recommendation 40
5.4 Humanlaya: Delivery-Driven RSI for Data Quality Assurance 41
5.5 ModelBest: Zero-Human Industrial AI Engineering 42
5.6 Tencent Hunyuan: Experience-Driven Self-Improvement 43
5.7 Agent-Native Research Lab: Verifiable Research Infrastructure for RSI 44
5.8 Frontis.AI: Enterprise Agent Evolution and Cross-Task Meta-Improvement 45

6 Challenges and Future Directions 46

7 Conclusion 49

Appendix 63
A RSI Landscape 63
B Industry Landscape 66
C RSI Across Applications 72
C.1 S1: RSI for Science 72
C.2 S2: RSI for Embodied Intelligence 74
C.3 S3: RSI for Software Engineering 76
C.4 S4: RSI for Healthcare 78

# 1 Introduction

Recent frontier-model development illustrates several forms of scaling in the improvement pipeline. Kimi K3 and Qwen3.8-Max contain 2.8 trillion and 2.4 trillion parameters, respectively, and each supports a context window of approximately one million tokens [1, 2]. The development process is also expanding. During the six months preceding GPT-5.6, OpenAI reports that the share of research compute devoted to internal coding inference grew 100-fold and internal agentic token use grew 22-fold, and average daily output tokens per active researcher exceeded twice the previous peak observed with GPT-5.5 [3]. Scale accumulates across training runs, model-assisted experiments, inference, evaluation, and human validation.

## 1.1 Scaling Burdens in Model Development

Despite the growing use of agentic tools and API-based automation, developers must still determine what to improve, construct the required resources, and establish whether each change works [4, 5]. As AI systems take on more demanding tasks, the cost of scaling this end-to-end development process becomes a bottleneck [6–9]. The following three challenges occur at diferent stages of the model lifecycle and motivate RSI:

• Development challenge 1: Resource-intensive foundation-model training. Foundation-model development remains resource-intensive across data preparation, architecture design, distributed optimization, and evaluation. Kimi K3 activates 16 of 896 experts and reports an approximate 2.5-fold improvement in scaling eficiency over Kimi K2, while Qwen3.8-Max activates 95 billion of its 2.4 trillion parameters [1, 2]. Sparse activation reduces per-token computation, but training at this scale still couples expert routing, parallelism, multimodal integration, long-context optimization, and systems design. OpenAI further reports that GPT-5.6 Sol designed and ran hundreds of experiments on its speculative-decoding draft model and monitored training through hardware failures and instability. The resulting changes improved token-generation eficiency by more than 15% [10]. Data quality also matters in addition to quantity. OpenAI’s GDPval illustrates that its 1,320 professional tasks required roughly 9,240 expert-hours in total, with contributors averaging more than 14 years of experience [6]. The Humanity’s Last Exam pipeline logged more than 70,000 submission attempts and sent approximately 13,000 model-stumping questions to expert review before producing a 3,000-question benchmark [7]. Architecture search remains expensive because candidate structures interact with their data, optimization, and hardware regimes. AgentNAS addresses part of this bottleneck by using an LLM to propose a task-specific seed architecture and construct its search space, but candidate selection still depends on combinatorial search under an externally specified objective [11].

• Development challenge 2: Scaling feedback and learning environments. Synthetic data and reinforcement learning automate parts of capability development, but introduce substantial requirements for generating and evaluating experience, requiring both experience-generation infrastructure and reliable mechanisms for evaluating and retaining updates. For instance, DeepSeek-V3.2 reports a post-training computational budget exceeding 10% of its pretraining cost [12], while NVIDIA’s AIMO-2 pipeline generated 3.2 million long-reasoning solutions and 1.7 million tool-integrated solutions, in addition to curating 540,000 problems [4].

• Development challenge 3: Recurring adaptation after deployment. Deployed systems consistently introduce changing documents, unfamiliar tools, incomplete context, and workflows involving interdependent actions. Improving such systems requires engineers to manually diagnose failures, revise retrieval and tool interfaces, manage persistent state, and repeat regression testing through discrete, human-led releases. Anthropic reports that agentic workloads use approximately four times as many tokens as ordinary chat, rising to about fifteen times for multi-agent systems because of longer contexts, coordination, environment setup, and end-to-end verification [13], while Meta reports that FBDetect identifies thousands of infrastructure regressions each week, and diagnosing one such regression required roughly ten engineer-hours [5].

## 1.2 From Development Burden to RSI

The burdens arise because model improvement remains a sequence of costly, externally coordinated interventions. To address these barriers, RSI inspects whether part of that coordination can become a persistent capability of the system being improved. We define recursive self-improvement (RSI) as an autonomous, closed-loop process in which an AI system identifies its own limitations, develops and validates improvements, and uses the resulting capabilities to improve the improvement process itself. The model evolution paradigm of RSI spans three dimensions: autonomy, eficiency, and innovation. Autonomy expands the system’s responsibility from executing a prescribed update to identifying limitations, extracting experience, proposing changes, and validating and retaining successors. Eficiency seeks more validated improvement from data, compute, inference, human review, and rework. Innovation allows the system to search beyond human-prescribed update strategies and feed useful discoveries back into later improvement rounds. These dimensions describe how the full improvement loop is organized and what it can inherit.

Rather than a particular learning algorithm or a one-of optimization result [14–16], RSI aims to improve both task performance and the mechanisms through which later improvements are discovered and implemented. The following cases illustrate this distinction at two points in the model lifecycle, including foundation-model training and persistent adaptation in software engineering, covered and studied in later sections.

• Case 1: Foundation-model training. A conventional experiment loop selects a better checkpoint while leaving the procedure for choosing later experiments unchanged. A-Evolve-Training instead consolidates post-training outcomes into a persistent research policy and discovery log, which a meta-agent revises to guide later workers’ recipe choices [17]. When development scores improved without corresponding external gains, the system redirected experiments toward data rebalancing and checkpoint selection. The retained policy changes both how successor models are trained and how later improvements are sought. Across four autonomous rounds on a 30B Nemotron model, the external score rose from 0.80 to 0.86, compared with 0.87 for the top human submission [17].

• Case 2: Software-engineering adaptation after deployment. Repairing a repository changes the software product but may leave the coding agent’s recurring failures untouched. Ouroboros instead uses reviewed deployment evidence to propose versioned changes to the agent’s tools, context assembly, prompts, and core implementation [18]. Candidate revisions undergo tests and human review before an accepted version replaces the runtime used for later work. The persistent update improves subsequent coding behavior and changes the mechanism through which later failures are diagnosed and repaired, while experts retain control over consequential corrections and deployment.

## 1.3 Challenges for RSI

While the two cases show how persistent changes can shape later improvement, the same persistence can carry errors or obscure where control resides. We examine three recurring problems that determine whether a self-updating system provides credible evidence of RSI.

• Safe inheritance. RSI requires changes to persist across tasks or improvement rounds, but persistence alone does not guarantee sustained gains. Gödel Agent [19], for example, rewrites both its task policy and improvement logic, yet 14% of its 100 MGSM optimization trials ended below the initial policy’s performance. Transfer tests, version histories, and rollback mechanisms are needed to retain useful updates without degrading earlier capabilities.

• Autonomy attribution. Generating better candidates does not necessarily mean the system has improved how candidates are discovered or selected. The Darwin Gödel Machine [16] evolves coding agents, raising performance on its SWE-bench subset from 20% to 50%, but its archive maintenance and parent-selection rules remain outside self-modification. RSI analysis must distinguish AI-controlled decisions from fixed search procedures and human acceptance criteria.

• Reliable verification. Repeated evaluator access can reward exploitation rather than capability gains. Anthropic’s automated research experiments [20] report random-seed cherry-picking and attempted test-labe extraction through evaluator queries. Evolving evaluators further complicate comparisons across rounds. The Red Queen Gödel Machine [21] addresses this by freezing evaluators within each epoch and validating replacements against an independent ground-truth anchor. Protected evaluation and matched computationa budgets are needed to separate genuine improvement from evaluator exploitation or increased search efort.

## 1.4 An Autonomy-Centered Framework

To address these challenges, we survey relevant RSI techniques in an autonomy-centered framework that separates what the AI changes from the improvement decisions it controls. Based on the scope of improvement responsibility internalized by AI, we review RSI techniques across five levels. Figure 1 maps representative systems across this progression, while Figure 2 isolates the corresponding loop structures. At each level, we identify where the improvement loop closes, what is retained for later rounds, and which critical decisions remain under human control, then introduce the techniques that implement this division of responsibility.

![](images/560ac880665c247343a3502d654ac06c16679690456669ddcb24fa63e1639292.jpg)

[Image: The image displays five parallel flowcharts representing stages of autonomy in AI improvement loops, labeled L1 through L5. Each column separates tasks into "Human Efforts" at the top and an "Agentic Loop" at the bottom, demonstrating a gradual transfer of responsibility from human-defined policies to automated execution and self-improvement. Key procedural blocks such as "Design Update Policy," "Plan Experience Acquisition," and "Update" are connected by arrows to show the cycle, with orange-highlighted boxes indicating specific capabilities like environment interaction or system improvement that emerge in higher levels.]  
The scope of improvement responsibility internalized by AI improves  
Figure 2 Loop Patterns of Five Levels. Gray dashed frames indicate human-controlled components. Green dashed frames indicate components within the RSI loop. Orange outlines highlight the newly internalized component at each level. The expanding green frames show that AI progressively automates a larger share of the improvement process.

• (L1) Improvement Execution Autonomy. Humans specify what should be improved, how it should be improved, and what constitutes success, while AI executes candidate updates. For example, FineWeb-Edu uses a model to apply human-defined educational-quality labels across a web corpus without choosing the labeling criterion [22].

• (L2) Improvement Strategy Autonomy. The objective, task boundary, and evaluation criteria remain externally fixed, but AI diagnoses weaknesses and decides how to improve the system. For example, Self-Harness uses execution traces to propose and test edits to its agent harness under a fixed benchmark and promotion rule [23].

• (L3) Learning-Signal or Experience-Acquisition Autonomy. The system also determines the experience needed for its next improvement round. For example, SIMA 2 uses assessments of current behavior to generate later practice tasks that target observed skill weaknesses [24].

• (L4) Environment Adaptation Autonomy. The improvement loop uses deployment interaction to revise persistent system state under external acceptance and governance rules. For example, PANDO admits or demotes reusable rules during a long-running interaction according to observed outcomes, so later actions inherit earlier experience [25].

• (L5) Recursive Inheritance Autonomy. The system persistently revises a mechanism that governs subsequent improvement, such as an improver, verifier, or successor-generation procedure. For example, A-Evolve-Training revises its research policy after development scores fail to predict external gains and uses the revised policy to direct the next training round [17].

## 1.5 Application Domains

While the autonomy levels describe the structure of an improvement loop, their practical meaning depends on the feedback available in a domain, as the same retained update may be straightforward to test in software engineering and dificult to validate in a physical or clinical setting. We consider science, embodied intelligence, software engineering, and healthcare because they expose four distinct feedback regimes, including experimental evidence with uncertain attribution, physical interaction with costly trials, executable tests with incomplete specifications, and high-stakes outcomes under expert oversight. These regimes allow us to compare how feedback cost and reliability afect the retention and reuse of improvements.

• (S1) RSI for Science. Scientific discovery involves open-ended exploration, costly experiments, and feedback that may not clearly identify the source of failure. We examine how accumulated evidence can improve scientific hypothesis modules, experimental agents, and reflection or improvement mechanisms, with attention to whether these changes support subsequent research beyond the current scientific result.

• (S2) RSI for Embodied Intelligence. Embodied agents generate experience through their own actions, while failures may arise from interacting perception, planning, and control components. Physical trials also impose limits on exploration and repeatability. We examine the evolution of environments and curricula, skills and agent harnesses, policies and action models, and world models and evaluators, focusing on how interaction feedback supports validated improvements that can be reused in later tasks.

• (S3) RSI for Software Engineering. Software engineering makes both the developed artifact and the developing agent accessible to executable modification and testing. We examine how repository feedback supports persistent changes to coding-agent implementations and harnesses, development experience and collaboration, and the improvement process itself. A central distinction is whether an update improves current task performance, the ability to produce stronger successors, or both.

• (S4) RSI for Healthcare. Healthcare combines restricted opportunities for trial and error with delayed, heterogeneous feedback and improvements whose validity may depend on the patient population or institution. We examine the evolution of clinical memory and knowledge, reasoning strategies, and tools and workflows, emphasizing how reviewed experience can inform subsequent cases under explicit validation and oversight.

Across these domains, we compare what is updated, how feedback supports its retention, and which decisions remain externally controlled. This analysis connects the autonomy framework to application-specific evidence and identifies the gaps between demonstrated improvement mechanisms and fuller recursive improvement.

## 1.6 Industrial Evidence

The domain analysis identifies the feedback and validation conditions that shape an improvement loop, while industrial systems show how these conditions are handled within operating pipelines, where integration and deployment constraints are immediate. We examine industrial practice because frontier improvement loops are not always first documented through conventional academic publications. Industrial materials, including technical reports, open-source systems, engineering blogs, model documentation, and deployed product infrastructures, often reveal system-level practices, such as evaluation pipelines, data flywheels, agent harnesses, automated experimentation, and deployment feedback loops, which are only partially represented in the academic literature. We use these materials to complement the research literature and to understand how self-improvement is implemented under real engineering constraints.

Building on the autonomy-centered framework and application analysis, we examine what responsibilities industrial systems assume for their own improvement and how these responsibilities vary across applications and engineering settings. We further analyze how constraints such as computational cost, feedback quality, and human involvement shape the organization of improvement loops and limit the attainable scope of autonomy. This perspective allows us to characterize both the mechanisms that have been demonstrated in deployed or production-oriented systems and the more ambitious visions of recursive improvement that remain to be validated, thereby clarifying the current progress and limitations of industrial RSI practice. Figure 18 reports the surveyed literature by autonomy level and improvement target, while Table 13 provides the corresponding landscape of industrial systems.

## 1.7 Differences from Existing Surveys

Existing surveys provide complementary taxonomies of self-evolving systems and the mechanisms from which improvement loops are built. These works establish much of the technical vocabulary on which our analysis relies. Our survey difers in four respects.

• Improvement loop as the unit of analysis. Prior surveys organize work by stages of self-evolution, update objects, timing, or technical mechanisms [26–29]. These views explain what changes and how the change is produced, but systems that update the same component may assign very diferent decisions to AI. We trace a complete loop: what triggers improvement, who proposes and validates a change, what persists, and which later decisions use the retained change.

• Responsibility as the autonomy criterion. Related frameworks examine capability levels, co-evolution, dynamic agent state, and AI-for-AI systems [30–33]. We operationalize autonomy through the improvement decisions transferred from external designers to the AI rather than through model capability or the number of automated components. Our five levels distinguish responsibility for execution, strategy selection, experience acquisition, environmental adaptation, and recursive inheritance.

• Separate evidence for recursion and performance. Evaluation surveys study model-based judgment, agent assessment, rubric-guided learning, and oversight failures [34–38]. Higher task performance alone does not show that an improvement mechanism was revised, retained, and reused. We distinguish structural recursion, in which a revised improvement mechanism governs a later round, from efective recursion, in which that mechanism produces stronger successors under comparable budgets and independent evaluation.

• Mechanisms compared across operating conditions. Work on correction, synthetic data, lifelong learning, memory, prompt optimization, and workflow design explains how individual components improve [39–49]. We examine how these mechanisms function within complete loops across science, embodied intelligence, software engineering, healthcare, and industrial practice, where feedback cost, validation, and external control difer [50–52]. Comparing the same loop questions across these settings reveals when a method depends on cheap executable feedback, repeated interaction, expert review, or production infrastructure.

These choices together position the survey between a catalog of improvement mechanisms and a general hierarchy of AI capabilities. Our aim is to determine which parts of an improvement loop current systems can assume, how retained changes afect later rounds, and what evidence supports claims of recursive progress.
