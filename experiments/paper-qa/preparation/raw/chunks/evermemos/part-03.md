# A Evaluation Details

A.1 Evaluation Settings and Fair Comparison LoCoMo backbones. We report LoCoMo results under two backbones: GPT-4.1-mini (primary, reflecting an up-to-date backbone) and GPT-4o-mini (to facilitate comparison with prior work). Following common practice in LTMOS evaluation, we standardize the backbone used forfinal answer generation to isolate the contribution of memory management from the base model.

Baseline executability. For EverMemOS and MemoryOS, we execute the full pipeline (memory construction, retrieval, and answering) with the specified backbone. For Mem0, MemU, MemOS, and Zep, we use their official APIs for memory management/retrieval; in this setting, we keep each baseline’s official memory configuration and prompting unchanged and apply the unified backbone only at the answering stage.

LongMemEval. Due to the extreme input length of LongMemEval, we cannot stably run all baseline APIs end-to-end; we therefore report baseline results from the official MemOS leaderboard<sup>2</sup> and evaluate EverMemOS with GPT-4.1-mini under the same protocol.

Retrieval configuration. EverMemOS uses a hybrid retriever that fuses dense retrieval (encoder: Qwen3-Embedding-4B (Zhang et al., 2025)) and sparse retrieval (BM25) via Reciprocal Rank Fusion (RRF), followed by episode re-ranking (Qwen3-Reranker-4B (Zhang et al., 2025)). Unless otherwise specified, we retrieve the top-10 MemScenes and select 10 Episodes for downstream inference.

MemBase statistics and construction hyperparameters. We report dataset-level MemBase statistics (Table 5) and memory-construction hyperparameters (Table 6) for LoCoMo and Long-MemEval. MemScenes are the clustering units produced by Phase II, and each MemScene contains a small set of MemCells. We use the same pipeline across datasets, while adopting datasetspecific clustering hyperparameters to reflect different dialogue structures and time spans. Long-MemEval contains 500 dialogue–question pairs (one per conversation). Max time gap is the maximum allowed temporal distance (in days): when assigning a MemCell A to a candidate MemScene, if the closest-in-time MemCell B already in that MemScene is farther than this threshold, A is not clustered into that MemScene.

Table 5: MemBase statistics on LoCoMo and Long-MemEval.

<table><tr><td>Metric</td><td>LoCoMo</td><td>LongMemEval</td></tr><tr><td>Dataset scale</td><td></td><td></td></tr><tr><td>#Conversations</td><td>10</td><td>500</td></tr><tr><td>#Questions</td><td>1,540</td><td>500</td></tr><tr><td>MemBase statistics</td><td></td><td></td></tr><tr><td>#Total MemCells</td><td>702</td><td>54,755</td></tr><tr><td>#Total MemScenes</td><td>286</td><td>40,138</td></tr><tr><td>Avg MemCells/conv.</td><td>70.2</td><td>109.5</td></tr><tr><td>Avg MemScenes/conv.</td><td>28.6</td><td>80.3</td></tr><tr><td>Avg MemCells/MemScene</td><td>2.45</td><td>1.36</td></tr><tr><td>MemCells/conv. (range)</td><td>34–95</td><td>82–154</td></tr><tr><td>MemScenes/conv. (range)</td><td>13–49</td><td>60–102</td></tr></table>

Table 6: Memory-construction hyperparameters.

<table><tr><td>Hyperparameter</td><td>LoCoMo</td><td>LongMemEval</td></tr><tr><td>Clustering threshold  $\tau$ </td><td>0.70</td><td>0.50</td></tr><tr><td>Max time gap (days)</td><td>7</td><td>30</td></tr></table>

Multi-round query rewriting frequency. On LoCoMo (GPT-4.1-mini), the sufficiency checker triggers a second-round query rewriting for 31.0% of questions.

Default evaluation mode. Unless otherwise specified, quantitative experiments use Memory-Augmented Reasoning (Episodes-only). We additionally report the effect of the consolidated Profile in Table 4, while Foresight is illustrated in the qualitative Case Study (Memory-Augmented Chat).

## A.2 LLM-as-Judge Reliability

We randomly selected 25 non-overlapping Q&A pairs from LoCoMo and 25 from LongMemEval, and generated model answers for each question. We recruited annotators via Prolific. For each Q&A pair, five independent human evaluators judged whether the generated answer was correct given the question and the reference answer. All participants provided informed consent via the platform interface and were compensated at approximately \$12.00/hour, consistent with fair-pay guidelines for academic research and above local minimum wage standards. Table 7 shows strong agreement between the LLM-as-judge protocol and human annotations: Cohen’s κ exceeds 0.89 and accuracy remains above 98% across benchmarks. Pearson r is 0.891 on LoCoMo and 0.979 on LongMemEval. These results suggest that GPT-4o-mini achieves human-level reliability for answer verification, enabling evaluation that is rigorous, reproducible, and cost-efficient.

Table 7: Reliability matrix for LLM-as-Judge.

<table><tr><td>Model</td><td>Cohen&#x27;s κ</td><td>95% CI</td><td>Accuracy</td><td>Pearson r</td></tr><tr><td>LoCoMo</td><td>0.891</td><td>[0.742, 1.000]</td><td>0.984</td><td>0.891</td></tr><tr><td>LongMemEval</td><td>0.978</td><td>[0.936, 1.000]</td><td>0.992</td><td>0.979</td></tr></table>

## A.3 Token Cost Breakdown

To improve cost transparency, we log all LLM API calls during LoCoMo evaluation (1,540 questions) under two backbones (GPT-4.1-mini and GPT-4omini) and attribute token usage to stages in our pipeline. Since LoCoMo evaluation uses Memory-Augmented Reasoning (Episodes-only), we do not invoke the Profile module; therefore, profilerelated tokens are excluded from Table 8. Table 8 maps stages to EverMemOS phases. Phase I corresponds to memory construction (add). In this Episodes-only setting, Phase II uses non-LLM computation (clustering/embedding updates) and thus incurs no additional LLM tokens. Phase III consists of retrieval (search) and answer generation (answer). The evaluate stage reflects LLM-asjudge scoring (three judges per question) and is reported separately. Phase III consumes 10.27M tokens (∼6.7k/question) with GPT-4.1-mini and 9.31M tokens (∼6.0k/question) with GPT-4o-mini; Phase I consumes 9.42M and 9.34M tokens, respectively, amortized over memory building.

Table 8: Token-level cost breakdown on LoCoMo (1,540 questions) under two backbones. Tokens are reported in millions (M); Total includes both prompt and completion.

<table><tr><td>Stage</td><td>#Calls</td><td>Prompt (M)</td><td>Total (M)</td></tr><tr><td colspan="4">GPT-4.1-mini</td></tr><tr><td>add</td><td>7056</td><td>8.66</td><td>9.42</td></tr><tr><td>search</td><td>2017</td><td>4.12</td><td>4.45</td></tr><tr><td>answer</td><td>1540</td><td>4.63</td><td>5.82</td></tr><tr><td>search+answer</td><td>3557</td><td>8.75</td><td>10.27</td></tr><tr><td>evaluate</td><td>4620</td><td>2.35</td><td>2.38</td></tr><tr><td colspan="4">GPT-4o-mini</td></tr><tr><td>add</td><td>7250</td><td>8.60</td><td>9.34</td></tr><tr><td>search</td><td>2219</td><td>4.37</td><td>4.62</td></tr><tr><td>answer</td><td>1540</td><td>3.84</td><td>4.69</td></tr><tr><td>search+answer</td><td>3759</td><td>8.21</td><td>9.31</td></tr><tr><td>evaluate</td><td>4620</td><td>2.14</td><td>2.17</td></tr></table>

## A.4 PersonaMem v2: Full Comparison Results

Table 9 reports the full comparison on PersonaMem v2 (32k) (Jiang et al., 2025) (2,447 questions across 9 scenarios). The Profile row indicates whether a memory system provides a profile-like component (not necessarily named “Profile”) that summarizes stable user information (e.g., MemOS maintains explicit vs. implicit preferences). For methods with such a component (✓), we generate answers using the retrieved memories plus the system’s profilelike component; for methods without it (✗), we generate answers using the retrieved memories only. EverMemOS achieves the best overall accuracy (53.25%), outperforming the strongest baseline (MemOS, 50.72%) by 2.53 points.

# B Additional Analyses

## B.1 Hyperparameter Sensitivity and Efficiency Trade-off

To better understand retrieval budgets, we analyze the MemScene budget N and episode budget K under a simplified setting that disables the agentic verification-and-rewriting loop in Phase III, isolating one-shot retrieval. Figure 5 shows that increasing N improves evidence-session recall and answer accuracy initially but quickly saturates; N=10 already yields strong recall. We therefore avoid bruteforce expansion of the retrieved scene set for efficiency. We also set N=10 to ensure the candidate pool contains at least K=10 MemCells even in extreme cases where each retrieved MemScene contains only a single MemCell. We choose K=10 episodes because most memory questions can be answered with a compact set of episodes while still covering difficult instances whose annotated evidence spans up to 7–8 recalled episodes. Finally, Figure 6 shows a favorable cost–accuracy frontier: decreasing K substantially reduces tokens used for downstream reasoning, and at moderate K values EverMemOS can achieve both lower token usage and higher accuracy than strong baselines.

## B.2 Accuracy Exceeding Recall on LoCoMo

In Figure 5, accuracy can exceed recall at small K on LoCoMo. Table 10 quantifies this effect: even when none of the annotated evidence sessions are retrieved (“zero recall”), 12–20% of questions are still answered correctly.

This primarily reflects information redundancy and non-unique evidence annotations: salient facts (identity, preferences, goals) recur across sessions, so the annotated evidence is not always the only session that supports the answer. For example, a question about “Caroline’s identity” is annotated with session [1], yet sessions [11–15] also state she is a transgender woman, enabling a correct answer from alternative sessions. In addition, LLMs can sometimes infer the correct response from semantically related retrieved content even when the exact annotated session is missing.

<table><tr><td>Scenario</td><td>Zep</td><td>Mem0</td><td>MemU</td><td>MemoryOS</td><td>MemOS</td><td>EverMemOS</td></tr><tr><td>Consultation</td><td>39.51</td><td>43.21</td><td>37.86</td><td>35.80</td><td>48.15</td><td>51.03</td></tr><tr><td>Email (Personal)</td><td>42.51</td><td>41.30</td><td>33.20</td><td>36.84</td><td>49.80</td><td>53.85</td></tr><tr><td>Translation</td><td>36.92</td><td>43.08</td><td>38.46</td><td>40.00</td><td>51.92</td><td>50.00</td></tr><tr><td>Email (Professional)</td><td>37.59</td><td>42.41</td><td>32.76</td><td>35.86</td><td>50.00</td><td>53.79</td></tr><tr><td>Creative Writing</td><td>41.22</td><td>42.86</td><td>35.51</td><td>35.51</td><td>48.16</td><td>55.10</td></tr><tr><td>Writing (Professional)</td><td>40.54</td><td>34.75</td><td>35.14</td><td>35.91</td><td>48.26</td><td>45.56</td></tr><tr><td>Knowledge Query</td><td>63.43</td><td>59.20</td><td>56.97</td><td>57.96</td><td>61.94</td><td>63.68</td></tr><tr><td>Social Media</td><td>32.35</td><td>38.66</td><td>34.03</td><td>35.29</td><td>46.64</td><td>47.90</td></tr><tr><td>Chat</td><td>44.87</td><td>40.30</td><td>34.22</td><td>36.88</td><td>44.87</td><td>52.09</td></tr><tr><td>Profile</td><td>✕</td><td>✕</td><td>√</td><td>√</td><td>√</td><td>√</td></tr><tr><td>Overall</td><td>43.40</td><td>43.85</td><td>38.70</td><td>40.05</td><td>50.72</td><td>53.25</td></tr></table>

Table 9: Full comparison on PersonaMem v2 (32k) (Jiang et al., 2025) (5,000 questions across 9 scenarios; accuracy, %).

Table 10: Accuracy vs. recall statistics on LoCoMo.

<table><tr><td>Metric</td><td>K=1</td><td>K=3</td></tr><tr><td>Recall</td><td>65.06%</td><td>86.32%</td></tr><tr><td>Accuracy</td><td>71.80%</td><td>87.81%</td></tr><tr><td>Zero-recall questions</td><td>429</td><td>125</td></tr><tr><td>Answered correctly</td><td>52 (12.1%)</td><td>25 (20.0%)</td></tr></table>

Overall, recall computed against annotated evidence can underestimate retrieval usefulness when evidence is distributed. Increasing K from 1 to 3 reduces zero-recall cases by 71% (429→125), narrowing the accuracy–recall gap.

Illustrative Cases. We provide three representative examples where answers remain correct despite missing the annotated evidence sessions:

• Redundant identity facts. Q: “What is Caroline’s identity?” The gold answer is transgender woman. Although the evidence is annotated in session [1], later sessions also explicitly mention this identity; the retriever surfaces those alternatives at small K, and the model answers correctly.

• Distributed activity mentions. Q: “What activities does Melanie partake in?” The gold answer spans multiple hobbies (e.g., pottery, camping, painting, swimming) with evidence annotated across multiple sessions. Retrieved sessions may miss the annotated ones but still contain sufficient mentions (e.g., pottery/painting) to support a correct response.

• Inference from related signals. Q: “Would Caroline pursue writing as a career option?” While the evidence is annotated in session [7], retrieved content from other sessions describes her career goal (e.g., becoming a counselor), enabling the LLM to infer that writing is unlikely.

## B.3 Profile Extraction Example

EverMemOS maintains a compact User Profile with two fields: explicitfacts (verifiable attributes and time-varying measurements) and implicit traits (preferences and habits). The profile is updated online from Phase II scene summaries with recencyaware updates for time-varying fields and conflict tracking when evidence is inconsistent. Table 11 provides an abridged example.

# C Reproducibility Artifacts

## C.1 Prompts for Agentic Retrieval

To make our system behavior transparent and reproducible, we include the core prompt templates used by our agentic retrieval controller.<sup>3</sup>

Sufficiency check. We use an LLM-based sufficiency check to decide whether the currently retrieved documents contain enough evidence to answer the user query. The prompt template (with placeholders) is shown below.

Table 11: Profile extraction example (de-identified): abridged evidence snippets and the resulting user profile.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Evidence snippets (excerpt) Retrieved user profile (excerpt)

2025-07-07: “I just measured my waist circumference, and it is 104 cm. Can you give me some advice?”
2025-10-20: “My waist is now 96 cm, down 8 cm! My pants feel loose.”

2025-11-03: “The doctor said my fatty liver has improved (moderate → mild). Waist is now 95 cm.”

2025-11-03: “My weight is still 80 kg, no rebound. I can keep it under control even in winter.”

Explicit facts.
Waist circumference: baseline 104 cm; latest 95 cm ( $\Delta = -9$  cm).
Weight: stable at 80 kg (no rebound).
Fatty liver grade: moderate → mild (improved).
Implicit traits.
Self-management: goal-oriented; consistently tracks health metrics and responds well to feedback.
Preference: requests immediately actionable adjustments.
</div>

```txt
You are an expert in information retrieval
    → evaluation. Assess whether the retrieved
    → documents provide sufficient information to
    → answer the user's query.

User Query:
{query}

Retrieved Documents:
{retrieved_docs}

Instructions:

1. **Analyze the Query's Needs**
- **Entities**: Who/What is being asked about?
- **Attributes**: What specific details
    → (color, time, location, quantity)?
- **Time**: Does it ask for a specific time
    → (absolute or relative like "last week")?

2. **Evaluate Document Evidence**
- Check **Content**: Do the documents mention
    → the entities and attributes?
- Check **Dates**: 
- Use the `Date` field of each document.
- For relative time queries (e.g., "last
    → week", "yesterday"), verify if document
    → dates fall within that timeframe.
- If the query asks "When did X happen?", do
    → you have the specific date or just a
    → vague mention?

3. **Judgment Logic**
- **Sufficient**: You can answer the query
    → *completely* and *precisely* using ONLY
    → the provided documents.
- **Insufficient**: 
- The specific entity is not found.
- The entity is found, but the specific
    → attribute (e.g., "price") is missing.
- The time reference cannot be resolved
    → (e.g., doc says "yesterday" but has no
    → date, or doc date doesn't match query
    → timeframe).
- Conflicting information without
    → resolution.

Output Format (strict JSON):
{{ 
  "is_sufficient": true or false,
  "reasoning": "Brief explanation. If
    → insufficient, state WHY (e.g., 'Found X but
    → missing date', 'No mention of Y').",
  "key_information_found": ["Fact 1 (Source: Doc
    → 1)", "Fact 2 (Source: Doc 2)"],
```

```jsonl
"missing_information": ["Specific gap 1", "Specific gap 2"]
}}
```

Multi-query generation (condensed). When the current retrieval is deemed insufficient, we generate 2–3 complementary follow-up queries targeted at the missing information. We omit examples and keep only the constraints that affect behavior (inputs, strategy choices, and the strict JSON output schema).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
You are an expert at query reformulation for
    $\rightarrow$ conversational memory retrieval.
Your goal is to generate 2-3 complementary
    $\rightarrow$ queries to find the MISSING information.

-------- Original Query:
{original_query}

Key Information Found:
{key_info}

Missing Information:
{missing_info}

Retrieved Documents (Context):
{retrieved_docs}

Strategy Selection (choose based on why info
    $\rightarrow$ is missing)
- Pivot / Entity Association: search related
    $\rightarrow$ entities/categories
- Temporal Calculation: anchor relative times
    $\rightarrow$ using document dates
- Concept Expansion: synonyms / general-specific
    $\rightarrow$ variants
- Constraint Relaxation: remove one constraint at
    $\rightarrow$ a time

Query Style Requirements (use DIFFERENT
    $\rightarrow$ styles)
1) Keyword Combo (2-5 words)
2) Natural Question (5-10 words)
3) Hypothetical Statement (HyDE, 5-10 words)

Output Format (STRICT JSON)
{
    "queries": ["Query 1", "Query 2", "Query 3"],
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
"reasoning": "Strategy used for each query $\hookrightarrow$ (e.g., Q1: Pivot, Q2: Temporal)"
}
</div>

## C.2 End-to-End Inference Trace (LoCoMo Multi-Hop Example)

To improve transparency, we provide an end-toend inference trace for a representative LoCoMo multi-hop question (conversation locomo\_6), including the MemBase hierarchy (MemScenes and MemCells) and the two-round retrieval process (sufficiency check and query rewriting) that leads to a correct final answer. We denote the retrieved MemScene count as N and the retrieved MemCell (episode) count as K (corresponding to scene\_top\_k and response\_top\_k in our implementation).

Trace at a glance.

• Question (multi-hop). “Does James live in Connecticut?” The dialogue never directly states James’s residence; the system must infer the answer from related evidence.

• MemBase hierarchy. 49 MemScenes / 91 MemCells; retrieval selects top N=10 Mem-Scenes (20%), then reranks/selects K=10 MemCells for answering.

• Round 1 retrieval + sufficiency. Top N=10 MemScenes (31 MemCells) → insufficient (is\_sufficient=false); missing an explicit residence mention / confirmation of living in Connecticut.

• Query rewriting. The controller generates refined queries targeting residence/location information.

• Round 2 retrieval. With 40 additional candidates, the top-ranked MemCell contains the key evidence that James adopted a dog from a shelter in Stamford, enabling an evidencegrounded inference.

• Inference + evaluation. Final answer: Likely yes; judged correct by 3/3 LLM judges.

Worked example (formatted). For readability, we summarize the trace in Table 12 (instead of printing raw JSON).

Table 12: End-to-end inference trace (LoCoMo multi hop example), summarized.

<table><tr><td>Stage</td><td>Key outputs</td></tr><tr><td>Input</td><td>Query: Does James live in Connecticut? (Category: multi-hop; Gold: Likely yes).</td></tr><tr><td>MemBase</td><td>49 MemScenes / 91 MemCells (conversation locomo_6).</td></tr><tr><td>Round 1</td><td>Top N=10 MemScenes (31 MemCells) → insufficient (is_sufficient=false); missing an explicit residence mention / confirmation of Connecticut.</td></tr><tr><td>Rewrite</td><td>Refined queries: (i) James residence Connecticut; (ii) Where does James currently live; (iii) James lives near McGee&#x27;s bar in Connecticut.</td></tr><tr><td>Round 2</td><td>+40 candidates; top result is James Adopts Shelter Dog Ned... (Apr 12, 2022) from cluster_004, mentioning “Stamford”.</td></tr><tr><td>Answer</td><td>Output: Likely yes; judged correct by 3/3 LLM judges.</td></tr></table>

Detailed trace. Round 1: initial retrieval and sufficiency check.

• Retrieval mode. Agentic MemSceneguided reranking (agentic\_scene\_rerank) with N=10 and K=10.

• Retrieved candidates. N=10 MemScenes (31 MemCells).

• Sufficiency verdict. is\_sufficient=false.

• Key information found. “James and Samantha moved in together near McGee’s Bar”; “James traveled to Nuuk recently”.

• Missing information. (i) explicit mention of James’s residence location; (ii) confirmation whether James lives in Connecticut.

Verifier rationale (excerpt).

```txt
None of the documents explicitly mention where
→ James currently lives or whether he lives in
→ Connecticut.
```

Query rewriting (Round 2 queries).

```txt
1) James residence Connecticut  
2) Where does James currently live  
3) James lives near McGee's bar in Connecticut
```

Round 2: top retrieved MemCells. The refined queries retrieve 40 additional candidates; top results are:

<table><tr><td>Rank</td><td>Scene</td><td>Subject (summary)</td></tr><tr><td>1</td><td>4</td><td>James Adopts Shelter Dog Ned and Discusses Gaming Progress with John (Apr 12, 2022)</td></tr><tr><td>2</td><td>43</td><td>James Announces Move-In with Samantha Near McGee’s Bar (Oct 31, 2022)</td></tr><tr><td>3</td><td>15</td><td>James Shares Recent Life Challenges and Support System (Jun 16, 2022)</td></tr><tr><td>4</td><td>44</td><td>James’s Family Road Trip Visiting Friends Josh and Mark (Nov 7, 2022)</td></tr><tr><td>5</td><td>22</td><td>James’s Upcoming Summer Trip to Toronto and Vancouver (Jul 9, 2022)</td></tr></table>

Key evidence (dialogue excerpt).

I adopted a pup from a shelter in Stamford last

week and my days have been so much happier,→

with him in the fam.,→

Key evidence (atomic fact).

• James adopted a pup named Ned from a shelter in Stamford last week (March 28–April 3, 2022).

Answer + evaluation.

James adopted his dog Ned from a shelter located

in Stamford, which is a city in Connecticut,,→

strongly implying he lives near Stamford,,→

Connecticut. Furthermore, when James and,→

Samantha moved in together on October 31,,→

2022, they rented an apartment near McGee's,→

bar, a location they both favored. Although,→

the exact city of this apartment is not,→

explicitly stated, given no mention of,→

relocation to another state and the previous,→

connection to Stamford, it is highly likely,→

that their residence is still in Connecticut,,→

near Stamford. Therefore, based on these,→

details, James does live in Connecticut with,→

high confidence.,→

Result: is\_correct=true (3/3 judges).
