arXiv:2602.21193v1 [cs.CL] 24 Feb 2026  


# On Data Engineering for Scaling LLM Terminal Capabilities  


Renjie Pi*, Grace Lam*, Mohammad Shoeybi, Pooya Jannaty, Bryan Catanzaro, Wei Ping†  


# Abstract  


Despite rapid recent progress in the terminal capabilities of large language models, the training data strategies behind state-of-the-art terminal agents remain largely undisclosed. We address this gap through a systematic study of data engineering practices for terminal agents, making two key contributions: (1) Terminal-Task-Gen, a lightweight synthetic task generation pipeline that supports seed-based and skill-based task construction, and (2) a comprehensive analysis of data and training strategies, including filtering, curriculum learning, long context training, and scaling behavior. Our pipeline yields Terminal-Corpus, a large-scale open-source dataset for terminal tasks. Using this dataset, we train Nemotron-Terminal, a family of models initialized from Qwen3(8B, 14B, 32B) that achieve substantial gains on Terminal-Bench 2.0: Nemotron-Terminal-8B improves from 2.5% to 13.0% Nemotron-Terminal-14B improves from 4.0% to 20.2%, and Nemotron-Terminal-32B improves from 3.4% to 27.4%, matching the performance of significantly larger models. To accelerate research in this domain, we open-source our model checkpoints and most of our synthetic datasets at https://huggingface.co/collections/nvidia/nemotron-terminal.  


![ace28a3cc7a48bee03c7998a6cd732dd.jpeg](images/0.png)

[Image: This diagram illustrates the Terminal-Task-Gen framework, structured around two primary input streams: "Dataset Adaptation" and "Synthetic Task Generation." The "Dataset Adaptation" process converts collected Math, Code, and SWE prompts through filtering and adaptation, while "Synthetic Task Generation" constructs scenarios by combining seed data, skill taxonomies, and pre-built Docker images.

Both streams feed into the "TRAJECTORY GENERATION" phase, where the Terminus 2 agent employs the DeepSeek-V3.2 model to interact with environments. Finally, the generated trajectories pass through "POST-PROCESSING"—specifically data decontamination and filtering—to produce the "Terminal-Corpus," a large-scale SFT dataset for terminal agents.]  


>Figure 1: Overview of Terminal-Task-Gen. Our framework combines Dataset Adaptation, which transforms existing benchmarks into terminal prompts, with Synthetic Task Generation, which uses seed data and a Skill Taxonomy to construct targeted scenarios. The tasks from both streams are utilized during Trajectory Generation phase, where agents interact with Dockerized environments to produce solution traces, followed by Post-Processing (decontamination and filtering) to yield the final SFT dataset.  


# 1. Introduction  


As large language models (LLMs) advance toward practical software engineering applications, terminal interaction has emerged as a critical capability. Tools like Claude Code (Anthropic, 2025) and Codex CLI (OpenAI,  


>*Equal technical contribution. Correspondence to: <renjiep@nvidia.com>, <gralam@nvidia.com>, <wping@nvidia.com>  


>†Leads the effort.  


>Table 1: Model performance comparison on Terminal-Bench 2.0.  


| Closed Source Models|Closed Source Models|Closed Source Models|Closed Source Models|Closed Source Models|Closed Source Models|Closed Source Models|
| ---|---|---|---|---|---|---|
| Model|GPT-5-Nano|GPT-5-Mini|Grok Code Fast 1|Grok 4|Gemini 2.5 Flash|Qwen3-Max-Thinking|
| Accuracy|7.90|24.0|14.2|23.1|16.9|22.5|
| Open Source Models|Open Source Models|Open Source Models|Open Source Models|Open Source Models|Open Source Models|Open Source Models|
| Model|Qwen3-32B|Qwen3-Coder|GPT-OSS (high) 20B|GPT-OSS (high) 120B|Nemotron-T-14B|Nemotron-T-32B|
| Size|32B|480B|20B|120B|14B|32B|
| Accuracy|3.37|23.9|3.10|18.7|<b>20.2</b>|<b>27.4</b>|  


(2025) demonstrate the potential of command-line proficiency, with frontier models showing promising results on benchmarks such as Terminal-Bench (Merrill et al., 2026). However, the training data mixtures behind these systems remain largely undisclosed, leaving fundamental questions about effective data design unanswered. This lack of transparency forces researchers into a costly trial-and-error process, primarily due to two significant bottlenecks in agentic data generation: (1) the scarcity of foundational resources, including diverse task prompts, requisite dependency files, and pre-configured environments; and (2) the logistical complexity of trajectory collection, as real-world human interactions are difficult to capture, while synthetic generation via LLM agents is prohibitively expensive due to the need for fresh environment instantiation and multi-turn interaction for every task. Current approaches to improving terminal capabilities fall into two main categories: improving agentic scaffolds (Antigma, 2025; Internet, 2025; JetBrains, 2025; Letta, 2025; Mux, 2025; Nichols, 2025; Singhal et al., 2025) or improving the underlying model for terminal use (Anthropic, 2025; DeepMind, 2025; Liu et al., 2025; MiniMax, 2025; Moonshot AI, 2025; OpenAI, 2025). One prominent approach for post-training models involves using adapters that wrap existing datasets in command-line interfaces (DCAgent, 2025; Development, 2025.). While the Terminal-Bench authors provide a repository of such adapters (Team, 2025) primarily for benchmark adaptation, these adapters can also be repurposed as a starting point for scaling training data. However, adapters inherit structural assumptions from source datasets never designed for sequential environment interaction, potentially limiting their effectiveness. Recent work has explored multi-agent frameworks (Austin, 2025; Peng et al., 2025) for more principled data generation, but these introduce computational complexity that scales poorly for large-scale training. The field thus lacks a practical framework that balances generation efficiency with the specific requirements of training effective terminal agents.  


We address this gap through a dual-strategy approach that combines dataset adaptation with synthetic task generation. Dataset adaptation provides broad coverage by transforming existing math, code, and software engineering datasets into Terminal-Bench format, efficiently scaling data volume while leveraging high-quality problem sources. Synthetic task generation offers finer-grained control: it enables targeted development of terminal-specific skills with control over task characteristics, such as difficulty, domain coverage, and primitive skill composition. These strategies are complementary and address distinct bottlenecks: adapters make the most of existing datasets to build foundational terminal capabilities at scale, while synthetic task generation provides the flexibility to target specific capability gaps. Building on this coarse-to-fine data generation pipeline, we develop Nemotron-Terminal, a family of models fine-tuned from Qwen3 models (Yang et al., 2025).  


Specifically, we make the following contributions:  


1. We introduce **Terminal-Task-Gen**, a scalable synthetic task generation pipeline that enables rapid exploration of task design and targeted generation for specific skills with different difficulty levels.  


2. We conduct a systematic study of data engineering strategies, examining filtering strategies for dataset adapters and synthetic tasks, curriculum learning for data mixing, long context training, and scaling trends.  


3. We conduct extensive experiments to validate the effectiveness of our curated dataset. As demonstrated in Table 1, on Terminal-Bench 2.0, our models achieve substantial improvements over the  


initial Qwen3 baselines, reaching competitive performance with significantly larger models while requiring only modest computational resources for training and inference. For example, our Nemotron-Terminal-32B outperforms Qwen3-Coder-480B (Yang et al., 2025) on Terminal-Bench 2.0 ($27.4 \pm 2.4$ vs. $23.9 \pm 2.8$). We release **Nemotron-Terminal models and Terminal-Corpus dataset** at https://huggingface.co/collections/nvidia/nemotron-terminal.  


# 2. Related Work  


## Agent Design.  


As seen through Claude Code (Anthropic, 2025) and Codex CLI (OpenAI, 2025), sophisticated agent scaffolding can significantly improve performance. Many leading terminal agents achieve frontier performance through innovations in scaffolding (Antigma, 2025; Internet, 2025; JetBrains, 2025; Letta, 2025; Mux, 2025; Nichols, 2025; Singhal et al., 2025). However, effective agent scaffolds are often model-specific and require extensive engineering. As base models improve, the marginal benefit of complex scaffolding will likely decrease. Rather than exploring variants in agentic design, we focus on scaling underlying model capabilities through targeted supervised fine-tuning.  


## Dataset Adapters.  


Several datasets on Hugging Face (DCAgent, 2025; Development, 2025,) collect agent execution traces by rolling out prompts from existing datasets through terminal environments. This approach can efficiently scale data collection by reusing existing prompts from different domains, including competitive coding and math. Despite the abundance of these datasets, no formal analysis has studied which characteristics of dataset adapters can affect downstream training effectiveness. In this work, we explore the strengths and weaknesses of this approach through a systematic study using custom datasets and adapters.  


## Synthetic Task Generation.  


Many studies have investigated how to effectively generate synthetic data for fine-tuning LLMs. Evol-Instruct (Xu et al., 2023) pioneered automated instruction data scaling through iterative in-depth and in-breadth evolution. Code Evol-Instruct (Luo et al., 2023) successfully adapted this strategy to automatically increase the complexity of code instruction data for effective fine-tuning. Since then, AgentInstruct (Mitra et al., 2024) and LAB (Sudalairaj et al., 2024) have demonstrated how to generate large-scale datasets from existing seed data through suggester-editor agent pairs and taxonomy-driven generation. Other works like MAGPIE (Xu et al., 2024) have explored extracting instruction data from aligned LLMs without seed data through unique prompting tactics.  


Recent work has explored bringing these ideas to scale terminal capabilities in LLMs, employing multi-agent systems to brainstorm ideas, generate tasks, design Docker environments, and validate generated tasks and environments (Austin, 2025; Peng et al., 2025). Since multi-agent systems can be time-consuming and costly, we design a simplified system that eliminates unnecessary coordination stages and optimizes environment validation to enable effective scaling. Through our systematic study and ablations, we provide actionable insights for scaling terminal-capable models.  


# 3. Background  


## 3.1. Terminal-Bench  


Terminal-Bench (Merrill et al., 2026; Team, 2025) has emerged as the standard benchmark for evaluating agents in terminal environments. The benchmark comprises 89 hand-crafted, human-verified tasks that span diverse domains including scientific computing, software engineering, machine learning, security, system administration, and data science. Unlike traditional code generation benchmarks that evaluate isolated functions, Terminal-Bench tasks require agents to complete end-to-end workflows, such as compiling code, training models, configuring systems, and debugging environments.  


As seen in Figure 2, each task in Terminal-Bench includes four components: (1) a natural language instruction describing the objective, (2) a containerized Docker (Merkel, 2014) environment providing the execution context, (3) a verification test suite that programmatically checks task completion, and (4) an oracle solution demonstrating a valid approach. Throughout this work, we use Terminal-Bench 2.0 as our primary evaluation benchmark and leverage Terminus 2, the model-agnostic reference agent released alongside the benchmark, for consistent evaluation across model checkpoints.  


![062a10c8b4905332b780d95247a72fa6.jpeg](images/3.png)

[Image: The image presents a hierarchical tree view of a `task_directory`, illustrating the organizational structure for a benchmark task. Key components include an `instruction.md` file and `task.toml` at the root, alongside directories for `environment`, `solution`, and `tests`. Within these subdirectories, specific files such as `Dockerfile`, `solve.sh`, and `test.sh` are shown, indicating the presence of execution contexts, reference solutions, and test cases respectively. Ellipses are used throughout the tree to represent additional, unlisted files or subdirectories within the structure.]  


>Figure 2: Terminal-Bench task directory structure.
Each task consists of an instruction prompt, task metadata, environment files, Dockerfile, reference solution, and test cases.  


![82e34f92a51874ccb990dade19269cea.jpeg](images/3-2.png)

[Image: This image displays a JSON-formatted object defining an agent's response structure. It includes fields for `analysis`, `plan`, and `commands`, where the commands list specific shell inputs like "ls -la" and "cd project" alongside a duration of 0.1 seconds. A final key, `task_complete`, is set to true, signaling the end of the task sequence. This structure matches the Terminus 2 agent scaffold prompt described in the figure caption.]  


>Figure 3: Terminus 2 agent response format. The Terminus 2 agent scaffold prompts the model to output responses in a JSON format, which includes: analysis, plan, commands, and task_complete.  


## 3.2. Terminus 2 Agent Framework  


Unlike traditional coding agents that provide multiple specialized tools, Terminus 2 (Team, 2025) only provides an interactive tmux session running inside a sandboxed Docker (Merkel, 2014) container. Through sending model-determined keystrokes to the tmux session, the agent has the flexibility to approach tasks using any available command-line tools.  


At each step, the agent receives the current terminal output, and the model is prompted to respond with a structured JSON format (Figure 3) that determines the next action sent to the environment.  


# 4. Synthetic Data Generation  


Training autonomous agents for terminal environments requires a systematic approach to data curation that balances breadth, depth, and scalability. We introduce a principled two-stage data generation framework: *dataset adaptation* for establishing broad foundational coverage, followed by *synthetic task generation* for targeted skill refinement. This coarse-to-fine strategy decouples data volume scaling from task design iteration: adapters efficiently leverage existing problem repositories to build general competencies, while synthetic generation enables precise control over skill composition, difficulty progression, and domain-specific requirements. Together, these complementary strategies yield a diverse, high-quality dataset for supervised fine-tuning (SFT) that systematically covers the operational and computational skills required for terminal-based problem solving.  


## 4.1. Dataset Adapters  


### 4.1.1. Prompt Datasets  


We selectively identify targeted high quality SFT prompt datasets that span the math, code, and software engineering (SWE) domains, since they are foundational to several of the topics covered in terminal use.  


#### Math Prompts.  


We use the Stage-2 prompt set from Nemotron-Cascade's math reasoning SFT data (Wang et al., 2025), which consists of 163K unique prompts drawn from OpenMathReasoning (Moshkov et al., 2025). To obtain this high-quality prompt set, Nemotron-Cascade filters out easy questions from the original datasets by excluding prompts whose DeepSeek-R1 (Guo et al., 2025) response length is shorter than 2K tokens.  


#### Code Prompts.  


We use the Stage-2 prompt set from Nemotron-Cascade's code reasoning SFT data, which consists of 79K prompts from OpenCodeReasoning (Ahmad et al., 2025) covering challenging coding problems. We further filter and deduplicate this set to obtain a 35K prompt subset.  


#### SWE Prompts.  


For software engineering tasks, we draw from Nemotron-Cascade's SWE code repair SFT data, which consists of 127K instances from SWE-Bench-Train (Jimenez et al., 2023), SWE-reBench (Badertdinov et al., 2025), SWE-Smith (Yang et al., 2025), and SWE-Fixer-Train (Xie et al., 2025). Each prompt includes a problem statement and the contents of one or more buggy code files. We further filter and deduplicate this set, resulting in 32K unique prompts.  


### 4.1.2. Adapter Format  


Dataset adaptation is a straightforward process that converts existing prompt datasets to Terminal-Bench format without requiring an LLM in the loop. Using the Terminus 2 system prompt template (Appendix A.2), we map each entry to the {instruction} placeholder, appending a unique instruction suffix based on the dataset type. The specific suffixes used for math, code, and SWE prompts are detailed in Appendix A.2. For each code file identified in a SWE prompt, we instantiate a corresponding file within the environment. As the Nemotron-Cascade datasets provide only prompts, these tasks consist of an instruction and environment, without associated test cases.  


## 4.2. Synthetic Task Generation  


While dataset adapters provide a foundational breadth of reasoning and code, they are inherently limited by the formats of their source repositories. To bridge the gap between general problem-solving and the specific rigors of terminal-based agency, we introduce **Terminal-Task-Gen**, a synthetic pipeline that generates executable tasks with precise control over skill complexity and environment constraints. By generating tasks from both structured seeds and a taxonomy of primitive skills, we ensure the training data directly reflects the operational nuances and multi-step tool interactions required for terminal agents.  


We present two complementary approaches for generating synthetic terminal operation tasks: **seed-based generation** and **skill-based generation**. Both methods leverage LLMs to produce diverse, executable terminal tasks while addressing distinct requirements of scalability, diversity, and domain coverage.  


### 4.2.1. Generation from Seed Data  


Seed-based generation complements dataset adaptation by using existing problems as inspiration, rather than as fixed templates. Instead of wrapping original prompts in a terminal scaffold, we prompt an LLM to synthesize new terminal tasks from seed problems. This approach is particularly effective for leveraging high-quality problem specifications from adjacent domains, such as scientific computing challenges, algorithmic problem sets, or domain-specific coding exercises, where well-defined problems exist but lack the terminal-oriented task structure required for agent training.  


#### Seed Data Structure.  


Each seed entry is a structured record containing: (1) a problem description specifying the computational challenge, (2) an optional domain label indicating the scientific or technical area (e.g., biology, physics, optimization), and (3) an optional reference solution providing a correct implementation. The reference  


solution, when available, serves as ground truth for generating test expectations but is never exposed to the
agent.  


#### Task Adaptation.  


The LLM acts as a task adapter that transforms each seed problem into a self-contained terminal task. This transformation involves several key operations. First, the abstract problem statement is augmented with concrete software engineering requirements: the agent must install necessary packages, read input from specified file paths, implement the solution, and write results to designated output locations. Second, the adapter generates realistic input data files that instantiate the problem with specific test cases, including edge cases and boundary conditions. Third, comprehensive pytest-based test cases are synthesized to verify correctness, which check output file existence, format compliance, numerical accuracy (with appropriate tolerances for floating-point results), and edge case handling. When a reference solution is provided in the seed data, it is included in the generation context, and the prompt instructs the LLM to use it as ground truth when designing the test cases.  


#### Conversion Guidelines.  


The conversion prompt encodes several principles to ensure task quality: complex problems are decomposed into verifiable units when necessary; practical constraints such as input sizes and precision requirements are added to ground the problem in realistic scenarios; and output formats are designed to enable unambiguous programmatic verification. This systematic adaptation enables the pipeline to convert diverse problem sources into a uniform task format suitable for agent evaluation.  


### 4.2.2. Generation from Primitive Skills  


Skill-based generation takes a fundamentally different approach: rather than adapting existing problems, it synthesizes novel tasks from a structured taxonomy of primitive terminal operation skills. We curate a list of primitive terminal operation skills and employ LLMs to expand and recombine these primitives into creative task specifications.  


#### Domain-Specific Generation.  


The task generation process is inherently domain-specific. We define 9 task domains: data processing, data querying, data science, debugging, dependency management, file operations, scientific computing, security, and software engineering. Each domain is associated with a dedicated generation prompt that guides the LLM to produce tasks aligned with the domain's focus areas. For instance, the data science prompt directs the model toward tasks involving statistical analysis and data transformation, whereas the security prompt emphasizes cryptographic operations and access control verification. This domain-aware prompting ensures that generated tasks exhibit coherent thematic focus while exercising skills appropriate to the target category.  


#### Skill Taxonomy.  


In each domain, primitive skills are collected and span multiple dimensions of terminal-based problem solving: (1) algorithmic skills such as graph traversal, constraint satisfaction, and backtracking search; (2) systems skills including file I/O, process management, and network configuration; (3) data processing skills such as parsing, serialization, and transformation pipelines; (4) mathematical skills including numerical integration and statistical modeling; (5) testing skills such as validation, verification, and benchmarking; and (6) web/security skills including HTTP handling, authentication, and vulnerability analysis. Skills for each domain are summarized in Appendix.  


#### Compositional Task Synthesis.  


The LLM is instructed to combine multiple primitives (typically 3–5 skills per task) in non-trivial ways, producing tasks that require integrated problem-solving rather than isolated skill application. Crucially, the generation prompt emphasizes *novelty*: the model is guided to invent new scenarios, thereby maximizing the diversity and coverage of the resulting tasks.  


>Table 2: DeepSeek-V3.2 performance on adapted math, coding, and SWE benchmarks. Using the Terminus 2 agent, we evaluate DeepSeek-V3.2 on AIME, LiveCodeBench, and SWE-bench Verified adapted to Terminal-Bench format, and we find that it performs reasonably well even under this terminal-based setting.  


| BENCHMARK (PASS@1)|DEEPSEEK-V3.2|
| ---|---|
| AIME 2024, AIME 2025|93.33|
| LIVECODEBENCH v6|67.20|
| SWE-BENCH VERIFIED|52.40|  


### 4.2.3. Task Format and Execution Environment  


Both generation methods produce tasks in a standardized format comprising: (1) a natural language task prompt specifying objectives and constraints, (2) pytest-based test cases with configurable weights for partial credit, (3) supplementary input files providing necessary data, and (4) a domain-specific Docker environment for consistent execution. The files are structured in the same way as Terminal-Bench, as shown in Figure 2. Note we do not generate oracle solutions, as producing ground-truth code is prohibitively difficult without human verification; instead, we generate tasks are easy to verify yet difficult to solve and use the synthesized test cases to evaluate the correctness of agent solutions.  


#### Solution Isolation.  


A key design principle enforced across all generation prompts is the separation between problem specification and solution information. All prompts explicitly instruct the LLM to avoid solution leakage: the task prompt visible to the agent must not reveal the algorithm, implementation approach, or any code that solves the problem. When reference solutions are available (e.g., in seed data), they are used exclusively for deriving ground-truth test expectations. This ensures that generated tasks require problem-solving rather than simple solution retrieval.  


#### Pre-Built Docker Images.  


A critical design decision that enables large-scale task generation is the use of **pre-built, domain-specific Docker images**. Rather than generating a unique Dockerfile per task similar to previous works (Austin, 2025; Peng et al., 2025), we maintain a fixed set of domain specific docker images, each pre-installing the packages and dependencies commonly required within that domain (e.g., pandas and scikit-learn for data science; cryptography libraries for security).  


This approach provides three scalability advantages. First, it *eliminates Dockerfile validation overhead*; by avoiding the costly multi-turn repair often needed for per-task environment generation, pre-built images enable efficient single-pass task creation. Second, it *reduces resource footprint*, utilizing just 9 shared base images instead of building and caching thousands of unique containers. Third, it *decouples environment and task generation*, allowing the pipeline to produce diverse scenarios within stable environments while retaining the flexibility for agents to install runtime dependencies.  


## 4.3. Teacher Model  


We select DeepSeek-V3.2 (Liu et al., 2025) as our teacher model for generating synthetic tasks and trajectories, motivated by its strong performance on Terminal-Bench 2.0 (Table 3). To further validate its suitability for producing dataset adapter trajectories, we evaluate DeepSeek-V3.2 on a few standard benchmarks adapted to Terminal-Bench format using the Terminus 2 agent framework (Table 2), including AIME 2024 (MAA, 2024), AIME 2025 (MAA, 2025), LiveCodeBench v6 (Jain et al., 2024), and SWE-bench Verified (Jimenez et al., 2023; OpenAI, 2024).  


## 4.4. Data Filtering  


We first decontaminate our SFT dataset by removing any prompt that has a 14-gram overlap with Terminal-Bench 2.0 test samples. Then, we apply various quality filters, including removing identity leaks and discarding responses that contain Chinese characters.  


Beyond quality filtering, we also experiment with removing incomplete trajectories generated by the teacher model to discourage the fine-tuned model from becoming overly verbose. When tests are available, we further experiment with only keeping trajectories that pass the tests.  


