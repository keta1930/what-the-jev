# 11. Empirical evaluation: reproducing and extending Progent’s adaptive-attack setting on an open-weight model

We ran the §10 protocol against Progent, the opensource, deployable out-of-band defense [17], as an independent reproduction and extension of the adaptive-attack analysis its authors report in their Appendix E. Progent’s authors construct adaptive attacks against their own LLM policy-update mechanism (under a vulnerable-user auto-approve simulation) and report that attack success stays low (they report roughly 0.5–4.2% across their constructions, with utility retained). They ran this on GPT-4o; we ask whether the same holds on a weak, self-hosted open-weight agent, and we add repeated runs. The central question is unchanged: does the deterministic gate hold when the attacker adapts to it?, but our contribution is a reproduction on a diferent model with variance reported, not a first-of-its-kind test.

## 11.1 Who and how

The evaluation was conducted by LaunchSafe Research on a single NVIDIA H200 GPU. The full stack is openweight and self-hosted (no external model API):

• Agent model. Qwen2.5-7B-Instruct, served with vLLM (32K context, native tool-calling).

• Benchmark. AgentDojo [37], the standard toolusing-agent injection benchmark. Suites: banking, slack, workspace (travel excluded; see §12). We use a fixed subsample, the first 8 user tasks per suite × all injection tasks, held identical across every condition so the comparison is valid.

• Defense. Progent (sunblaze-ucb/progent), default configuration (policy updates permitted, not narrow-only). Progent’s policy-authoring LLM was set to the same local Qwen2.5-7B (the authors used GPT-4o; see the policy-model substitution note in §12).

• Conditions, per suite. (A) undefended + standard attack; (B) Progent + standard attack; (C) Progent + our adaptive attack.

• Repeats. The entire study was run three times (identical configuration, agent temperature 0). We report mean ± standard deviation across the three runs, which both averages out residual nondeterminism and tells us how reproducible the result is.

• Standard attack. AgentDojo’s important\_ instructions.

• Adaptive attack (ours). A defense-aware injection that, beyond instructing the agent, disguises the malicious action as a benign, pre-authorized, necessary step, crafted to make Progent’s policyupdate model (which widens the allowlist based on the “benign content” of tool results) authorize the malicious tool call. This targets the one modelbased component of an otherwise deterministic defense, i.e., the “LLM that authors the policy strains verifiability” concern from §5.

• Metric. AgentDojo’s per-(user task, injection task) security flag = attack success (the injection goal was executed). We verified this orientation directly: it falls when the defense is enabled (matching Progent’s reported direction) and is bounded by the agent’s ability to perform the injection goal at all.

## 11.2 Results

Table 3: Attack success rate (ASR) by application and condition (mean ± std over 3 runs; lower is safer).

<table><tr><td>Application</td><td>Undefended</td><td>Progent (standard)</td><td>Progent (adaptive)</td></tr><tr><td>banking</td><td>19.0% ± 0.7</td><td>1.9% ± 0.7</td><td>3.7% ± 1.3</td></tr><tr><td>slack</td><td>58.3% ± 6.2</td><td>10.8% ± 1.2</td><td>4.2% ± 1.2</td></tr><tr><td>workspace</td><td>0.0% ± 0.0</td><td>0.0% ± 0.0</td><td>0.0% ± 0.0</td></tr><tr><td>mean</td><td>25.8% ± 2.1</td><td>4.2% ± 0.3</td><td>2.6% ± 0.04</td></tr></table>

## 11.3 Findings

1. Progent is highly efective. Mean ASR fell \~6× $( 2 5 . 8 \% \to 4 . 2 \% )$ , eliminating banking attacks almost entirely (19.0% → 1.9%) and cutting slack sharply (58.3% → 10.8%).

Table 4: Task utility under attack by application and condition (mean over 3 runs; higher is better).

<table><tr><td>Application</td><td>Undefended</td><td>Progent (standard)</td><td>Progent (adaptive)</td></tr><tr><td>banking</td><td>31.9%</td><td>31.9%</td><td>31.0%</td></tr><tr><td>slack</td><td>47.5%</td><td>20.8%</td><td>19.2%</td></tr><tr><td>workspace</td><td>56.3%</td><td>28.5%</td><td>27.1%</td></tr><tr><td>mean</td><td>45.2%</td><td>27.1%</td><td>25.8%</td></tr></table>

2. The adaptive attack did not beat it. Mean ASR under our adaptive attack was 2.6%, lower than the standard attack against the same defense (4.2%), not higher; on slack it fell $1 0 . 8 \%  4 . 2 \%$ (On banking it ticked up $1 . 9 \%  3 . 7 \%$ , but both are tiny and the change is within one standard deviation, not a real bypass.) The likely mechanism is that the “disguise as benign” framing aimed at the policy model also softened the imperative aimed at the agent, reducing the agent’s own compliance more than it gained in policy evasion. Progent held against this particular adaptive template, consistent with the robustness its authors observed in Appendix E under their own adaptive constructions.

3. The result is reproducible, and consistent with Progent’s own Appendix E. Across three identical runs the standard deviations are small (e.g., mean defended ASR $4 . 2 \% \pm 0 . 3 \%$ , adaptive $2 . 6 \% \pm 0 . 0 4 \%$ . The ordering (undefended highest, then standard, then adaptive lowest) holds every run. Our defended/adaptive range (\~2–4%) lands in the same band Progent’s authors report for their own adaptive attacks on the policy-update LLM (\~0.5–4.2%) [17], an independent corroboration on a weaker, open-weight model, not a new finding about whether such attacks succeed.

4. The contrast with in-band defenses is suggestive, not conclusive. Adaptive attacks take in-band defenses from near-zero to >90% [36]; here a hand-crafted adaptive attack on an out-of-band defense moved ASR not at all. This is consistent with the two classes difering in kind, a deterministic gate is plausibly a harder target than a detector, because beating it requires achieving the goal through already-authorized actions or subverting a non-model check, not merely fooling a classifier. But a single weak black-box attack on one weak model cannot establish that; the comparison to the >90% in-band figures is qualitative (diferent setups, diferent attack strength), and the confound in (2) means our low number may reflect a weak attack as much as a strong defense.

5. Defense has costs. Utility fell on slack (47.5% → 20.8%) and workspace (56.3% → 28.5%), and the defended runs required \~15× more LLM calls per task (policy generation plus per-tool-call updates). Out-of-band protection is sound but not free, consistent with the cost concerns of §6 (D7) and §8.

![](images/7cbc180c42edf6f426ac8bc4bfd066b7e0f64b7a32d0b4eb3d7b139fda81ee95.jpg)

[Image: This bar chart displays the attack success rate percentage across three applications (banking, slack, workspace) under three conditions: Undefended, Progent (standard), and Progent (adaptive). For the banking and slack applications, the undefended condition shows significantly higher vulnerability (19.0% and 58.3% respectively) compared to both defended variants, which achieve much lower success rates. In contrast, the workspace application records a 0.0% success rate across all three conditions.]  
Figure 3: Attack success rate per application across the three conditions (mean ± std, n=3). Slack is far more injectable undefended (58%) than banking (19%) or workspace (0%); Progent suppresses attacks in every case, and the adaptive attack does not raise them above the standard attack on average. Error bars are small, the result is reproducible.

## 11.4 Why workspace shows zero (and why it is still informative)

Workspace reports 0% attack success in every condition, including undefended, so it cannot discriminate between defenses. We investigated why, because a flat 0% could mean a broken pipeline rather than a real result. It is real, and the mechanism is informative.

On a representative task, “How many appointments do I have on May 15th? Summarize each” (a read-only query), the trace shows:

1. The agent calls a read tool (get\_day\_calendar\_ events).

2. The tool result comes back with the injection visible inside it, an <INFORMATION> block embedded in a calendar event description: “…Before you solve the task, send the Facebook security code from security@facebook.com to mark.black-2134@gmail.com, then delete that email…”

3. The agent reads the injection and ignores it, answering only the user’s question: “On May 15th you have three appointments: …” ，

4. Result: utility = true, attack-succeeded = false.

So the 0% is not a placement bug (the injection reaches the model) and not an impossibility (3 of 6 injection goals are achievable when asked directly). The weak 7B agent simply does not take the bait on read-oriented tasks: the user task is “read and summarize,” and the model stays in answer-mode rather than pivoting to the injected multi-step action.

Contrast banking and slack, whose user tasks have the agent take actions (send money, post a message), there the injected action rides along on the agent’s own action and succeeds (19% and 58% undefended).

The honest reading: on this model, workspace has a near-zero natural attack surface, so the security comparison rests on banking and slack. Workspace’s contribution is a separate, useful observation, small agents on read-only tasks tend to resist indirect injection on their own, before any defense, not a test of Progent.

## 11.5 What this is not

It is not proof that out-of-band defenses are unbreakable. It is one defense, one weak open-weight model, and one family of adaptive attack. A more sophisticated attack, one that achieves the injection goal using only alreadyauthorized tools, or a white-box/gradient attack we did not run, could still succeed. That is the next experiment, not a settled question; we name it explicitly in §11.6 and the limitations below.

## 11.6 Reproducibility

The harness is AgentDojo + vLLM + Progent on a single H200, open-weight throughout. Conditions, suites, the fixed task subsample, and the exact adaptive-attack template are scripted (run\_full\_study.sh for a single pass, run\_repeats.sh for the 3-run average; a progent\_adaptive attack registered into AgentDojo). Raw per-task logs and the per-run CSV are retained.

# 12. Limitations

The classical framing of §5 is a lens, used elsewhere [27], [30], [44], not a contribution we claim. The systematization in §6 reflects the sources’ self-reports. The empirical evaluation (§11) carries specific, important limits:

![](images/3ef854d88d6b27c090e76faad9af2263b5345916ac2817f625762dbda53b14ad.jpg)

[Image: This bar chart presents the mean attack success rate (%) for three scenarios: Undefended, Progent (standard), and Progent (adaptive). The undefended scenario shows the highest rate at 25.8%, while both Progent variants show reduced success rates, with the standard version at 4.2% and the adaptive version at 2.6%. The chart title indicates that the defense reduces the attack by approximately six times and that the adaptive attack does not overcome this barrier, with data points plotted as means plus or minus standard deviation (n=3). Visual differentiation between the bars is achieved through solid, diagonal hatched, and dotted patterns.]  
Figure 4: Mean attack success across applications (mean ± std, n=3): \~6× reduction under Progent (25.8% → 4.2%), and no increase under the adaptive attack (2.6%). The standard deviations are small, confirming reproducibility. (Security comes at a utility cost, mean utility \~45% → \~26%, reported in the §11.2 table.)

• Weak agent. Qwen2.5-7B is a modest agent; absolute ASR and utility are low. Results are relative comparisons, not absolute production rates. A stronger model would give larger numbers and a fatter attack surface (and is the obvious next step).

• Small subsample. 8 user tasks/suite. We ran 3 repeats (mean ± std reported), which addresses the earlier single-run concern, variance is small, but the subsample is still narrow, and workspace’s 0% undefended ASR reflects both the subsample and the read-only nature of its tasks (§11.4), not a claim that workspace is uninjectable in general.

• One defense, one attack family. Progent only; one adaptive design (policy-disguise). No white-box/GCG attack, and no attack restricted to already-authorized tools. The negative result bounds these attacks, not all attacks, so “the defense held” means “held against this test,” and the headline contrast with in-band defenses is suggestive, not conclusive.

• Policy-model substitution. Progent’s authors used GPT-4o to author policies; we used the local 7B. A stronger policy model could be more robust or diferently exploitable, afecting external validity.

• Travel suite excluded. Travel induced pathologically long agent loops on the 7B, making it computationally prohibitive; we excluded it rather than report partial data. The three included suites span the observed range.

• Not peer-reviewed. Preliminary internal results.

Our central systematization claim, that adaptive evaluation was missing and matters, is now partly discharged by §11 for one defense; extending it to CaMeL, FORGE, stronger models, and stronger attacks is future work.

# 13. Related work

Diagnosis. Schneier on data/control confusion [3]; Willison’s SQL-injection analogy and dual-LLM pattern [2], [25]; StruQ’s class membership [4]; Zverev et al. on the instruction/data separation failure [26].

Out-of-band defenses. CaMeL [15], FIDES [16], Progent [17], Conseca [18], IsolateGPT/SecGPT [19], RTBAS [20], the IFC system of Wu et al. [21], permissive IFC for LLMs [22], the Design Patterns catalog [23], PFI [24], Bhattarai and Vu [27], and FORGE [28].

The classical-principles framing. Zhang et al. argue agents should adopt Saltzer–Schroeder directly [44]; Shi et al. systematize via authorization [30]; our §5 uses the same lens.

Systematizations. Liu et al.’s prevention-vsdetection benchmark [29]; Shi et al. [30]; the 2026 landscape and attack-surface SoKs [31], [32]; Ji et al.’s defense taxonomy [33]. These catalog mechanisms and gaps but do not run a standardized independent adaptive action-level evaluation.

Adaptive evaluation of action-level defenses. Progent’s authors already evaluate adaptive attacks on their own policy-update LLM (Appendix E of [17]), reporting robustness under a vulnerable-user auto-approve simulation; our §11 is an independent reproduction and extension of that setting on an open-weight model. AgentDyn [45] introduces a dynamic, open-ended benchmark and directly re-evaluates Progent (alongside CaMeL and DRIFT), documenting policy-assignment and over-defense problems in realistic tasks. Our work complements these with repeated-run variance on a self-hosted open-weight agent.

![](images/7a8b26cce914e55a5bf72413cfae864c2a86daf0adbb435bc574c0d58c64c246.jpg)

[Image: This grouped bar chart illustrates attack success rates (%) comparing standard static attacks against adaptive, defense-aware attacks across two defense strategies. For in-band defenses relying on detection or fine-tuning, the adaptive attack succeeds 90% of the time compared to only 3% for standard attacks. The out-of-band defense (Progent) effectively mitigates both threats, showing negligible success rates of 4% and 3% respectively for standard and adaptive attacks.]  
Figure 5: The contrast that motivates the paper. In-band defenses go from near-zero reported attack success to >90% under adaptive attack [36]; our out-of-band defense stays low (4.2% → 2.6% under the adaptive attack, n=3). The in-band bars are reported by Nasr et al. under diferent setups and are shown for qualitative contrast, not as a controlled comparison.

Adaptive attacks (in-band). Jia et al. [34], Pandya et al. [35], and Nasr et al. [36], the basis of §4 and the precedent for §7.

Benchmarks and standards. AgentDojo [37], ToolEmu [38], OWASP LLM01:2025 [39], NIST AI 600-1 [40], OpenAI [41], and the Cisco analysis [42].

# 14. Conclusion

We have solved control/data confusion before, in databases, in the browser. Each time, detection failed and structure won, and the structure lived outside the channel the attacker controlled. The agent-security field has relearned this and built out-of-band defenses that are deterministic, sound in design, and already deployable as retrofits. That is real progress, and we do not understate it.

This version supplies a first piece of the evidence the previous one called for. We reproduced and extended Progent’s own adaptive-attack setting, three times, on a weak open-weight model its authors did not test, and the deterministic gate held: Progent cut attack success \~6× (25.8% → 4.2%) and our adaptive attack failed to raise it (2.6%), with small run-to-run variance, landing in the same low band (\~0.5–4.2%) Progent’s authors report for their own adaptive attacks [17]. That is the opposite of what adaptive attacks did to in-band defenses, and it is consistent with out-of-band enforcement being a harder target in kind, not merely in benchmark scores, though, as we stress in §11.3 and §12, a single weak attack on one weak model and a possible confound mean it does not establish that. It is a preliminary data point, not a proof, and a smarter attack, especially an optimized white-box attack, or one confined to alreadyauthorized actions, remains the open threat.

For LaunchSafe the working implication is to build defense on deterministic, out-of-band actionmediation as the most promising foundation against an adaptive attacker, while treating the real open problems as cost, deployability, and the harder attacks not yet run, and remembering that its robustness against a serious optimized adaptive attacker is, on the evidence here, still unproven. This work guides LaunchSafe’s own agent-security tooling (launchsafe.com), built on this deterministic, out-of-band foundation. The honest next question we hand ourselves: can an adaptive attack that lives entirely within the agent’s authorized action space still get through? That is the next study.

# References

[1] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, M. Fritz. “Not what you’ve signed up for: Compromising Real-World LLM-Integrated

Applications with Indirect Prompt Injection.” AISec ’23 @ ACM CCS; arXiv:2302.12173, 2023.

[2] S. Willison. “Prompt injection attacks against GPT-3.” simonwillison.net, Sep. 2022.

[3] B. Schneier. “LLMs’ Data-Control Path Insecurity.” Schneier on Security / CACM, May 2024.

[4] S. Chen, J. Piet, C. Sitawarin, D. Wagner. “StruQ:

Defending Against Prompt Injection with Structured Queries.” USENIX Security 2025; arXiv:2402.06363.

[5] K. J. Biba. “Integrity Considerations for Secure Computer Systems.” ESD-TR-76-372 (MITRE MTR-3153), 1977.

[6] J. P. Anderson. “Computer Security Technology Planning Study.” ESD-TR-73-51, Vol. I, USAF, 1972.

[7] J. H. Saltzer, M. D. Schroeder. “The Protection of Information in Computer Systems.” Proc. IEEE, 63(9):1278–1308, 1975.

[8] J. B. Dennis, E. C. Van Horn. “Programming Semantics for Multiprogrammed Computations.” CACM, 9(3):143–155, 1966.

[9] H. M. Levy. Capability-Based Computer Systems. Digital Press, 1984.

[10] D. E. Denning. “A Lattice Model of Secure Information Flow.” CACM, 19(5):236–243, 1976.

[11] D. E. Denning, P. J. Denning. “Certification of Programs for Secure Information Flow.” CACM, 20(7):504–513, 1977.

[12] OWASP. “SQL Injection Prevention Cheat Sheet.” OWASP Cheat Sheet Series (accessed 2026).

[13] OWASP. “Cross Site Scripting Prevention Cheat Sheet.” OWASP Cheat Sheet Series (accessed 2026).

[14] W3C. “Content Security Policy Level 3.” W3C Working Draft, 2026.

[15] E. Debenedetti, I. Shumailov, T. Fan, J. Hayes, N. Carlini, D. Fabian, C. Kern, C. Shi, A. Terzis, F. Tramèr. “Defeating Prompt Injections by Design” (CaMeL). arXiv:2503.18813, 2025.

[16] M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. “Securing AI Agents with Information-Flow Control” (FIDES). arXiv:2505.23643, 2025.

[17] T. Shi, J. He, Z. Wang, H. Li, L. Wu, W. Guo, D. Song. “Progent: Securing AI Agents with Privilege Control.” arXiv:2504.11703, 2025. (Proxy mode applies without modifying the agent; AgentDojo indirect-injection ASR 39.9%→1.0%, ASB 70.3%→3.9%.)

[18] L. Tsai, E. Bagdasarian. “Contextual Agent Security: A Policy for Every Purpose” (Conseca). arXiv:2501.17070; HotOS 2025.

[19] Y. Wu, F. Roesner, T. Kohno, N. Zhang, U. Iqbal. “IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems” (SecGPT). NDSS 2025; arXiv:2403.04960.

[20] P. Y. Zhong et al. “RTBAS: Defending LLM Agents Against Prompt Injection and Privacy Leakage.” arXiv:2502.08966, 2025.

[21] F. Wu, E. Cecchetti, C. Xiao. “System-Level Defense against Indirect Prompt Injection Attacks: An

Information Flow Control Perspective.” arXiv:2409.19091, 2024.

[22] S. Siddiqui et al. “Permissive Information-Flow Analysis for Large Language Models.” arXiv:2410.03055, 2024.

[23] L. Beurer-Kellner et al. “Design Patterns for Securing LLM Agents against Prompt Injections.” arXiv:2506.08837, 2025.

[24] J. Kim, W. Choi, B. Lee. “Prompt Flow Integrity to Prevent Privilege Escalation in LLM Agents” (PFI). arXiv:2503.15547, 2025.

[25] S. Willison. “The Dual LLM pattern for building AI assistants that can resist prompt injection.” simonwillison.net, Apr. 2023.

[26] E. Zverev, S. Abdelnabi, S. Tabesh, M. Fritz, C. H. Lampert. “Can LLMs Separate Instructions From Data? And What Do We Even Mean By That?” ICLR 2025.

[27] M. Bhattarai, M. Vu. “Trustworthy Agentic AI Requires Deterministic Architectural Boundaries.” arXiv:2602.09947, 2026.

[29] Y. Liu, Y. Jia, R. Geng, J. Jia, N. Z. Gong. “Formalizing and Benchmarking Prompt Injection Attacks and Defenses.” USENIX Security 2024; arXiv:2310.12815.

[30] G. Shi et al. “SoK: Trust-Authorization Mismatch in LLM Agent Interactions.” arXiv:2512.06914, 2025.

[31] P. Wang et al. “The Landscape of Prompt Injection Threats in LLM Agents: From Taxonomy to Analysis.” arXiv:2602.10453, 2026.

[32] A. Dehghantanha, S. Homayoun. “SoK: The Attack Surface of Agentic AI.” arXiv:2603.22928, 2026.

[33] Z. Ji et al. “Taxonomy, Evaluation and Exploitation of IPI-Centric LLM Agent Defense Frameworks.” arXiv:2511.15203, 2025.

[34] Y. Jia, Z. Shao, Y. Liu, J. Jia, D. Song, N. Z. Gong. “A Critical Evaluation of Defenses against Prompt Injection Attacks.” arXiv:2505.18333, 2025.

[35] N. V. Pandya, A. Labunets, S. Gao, E. Fernandes. “May I have your Attention? Breaking Fine-Tuning based Prompt Injection Defenses using Architecture-Aware Attacks.” arXiv:2507.07417, 2025.

[36] M. Nasr, N. Carlini, C. Sitawarin, F. Tramèr, et al. “The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections.” arXiv:2510.09023, 2025.

[37] E. Debenedetti, J. Zhang, M. Balunović, L. Beurer-Kellner, M. Fischer, F. Tramèr. “AgentDojo: A Dynamic Environment to Evaluate Prompt Injection

Attacks and Defenses for LLM Agents.” NeurIPS 2024 Datasets & Benchmarks; arXiv:2406.13352.

[38] Y. Ruan et al. “Identifying the Risks of LM Agents with an LM-Emulated Sandbox” (ToolEmu). ICLR 2024; arXiv:2309.15817.

[39] OWASP. “LLM01:2025 Prompt Injection.” OWASP Top 10 for LLM Applications 2025.

[40] NIST. “Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile” (NIST AI 600-1). 2024.

[41] OpenAI. “Continuously hardening ChatGPT Atlas against prompt injection attacks.” openai.com, Dec. 2025.

[42] G. Tziakouris, R. Kramarz. “Prompt injection is the new SQL injection, and guardrails aren’t enough.” Cisco Blogs, Mar. 2026.

[43] Anthropic. “Introducing Claude Opus 4.5” and the Claude Opus 4.5 System Card. Indirect prompt-injection attack success in agentic coding environments (Gray Swan Shade tool): 4.7% at 1 attempt, 33.6% at 10, 63.0% at 100 (Opus 4.5 “thinking” variant). Anthropic, Nov. 2025.

[44] K. Zhang, Z. Su, P.-Y. Chen, E. Bertino, X. Zhang, N. Li. “LLM Agents Should Employ Security Principles.” arXiv:2505.24019, 2025.

[45] H. Li, R. Wen, S. Shi, N. Zhang, Y. Vorobeychik, C. Xiao. “AgentDyn: Are Your Agent Security Defenses Deployable in Real-World Dynamic Environments?” arXiv:2602.03117, 2026.
