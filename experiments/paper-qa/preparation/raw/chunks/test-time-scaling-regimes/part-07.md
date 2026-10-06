# D Reasoning LLMs and Evaluated Models

Open-weight reasoning models are trained or configured to emit intermediate steps for multi-step tasks in mathematics, science, and code (Guo et al., 2025; Yang et al., 2025a; Abdin et al., 2025). Their post-training methods use explicit reasoning traces, verifiable rewards, or preference signals, while inference interfaces determine how reasoning is elicited and budgeted. These choices afect reasoning accuracy, output length, and inference cost. Figure 1 presents a selective chronology of the model families.

## D.1 Common post-training pipeline archetypes

Open-weight reasoning pipelines recur in three post-training archetypes.

(1) SFT→RL pipelines. A common recipe first applies supervised fine-tuning (SFT) on curated chainof-thought (CoT) demonstrations (Wei et al., 2022), then uses reinforcement learning (RL) to optimize behavior under a reward signal. The reward may reflect verifiable correctness, human or model preferences, or conciseness. Examples include Sky-T1-7B (NovaSky Team, 2025c), Light-R1 (Wen et al., 2025), and Phi-4 reasoning variants (Abdin et al., 2025).

Adjacent designs use SFT-only distillation in the original Sky-T1 (NovaSky Team, 2025b), preference optimization in Sky-T1-Flash (NovaSky Team, 2025a), or branch–merge distillation in TinyR1 (Sun et al., 2025).

(2) Distillation-based pipelines. Distillation uses teacher-generated reasoning traces as SFT data for a smaller student. DeepSeek-R1 supplies traces for its distilled students (Guo et al., 2025), while OpenThoughts3 uses QwQ-32B as its trace generator (OpenThoughts Team, 2025e). Once the traces are fixed, the student is trained with cross-entropy SFT rather than an online RL stage. Workflows such as Bespoke-Stratos (Bespoke Labs, 2025a), OpenThoughts/OpenThinker (OpenThoughts, 2025), and Open-R1 (Hugging Face, 2025; Open-R1 Team, 2025e) difer in both data volume (from ∼10K to > 1M examples) and filtering procedures such as exact-match checks and unit tests.

(3) Parameter-space fusion and merging. A third line omits gradient updates during the merge stage and combines aligned pretrained or post-trained checkpoints directly in parameter space. Select–Calculate– Erase (SCE), for example, computes a structured weighted merge of aligned checkpoint parameters (Wan et al., 2025). Related FuseAI work includes distribution-level knowledge fusion (Wan et al., 2024a), the fusethen-merge pipeline of Wan et al. (2025), and SFT+DPO implicit fusion (Yang et al., 2025b); the FuseO1 family also uses SCE. Branch–merge schemes appear in TinyR1 (Sun et al., 2025). The merge stage requires no new training data, but it is restricted to compatible checkpoints.

## D.2 Cross-cutting mechanisms and inference controls

Four mechanism classes distinguish the systems in Figure 1 and Table 2: verified SFT and trace distillation, RL and preference optimization, inference-time control and aggregation, and parameter-space composition.

CoT distillation and verified SFT. CoT distillation transfers teacher-generated solution decompositions to a student through standard SFT. Reasoning pipelines may filter these traces with exact-match checks or unit tests before training (NovaSky Team, 2025b; Bespoke Labs, 2025a; OpenThoughts, 2025). When supervision includes human labels, annotator reliability is a separate source of error (Ghiasvand et al., 2026).

RL and preference optimization. RL-style post-training can optimize policies directly for correctness or preference-aligned behavior. In open-weight work, it appears as outcome-based RL in verifiable domains such as mathematics and code, or as preference optimization that penalizes unnecessarily long reasoning. Direct Preference Optimization (DPO) optimizes a preference objective without fitting the explicit reward model and value function used in Reinforcement Learning from Human Feedback (RLHF) (Rafailov et al., 2023; Ouyang et al., 2022). Reasoning-model objectives may prefer shorter correct chains or penalize redundant verification, as in Sky-T1-Flash (NovaSky Team, 2025a).

Inference-time scaling and aggregation. Test-time scaling methods allocate inference-time compute by sampling and aggregating multiple candidates, as in majority-vote self-consistency (Wang et al., 2023). Other controls set a “thinking budget” that extends or truncates deliberation, trading token use and latency against accuracy (Muennighof et al., 2025). These procedures modify the decision rule beyond the base conditional distribution and are therefore part of the evaluated system.

Model merging and fusion. Parameter-space fusion combines checkpoints without gradient updates. FuseO1 checkpoints (FuseAI, 2025a;b) use SCE merging to combine long-CoT and concise-answering models, and the merge itself requires no additional training data. Fusion can change reasoning length and response style while holding the backbone family and parameter count fixed.

## D.3 Comparison of representative open-weight reasoning models

Table 2 groups evaluated families and related reference models by post-training mechanism, training-data scale, base model, and inference controls. Because sampling, aggregation, and reasoning budgets can change performance without changing weights, benchmark reports must identify both the checkpoint and the inference protocol.

The mechanisms also impose diferent dependencies. Verified SFT depends on trace quality and filtering, while RL depends on reward construction and verification. Inference-time controls determine generation and evaluation cost. Parameter-space fusion instead requires compatible checkpoints and can change response length and style without changing the parameter count.

Table 2: Family-level comparison of representative open-weight reasoning models.

<table><tr><td>Model / Family</td><td>Paradigm</td><td>Training data</td><td>Base model</td><td>Technical remarks</td></tr><tr><td>DeepSeek-R1 (teacher)</td><td>SFT + RL (verifiable)</td><td>Multi-stage (cold-start + RL)</td><td>DeepSeek-V3-Base</td><td>R1-Zero applies RL from a base model; R1 adds cold-start data and multi-stage SFT/RL; teacher for open distillations (Guo et al., 2025).</td></tr><tr><td>DeepSeek-R1-Distill $^{\dagger}$ </td><td>Distillation (supervised fine-tuning)</td><td>~800k supervised samples (~600k reasoning)</td><td>Qwen2.5 (1.5B–32B), Llama-3.1-8B</td><td>Teacher-generated supervised fine-tuning into standard backbones across small and midsize models (Guo et al., 2025; DeepSeek-AI, 2025a).</td></tr><tr><td>QwQ-32B</td><td>RL reasoning</td><td>RL post-training (blog-reported)</td><td>Qwen2.5-32B</td><td>Dense 32B RL reasoner; reference “thinking” model used as teacher in multiple open pipelines (Qwen Team, 2025e;a).</td></tr><tr><td>Qwen3 Thinking $^{\dagger}$  (4B / 30B-A3B / Next-80B-A3B)</td><td>SFT + RL (thinking)</td><td>Long-CoT cold start + reasoning RL + mode fusion + distillation (Yang et al., 2025a)</td><td>Qwen3; sparse MoE variants</td><td>Thinking-specialized checkpoints; 4B and 30B variants report 262K context; Next-80B uses high-sparsity MoE + hybrid attention with GSPO for RL stability (Qwen Team, 2025c;b;d; Zheng et al., 2025).</td></tr><tr><td>s1 / s1.1 (SimpleScaling)</td><td>SFT-only (data-minimized) + inference-time control</td><td>1k curated, math-dominant CoTs</td><td>Qwen2.5-Instruct (multiple sizes)</td><td>Minimal SFT with termination control; compatible with sampling and aggregation protocols (Muennighoff et al., 2025).</td></tr><tr><td>Sky-T1 $^{\dagger}$  (NovaSky)</td><td>SFT + preference/RL</td><td>~17k curated prompts + preference pairs (Flash)</td><td>Qwen2.5-7B/32B</td><td>Rejection-sampled and verified traces; Flash uses length-sensitive preference optimization (SimPO-style) + optional rewriting (FCS+1) to reduce overthinking (Li et al., 2025a; NovaSky Team, 2025c;a).</td></tr><tr><td>Bespoke-Stratos $^{\dagger}$ </td><td>Distillation (verified SFT)</td><td>17k verified CoTs (math/code/sci)</td><td>Students: Qwen2.5-7B/32B / Teacher: DeepSeek-R1</td><td>Correctness-filtered distillation (exact-match math, unit tests for code); open Curator pipeline (Bespoke Labs, 2025a).</td></tr><tr><td>OpenThinker $^{\dagger}$  (OpenThoughts)</td><td>SFT-only (curated)</td><td>114k–1.2M reasoning traces (math/code/sci/puzzles)</td><td>Qwen2.5 (1.5B–32B)</td><td>Early releases test answer verification; OpenThoughts3 reports 1,000+ recipe experiments; Evalchemy evaluation (Guha et al., 2026).</td></tr><tr><td>Open-R1 $^{\dagger}$  (Distill)</td><td>SFT-only (verified)</td><td>350k verified traces (math/code/sci)</td><td>Qwen2.5-Math-7B</td><td>Mixture-of-Thoughts: verified DeepSeek-R1 traces; fixed checkpoint for scaling and verifiable-RL follow-ons (Hugging Face, 2025; Open-R1 Team, 2025e).</td></tr><tr><td>Open-R1 (Math) / OlympicCoder</td><td>SFT-only (verified/partial)</td><td>220k math (verified); CodeForces-CoTs (~100k traces; partial)</td><td>Qwen2.5-Math-7B; Qwen2.5-Coder-7B/32B</td><td>Math Verify with a judge fallback for 12% of math samples; code traces use public tests and are not exhaustively verified; decontamination is documented (Open-R1 Team, 2025f;a; Penedo et al., 2025).</td></tr><tr><td>LIMO / LIMO-v2 / LIMR† (GAIR)</td><td>SFT-only (data-minimized) + RL (verifiable)</td><td>800 curated math; 1.4k RL-selected items</td><td>Qwen2.5-32B-Instruct (LIMO); Qwen2.5-Math-7B (LIMR)</td><td>Small-data SFT and learning-impact selection for RL; v2 pairs an updated 800-example dataset with a 32B checkpoint (Ye et al., 2025; GAIR, 2025b;a; Li et al., 2025b).</td></tr><tr><td>Light-R1 / TinyR1† (Qihoo360)</td><td>SFT + preference/RL; merge (branch-merge)</td><td>76k + 3k CoTs; verified preference pairs</td><td>Qwen2.5; DeepSeek-R1-Distill backbones</td><td>Curriculum/step-wise SFT + DPO; GRPO on distilled variants; TinyR1 uses branch specialization followed by merging across domains (Wen et al., 2025; Sun et al., 2025).</td></tr><tr><td>FuseO1† (FuseAI)</td><td>Merge (parameter fusion)</td><td>N/A</td><td>DeepSeek-R1-Distill-32B, QwQ-32B-Preview, Sky-T1-32B (incl. Flash)</td><td>SCE-style parameter-space merging of long-CoT and concise models; requires no new data during merging (FuseAI, 2025c).</td></tr><tr><td>gpt-oss-20b† (OpenAI)</td><td>CoT RL (MoE)</td><td>CoT RL post-training (model card)</td><td>OpenAI MoE (21B total / 3.6B active)</td><td>MXFP4 quantization; low, medium, and high reasoning-effort settings vary token use, latency, and accuracy (OpenAI et al., 2025).</td></tr><tr><td>Phi-4 Reasoning† (Microsoft)</td><td>SFT + RL (verifiable)</td><td>Distilled traces + ~6k RL math</td><td>Phi-4 (14B)</td><td>Teachable-prompt selection + long-CoT SFT; outcome-based RL in “plus”; evaluated with inference-time budget and sampling controls (Abdin et al., 2025).</td></tr><tr><td>Nemotron Reasoning† (NVIDIA)</td><td>SFT-only (OpenReasoning); SFT + verifiable RL (AceReason)</td><td>Large-scale synthetic post-training</td><td>Qwen2.5 (OpenReasoning, AceReason); hybrid Mamba-Transformer (Nano v2)</td><td>OpenReasoning is SFT-only; AceReason uses SFT followed by verifiable RL; Nano v2 uses a hybrid Mamba-Transformer architecture (NVIDIA, 2025; Liu et al., 2025d; NVIDIA et al., 2025).</td></tr><tr><td>EXAONE-4.0† (LG AI)</td><td>SFT + preference/RL</td><td>Multi-domain math/code/science mixtures</td><td>EXAONE-4.0-32B / 1.2B</td><td>Unified modes (chat vs. reasoning); long-context support; preference/RL stages to balance correctness and verbosity (Bae et al., 2025).</td></tr></table>

† At least one checkpoint or configuration from this family appears in the 20-configuration repeated-mathematics roster in Section G.4. Unmarked rows provide broader field context for that roster.

### D.3.1 DeepSeek-R1 and distilled students: RL post-training and supervised distillation

DeepSeek-R1 uses large-scale RL on tasks with verifiable outcomes. DeepSeek-R1-Zero is trained with RL directly from a base model, without an SFT warm start. The report describes self-verification and reflection in its outputs, along with lower readability and language mixing. DeepSeek-R1 adds cold-start data, SFT, RL, and rejection sampling to address those output problems while retaining the reasoning behavior (Guo et al., 2025).

The DeepSeek-R1-Distill family transfers R1 outputs into standard dense backbones rather than running RL directly on smaller policies. The released students include Qwen2.5-based checkpoints at 1.5B, 7B, 14B, and 32B, and a Llama-3.1-based 8B checkpoint (Guo et al., 2025). The Hugging Face model cards report that the Qwen2.5 students are fine-tuned on ∼800K DeepSeek-R1-curated samples (DeepSeek-AI, 2025a). The project reports that these distilled checkpoints outperform its attempts to train smaller models directly with RL (DeepSeek-AI, 2025b).

### D.3.2 Qwen reasoning models: thinking-mode post-training and sparse MoE

Qwen treats “thinking” as an explicit post-training target and uses both dense and sparse-MoE architectures. QwQ-32B is a dense 32B model post-trained with RL; Qwen reports benchmark results comparable to DeepSeek-R1 and o1-mini (Qwen Team, 2025e;a). Unlike the distilled families above, QwQ-32B is posttrained directly for reasoning.

Qwen3 separates thinking and non-thinking behavior through a staged pipeline: long-CoT cold start, reasoning RL, “thinking mode fusion,” general RL, and strong-to-weak distillation (Yang et al., 2025a). The evaluated Qwen3-4B-Thinking-2507 checkpoint has no mode toggle and a reported 262K context window (Qwen Team, 2025c). Qwen3-30B-A3B-Thinking-2507 uses sparse MoE, with 30.5B total and 3.3B active parameters (128 experts, 8 active), and reports the same context length (Qwen Team, 2025b).

Outside the evaluated roster, Qwen3-Next-80B-A3B-Thinking combines hybrid attention with a highersparsity MoE. Its model card attributes RL stability and eficiency in this setting to Group Sequence Policy Optimization (GSPO) (Qwen Team, 2025d; Zheng et al., 2025). The checkpoint’s default prompt template enforces thinking mode.

### D.3.3 NovaSky: verified trace distillation and length control

The Sky-T1 line uses small verified corpora to train long-CoT behavior in instruction-tuned backbones; later variants add preference optimization or RL (NovaSky Team, 2025b;a;c).

Sky-T1-32B-Preview fine-tunes Qwen2.5-32B-Instruct on roughly 17K demonstrations distilled from QwQ-32B-Preview and selected by rejection sampling. The reported math and code results improve over the base model. In the paper’s perturbation experiments, shufling or deleting reasoning steps causes larger accuracy losses than perturbing surface tokens (Li et al., 2025a; NovaSky Team, 2025b).

Sky-T1-32B-Flash (NovaSky Team, 2025a) penalizes overthinking during training. It forms preference pairs from the shortest and longest correct candidates and adds hard-negative pairs that contrast a short incorrect answer with a long correct one on dificult prompts. The method then applies a length-sensitive, SimPO-style preference objective (Meng et al., 2024). An optional “FCS+1” rewrite retains the first correct mathematics solution and one additional solution; code outputs are not rewritten.

Sky-T1-7B (NovaSky Team, 2025c) uses an iterative SFT/RL schedule starting from Qwen2.5-Math-7B. It first applies SFT on a small verified set of QwQ-distilled traces, followed by RL with PRIME-style prompt filtering and rollouts on Eurus-2-RL-Data (Cui et al., 2026). A second distillation and SFT stage precedes the final RLOO-based RL stage (Ahmadian et al., 2024).

### D.3.4 Bespoke-Stratos: reasoning distillation as data curation

Bespoke-Stratos uses verified teacher traces as cross-entropy SFT data. The pipeline distills DeepSeek-R1 outputs into Bespoke-Stratos-17k and fine-tunes Qwen2.5-Instruct backbones at multiple scales (Be spoke Labs, 2025a).

Bespoke-Stratos-17k contains 16.7K examples produced with a Sky-T1-style distillation recipe (Bespoke Labs, 2025b). Candidate traces from DeepSeek-R1 are filtered by strict answer checks for mathematics and unit-test execution for code before SFT.

The project releases two checkpoints. Bespoke-Stratos-32B fine-tunes Qwen2.5-32B-Instruct on this dataset, and Bespoke-Stratos-7B applies the same procedure to Qwen2.5-7B-Instruct (Bespoke Labs, 2025c;d). The project reports improvements over both base models on its mathematics and code evaluations (Bespoke Labs, 2025a).

### D.3.5 OpenThoughts/OpenThinker: scaling supervised reasoning data

OpenThoughts studies SFT-only reasoning post-training with composed synthetic traces, testing how performance changes with the volume and composition of the supervision data (Guha et al., 2026; OpenThoughts, 2025).

The first release, OpenThoughts-114K (OpenThoughts Team, 2025c), generates long-form traces for mathematics, science, code, and puzzle prompts and verifies correctness before assembling the dataset. The corresponding OpenThinker models use cross-entropy SFT on Qwen2.5 instruction-tuned backbones and are evaluated with Evalchemy. This shared training and evaluation code supports comparisons between verified and unverified trace sets. Later ablations report that answer verification helps at 32B but hurts at 7B. OpenThoughts3 omits answer verification (Guha et al., 2026).

OpenThoughts2-1M contains one million curated examples and is used to train OpenThinker2-32B; the authors report matching DeepSeek-R1-Distill-32B on AIME and LiveCodeBench (OpenThoughts Team, 2025d;a). The OpenThoughts3-1.2M recipe was selected through more than 1,000 controlled experiments and uses QwQ-32B as its trace teacher (OpenThoughts Team, 2025e). OpenThinker3-7B is trained by SFT on the 1.2M-example mixture, reported as 850K mathematics, 250K code, and 100K science examples, and its model card reports results on AIME’25, LiveCodeBench, and GPQA Diamond (OpenThoughts Team, 2025b;e). The evaluation includes OpenThinker2-32B and OpenThinker3-1.5B, trained with the OpenThoughts2 and OpenThoughts3 recipes, respectively.

### D.3.6 OpenAI gpt-oss-20b

gpt-oss-20b is an MoE transformer post-trained with chain-of-thought RL (OpenAI, 2025b; OpenAI et al., 2025). It uses MXFP4 quantization and has approximately 21B total parameters, with 3.6B active per token. Its inference interface exposes three reasoning-efort settings: low, medium, and high (OpenAI, 2025a).

### D.3.7 Microsoft Phi-4 reasoning models

Microsoft’s Phi-4 reasoning line specializes a 14B foundation model through curated supervision and, for one variant, a short outcome-based RL stage. Starting from Phi-4 (Abdin et al., 2024), Phi-4-reasoning applies SFT to prompts described as “teachable” (diverse and challenging but within the student’s learnable regime), paired with long-form demonstrations from o3-mini. The report studies this prompt-selection criterion and evaluates longer reasoning budgets and repeated sampling as inference controls (Abdin et al., 2025).

Phi-4-reasoning-plus adds a short outcome-based RL stage that rewards final-answer correctness on a verified mathematics set. The report associates this stage with higher benchmark accuracy and longer average reasoning traces (Abdin et al., 2025). Microsoft also releases compact variants. Phi-4-mini-reasoning (3.8B) uses mid-training on distilled long-CoT data, long-CoT SFT, rollout-DPO preference optimization, and verifiable-reward RL for mathematics (Xu et al., 2025). Phi-4-mini-flash-reasoning uses a hybrid SambaY design and Diferential Attention for 64K-context reasoning (Microsoft, 2025). For a 2K-token prompt and 32K-token generation under vLLM, the accompanying work reports up to 10× the decoding throughput of Phi-4-mini-reasoning. It also reports higher scores on MATH-500, AIME 2024, AIME 2025, and GPQA Diamond, although the Flash variant does not use RL post-training (Ren et al., 2025).

### D.3.8 NVIDIA Nemotron reasoning models

The evaluated NVIDIA releases include OpenReasoning-Nemotron-1.5B, a dense Qwen2.5-derived SFT model for mathematics, code, and science (NVIDIA, 2025), and AceReason-Nemotron-1.1-7B, which uses an SFT-and-RL pipeline for mathematics and code (Liu et al., 2025d). Related NVIDIA work releases the OpenMathReasoning (Moshkov et al., 2025) and OpenCodeReasoning (Ahmad et al., 2025a;b) data and model pipelines.

NVIDIA-Nemotron-Nano-9B-v2 uses a hybrid Mamba–Transformer architecture with controllable reasoning (NVIDIA et al., 2025). The roster therefore contains a 1.5B dense baseline, a 7B SFT-and-RL specialist, and a 9B hybrid model with reasoning controls.

### D.3.9 Open-R1 and OlympicCoder: open reproductions for math and competitive programming

Open-R1 (Hugging Face, 2025) publishes a staged reproduction of DeepSeek-R1-style post-training, including its data mixtures, verification procedures, and inference protocols.

A central component is Mixture-of-Thoughts (Open-R1 Team, 2025b), a ∼350K dataset of verified traces distilled from DeepSeek-R1 across mathematics, code, and science. OpenR1-Distill-7B is trained by SFT on this mixture and provides a fixed checkpoint for analyzing repeated sampling, aggregation, and subsequent verifiable-reward RL (Open-R1 Team, 2025e). Open-R1 also provides a mathematics-only corpus, OpenR1- Math-220k, derived from NuminaMath 1.5 with multiple traces per problem and automatic verification by Math Verify. When rule-based checks are insuficient, Llama-3.3-70B-Instruct is the fallback judge; the dataset card reports that this applies to 12% of samples (Ben Allal et al., 2025; Open-R1 Team, 2025f).

OlympicCoder applies the same approach to competitive programming, where verification depends on test coverage. CodeForces-CoTs contains more than 10K CodeForces problems and nearly 100K C++/Python traces generated by DeepSeek-R1. The dataset is not exhaustively filtered; about 84% of its Python solutions pass the public tests (Open-R1 Team, 2025a). OlympicCoder-7B and OlympicCoder-32B fine-tune Qwen2.5-Coder instruction models on decontaminated CodeForces-style CoT planning data and are evaluated on an IOI’2024 subset, LiveCodeBench, and other standardized competitive-programming benchmarks (Open-R1 Team, 2025d;c; Penedo et al., 2025). The mathematics corpus uses automatic verification with an LLM fallback judge, whereas the code corpus relies on public tests and is only partially verified.

### D.3.10 GAIR “Less is More”: data-minimized reasoning and impact-aware RL

GAIR’s “Less is More” line tests whether data selection can substitute for training-set volume. For LIMO, candidate solutions to 2,125 mathematics problems are sampled from DeepSeek-R1, DeepSeek-R1- Distill-Qwen-32B, and QwQ-32B. The highest-scoring solution for each problem is retained, the resulting problem–solution pairs are ranked, and the top 800 are used to fine-tune Qwen2.5-32B-Instruct (Ye et al., 2025). The study evaluates the resulting checkpoint with additional inference-time compute, treating data selection and inference allocation as separate choices. LIMO-v2 pairs an updated 800-example dataset with a corresponding Qwen2.5-32B-Instruct checkpoint release (GAIR, 2025b;a).

LIMR introduces Learning Impact Measurement (LIM), which selects RL prompts by matching reward trajectories to the model’s learning dynamics. In its experiments, RL on 1,389 selected prompts matches or exceeds RL on the full 8,523-prompt pool. The reported comparison also difers by model scale: the smallest SFT sets work best at larger scales, whereas LIM-selected RL improves the smaller models tested (Li et al., 2025b).

### D.3.11 FuseAI/FuseO1: parameter-space merging

Checkpoint merging combines trained models directly in parameter space without gradient updates. FuseAI studies heterogeneous model fusion (Wan et al., 2025).

FuseAI work includes distribution-level knowledge fusion (Wan et al., 2024a), FuseChat’s fuse-then-merge pipeline (Wan et al., 2025), and SFT+DPO implicit fusion (Yang et al., 2025b). FuseChat introduces SCE (Select–Calculate–Erase), a parameter-matrix merge rule built around fusion vectors (weight diferences from a pivot) and a structured per-matrix procedure (Wan et al., 2025). The FuseO1 family combines DeepSeek-R1-Distill-Qwen-32B, QwQ-32B-Preview, and Sky-T1-32B variants through SCE, without gradient updates or new data during the merge (FuseAI, 2025c;a;b). Including a Flash parent is intended to combine long- and short-reasoning behavior.

### D.3.12 Light-R1 and TinyR1: curriculum post-training and branch–merge distillation

Light-R1 uses curriculum-style post-training to induce long-CoT behavior; TinyR1 trains domain-specific branches and then merges them.

Light-R1 uses two-stage curriculum SFT followed by semi-on-policy DPO to train long-form reasoning and response style (Wen et al., 2025). In its “from scratch” setting, Light-R1-32B starts from Qwen2.5-32B-Instruct and uses mathematics-focused data (Qihoo360, 2025b). A 3K “stage-2” hard long-CoT set is then applied to DeepSeek-R1-Distill-Qwen checkpoints, producing Light-R1-7B-DS and Light-R1-32B-DS (Qihoo360, 2025d;c). The report attributes higher benchmark scores for these students to the additional SFT stage. GRPO post-training produces Light-R1-14B-DS; the report observes higher reward alongside longer outputs (Wen et al., 2025; Qihoo360, 2025a).

TinyR1-32B-Preview uses Branch–Merge Distillation. It distills DeepSeek-R1 into domain-specific branches through SFT and then merges them. Relative to DeepSeek-R1-Distill-Qwen-32B, the paper reports average gains of 5.5 points in mathematics, 4.4 in code, and 2.9 in science. TinyR1 also approaches DeepSeek-R1 on AIME’24 under the reported evaluation settings (Sun et al., 2025).

### D.3.13 SimpleScaling s1.1: small-data SFT and budget forcing

SimpleScaling’s s1.1 family uses SFT on a small curated reasoning set and budget forcing at inference time, replacing the earlier Gemini-generated traces with DeepSeek-R1 traces. Budget forcing truncates or extends a reasoning trace to control test-time compute (Muennighof et al., 2025).

Across several Qwen model sizes, s1.1 combines sequential budget forcing with parallel methods such as majority voting and REBASE; s1.1-32B is the primary reference model (Muennighof et al., 2025).

### D.3.14 LG EXAONE-4.0: unified chat and reasoning modes

EXAONE-4.0 treats chat-style assistance and explicit reasoning as two modes of one model family. Its unified post-training recipe jointly trains non-reasoning and reasoning behavior, followed by preferencelearning stages for correctness, brevity, and language consistency in the 32B and 1.2B models (Bae et al., 2025).

The 32B model uses a 3:1 ratio of sliding-window to global-attention layers, removes rotary positional embeddings from global-attention layers, and applies QK-Reorder-Norm. Long-context post-training accompanies these architectural changes. Post-training includes an RL stage and multi-turn, long-horizon tool-use examples with execution feedback (Bae et al., 2025).

# E Prompt and Inference Interfaces

Configurations use their model-native reasoning interfaces. Most receive a zero-shot mathematics instruction requesting step-by-step reasoning and a boxed final answer; gpt-oss also uses low, medium, and high efort controls. Scoring uses the extracted final answer. In the repeated-mathematics block, gpt-oss prompt coverage varies by task, as detailed in Section G.4.

# F Aggregation Reference Interface

The reference interface implements the aggregation protocol in Section 3.3 through three stages: evidence reducers map confidence or reward signals to candidate scores; fixed-bank rules select an answer from aligned answer and score arrays; and online predicates decide whether to stop sampling or generation from the history observed so far. Separating these stages allows the same candidate bank to be evaluated under several decision rules and the same rule to be paired with diferent evidence sources, without conflating candidate generation with post-generation selection.

The interface accepts a one-dimensional candidate bank for one problem or a two-dimensional array for a batch. Score-free consensus, score-based selection, and across-rollout stopping use the same extracted-answer representation. Fixed-bank routines may also return the index of a representative candidate when the selected answer needs a rationale. In Listing 1, plurality selects “A”, whereas Best-of-N and softmax-weighted voting select “B”; the causal stopping predicate reads only the revealed answer prefix.

```julia
answers = ["A", "A", "A", "B"]
scores = [0.30, 0.30, 0.30, 0.85]

plurality = agg.majority_vote(answers)    # "A"
best = agg.best_of_n(answers, scores)    # "B"
weighted = agg.softmax_weighted_vote(
    answers, scores, temperature=0.1
)
observed = ["A"] * 8 + ["B"] * 2
stop, probability = agg.adaptive_consistency_stop(
    observed, threshold=0.95, return_prob=True
)
# (True, 0.9673...)
```  
Listing 1: Reference-interface pseudocode for fixed-bank aggregation and causal stopping. Higher candidate scores indicate stronger evidence.

