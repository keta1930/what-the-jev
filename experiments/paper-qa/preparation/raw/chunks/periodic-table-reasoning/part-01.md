# The Periodic Table of LLM Reasoning: A Structured Survey of Reasoning Paradigms, Methods, and Failure Modes

Avinash Anand Avinash.Anand@singaporetech.edu.sg SIT × Nvidia AI Center (SNAIC)

Mahisha Ramesh mahisha23121@iiitd.ac.in MIDAS Lab, IIIT Delhi

Avni Mittal avni.mittal2002@gmail.com MIDAS Lab, IIT Mandi

Ashutosh Kumar ak1825@rit.edu Owl Autonomous Imaging, Inc. <sup>∗</sup>

Rishitej Reddy Vyalla rishitej23439@iiitd.ac.in MIDAS Lab, IIIT Delhi

Erik Cambria cambria@ntu.edu.sg Professor, College of Computing & Data Science, NTU Singapore

Zhengkui Wang zhengkui.wang@singaporetech.edu.sg Associate Professor, Director, SIT × Nvidia AI Center (SNAIC)

Timothy Liu timothyl@nvidia.com NVIDIA AI Technology Centre, Singapore

Aik Beng Ng aikbengn@nvidia.com NVIDIA AI Technology Centre, Singapore

Simon See ssee@nvidia.com NVIDIA AI Technology Centre, Singapore

Rajiv Ratn Shah rajivratn@iiitd.ac.in Associate Professor, Department of Computer Science and Engineering, IIT Kanpur

# Abstract

Reasoning is now a primary focus of how we evaluate, improve, and interpret Large Language Models (LLMs), covering Chain-of-Thought (CoT) inference, mathematical problemsolving, multi-hop question answering, code generation, retrieval-augmented reasoning, tool use, and multimodal decision-making. In this survey, we present the Periodic Table of LLM Reasoning, a structured framework to categorize more than 300 recent papers along reasoning paradigms, methodological mechanisms, evaluation settings, and common failure modes. This paper classifies LLM reasoning into nine major paradigms: Chain-of-Thought reasoning, Multi-Hop reasoning, Mathematical reasoning, Commonsense reasoning, Visual and Temporal reasoning, Code and Algorithmic reasoning, Retrieval-Augmented reasoning, Tool-Augmented or Agentic reasoning, and Reinforcement reasoning on learning. We discuss the most prominent methods for each paradigm, including prompting strategies, architectural interventions, supervised fine-tuning, verifier-guided inference, reward modeling, retrieval mechanisms, tool interfaces, agentic workflows, and benchmark design. The paper argues that LLM reasoning is not a single emergent capability but a family of scafolded behaviors that are shaped by the interaction between a model scale, task structure, external memory, supervision signals, and evaluation protocols. We also synthesize recurring failure modes across paradigms, including reasoning hallucinations, brittle multi-step inference, spurious rationales, weak causal grounding, poor out-of-distribution generalization, benchmark contamination, and unreliable self-verification. Although many recent methods have shown improvements in specific reasoning settings, we observe that it is often hard to compare progress across paradigms, as gains might come from prompting, retrieval, verifier design, or benchmark-specific structure rather than from more general reasoning ability. The survey connects reasoning methods with their assumptions, strengths, and ways of failing, providing a reference map of the current field and a diagnostic framework for assessing future work. More generally, we argue that robust LLM reasoning will require systems that go beyond isolated task performance to support meta-reasoning, multimodal and temporal grounding, adaptive tool use, and principled evaluation of reasoning under distribution shift.

# 1 Introduction

LLMs have shown strong empirical performance on diverse reasoning tasks (White et al., 2025); however, the depth, generality, and reliability of their reasoning abilities remain contested. This survey synthesizes existing work to examine the reasoning capabilities of LLMs, their limitations, and the open challenges in evaluating and improving reasoning capabilities (Figure 1). The core question motivating this work: can reasoning abilities emerge in LLMs without task-specific reasoning supervision? While earlier neural language models relied largely on surface-level pattern matching and statistical regularities (Geirhos et al., 2020; McCoy et al., 2019; Tenney et al., 2019), recent large-scale transformer LLMs have demonstrated increasingly complex reasoning behaviors, including multi-step inference, compositional reasoning, temporal consistency, and limited causal or counterfactual reasoning (Wei et al., 2022a;b; Chowdhery et al., 2023). Nevertheless, these capabilities remain fragile and highly sensitive to prompting strategies, task formulation, distribution shift, and evaluation methodology (Gendron et al., 2023; Berglund et al., 2024).

Prompting plays a central role in eliciting LLM capabilities. Techniques such as zero-shot prompting (Xian et al., 2018; Kojima et al., 2022), few-shot prompting (Brown et al., 2020), and chain-of-thought (CoT) prompting (Wei et al., 2022b) demonstrate that the same model can exhibit qualitatively diferent behaviors depending on how a task is framed. This sensitivity has motivated extensive study of the interactions among model architecture, scale, and prompting strategies as mechanisms for reasoning. Although larger models generally achieve stronger reasoning performance, scale alone does not guarantee robust reasoning ability. Many reasoning behaviors emerge only when suficient scale is paired with appropriate instruction tuning, prompting structure, and contextual guidance.

Transparency and interpretability present additional challenges for reasoning in LLMs. Although techniques such as chain-of-thought prompting (Wang et al., 2023) expose intermediate reasoning traces (Wei et al., 2022b), it remains doubtful whether these traces faithfully reflect the underlying computational processes (Lyu et al., 2023) or merely plausible post hoc rationalizations. This raises broader questions about whether LLM reasoning aligns with human-interpretable logical structure or instead emerges from statistical patterns learned during training (Kadavath et al., 2022). As LLMs are increasingly deployed in high-stakes and real-world settings, understanding how models arrive at conclusions becomes as important as evaluating the correctness of their outputs.

Despite recent progress, LLMs continue to exhibit important limitations, particularly in handling ambiguity and contradiction, distinguishing correlation from causation, transferring reasoning across domains, and grounding knowledge in physical or experiential reality (Teo et al., 2025). These shortcomings have motivated the development of retrieval-augmented (Lewis et al., 2020), tool-augmented (Schick et al., 2023), and modular reasoning systems that combine language models with external memory, search, symbolic tools, or execution environments (Yao et al., 2022). While such hybrid approaches often improve reliability and factual consistency, they also raise foundational questions about whether reasoning should be understood as a monolithic capability or as a composition of separable cognitive sub-processes (Budagam et al., 2024).

![](images/5395320e4e82947d3c53ce413aafbd01c284c6850dda054b0318eee9fdea59d2.jpg)

[Image: The image presents a three-part conceptual diagram detailing the internal architecture of reasoning in language models. The first section, "What the model sees," defines "In-Context Memory" as the visibility of the full token sequence and prior reasoning steps treated as plain text. The middle section, "From tokens to a distribution," explains "Parametric Knowledge" where facts are encoded in frozen MLP weights and processed through attention mechanisms to form a probability distribution. The final section, "The probabilistic exit," asserts "No Symbolic Engine," noting that planning and arithmetic are constrained to the textual context or parametric stack rather than a specialized symbolic component.]  
Figure 1: The foundational mechanism diagram. Shows one forward pass: context stream → layers → distribution → sampled token. Annotated to show where in-context info lives vs parametric knowledge vs attention, so students see that "reasoning" is repeated next-token prediction.

This survey also examines reasoning in LLMs across multilingual and multimodal settings (Achiam et al., 2023; Zhang et al., 2023), mathematical and symbolic problem solving (Hendrycks et al., 2021), and aspects of social and commonsense cognition. We compare these behaviors with human reasoning patterns while considering the extent to which current architectures genuinely perform structured reasoning versus simulating its observable outputs. Finally, we discuss meta-reasoning and self-reflective inference, where models evaluate and revise their own intermediate reasoning processes, as a potentially important direction for improving robustness, calibration, and generalization in future systems (Shinn et al., 2023; Madaan et al., 2023).

The primary contributions of this survey are as follows:

• We develop a structured taxonomy of reasoning paradigms (Figure 2) in LLMs, covering approaches such as Chain-of-Thought, Multi-Hop, Mathematical, Commonsense, Multimodal, Retrieval-Augmented, Tool-Augmented, and Reinforcement Learning-based reasoning.

• We examine methodological trends across the literature, including prompting strategies, architectural design choices, training paradigms, and evaluation benchmarks to assess reasoning capabilities.

• We analyze recurring limitations and failure modes in LLM reasoning, including hallucinated reasoning traces, brittle multi-step inference, poor causal generalization, and sensitivity to prompting and task formulation.

• We synthesize emerging research directions, including meta-reasoning, self-reflective and selfimproving reasoning frameworks, multimodal reasoning, and socially grounded reasoning systems.

• We discuss open research challenges and highlight directions toward more robust, interpretable, and generalizable reasoning systems.

# 2 Methodology

This survey takes the canonical inspirations from a few established systematic review practices (Moher et al., 2009; Keele et al., 2007; Jesson et al., 2011)and follows a structured review methodology. This involves creating search parameters, selecting databases, applying inclusion and exclusion filters, and assessing the quality of each paper based on empirical rigor, relevance, reproducibility, and overall research impact.

![](images/487aba64fd7f62c5f4a9f498cd60184ff2e3f0804f41f136a00d3b038b06fded.jpg)

[Image: This image displays a structured taxonomy of reasoning methods organized into a 6x6 grid containing 36 distinct entries. The categories are defined by six column headers ranging from Stepwise Decomposition to Cross-Boundary, which correspond to a color-coded legend at the top featuring blue, purple, orange, yellow, red, and green indicators. Each numbered card, from 01 to 36, presents a specific technique like "Chain-of-Thought" (Co) or "Retrieval-Augmented" (RAG) along with a brief definition describing its function. This systematic chart categorizes various algorithmic strategies, grouping them by characteristics such as their use of intermediate steps, domain expertise, or learning mechanisms.]  
Figure 2: A taxonomy of LLM reasoning paradigms. Thirty-six families of methods are arranged into a $6 \times 6$ grid: columns group paradigms by how reasoning is composed (stepwise decomposition, domain-specific, contextual & grounded, augmented, learning & reflective, and cross-boundary), while rows situate them along a cognitive spectrum from training foundations up to high-level cognition.

## 2.1 Search Process

We began by identifying relevant keywords that represent the types of reasoning in LLMs. The broader terms include “large language models”, “reasoning”, “chain of thought reasoning”, “multi-hop reasoning”, and “commonsense reasoning”.

![](images/1e0c456bb05731640059a05ec2832eed20b43172cc3ee4e9881c656dc2d42c45.jpg)

[Image: This diagram illustrates the process of an LLM solving a math problem across three distinct columns: "Pipeline," "Worked Example," and "Inside the Model." The left column outlines five sequential abstract stages—Input, Parse, Reason, Execute, and Answer—using icons and brief descriptions. The center column applies these stages to a specific word problem ("A train travels 60 km in 1.5 h"), demonstrating the extraction of variables, formula substitution ($v = d/t$), and arithmetic calculation. The right column details the internal mechanisms driving these actions, such as token-level attention for parsing, decoder logic for generating intermediate computation tokens, and conditions for verifying unit consistency.]  
Figure 3: Mathematical reasoning flow. Left: the generic LLM reasoning pipeline. Middle: a math-specific worked example aligned stage-by-stage. Right: what happens inside the model at parsing, computation, and verification.

A list of more specific keywords was added for each reasoning type, such as for mathematical reasoning: “mathematical reasoning”, “equation solving by LLMs”, and “symbolic reasoning”; for visual reasoning: “image-text reasoning” and “visual commonsense reasoning”; for RAG-based reasoning: “RAG models” and “information retrieval for reasoning”; for code reasoning: “algorithmic reasoning” and “program synthesis with LLMs”; for tool-augmented reasoning: “agentic reasoning” and “external tools.” Then, we performed an expanded search using the combinations of Boolean operators and keyword variants to maximize coverage across reasoning paradigms and terminology diferences across multiple venues. Conclusively, the keyworddriven approach covered both theoretical and applied work on LLM reasoning. The duplicate entries across databases were removed with manual supervision, and papers were screened based on title, abstract, introduction, and full-text relevance where necessary.

## 2.2 Databases

We conducted a systematic search across several academic databases and research repositories to identify peer-reviewed publications and high-impact preprints related to language modeling. The sources included:

• IEEE Xplore, for peer-reviewed conference proceedings, journal articles, and technical standards in computer science and artificial intelligence.

• Google Scholar, for broad interdisciplinary coverage and citation-based discovery of influential journal articles, conference papers, and preprints.

• ACM Digital Library, for peer-reviewed journals and conference proceedings in computing, artificial intelligence, and related fields.

• arXiv, for recent preprints that provide early access to emerging research prior to formal peer review.

• SpringerLink, for journal articles, conference proceedings, and scholarly books ofering theoretical and methodological perspectives.

• Papers with Code, for identifying research papers accompanied by publicly available implementations, datasets, and benchmark results, thereby supporting reproducibility and empirical comparison.

## 2.3 Inclusion and Exclusion Criteria

Given the deliberately broad scope of the search, the initial set of retrieved records contained both studies outside the survey’s focus and duplicate entries across databases. Thus, to improve the relevance and consistency of the final corpus, we applied predefined inclusion and exclusion criteria during the screening process as shown in Table 1.

<table><tr><td>Dimension</td><td>Include</td><td>Exclude</td></tr><tr><td>Topic relevance</td><td>Addresses one or more listed reasoning types (e.g., CoT, Multi-Hop)</td><td>Does not primarily address a listed reasoning type</td></tr><tr><td>Venue &amp; review status</td><td>Peer-reviewed journal or conference; preprints only if widely cited, adopted in benchmarks, later accepted, or needed for very recent developments</td><td>Non-peer-reviewed source (blog, white paper, preprint) without strong citation impact</td></tr><tr><td>Recency</td><td>Published within the last 5 years, unless a seminal paper</td><td>Older than 5 years with no historical significance</td></tr><tr><td>Methodological clarity</td><td>Methods described clearly (training schemes, models, experiments)</td><td>Lacks methodological detail or sufficient experimental validation</td></tr><tr><td>Novelty</td><td>Presents novel techniques, theories, or applications</td><td>Substantially duplicates another included paper</td></tr><tr><td>Empirical evidence</td><td>Reports results with performance metrics (accuracy, precision, recall) when applicable</td><td>Lacks technical depth or reports no empirical results</td></tr></table>

Table 1: Inclusion and exclusion criteria applied to candidate papers.

## 2.4 Quality Assessment

We developed eight Quality Assessment Criteria (QACs) to evaluate the relevance, rigor, clarity, and impact of each candidate study. Each criterion was rated qualitatively using a four-point scale: poor, fair, good, or excellent. The assessment supported consistent comparison across studies and informed their selection and prioritization for inclusion in the survey.

• QAC1 (Contribution): To what extent does the study advance the understanding or capability of the reasoning paradigm it investigates?

• QAC2 (Clarity): Are the study’s motivation, methodology, and findings presented clearly enough to be understood by readers outside the immediate subfield?

• QAC3 (Theoretical and practical relevance): Does the study address both the theoretical foundations and practical implications of the proposed approach?

• QAC4 (Experimental rigor): Are the experiments suficiently rigorous in terms of dataset size, benchmark coverage, baseline selection, evaluation metrics, ablation studies, and experimental controls?

• QAC5 (Scholarly impact): Has the study demonstrated substantial research influence, considering its citation count relative to its publication age?

• QAC6 (Research novelty): Does the study investigate an under-explored problem, reasoning capability, methodology, or application area?

• QAC7 (Positioning within the literature): Does the study adequately contextualize its contributions and distinguish them from related work?

• QAC8 (Reproducibility): Are the experimental configuration, datasets, evaluation procedures, implementation details, and availability of code or data documented suficiently to support replication?

## 2.5 Data Collection and Analysis

The collected papers were organized into a database annotated with metadata (title, authors, year, and primary focus) and categorized by reasoning type. Figure 4 shows the distribution across reasoning types in LLMs, and Figure 5 tracks publication volume per category over time. We analyzed the collection to identify recurring themes, methodological trends, and gaps in coverage.

![](images/d8d049b9998907b576917465a928ca0428d2dcfba779f2cb6e027e9c4899bdb9.jpg)

[Image: This horizontal bar chart illustrates the distribution of collected research papers across fourteen distinct reasoning categories related to Large Language Models. The x-axis indicates the "Number of papers," ranging from 0 to over 30, while the y-axis lists the categories in descending order of frequency. The "Code/Algorithmic" category has the highest count with 33 papers, followed by "Meta-Reasoning/Self-Evolving" at 31, whereas the lowest counts are observed for "Temporal" and "Commonsense" reasoning, each appearing in 10 papers. Multiple intermediate categories, including "RAG-based" and "Chain-of-Thought," show counts ranging between 22 and 28.]  
Figure 4: Distribution of research papers by reasoning paradigm.

Based on the collected literature, we developed a hierarchical taxonomy of reasoning paradigms and their associated sub-problems, as illustrated in Figure 6. This framework supports a large-scale synthesis of prior work across prompting strategies, model architectures, training objectives, and evaluation settings. The resulting taxonomy not only organizes the literature into interconnected reasoning categories but also reveals shared methodological patterns, recurring limitations, and emerging directions for future research.

# 3 Types of Reasoning

Reasoning in LLMs is typically understood as the ability to perform structured transformations on a given information to derive conclusions, solve multi-step problems, generalize across contexts, or generate coherent intermediate inferences. Unlike classical symbolic AI systems, where reasoning is explicitly encoded through formal rules and logical operators, reasoning in LLMs emerges implicitly through large-scale language modeling and is observed primarily through model behavior during inference. It is often evaluated operationally, by examining whether models can sustain coherent chains of inference, integrate distributed information, perform abstraction, adapt across domains, or revise conclusions under new evidence.

Diferent reasoning paradigms emphasize diferent capabilities and computational structures. Some focus on explicit intermediate reasoning traces, such as Chain-of-Thought and Multi-Hop reasoning, while others emphasize domain-specific competence, including Mathematical and Code/Algorithmic reasoning. Additional paradigms address contextual and grounded understanding, such as Commonsense, Visual, Temporal, and Social reasoning. Recent work further extends reasoning through external augmentation mechanisms, including RAG and Tool-Augmented systems, as well as through reflective and adaptive frameworks such as

Publication Trends Across Reasoning Paradigms

<table><tr><td></td><td>≤2022</td><td>2023</td><td>2024</td><td>2025</td></tr><tr><td>Chain-of-Thought</td><td>0</td><td>0</td><td>11</td><td>16</td></tr><tr><td>Multi-Hop</td><td>0</td><td>0</td><td>15</td><td>1</td></tr><tr><td>Mathematical</td><td>0</td><td>0</td><td>8</td><td>19</td></tr><tr><td>Commonsense</td><td>1</td><td>4</td><td>3</td><td>2</td></tr><tr><td>Visual/Multimodal</td><td>1</td><td>0</td><td>6</td><td>18</td></tr><tr><td>Temporal</td><td>6</td><td>2</td><td>9</td><td>5</td></tr><tr><td>Code/Algorithmic</td><td>1</td><td>5</td><td>11</td><td>16</td></tr><tr><td>RAG-based</td><td>0</td><td>5</td><td>11</td><td>12</td></tr><tr><td>Tool-Augmented</td><td>0</td><td>2</td><td>11</td><td>14</td></tr><tr><td>RL for Reasoning</td><td>0</td><td>0</td><td>8</td><td>20</td></tr><tr><td>Multilingual</td><td>6</td><td>2</td><td>9</td><td>5</td></tr><tr><td>Meta-Reasoning</td><td>0</td><td>1</td><td>15</td><td>15</td></tr><tr><td>Social/Cognitive</td><td>2</td><td>3</td><td>4</td><td>7</td></tr></table>

Figure 5: Distribution of publications by reasoning paradigm and year. Darker cells indicate higher publication volume.

RL-based and Meta-Reasoning approaches. This section organizes these paradigms into a unified taxonomy of reasoning behaviors studied in modern LLMs.

