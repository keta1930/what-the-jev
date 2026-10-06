# Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents

Praneeth Narisetty, Shiva Nagendra Babu Kore,

Uday Kumar Reddy Kattamanchi, Jayaram Kumarapu

LaunchSafe Research

{praneeth, shiva, uday, jayaram}@launchsafe.com

# Abstract

Recent work (2024 to 2026) has converged on a strategy for defending tool-using LLM agents against indirect prompt injection: rather than training the model to refuse malicious instructions, enforce security outside the model with a deterministic policy that mediates the agent’s actions. Systems such as CaMeL, FIDES, Progent, RTBAS, and FORGE realize this with capabilities, information-flow labels, and reference monitors, and several report near-elimination of attacks on the AgentDojo benchmark. We make two contributions. First, we organize these out-of-band defenses as instances of classical integrity protection (Biba), reference monitoring, and least privilege, yielding a structured comparison of what they do and do not cover. Second, we warn that every one of them is validated only on static benchmarks (a fixed set of injection attempts), the same methodology that made in-band defenses look strong until adaptive, defense-aware attacks broke twelve of them at over 90% success; we specify the threat model and protocol an adaptive evaluation requires. We then run that protocol as an independent reproduction and extension of Progent’s own adaptive-attack analysis, on AgentDojo, with an open-weight agent (Qwen2.5-7B) self-hosted on a single H200, a setting its authors did not test. Averaged over three runs, the defense held: Progent cut mean attack success roughly sixfold (25.8% to 4.2%), and a hand-crafted adaptive attack did not raise it (2.6%). This is one small-scale data point on a weak model with a single black-box attack template; a stronger optimized (white-box GCG) attack remains open. The result is consistent with, but does not establish, the hypothesis that deterministic out-of-band enforcement is a harder target for an adaptive attacker than in-band detection.

Keywords: prompt injection, indirect prompt injection, prompt injection defense, LLM agents, LLM agent security, AI agent security, agentic AI, autonomous agents, tool-using language models, tool use, function calling, out-of-band defense, reference monitor, privilege control, least privilege, Biba integrity,

Saltzer–Schroeder, information-flow control, capabilities, taint tracking, adaptive evaluation, adaptive attacks, defense-aware attacks, adversarial robustness, red teaming, jailbreak, GCG, AgentDojo, ASB, Progent, CaMeL, FIDES, FORGE, RTBAS, Qwen2.5, LLM security, AI safety, AI security.

# 1. Introduction

A production LLM agent is given tools, and through them, consequences: it can read a database, call an internal API, send mail, move money. It also reads text it does not control (a web page, a support ticket, a PDF, the body of an email it was asked to summarize). When an attacker plants instructions in that text and the agent follows them, the damage is not a bad sentence but an action: a leaked record, a deleted row, a transfer. This is prompt injection [1], and in an agent with tools it is an authorization problem, not a content problem.

The first generation of defenses treated it as content. Input classifiers, guardrail models, jailbreak detectors, and adversarial fine-tuning all try to recognize malicious text. By 2025 the evidence against this approach was strong: adaptive attackers recover high success rates against the detectors they were tested on [34], [36], and vendors building production agents now say plainly that injection is unlikely to be fully solved at the model layer [41].

The second generation gave up on the model and moved enforcement outside it. If the model cannot be trusted to refuse, then wrap it in a layer that decides what actions are permitted regardless of what the model was talked into. CaMeL [15], FIDES [16], Progent [17], RTBAS [20], Conseca [18], and FORGE [28] are instances of this move. They difer in mechanism, capabilities, taint labels, symbolic privilege rules, isolation, but they share a structure that security has used since the 1970s: a deterministic reference monitor enforcing a policy at the point where an action takes efect. Several report strong results. Progent cuts AgentDojo indirectinjection success from 39.9% to 1.0% [17]; CaMeL solves 77% of AgentDojo tasks under attack with no successful injections in its threat model, against 84% undefended

[15].

This paper does two things. Sections 2–6 organize the second-generation defenses through the classical primitives they instantiate, and compare them on a common set of dimensions. This framing is not ours to claim, Zhang et al. argue LLM agents should adopt the Saltzer–Schroeder principles directly [44], Bhattarai and Vu build an architecture on reference monitors plus information-flow control [27], and Shi et al. systematize the field through an authorization lens [30]. We use the lens because it makes the comparison sharp, not because it is new.

The contribution is in Sections 7–10, and it is a problem the field has not confronted. The second-generation defenses are evaluated the same way the first generation was: against a fixed benchmark of attacks. That method already failed once. Nasr et al. took twelve published inband defenses, most reporting near-zero attack success, and recovered success above 90% for most of them with adaptive, defense-aware attacks [36]. The action-level defenses have not faced this test. Their reported numbers describe how they perform against attacks chosen before the defense existed, not against an attacker who knows the defense and optimizes against it. We argue this makes current confidence premature, specify what an adaptive evaluation of an action-level defense would require, and, new in this version (§11), execute that evaluation against Progent as an independent reproduction and extension of the adaptive-attack analysis its own authors report in their Appendix E [17].

2. Prompt injection is an old vulnerability class Prompt injection is the newest case of a failure that recurs wherever one channel carries both control and data with no structural boundary between them.

Table 1: The same control/data confusion recurs across eras of computer security.

<table><tr><td>Era</td><td>Vulnerability</td><td>What gets confused</td><td>What fixed it</td></tr><tr><td>1990s</td><td>Buffer overflow, format string</td><td>Attacker data overruns into control state</td><td>Bounds, W^X, non-executable data</td></tr><tr><td>2000s (DB)</td><td>SQL injection</td><td>User input concatenated into a parsed query</td><td>Parameterized queries [12]</td></tr><tr><td>2000s (web)</td><td>Cross-site scripting</td><td>User input rendered into parsed markup</td><td>Output encoding; CSP [13], [14]</td></tr><tr><td>2020s</td><td>Prompt injection</td><td>Untrusted text shares the token stream with instructions</td><td>(open)</td></tr></table>

Schneier frames the root cause directly: mixing data with commands “is at the root of many of our computer security vulnerabilities” [3]. The StruQ authors place prompt injection in the family by name: it is “yet another instance of this vulnerability pattern” [4]. Willison drew the SQL-injection parallel when he named the attack in 2022 [2].

The cured members of the family teach one lesson: detection lost and structure won. SQL injection was not solved by better recognition of malicious queries but by parameterized queries, which fix the query’s structure before binding user input so that input cannot be parsed as control [12]. XSS was contained by output encoding and a policy on where executable content may come from [13], [14].

Prompt injection resists the same fix in one specific way. SQL has a grammar, so a prepared statement can separate code from data because a parser distinguishes them. Natural language has no such grammar, and the model is trained to follow instructions wherever they appear. Zverev et al. measure this: current models do not maintain a usable separation between instructions and data, and neither prompting nor fine-tuning reliably induces one [26]. This is the structural fact the whole field rests on: control/data separation cannot be enforced inside the model, so it must be enforced outside it. Figure 1 contrasts the two postures.

(The pre-digital precedent is in-band telephone signaling, where control tones travelled on the voice channel and could be forged; the industry moved signaling out of band. We note it as an analogy, not as a claim about why SS7 was designed.)

# 3. Threat model

We use the threat model now standard in this literature [15], [16], [37], and state it because disagreements about defense efectiveness are often disagreements about the model.

Assets. Integrity of consequential actions (tool calls, writes, sends, payments) and confidentiality of data the agent can reach (system prompts, user records, retrieved private documents).

Trust labels. The system prompt is high-integrity. The primary user’s direct input is treated as highintegrity, with the caveat in §8.3 that this can be wrong. Everything else (retrieved documents, web pages, tool results, file contents, email, prior outputs of other agents, persisted memory) is untrusted.

Attacker. Controls the content of at least one untrusted channel, knows the system design including any deployed defense, and is adaptive: it can iterate, optimize adversarial strings, and craft inputs against the specific monitor in place [34], [36]. It does not control the model weights or the enforcement layer.

Direct vs. indirect. Direct injection arrives in the user’s turn; indirect injection arrives in content the agent consumes while working [1]. Indirect injection is the harder case for tool-using agents and our focus.

Why actions are the point. A chatbot that says something harmful is a content failure; an agent that does something harmful is an authorization failure. The defenses we study target actions. Section 8.1 returns to the harms this scope leaves out.

(a) In-band: control and data share one channel  
![](images/5cdfa7541565409b279a0f7dfafe323e4747a8c17d32cd2fb2a0a8e076011d45.jpg)

[Image: This flowchart illustrates a system architecture labeled as "In-band," where "Trusted instructions" and "Untrusted data" are both directed into a single shared component labeled "One token stream (no boundary)." Arrows indicate that these distinct inputs merge without distinction before flowing into a gray block identified as an "LLM" (Large Language Model). The final output of this pipeline is an "ACTION," demonstrating a direct link between the merged inputs and the resulting behavior. According to the accompanying caption, this setup represents a vulnerability where control signals and data share the same transmission medium, potentially allowing untrusted data to influence the model's execution.]  
The model follows whichever instruction it reads, injected or not

(b) Out-of-band: a deterministic layer mediates the action  
![](images/743e821fe6eb9821d68d60e268bed0134afa65a5f264a9b93a82d815300b38cc.jpg)

[Image: The image displays a flowchart illustrating a process where "Trusted [HIGH]" and "Untrusted [LOW]" inputs are directed into a module labeled "LLM (may be compromised)." The output of the model is a "Proposed action," which serves as input for a subsequent "POLICY MONITOR" block. Finally, the policy monitor determines the outcome of the pipeline, leading to a final decision to "Allow / deny" the action.]  
Provenance-tagged inputs; low-integrity data cannot authorize a high-integrity action  
Figure 1: The same vulnerability, two postures. (a) In-band: control and data share one token stream. (b) Out-ofband: a deterministic monitor mediates the action.

# 4. In-band defenses provide no guarantee against adaptive attackers

By in-band defenses we mean those operating on or inside the model and channel under attack: input/output classifiers, guardrail models, instruction hierarchies, spotlighting, and adversarial fine-tuning (StruQ, SecAlign, and successors). We report scores in the units the sources use, attack success values (ASV) and false-negative rates (FNR) on a 0–1 scale.

The instruction hierarchy leaks before any adaptive efort: on GPT-4o-mini it admits existing combined attacks at ASV 0.68 (OpenPromptInjection) and 0.75 (MMLU-PI) [34].

Fine-tuning defenses fall to adaptive optimization. Against adaptive GCG, Jia et al. drive StruQ to ASV \~1.00 on MMLU-PI and 0.80–1.00 on OpenPromptInjection, and SecAlign to 0.88 on MMLU-PI (0.46 on OpenPromptInjection), far above the near-zero values originally reported, and both lose utility under attack [34]. Pandya et al. break StruQ, SecAlign, and a successor with an architecture-aware attack at up to 85–95% success on unseen prompts [35].

Detectors trade a flattering metric for a real blind spot. Attention Tracker reaches AUC 1.00 on standard benchmarks but has FNR 0.69 on MMLU-PI, and a separatortoken-only adaptive attack pushes that to 1.00, a full bypass with trivial efort [34]. AUC on a static benchmark overstates resilience.

The clearest result is Nasr et al.: twelve published defenses, most originally reporting near-zero attack success, broken at above 90% for most under adaptive attack, spotlighting and sandwiching above 95%, PromptGuard and Model Armor above 90%, MetaSecAlign at 96%, with known-answer detectors and others also falling; human red-teaming reached 100% [36].

A guardrail model used to screen for injections is itself a model and is itself injectable, as OWASP’s guidance notes [39], which follows directly from §2.

Industry has conceded the model-layer limit. OpenAI states injection is “unlikely to ever be fully ‘solved’ ” [41]. Anthropic’s strongest reported numbers for Claude Opus 4.5 are real but not guarantees: against indirect prompt injection in agentic coding environments (Gray Swan’s Shade adaptive red-teaming), attack success rises from 4.7% at one attempt to 33.6% at ten and 63.0% at one hundred [43]. A defense whose failure probability climbs toward certainty under repetition reduces incidents; it does not bound them.

Two clarifications matter for what follows. First, “no guarantee” is the defensible claim, and it is a structural one: §2 shows the model has no reliable instruction/data boundary, so no amount of in-band training or filtering can promise to refuse. It is not the stronger claim that in-band defenses always fail, some hold non-adaptive attacks to low success rates, and they have value as one layer of defense-in-depth. Second, and this is the thread of the paper: the reason adaptive attacks are decisive here is that the in-band defenses were believed efective on the strength of static benchmarks, and the belief did not survive contact with an attacker who optimized against them.

# 5. The classical lens

Enforcement that the model cannot provide must come from a deterministic mechanism around it. Security named that mechanism long ago, and reading the modern defenses through it makes them comparable. We present this as a lens, not a discovery; prior work uses the same vocabulary [27], [30], [44].

Biba integrity. Biba’s model protects against improper modification with two rules: a subject may not read data below its integrity level without being lowered to that level (Simple Integrity, the low-water-mark reading), and a subject may not write above its level (the Star Integrity property, “no write up”) [5]. Applied to an agent: when the model reads untrusted data its effective integrity drops, and a dropped subject may not authorize a high-integrity action. Both rules are needed, the first to capture the contamination, the second to block the action. Figure 2 shows the invariant.

Reference monitor. Anderson’s reference monitor validates every access against the policy, and must be always invoked (complete mediation), tamperproof, and small enough to verify [6]. Every credible action-level defense is a reference monitor at the tool boundary; the three requirements give a checklist, and a vocabulary for failures (a side channel is incomplete mediation; an LLM that authors the policy strains verifiability).

Saltzer–Schroeder. The 1975 principles map onto agent security: complete mediation, least privilege, failsafe defaults, and economy of mechanism [7]. Progent’s per-tool-call checking enforcing least privilege [17] and the preference for a small deterministic policy engine over a model-based judge are direct applications. Zhang et al. make the same mapping the center of their proposal [44].

Capabilities and information flow. A capability is an unforgeable token carrying both the designation of an object and the rights to it, which removes ambient authority [8], [9], CaMeL’s “capability” tags a value’s provenance and permitted readers and is checked at toolcall sinks [15]. Information-flow control labels data and propagates the labels under a lattice order [10], with the classic dificulty being implicit flows through control decisions [11]; FIDES’s taint labels [16] and the IFC framing of Wu et al. [21] instantiate it, and the implicit-flow problem is exactly the side channel CaMeL reports against itself.

Read this way, the defenses line up: Dual-LLM [25] separates subjects by integrity; CaMeL [15] adds capabilities and a deterministic interpreter; FIDES [16] is taint tracking with integrity and confidentiality labels; Progent [17] is least privilege via symbolic per-call rules; RTBAS [20] gates tool calls on flow labels (and we read it as enforcing the same integrity invariant, though it does not invoke Biba by name); FORGE [28] is a reference monitor over Datalog policies. The lens organizes them; it does not, by itself, tell us which ones survive a real attacker.

# 6. A systematization of out-of-band defenses

We compare the principal defenses on eight dimensions: (D1) enforcement primitive; (D2) is the gate deterministic or an LLM in the loop; (D3) where the monitor sits; (D4) integrity (action) coverage; (D5) confidentiality coverage; (D6) implicit-flow / side-channel handling; (D7) reported cost; (D8) can it retrofit onto an unmodified agent. These dimensions follow from the referencemonitor and IFC framing of §5; we do not claim they are the only possible axes, and the classification of each row reflects the sources’ own descriptions.

Three points. The gates are deterministic where it counts (D2): the field learned that the gate must not be a model. Confidentiality and implicit flows are the weak columns (D5, D6), most systems gate actions well and handle exfiltration and side channels poorly, a point §8 develops. And contrary to a common impression, retrofit is not the open problem (D8): Progent’s proxy mode applies “without altering the agent’s internal implementation” [17], and FORGE enforces policies “without modification to the underlying agents” [28]. Deployment onto existing agents is, at least in prototype, already solved.

(D7 mixes units, task percentages, token multipliers, utility loss, because the sources do; it should be read as “what each paper reports,” not a normalized comparison.)

# 7. The gap is evaluation, not deployment

If retrofit is solved and the mechanisms are sound, what is missing? The answer is in column D7 and in how every cell in the table was produced. Most of each defense’s headline security is reported against a static benchmark: AgentDojo’s fixed injection set [37], ASB, or similar. The attacks were fixed before the defense existed. Adaptive evaluation has begun in places, Progent’s authors construct adaptive attacks against their own policy-update LLM in Appendix E [17], and Agent-Dyn [45] re-evaluates Progent and CaMeL on harder dynamic tasks, but the field still lacks a standardized, independent, defense-aware adaptive protocol applied across these systems, attack families (black-box and white-box), and models.

This is the precise methodology that failed for in-band defenses. StruQ, SecAlign, PromptGuard, Spotlighting, and the rest reported near-zero attack success on static benchmarks. Then Jia et al. and Nasr et al. let the attacker move second, and the numbers inverted, twelve defenses above 90% [34], [36]. The static benchmark did not measure what it was taken to measure. It measured resistance to a known attack set, and was read as resistance to attackers.

We have no result showing the action-level defenses would fall the same way. Their gates are deterministic, which is a harder target than a classifier, and an adaptive attacker faces a diferent problem: not “evade a detector” but “drive a consequential action while respecting the policy.” That may be genuinely hard. But it is untested. The defenses’ authors are often careful about this, CaMeL demonstrates side channels against itself [15], Progent constructs adaptive attacks on its own policy LLM [17], and FORGE and Conseca name adversarial-planning risks, yet the systematic, independent, multi-attack adaptive evaluation that the in-band defenses received has not been assembled for this class. Until that happens, the field is largely in the position it was in for in-band defenses just before they broke: confident, on the basis of an evaluation method with a demonstrated blind spot.

![](images/2d8081306c7c2f0259d1f87db83a7988c2c608baef0ee2d4ae110ea933b80fcb.jpg)

[Image: The diagram illustrates a security model distinguishing between high and low data classifications. The top "HIGH" tier contains system prompts and authority to call tools, while the bottom "LOW" tier includes attacker-influenceable inputs like web pages and emails. A downward arrow signifies that reading low data lowers the trust of the subject, marked by a note about the "low-water-mark." Conversely, an upward red arrow terminating in an "X" enforces a "No write up" rule, indicating that low-level data cannot authorize high-level actions.]  
Figure 2: The Biba integrity invariant on an agent’s action surface. Reading low-integrity data lowers the subject (Simple Integrity / low-water-mark); a lowered subject may not authorize a high-integrity action (no write up). The only sanctioned upward path is endorsement from a trusted channel.

Table 2: Systematization of out-of-band defenses across eight dimensions (D1–D8).

<table><tr><td>System</td><td>D1</td><td>D2</td><td>D3</td><td>D4</td><td>D5</td><td>D6</td><td>D7 cost (reported)</td><td>D8 retrofit</td></tr><tr><td>Dual-LLM [25]</td><td rowspan="2">subject separation capabilities + CFI</td><td>deterministic controller</td><td>orchestrator</td><td>yes</td><td>partial</td><td>not addressed</td><td>design only</td><td>no (rebuild)</td></tr><tr><td>CaMeL [15]</td><td>deterministic interpreter</td><td>custom interpreter</td><td>yes</td><td>yes</td><td>side channels shown by authors</td><td>77% vs 84% tasks (o3, under attack); 2.82× in / 2.73× out tokens</td><td>no (rewrite agent)</td></tr><tr><td>FIDES [16]</td><td>taint labels (C+I)</td><td>deterministic sink check</td><td>planner</td><td>yes</td><td>yes</td><td>improves on prior IFC; trade-offs stated</td><td>no headline figure</td><td>no (adopt planner)</td></tr><tr><td>Progent [17]</td><td>symbolic privilege rules</td><td>deterministic check; LLM-authored policy</td><td>tool-call layer</td><td>yes</td><td>partial</td><td>n/a</td><td>AgentDojo 39.9%→1.0%; ASB 70.3%→3.9%</td><td>yes (proxy mode)</td></tr><tr><td>Conseca [18]</td><td>JIT policy from trusted context</td><td>deterministic</td><td>planner / executor</td><td>yes</td><td>partial</td><td>adversarial-planning risk</td><td>not reported</td><td>no (planner split)</td></tr><tr><td>RTBAS [20]</td><td>IFC + screeners</td><td>mixed (LM-judge screener)</td><td>tool-call gating</td><td>yes</td><td>yes</td><td>partly heuristic</td><td>~2% utility loss</td><td>partial (LLM in loop)</td></tr><tr><td>FORGE [28]</td><td>Datalog reference monitor</td><td>deterministic</td><td>action boundary</td><td>yes</td><td>partial</td><td>policy-dependent</td><td>not reported</td><td>yes (no agent change)</td></tr></table>

So the open question is not “can we deploy a reference monitor onto an existing agent” (yes) but “does the reference monitor hold when the attacker optimizes against it” (unknown). That is the evaluation this area lacks, and it is where efort should go.

# 8. What remains even if the defenses hold

Set aside adaptive robustness for a moment. The actionmediation approach has limits that hold by construction, which a defender adopting any system in §6 inherits. We lead with the two that are least discussed.

## 8.1 Adaptive evaluation is missing (and so is the methodology for it)

This is §7 restated as an agenda item. While individual papers probe adaptive robustness (Progent’s Appendix E [17], AgentDyn [45]), there is still no standardized, independent, defense-aware evaluation applied uniformly across action-level defenses, and no agreed threat model for what “the attacker optimizes against the monitor” means when the monitor is deterministic and the attacker’s lever is the model’s reasoning. Wang et al. and Shi et al. catalog defense gaps [30], [31], but neither runs this evaluation. Section 10 specifies what it would take.

## 8.2 Provenance assignment is the trusted base, and it is under-specified

Every labeling scheme rests on an oracle that assigns initial provenance, and the universal simplification is that the primary user’s input is trusted. Willison names the failure: if a user can be tricked into pasting untrusted content, the labels are wrong at the source [25]. FIDES’s deployed form inherits the dual risk, a forgotten label defaults to trusted [16]. Provenance is the trusted computing base of the whole approach, and assigning it correctly at real system boundaries (which header, which span, which upstream agent) is where deployments will fail. It is under-specified in every system we surveyed.

## 8.3 In-the-loop tasks

The clean defenses work by keeping untrusted data out of the trusted plan. But many real tasks require the model to act on untrusted content, “read this email and, if it’s a meeting request, add it to my calendar.” The untrusted data must drive a consequential action. The current answer is to ask the user to endorse the action (RTBAS, CaMeL) [20], [15], which both reintroduces a human judgment an attacker can target and produces approval fatigue. A principled account of which in-theloop tasks are securable does not exist, and is the deepest open problem here.

## 8.4 Text-to-text harms

Action mediation protects actions. It does nothing about injections whose payload is text, a poisoned document that yields a misleading summary, or an injected instruction to the user. CaMeL states this as an explicit non-goal [15]. As agents produce more text that people act on, this undefended channel grows.

## 8.5 Implicit flows and side channels

CaMeL demonstrates two working side channels against itself (an indirect-dependency leak and an attacker-triggered exception leak) and discusses a timing channel its implementation mitigates, concluding it “is vulnerable to side-channel attacks” [15]. This is the classical implicit-flow problem [11]. Taint systems that track only explicit data dependence miss these by construction, and sound handling pulls against the small-and-verifiable ideal of a reference monitor.

# 9. Implications for a retrofit defense

Because retrofit is already feasible (§6) and adaptive robustness is the real unknown (§7), the useful design question is narrow: what would a retrofit monitor need to do that current ones do not? One under-explored direction is provenance-awareness. Progent’s proxy checks tool-call names and arguments [17]; it does not track the provenance of the data those arguments derive from. A monitor that consulted transitive provenance could enforce the Biba invariant directly rather than approximating it with argument patterns. The obstacle is real and worth stating: a layer that sees only tool I/O cannot observe how the model laundered low-integrity text into a high-integrity argument inside its hidden reasoning (§8.5). Whether provenance-aware retrofit is achievable without instrumenting the model is an open question, and we do not claim to have answered it. We flag it as the design problem that follows from the systematization, not as a finished contribution.

# 10. A protocol for adaptive evaluation

The paper’s concrete deliverable is a specification of the evaluation §7 calls for, so that it can be run by us or others. §11 reports our first execution of it; this section states the protocol in general form.

Targets. Open or reproducible action-level defenses, Progent (open source), CaMeL, and any with available implementations, on AgentDojo [37] (97 tasks, 629 security cases) and ASB.

Attacker. Defense-aware and adaptive, following Jia et al. and Nasr et al. [34], [36]: adaptive string optimization against the deployed monitor; provenancespoofing where labels are attacker-influenceable; endorsement-targeting social engineering for in-the-loop tasks; and side-channel probes of deterministic policies. The attacker knows the policy.

Metrics. Action-level ASV/FNR on a 0–1 scale; utility retention against an undefended baseline; endorsement-request rate (a usability and §8.3-exposure proxy); and monitor overhead.

What would the result mean. If deterministic action monitors hold near-zero ASV under a strong, optimized adaptive attack, that is evidence that the secondgeneration defenses are meaningfully stronger than the first, and it would help justify the field’s current confidence. If they fall the way the in-band defenses did, the field is repeating its mistake and the reported numbers are not measuring security. Either outcome is worth knowing, and neither is known today.
