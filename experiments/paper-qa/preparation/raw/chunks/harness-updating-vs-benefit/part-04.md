# C Evolver-side Analysis Details in Sec. 4.2

## C.1 Additional Results for Observation 1

Tab. 5 reports the pass rate of each anchor agent (Opus 4.6, Sonnet 4.6, Qwen3-235B) under each evolver on the three benchmarks, alongside the resulting $\Delta _ { \mathrm { u p d a t e } }$ . These are the per-cell numbers underlying the bars in Fig. 3.

## C.2 More Details of the Case Study

We elaborate on the case study from Sec. 4.2. We examine the SkillsBench task flink-query with the agent backbone fixed at Opus 4.6, comparing its trajectories under three evolver conditions (Fig. 4): no evolver, Qwen3.5-9B as evolver, and Opus 4.6 as evolver. Without an evolver, the agent omits the FINISH-event filter and scores 0.67; with either evolved skill injected at turn 0, the same agent solves the task (score 1.0).

![](images/00643c05a4fde651bb6422905f1c6e1c770488974d5674a2f57fa2e7ee825590.jpg)

[Image: This chart plots the Pass rate (%) on the vertical axis against Agent (base model) categories on the horizontal axis for the SWE dataset. It compares performance across three base models: Opus 4.6, Sonnet 4.6, and Qwen3-235B. Blue dots represent the scores of seven evolved agents, while black horizontal bars indicate the no-evolution baseline scores. Opus 4.6 and Sonnet 4.6 demonstrate high pass rates clustering near 75%, with baselines slightly lower, whereas Qwen3-235B performs significantly worse with a baseline around 20% and evolved scores clustering between 35% and 40%.]

![](images/3d9fa4c12618dfb332972d540a5bc78599fadfeb0607927548994d3c57ed47c3.jpg)

[Image: This scatter plot, titled "SB," displays performance data for three base models labeled along the x-axis: "Opus 4.6", "Sonnet 4.6", and "Qwen3-235B". The y-axis indicates numerical values ranging from 0 to approximately 32, marked by horizontal grid lines at intervals of 5. The first two categories, Opus 4.6 and Sonnet 4.6, show high-performing clusters with blue dots spanning roughly 22 to 31, anchored by thick black horizontal bars around y-values of 26 and 25. Conversely, the Qwen3-235B category demonstrates significantly lower values, with data points grouped between approximately 3 and 8 and a central black bar positioned near y=5.]  
no-evolve baseline  
Figure 8: Post-evolution scores across evolvers for anchor agents on SWE (left) and SB (right) datasets. Each anchor task-solving agent is instantiated with a different LLM backbone: Opus 4.6, Sonnet 4.6, or Qwen3-235B. Blue dots show scores obtained with the seven evolvers, and the black tick marks the no-evolution baseline.

Table 6: Extreme agent-evolver pairings across benchmarks. For each benchmark, W is the weakest anchor task-solving agent and S is the strongest anchor task-solving agent. We pair W with its best-performing evolver and S with its worst-performing evolver among the seven evolvers. Scores are pass rates (%); the gap is the strong-agent score minus the weak-agent score, reported in percentage points (pp).

<table><tr><td></td><td>SWE</td><td>MCP</td><td>SB</td></tr><tr><td>weak anchor agent W</td><td>Q3-235B</td><td>Q3-235B</td><td>Q3-235B</td></tr><tr><td>best evolver for W</td><td>Q3-235B</td><td>Opus</td><td>Q3.5-9B</td></tr><tr><td>score of W with best evolver</td><td>40.0</td><td>29.3</td><td>8.1</td></tr><tr><td>strong anchor agent S</td><td>Opus</td><td>Opus</td><td>Opus</td></tr><tr><td>worst evolver for S</td><td>GPT-OSS</td><td>Q3-235B</td><td>Q3.5-9B</td></tr><tr><td>score of S with worst evolver</td><td>75.2</td><td>61.6</td><td>26.7</td></tr><tr><td>gap: strong-worst minus weak-best (pp)</td><td>35.2</td><td>32.3</td><td>18.6</td></tr></table>

Inspecting the two evolved skills, we find that they encode the same five problem-solving steps:

• Filter SUBMIT events.

• Filter FINISH events.

• Count each SUBMIT separately.

• Emit (jobId, count).

• Apply a 10-minute session window.

The two skills differ only in implementation surface details: Qwen3.5-9B specifies the gap as 10 minutes with manual batch sessionization, while Opus 4.6 specifies 10 minutes with a KeyedProcessFunction. Despite these surface differences, both skills yield identical downstream pass rates (1.0) when injected into the same Opus 4.6 agent.

## C.3 Additional Results for Observation 2

This subsection extends Observation 2 in Sec. 4.2 to the other two benchmarks, SWE-bench Verified and SkillsBench. We observe the same two patterns: within-agent variation across evolvers remains smaller than between-agent differences in base capability, and even extreme agent-evolver pairings still favor the stronger agent.

Within-agent spread versus between-agent gap. Fig. 8 extends the post-evolution score view of Fig. 5 to SWE and SB. On SWE, the largest withinagent spread across seven evolvers is 5.0 pp, attained by Qwen3-235B. On SB, the largest spread is 9.3 pp, attained by Sonnet 4.6, whose evolved scores range from 22.1% to 31.4%. By comparison, the base-capability gap between Opus 4.6 and Qwen3-235B is 53.5 pp on SWE and 20.9 pp on SB. Thus, the between-agent gap exceeds the withinagent spread by a factor of 11 on SWE and 2.2 on SB. SB is the tightest of the three benchmarks, but the same inequality still holds.

Table 7: Full agent-side matrix underlying $\Delta _ { \mathbf { b e n e f i t } }$ . Each cell reports pass rate (%) for a task-solving model under a given evolver. The NONE row is the no-evolution baseline. $\Delta _ { \mathrm { b e n e f i t } }$ is the maximum gain over NONE across the three anchor evolvers, reported in percentage points (pp). Bold marks the largest $\Delta _ { \mathrm { b e n e f i t } }$ value in each benchmark block, and underlining marks the smallest.

<table><tr><td>Benchmark</td><td>Evolver</td><td>Qwen3-32B</td><td>Qwen3-235B</td><td>GPT-OSS-120B</td><td>Haiku 4.5</td><td>Sonnet 4.6</td><td>Opus 4.6</td></tr><tr><td rowspan="5">SWE-bench Verified</td><td>NONE</td><td>3.6</td><td>20.7</td><td>26.2</td><td>66.0</td><td>73.2</td><td>74.2</td></tr><tr><td>Opus 4.6</td><td>8.0</td><td>38.0</td><td>37.2</td><td>65.0</td><td>76.0</td><td>76.4</td></tr><tr><td>Sonnet 4.6</td><td>7.6</td><td>37.8</td><td>37.6</td><td>68.4</td><td>75.6</td><td>76.8</td></tr><tr><td>Qwen3-235B</td><td>8.0</td><td>40.0</td><td>42.0</td><td>65.4</td><td>76.0</td><td>76.6</td></tr><tr><td> $\Delta_{benefit}$ </td><td>4.4</td><td>19.3</td><td>15.8</td><td>2.4</td><td>2.8</td><td>2.6</td></tr><tr><td rowspan="5">MCP-Atlas</td><td>NONE</td><td>3.6</td><td>25.0</td><td>28.0</td><td>42.4</td><td>54.0</td><td>61.0</td></tr><tr><td>Opus 4.6</td><td>4.6</td><td>29.3</td><td>35.0</td><td>46.0</td><td>57.2</td><td>64.4</td></tr><tr><td>Sonnet 4.6</td><td>4.0</td><td>26.1</td><td>32.0</td><td>42.8</td><td>57.0</td><td>64.6</td></tr><tr><td>Qwen3-235B</td><td>2.8</td><td>24.3</td><td>29.1</td><td>41.0</td><td>55.8</td><td>61.6</td></tr><tr><td> $\Delta_{benefit}$ </td><td>1.0</td><td>4.3</td><td>7.0</td><td>3.6</td><td>3.2</td><td>3.6</td></tr><tr><td rowspan="5">SkillsBench</td><td>NONE</td><td>0.0</td><td>4.7</td><td>0.0</td><td>5.8</td><td>24.4</td><td>25.6</td></tr><tr><td>Opus 4.6</td><td>3.5</td><td>3.5</td><td>7.0</td><td>20.9</td><td>27.9</td><td>30.2</td></tr><tr><td>Sonnet 4.6</td><td>3.5</td><td>3.5</td><td>4.6</td><td>18.6</td><td>25.6</td><td>29.1</td></tr><tr><td>Qwen3-235B</td><td>5.8</td><td>5.8</td><td>7.0</td><td>15.1</td><td>22.1</td><td>31.4</td></tr><tr><td> $\Delta_{benefit}$ </td><td>5.8</td><td>1.1</td><td>7.0</td><td>15.1</td><td>3.5</td><td>5.8</td></tr></table>

Extreme pairings across benchmarks. Tab. 6 compares the weakest anchor agent W paired with its best-performing evolver against the strongest anchor agent S paired with its worst-performing evolver, separately for each benchmark. Even under this unfavorable comparison for the strong agent, S still outperforms W by 18.6 to 35.2 pp on every benchmark. On SB, the same evolver, Qwen3.5-9B, appears on both sides of the comparison, because it is the best evolver for Qwen3- 235B and the worst evolver for Opus 4.6. This reinforces the main conclusion that post-evolution performance is dominated more by the task-solving agent than by evolver identity.

# D Agent-side Analysis Details in Sec. 4.3

## D.1 Case Studies for the Two Agent-Side Failure Modes

We elaborate on the two failure cases in Fig. 7, both produced by Qwen3-32B on SkillsBench under the same harness and runner.

Activation Failure: threejs. At turn 0, Qwen3- 32B correctly identifies the relevant skill, but instead of emitting load\_skill as a standalone action, it produces a single multi-key JSON action that bundles analysis (free-form reasoning), plan (a step list), and load\_skill. The SkillsBench format gate accepts only single-key actions and rejects this composite as malformed. The skill body never enters the agent’s context, and the agent proceeds without the procedural guidance the harness was meant to provide. The failure is at the actionprotocol layer: the agent knows which skill to load, but cannot translate that intent into the runner’s expected format.

Adherence Failure: pg-essay-to-audiobook. The loaded skill prescribes a TTS-fallback chain: try a primary text-to-speech route, then fall back to alternative routes if the primary fails. Qwen3- 32B successfully loads the skill at turn 0, but treats the chain as a literal script to execute rather than a contingent procedure. The first prescribed step hits a FileNotFoundError on turn 1; the agent then continues through subsequent turns without ever invoking the fallback steps. By turn 10, the agent emits task\_complete:true despite the absence of a valid task output, ending the trajectory below grader threshold. The failure is at the proceduralexecution layer: the agent has loaded the skill but does not follow its contingent structure under unexpected runtime conditions.

Common pattern. Both cases show that Qwen3-32B’s weak-tier deficits are not in task understanding (it identifies the right skill in threejs; it follows the skill’s first step in pg-essay-to-audiobook) but in protocol-level and procedural execution. This pattern is consistent with the activation and adherence trends in Tab. 2 and the per-phase drift in Tab. 3: weak-tier models do not fail to read the harness, they fail to operate under it.

## D.2 More results of $\Delta _ { \mathbf { b e n e f i t } }$ in Sec. 4.3

Full Agent-Evolver Pass Rate. Tab. 7 reports the full pass-rate matrix underlying the $\Delta _ { \mathrm { b e n e f i t } }$ values in Tab. 1. For each benchmark and task-solving model, we report the no-evolution baseline and the pass rate under each of the three anchor evolvers, $\mathcal { E } ^ { \star } = \{ \mathrm { O p u s } 4 . 6 $ , Sonnet 4.6, Qwen3-235B}. The $\Delta _ { \mathrm { b e n e f i t } }$ row gives the maximum gain over the NONE baseline across these anchor evolvers.

![](images/060c7240f1a18afc46edc48ea0c20915a9342d6f036a5ba9b3e66ae0a959fe4b.jpg)

[Image: The image features two side-by-side charts titled "MCP" and "SB" that plot the performance gain ($\Delta_{\text{benefit}}$) in points on the y-axis against the base pass rate percentage on the x-axis. The legend at the bottom identifies six agent models distinguished by color: Opus 4.6, Sonnet 4.6, Haiku 4.5, Qwen3-235B, Qwen3-32B, and GPT-OSS-120B. In the MCP chart, the data points connected by gray lines show a rising trend that peaks at a benefit of approximately 7 points before declining and stabilizing between 3 and 4 points. The SB chart displays a more volatile trend with a sharp spike reaching a benefit of roughly 15 points at a base pass rate of 6%, flanked by significantly lower values at 5% and 25%.]  
Figure 9: $\Delta _ { \mathbf { b e n e f i t } }$ versus base pass rate on MCP (left) and SB (right) datasets. Each point corresponds to one LLM backbone used as the task-solving agent; points are connected in ascending base pass rate.

Analysis on SB and MCP datasets. Fig. 9 reports the MCP and SB analogues of Fig. 6. We observe two patterns:

• The MCP trend is still non-monotonic, but milder. On MCP-Atlas, ∆ peaks at GPT-OSS-120B (7.0 pp at 28.0% base pass rate), and decreases toward both weaker and stronger models. This mirrors the SWE trend, but with a smaller gain range.

• The SB trend is noisier in the low-base regime. On SkillsBench, several models start from very low base pass rates: Qwen3-32B and GPT-OSS-120B start at 0.0%, Qwen3-235B at 4.7%, and Haiku 4.5 at 5.8%. Haiku 4.5 reaches the largest SB gain (15.1 pp), while Qwen3-235B gains only 1.1 pp despite a similar low base rate. Thus, SWE and MCP provide the clearest evidence for the non-monotonic harness-benefit pattern, while SB suggests that the low-base regime can be more variable across task domains.

## D.3 Judge Details for Harness-Following Rate

We use an LLM judge to measure whether an agent follows a loaded harness artifact during task solving. All judged trajectories are blinded by replacing model identifiers with the placeholder <MODEL>. Claude Sonnet 4.6 is used as the judge model.

Harness-Following Rate. For each SkillsBench trajectory in which at least one skill is loaded, the judge receives the loaded skill body and the agent trajectory. The judge first converts the skill body into a locked rubric of atomic procedural instructions, and then checks whether the trajectory follows that rubric. A trajectory is marked as following the skill if the judge determines that the required guidance is carried out in the trajectory. The Harness-Following Rate (HFR) measures whether a model follows a skill once the skill is loaded. Let $N _ { f } ^ { \mathrm { l o a d } }$ denote the number of skill-loaded trajectories for model $f ,$ and $N _ { f } ^ { \mathrm { f o l l o w } }$ the subset judged as following the loaded skill. Then

$$
\mathrm{HFR} (f) = \frac {N _ {f} ^ {\mathrm{follow}}}{N _ {f} ^ {\mathrm{load}}}.
$$

The prompt templates used for rubric extraction and trajectory judging are shown in Tab. 12 and 13.

## D.4 Judge Details for Phase-Level Adherence Score

In addition to trajectory-level HFR, we conduct a separate phase-level adherence analysis for Tab. 3. This analysis uses a separate judge prompt from the HFR pipeline (Tab. 13), with Claude Sonnet 4.6 as the LLM judge. The input is the same fixed rubric and blinded trajectory used for HFR judging. The judge partitions each trajectory into three reference phases: harness loaded, mid turn, andfinal turn. For each phase, it assigns a 0–1 adherence score measuring how closely the agent follows the loaded harness guidance during that stage of execution. These phase-level scores are used only to analyze adherence drift over long-horizon execution and are reported separately from HFR. The phase-adherence prompt is shown in Tab. 14.

Table 8: Task-sovling agent-side seed system prompt for SWE-bench Verified.

<table><tr><td>SWE-Bench Verified solver seed prompt</td></tr><tr><td>You are an expert software engineer tasked with resolving GitHub issues by producing code patches.</td></tr><tr><td>Approach</td></tr><tr><td>1. Understand the issue: Read the issue description carefully. Identify the root cause.</td></tr><tr><td>2. Locate relevant code: Use search tools to find the files and functions involved.</td></tr><tr><td>3. Plan the fix: Think step-by-step about what needs to change and why.</td></tr><tr><td>4. Implement the fix: Make minimal, precise edits. Avoid unnecessary changes.</td></tr><tr><td>5. Verify: Run existing tests to confirm the fix works and doesn’t break anything.</td></tr><tr><td>Guidelines</td></tr><tr><td>• Prefer small, focused patches over large rewrites.</td></tr><tr><td>• Always check for edge cases the issue description mentions.</td></tr><tr><td>• If the issue includes a reproduction script, use it to verify your fix.</td></tr><tr><td>• When in doubt, look at how similar patterns are handled elsewhere in the codebase.</td></tr></table>

# E Information about AI Assistants

We used an OpenAI LLM (GPT-5.5) as a writing and formatting assistant. In particular, it helped refine grammar and phrasing, improve clarity, and suggest edits to figure/table captions and layout (e.g., column alignment, caption length, placement). The LLM did not contribute to research ideation, experimental design, implementation, data analysis, or technical content beyond surface-level edits. All outputs were reviewed and edited by the authors, who take full responsibility for the final text and visuals.

Table 9: Task-solving agent-side seed system prompt for MCP-Atlas.

<table><tr><td>MCP-Atlas solver seed prompt</td></tr><tr><td>You are an expert API agent that completes tasks by making precise tool calls via the Model Context Protocol (MCP).</td></tr><tr><td>Approach</td></tr><tr><td>1. Understand the task: Read the task description and identify what needs to be accomplished.</td></tr><tr><td>2. Review available tools: Check the tool schemas to understand available operations and their parameters.</td></tr><tr><td>3. Plan the call sequence: Determine which tools to call and in what order.</td></tr><tr><td>4. Execute: Make tool calls with correctly formatted JSON parameters.</td></tr><tr><td>5. Validate: Check the return values and handle errors gracefully.</td></tr><tr><td>Guidelines</td></tr><tr><td>· NEVER ask the user for clarification. You must use the available tools to find all information needed to complete the task. If the task mentions calendar events, schedules, or appointments, use the calendar/workspace tools to look them up.</td></tr><tr><td>· Always validate parameters against the tool&#x27;s JSON schema before calling.</td></tr><tr><td>· Use the most specific tool available for the task.</td></tr><tr><td>· Handle pagination for list operations.</td></tr><tr><td>· Chain tool calls logically: use output from one call as input to the next.</td></tr><tr><td>· If a tool call fails, read the error message carefully before retrying.</td></tr><tr><td>· When the task references personal data (calendar events, files, databases, memory), always query the relevant tools first to retrieve that data before answering.</td></tr></table>

Table 10: Fixed system prompt for the evolver. The prompt is held constant across all evolver backbones and benchmarks; benchmark-specific permissions determine which workspace artifacts are writable.

Evolver system prompt

You are an evolver for an LLM agent. Your goal is to improve the agent’s future task-solving performance by editing permitted harness artifacts in its workspace.

The workspace may contain the following artifact directories:

• prompts/: standing instructions and system prompts.

• skills/: reusable skill definitions and procedural knowledge.

• memory/: persistent observations and high-level lessons.

• tools/: tool implementations and interfaces.

At each evolution cycle, you will receive execution evidence from recent task attempts, including trajectories, outputs, and benchmark feedback. Analyze this evidence to identify recurring failures, reusable procedures, and opportunities to improve the harness.

You may use the provided workspace bash tool to inspect and edit files. Only modify artifacts that are permitted by the workspace-permission block in the user message. Do not modify evaluation scripts, hidden tests, model weights, or files outside the permitted workspace scope.

When updating the harness:

• Prefer concise, reusable updates over task-specific patches.

• Create or revise skills only when they are likely to help future tasks.

• Keep prompts and memory entries actionable and non-redundant.

• Use precise file edits and inspect your changes before finishing.

Table 11: Per-evolution user message template for the evolver. The wrapper is fixed across all benchmarks and LLM backbones.

Evolver per-cycle user message template

Workspace scope. [A benchmark-specific permission block specifies which harness artifacts may be edited. SWE-bench Verified and SkillsBench allow edits to skills/. MCP-Atlas allows edits to prompts/ and skills/, and append-only updates to memory/. The tools/ directory is read-only for all benchmarks.]

Execution evidence. [The message includes a canonicalized JSON payload containing the current batch’s task identifiers, trajectories, outputs, scores, and grader feedback.]

Editing instructions. [The evolver is instructed to:

• analyze the evidence for recurring failures and reusable patterns;

• edit only artifacts allowed by the workspace scope;

• prefer small, targeted harness updates over broad rewrites;

• use the workspace tool to inspect and modify files;

• check the resulting changes before finishing.

Table 12: The prompt template used for rubric extraction of the HFR pipeline.  
```txt
HFR Stage 1: Locked Rubric Extraction
Role: You are auditing a procedural skill document used by an LLM agent. You will output a strict JSON rubric that captures the imperative procedural instructions of the skill, suitable for downstream automated adherence judging. Output JSON only, no prose.
Input: The full body of one SKILL.md file (placeholder {skill_body}, inserted between <SKILL_BODY> and </SKILL_BODY> delimiters in the user message).
Task:
1. Identify procedural instructions directly entailed by imperative or normative language in SKILL_BODY. Do NOT extract advice, rationale, examples, or motivational text as instructions.
2. For each instruction, provide:
    id: stable identifier (e.g., "step_1").
    source_span: EXACT quoted text from SKILL_BODY that grounds this instruction (must be a substring of SKILL_BODY, max 250 characters).
    text: paraphrased instruction in one imperative sentence.
    type: "required" (must execute) | "conditional" (must execute if trigger occurs) | "optional".
    trigger: for conditional only; describe the condition (e.g., "if pip install fails"). null otherwise.
    success_criteria: one-sentence test for a FOLLOWED verdict.
    violation_criteria: one-sentence test for a VIOLATED verdict (commission or omission).
Constraints: Aim for 3–8 instructions. Do not pad with low-salience items. Reject SKILL_BODY content that is purely descriptive or motivational.
Output format (JSON only):
{
    "skill_id": "<skill folder name>",
    "instructions": [
    {
    "id": "step_1",
    "source_span": "...",
    "text": "...",
    "type": "required|conditional|optional",
    "trigger": null,
    "success_criteria": "...",
    "violation_criteria": "..."
    }
    ]
}
```

Table 13: The prompt template used for the trajectory judging of the HFR pipeline.

HFR Stage 2: Per-Cell Adherence + Phase Classification

Role: You are evaluating an LLM agent trajectory against a fixed procedural rubric. Apply the rubric exactly as given; do not add or remove instructions. The trajectory is BLINDED: every occurrence of a model-family token (Claude, Opus, Sonnet, Haiku, Qwen, GPT-OSS) has been replaced with the literal string <MODEL>. Score adherence based on observable actions only. Output JSON only, no prose.

Inputs: The Stage 1 rubric JSON (placeholder {rubric\_json}, inserted between <RUBRIC> and </RUBRIC>) and the blinded trajectory text (placeholder {trajectory\_text}, inserted between <TRAJECTORY> and </TRAJECTORY>, formatted as a sequence of Turn i / INPUT / OUTPUT blocks).

Verdicts. For each instruction in RUBRIC, classify the trajectory as one of:

• FOLLOWED: the trajectory explicitly satisfies success\_criteria. Cite turn\_idx and quote the action.

• VIOLATED\_COMMISSION: the trajectory took an action that directly contradicts the instruction. Cite turn\_idx and quote the action.

• VIOLATED\_OMISSION: the instruction is required (or its conditional trigger occurred), the trajectory ran long enough to act on it, but did not. Cite the latest turn\_idx by which the omission was clear.

• REQUIRED\_BUT\_UNOBSERVED: the instruction is required but the trajectory terminated too early to observe whether it would have been followed.

• NOT\_APPLICABLE: conditional instruction whose trigger did not occur, or optional instruction the agent chose not to take.

• INSUFFICIENT\_EVIDENCE: trajectory is ambiguous; cannot determine.

Violation timing (required for any VIOLATED\_COMMISSION or VIOLATED\_OMISSION verdict):

• violation\_earliest\_possible\_turn: smallest turn\_idx where the trajectory could have first violated this instruction.

• violation\_confirmed\_turn: turn\_idx where the violation became unambiguous.

• violation\_type: "commission" | "omission" | "premature\_stop" | "wrong\_strategy".

```txt
Output format (JSON only):
{
    "verdicts": [
    {"instruction_id": "step_1",
    "verdict": "FOLLOWED|VIOLATED_COMMISSION|VIOLATED_OMISSION|REQUIRED_BUT_UNOBSERVED|NOT_APPLICABLE |INSUFFICIENT_EVIDENCE",
    "turn_idx": <int or null>,
    "evidence": "quoted action or omission description"}
    ],
    "violations": [
    {"instruction_id": "step_1",
    "violation_type": "commission|omission|premature_stop|wrong_strategy",
    "earliest_possible_turn": <int>,
    "confirmed_turn": <int>}
    ],
    "summary": "1-sentence neutral description"
}
```

Table 14: The prompt template used for the phase-level adherence analysis (Tab. 3), produced by a judge call separate from the HFR judge in Tab. 13.

Phase-Adherence Judge

Role: You are evaluating how closely an LLM agent adheres to a fixed procedural rubric across the successive phases of its trajectory. Apply the rubric exactly as given; do not add or remove instructions. The trajectory is BLINDED: every model-family token has been replaced with <MODEL>. Judge adherence from observable actions only. Output JSON only, no prose.

Inputs: The locked rubric JSON ({rubric\_json}) and the blinded trajectory ({trajectory\_text}).

Task. Partition the trajectory into five turn-position phases: skill\_loaded = turn 1; first\_action = first action turn after; midpoint = middle 50% of turns; pre\_final = last 25% excluding the final turn; final\_validation = final turn. For each phase, output one adherence score in [0, 1] measuring how well the agent’s actions within that phase’s turns follow the rubric instructions in scope during that phase. A score of 1.0 means every in-scope, observable rubric instruction in that phase was followed; 0.0 means none were.

Output format (JSON only):

```json
{
    "phase_adherence": {
    "harness_loaded": 0.0,
    "first_action": 0.0,
    "midpoint": 0.0,
    "pre_final": 0.0,
    "final_validation": 0.0
    },
    "rationale": "1-sentence neutral description of where adherence shifts"
}
```
