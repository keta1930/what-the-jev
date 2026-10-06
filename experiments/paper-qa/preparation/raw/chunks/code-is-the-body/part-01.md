# Code Is the Body:

# Agent-Owned Software Bodies for Recursive Evolution and Descent

AN OURARK RESEARCH PUBLICATION

Roy Zhao<sup>1</sup> Zhenyu Zhao<sup>2</sup>

<sup>1</sup>Paul G. Allen School of Computer Science & Engineering, University of Washington <sup>2</sup>Independent researcher

royzh@cs.washington.edu garyzhao@gmail.com

# Abstract

Personalized AI agents are often configurable without giving users control over the artifacts that determine their future behavior. We present OurArk, an architecture for persistent personal agents centered on an agent-owned software body: an identity-bearing, inspectable, and versioned artifact under human custody. The body contains behavior-defining code, prompts, tools, skills, policies, tests, and evolution mechanisms. Memories and credentials remain private instance state, while model inference is treated as a replaceable external service.

OurArk defines governed self-evolution and recursive descent over the same body. Self-evolution produces isolated candidate changes that are validated, reviewed, and merged under human control, enabling human–agent co-development of the agent’s software body. Descent creates an independently versioned descendant with a distinct identity, mission, history, and fresh private-state boundary; compatible descendants can themselves source further descent. After divergence, direct-parent changes and peer skills can be inspected for selective local adaptation

We implement the architecture in the open-source Genesis creation engine and Enoch reference agent. A four-agent, threedescent linear lineage and executable regression tests demonstrate recursive creation, inherited validation contracts, isolated body changes, human-controlled review, and failed-update recovery. OurArk provides a concrete substrate for personal agents that people can possess, govern, specialize, and evolve over time.

# 1 Introduction

Personal computers made computation individually accessible, and smartphones made it continuously available. We believe a comparable transition for AI is toward one or more persistent agents that a person can genuinely call their own. Agents will become specialized for work, daily life, research, or other purposes, shaped over time by that person’s values, habits, feedback, and experience.

Current personalization only partially serves that goal. Agent components are often assembled and changed by a platform, so a user may customize behavior without possessing the artifacts that determine how it can evolve. Our design thesis is that a long-lived personal agent should have an identity-bearing software body that its user can possess, inspect, and govern, one that the agent and user modify continuously.

For OurArk agents, code, tools, skills, policies, tests, and evolution mechanisms belong to the body. Memories, credentials, and instance history remain private state. Finally, model inference is currently external. “Agent-owned” describes the body’s lifecycle role, while a human custodian retains possession and authority. Correspondingly, self-evolution means modifying the agent’s own body in conjunction with user oversight. The demonstrated lineage is co-evolved: humans provide purpose and promotion decisions while agents assist implementation, validation, and learning from joint work.

OurArk defines evolution and descent over the same body. Evolution produces a candidate modification to an existing body. Descent materializes a new, independently versioned agent with a distinct identity, mission, history, and fresh private-state boundary. Every compatible descendant can evolve and source another descent, so a seed can become the root of a specialized family. After bodies diverge, direct-parent changes can be exposed as candidates for local adaptation, and peer learning remains an option.

The reference implementation makes these operations concrete with standalone repositories and a reusable creation engine, Genesis. The tests verify two successive descents, in which a descendant can create another descendant. The prototype records a three-step linear lineage: Lucy to Adam to Seth to Enoch. It also supports human-governed candidate changes and requires descendants to pass inherited regression tests. We demonstrate a system where an owned, versioned artifact provides a concrete unit of continuity, descent, specialization, transfer, and governance.

This paper makes three systems contributions:

1. Agent-owned software bodies. We define a practical boundary among an identity-bearing evolvable body, private noninheritable instance state, an external reasoner, and human custody and promotion authority.

2. Governed self-evolution and recursive descent. We present an architecture in which an agent can modify its own software body through isolated implementation, validation, review, and human-controlled promotion. The same body can serve as the source for an independently versioned descendant, and compatible descendants can produce further descendants.

![](images/f893d308ff7cae1b7461e4f8e948a14b5d07cd809153032ab3620124fe4d00f7.jpg)

[Image: The image presents a block diagram of a Personal-Agent Instance architecture. A "Human custodian" at the top governs the "Versioned body" and protects the "Private instance state," which are grouped within a dashed boundary representing the instance itself. The "Versioned body," containing identity and code, maintains a runtime connection with the "Private instance state," which holds credentials and memories. Outside this boundary, an "External reasoner" for model inference connects bidirectionally to the private state via an adapter.]  
Figure 1: Body, state, reasoner, and custodian boundaries. The versioned body carries identity and evolvable behavior across restarts and descent. Private state belongs to one instance, the reasoner can be replaced without redefining lineage, and the human custodian retains administrative and promotion authority. Descent copies the body, initializes a new private-state boundary, and does not inherit model weights.

3. Independent specialization and selective transfer. After parent and descendant bodies diverge, each retains its own mission and version history. We distinguish later changes inherited from a direct parent from skills learned from peers, and implement processes for inspecting and adapting either through the receiving agent’s own testing and review process.

# 2 System Model and Design Principles

An OurArk agent instance is a tuple $A = \left( B , S , R \right)$ under a human custodian �. The body � contains identity-bearing, versioned artifacts that determine the agent’s capabilities and change process. Private state � contains credentials, memories, logs, and queues associated with one living instance. The external reasoner � supplies model inference but is not the durable carrier of identity. The custodian � possesses the body and private state and controls promotion into the authoritative body.

Here agent-owned denotes lifecycle ownership: the body is the durable artifact through which the agent’s behavior evolves. The human custodian retains custody and final authority. Ownership also does not require exclusive authorship or vendoring of every transitive library.

The architecture defines three operations:

• evolve �, � �′ produces a change in the candidate body from context or pressure �; �′ becomes authoritative only after the configured validation and promotion process.

• descend $B , m ) \ \to \ ( B _ { d } , S _ { d } )$ creates a body with a distinct identity, mission �, and version history, together with a fresh private-state boundary $S _ { d } .$

• transfer $\ { B _ { p } , B _ { d } , \Delta ) }  \ B _ { d } ^ { \prime }$ lets a descendant inspect and locally adapt a selected change Δ from a parent or peer without surrendering its independent history. These operations support six design principles:

1. Custody and continuity: the user can possess and move the body and state. The architecture does not bind identity solely to a model call or provider.

2. Body-level personalization: code, prompts, tools, skills, policies, tests, and evolution mechanisms can change, not memory alone.

3. Reproducible descent: a named source produces a runnable descendant with explicit identity, lineage, and inherited regression contracts.

4. Independent specialization: descendants evolve without forced synchronization with a parent or central template.

5. Accountable change: candidate mutations expose their request, dif, validation outcome, version, and promotion decision.

6. Human governance: mission, secrets, external permissions, deployment, and promotion remain subject to human policy and authorization.

# 3 Architecture

OurArk separates the inheritable body from private instance state and an external reasoner, then defines descent and governed evolution over that body.

![](images/b755aad95255924fbd8b44b5532f846132c273d5418ea97355d60354122af2db.jpg)

[Image: This diagram illustrates a generational lineage model starting with Lucy (G0) descending sequentially through Adam (G1), Seth (G2), and Enoch (G3). Connections between these primary generations are marked with solid lines labeled "descent." Adam also connects via a dashed "branch" arrow to a yellow box labeled "Specialized descendant." Additionally, a separate box for "Genesis," defined as a "descent operator," is shown to "materialize" into the Seth (G2) node via a dashed arrow.]  
Figure 2: Recursive descent. Solid lineage edges show the implemented linear prototype. The dashed lineage edge from Adam shows a branch permitted by the architecture but not evaluated. Genesis materializes each birth from a selected compatible body and is not the runtime owner of descendants.

## 3.1 The repository as body

An agent body is represented by a standalone, versioned repository containing:

• a machine-readable identity and mission;

• the runtime and communication interfaces;

• adapters for model reasoning and persistent memory;

• skills and action policies;

• schemas and exclusion boundaries for local configuration and instance metadata, not their private values;

• tests and diagnostic checks; and

• code for update, inheritance, learning, and evolution.

Identity declarations name the agent, generation, direct ancestor, mission, principles, source package, and skills. A separate lineage record supplies ancestry, an immutable parent-at-birth source, the descendant’s birth commit, and a route for discovering later parent changes. The repository is the inheritable body while a working copy plus excluded local state is a living instance of that body.

## 3.2 Reasoning outside the body

OurArk agents invoke a model through a session adapter, supplying it with selected identity, memory, repository, and task context. Model weights and service state are not durable agent identity. This lets reasoner replacement remain distinct from body evolution.

## 3.3 Genesis: creating descendants

Genesis currently accepts an agent name, mission, target repository, and a selected ancestor source. It performs the following transformation:

1. verify a clean tracked ancestor, record its full commit identifier, and resolve its declared manifest of tracked UTF-8 body files and pinned runtime dependencies;

2. copy identity-specific body artifacts while transforming package paths and identity-bearing text, retaining immutable dependency references;

3. write the new identity, mission, generation, and immutable direct-parent provenance;

4. initialize and stage an independent repository;

5. resolve declared dependencies, run the inherited suite, and reject a failed or dirty validation; and

6. create the birth commit only after validation succeeds, then record its full identifier in a metadata-only provenance commit.

Any compatible Genesis descendant can serve as the source for another generation. In the current prototype, compatibility means that Genesis can resolve the source body’s declared manifest and pinned dependencies, perform its required identity transformations, and complete inherited validation without modifying the recorded source. Recursive compatibility, rather than a privileged root template, creates the lineage. Genesis materializes the selected parent’s declared body composition, including accumulated identity-specific capabilities, adapters, and tests, instead of regenerating every agent from a central schema.

## 3.4 Governed body evolution

Body evolution in Enoch can originate from six sources: an explicit user request, human feedback, joint-work experience, direct-parent inheritance, cross-agent learning, and LLM brainstorming. A user request is a direct instruction to modify the agent’s body and can initiate the change workflow directly. Feedback and experience are derived from prior conversation turns and work-event histories and may be converted into candidate improvements. Through inheritance, Enoch can inspect later changes made by its direct parent. Through learning, it can inspect skills published by other agents. In either case, selected material is adapted to Enoch’s own body rather than applied automatically. For brainstorming, a user provides an evolution theme, and a model session proposes possible improvements.

![](images/a238eef7f765feccba4f1c633e314dc8d4791cebc1d9cc9a30e8e8443165d8ff.jpg)

[Image: A horizontal flowchart illustrates a six-stage process beginning with "Six sources" such as user requests, feedback, and learning. The workflow progresses through "Pressure" (optional theme) and "Co-evolve" (select, adapt, implement), passes a "Validate" gate, undergoes a "Promote" stage via human decision, and concludes with an "Evolved body." A caption below states that rejected or failed candidates leave the authoritative body unchanged.]  
Figure 3: Single-lane co-evolution flow. Six sources expose candidate pressures, the human and agent jointly shape a candidate body change, validation checks it, and the human controls promotion. A failed or rejected candidate leaves the authoritative body unchanged.

The architecture requires durable body versions, isolated candidate changes, validation gates, inspectable change records, human-controlled merge decisions, and failed-update rollback. The reference implementation realizes this lifecycle with Git branches, commits, GitHub pull requests, and isolated worktrees. Whether a change begins as a direct user request or as an approved candidate, Enoch isolates the work, modifies the body, runs validation, and publishes the result for review. A human decides whether the reviewed change is merged. Rejected or failed work leaves the authoritative body unchanged. If a later update to the authoritative revision fails its post-update health checks, Enoch restores the previous revision and does not restart into the failed version. The demonstrated protocol operates in co-evolve mode: Enoch can help propose, implement, and validate changes, but humans retain merge authority.

## 3.5 Inheritance, learning, and specialization

OurArk distinguishes three forms of capability transfer:

Descent copies a parent’s body once to create a new independent agent.

Inheritance is selective and pull-based. A descendant asks its declared direct-parent source for recent change candidates and may adapt one through its own branch, tests, and review. Parents do not push mutations into living descendants, and descendants do not continuously mirror a shared base. The current implementation records an immutable birth baseline for new descendants and uses it to resolve historical lineage.

Learning imports a published skill or pattern from any trusted agent. Unlike inheritance, learning is not constrained to the parent edge and is explicitly an adaptation rather than ancestry.

This difers from object-oriented inheritance. A subclass obtains behavior through a live class relation; an OurArk descendant receives a body once and later chooses whether to adapt a parent change after divergence. It may reject that change or learn from a peer while preserving its own mission and history.

# 4 Implementation

The prototype is implemented in Python and organized as separate repositories. It is reasoner-agnostic: the mechanism checks reported in Section 5 run locally without live model inference, and model calls are mocked where adapters are exercised. External coding agents assisted the co-evolution process, but model choice was neither controlled nor evaluated as an experimental variable. Enoch factors chat, reasoning runtime, version control, and code-forge access behind provider protocols. Telegram, Codex, Git, and GitHub are the bundled adapters rather than architectural requirements.

Use of generative AI tools. OpenAI ChatGPT assisted with manuscript drafting, revision, and citation checking. AI coding agents assisted software implementation, testing, and documentation during the co-evolution process. The authors reviewed and verified all generated material and take full responsibility for the paper, references, claims, and software.

Unless otherwise stated, the implementation description and executable evidence refer to the frozen Genesis v0.1.1 and Enoch v0.3.1 snapshots. Later default-branch development is outside the evaluated snapshot.

The lineage is also a compact co-evolution case study:

<table><tr><td></td><td>Generation</td><td>Body</td><td>Capability transition</td><td>New body mechanisms</td></tr><tr><td></td><td>0</td><td>Lucy</td><td>Exist as an owned agent body</td><td>identity, mission, minimal runtime, memory boundary, teaching, and tests</td></tr><tr><td></td><td>1</td><td>Adam</td><td>Operate and inherit</td><td>operational interfaces, instances, lineage, direct-parent inheritance, and peer learning</td></tr><tr><td></td><td>2</td><td>Seth</td><td>Work on delegated and ongoing tasks</td><td>task execution, backlog, queues, scheduled jobs, and status reporting</td></tr><tr><td></td><td>3</td><td>Enoch</td><td>Evolve its own body under governance</td><td>multi-pathway evolution intake, provenance records, isolated worktrees, validation, review handoff, and failed-update rollback</td></tr></table>

The lineage shows cumulative specialization from exist → operate and inherit → work → evolve.

Genesis is maintained as a separate creation engine rather than embedded in the root, allowing creation from any compatible body without making Genesis the runtime owner of descendants. The v1 public artifacts are Genesis and the Enoch body. Lucy, Adam, Seth, and all credentials, memories, logs, chat identifiers, and runtime task state remain private. Reviewable Enoch code-change records remain visible in its public repository. The reproducibility snapshot below refers to immutable public Genesis and Enoch commits.

# 5 Executable Mechanism Evidence

The prototype is intended to show that the architectural mechanisms execute, not to claim a new model capability or benchmark result. The first table maps each principal claim to executable evidence in the tested prototype.

<table><tr><td>Architecture claim</td><td>Executable evidence</td><td>Status</td></tr><tr><td>Recursive descent</td><td>Genesis creates independently versioned first- and second-generation bodies and records full parent-at-birth and descendant-birth identifiers.</td><td>demonstrated</td></tr><tr><td>Body/state boundary</td><td>Tracked-body selection excludes untracked worktree artifacts, while agent tests keep configured private instance state outside inherited body files.</td><td>demonstrated</td></tr><tr><td>Inherited contracts</td><td>A descendant resolves pinned dependencies and runs its inherited suite before birth. Failed or dirty validation prevents the birth commit.</td><td>demonstrated</td></tr><tr><td>Governed body evolution</td><td>Enoch hands approved candidates to the normal task workflow, performs changes in isolated worktrees, validates them, and publishes reviewable work while a human retains merge authority. A failed software update restores the previous revision.</td><td>demonstrated</td></tr><tr><td>Multi-source evolution</td><td>Enoch evolves from all six sources and links proposal decisions to implementation tasks.</td><td>demonstrated</td></tr><tr><td>Post-divergence transfer</td><td>New descendants expose an immutable baseline and tests distinguish direct-parent inheritance from peer-learning routes, but no controlled end-to-end adaptation has been run.</td><td>partial</td></tr></table>

For reproducibility, the following snapshot reports release validation results and one cross-artifact compatibility gate. Each linked commit is immutable and public.

The open-source artifacts are available at our-ark/genesis and our-ark/enoch. All reported results refer to the immutable releases and commits below. The Apache-2.0 code artifacts are provided as versioned releases: Genesis v0.1.1 and Enoch v0.3.1.

<table><tr><td>Artifact</td><td>Public snapshot</td><td>Runtime</td><td>Validation scope</td><td>Result</td></tr><tr><td>Genesis</td><td>e7bb896</td><td>CPython 3.12</td><td>creation, recursive descent, body selection, pinned dependencies, and inherited validation</td><td>29/29 passed</td></tr><tr><td>Enoch body</td><td>1021e1d</td><td>CPython 3.11–3.14</td><td>complete body suite, including evolution, inheritance, learning, task execution, updates, and worktree management</td><td>753/753 passed</td></tr><tr><td>Genesis × Enoch</td><td>e7bb896 + 1021e1d</td><td>CPython 3.12</td><td>descendant birth with inherited Enoch contracts and pinned shared-library references</td><td>passed</td></tr></table>

The Enoch v0.3.1 release CI passed on CPython 3.11, 3.12, 3.13, and 3.14. The Genesis v0.1.1 release CI also passed on those Python versions, together with its macOS/CPython 3.12 job. The final cross-artifact check ran Genesis from its frozen release commit against the exact public Enoch v0.3.1 commit. It created a fresh descendant, ran the inherited validation contracts, and preserved the declared body and pinned-dependency boundaries.

The snapshot can be rerun after checking out Genesis v0.1.1 and Enoch v0.3.1 in their respective repository roots:

```shell
# Genesis v0.1.1
python -m unittest -q tests/test_genesis_creator.py

# Enoch v0.3.1
python -m pip install --disable-pip-version-check --require-hashes \
-r .github/requirements/test-build.txt

python -m unittest discover -s tests -t .
python -m unittest discover -s libraries/launchd/tests
python -m unittest discover -s libraries/systemd/tests

# From the Genesis v0.1.1 repository against Enoch v0.3.1
python scripts/verify_enoch_descent.py \
--source https://github.com/our-ark/enoch.git \
--ref 1021e1dacce85f4a2edebd865673671bb37a2142 \
--trust-source \
--name my-agent
```

# 6 Discussion

OurArk contributes an agent framework. The long-term direction is a personal ecosystem rather than one universal assistant. A person might own several bodies with diferent missions, skills, permissions, and private-state boundaries. Shared ancestry can reduce creation cost while independent histories preserve specialization. A future Intent-to-Agent Materialization layer could map natural-language intent to a trusted source body, adapt and validate it, and place the result under the user’s custody. The current Genesis instead requires a user-selected source, name, and mission.

Git is not an architectural requirement. Another substrate could supply durable identifiers, isolated changes, inspectable diferences, validation, promotion, and recovery. Conversely, a branch alone lacks the identity, mission, state, interface, and authority boundaries that make an independently running agent.

# 7 Limitations and Threats to Validity

The prototype contains one co-evolved linear lineage from one development team with no sibling branch or population-scale process evaluated. Tests mostly use mocked services and establish mechanisms, not long-running reliability, proposal or specialization quality, review burden, or semantic safety. Behavioral continuity across reasoner replacement is also unmeasured.

Genesis rewrites identity-bearing text using boundary-aware string substitutions rather than language-specific parsers. Its manifest checks and inherited tests reject invalid body declarations and detected regressions, but cannot guarantee that every transformed file is semantically correct. New descendants record exact parent-at-birth and descendant-birth commits, whereas the historical Lucy-to-Enoch lineage predates this provenance format. Inheritance discovery is intentionally bounded, and we have not evaluated a complete post-divergence transfer from discovery through adaptation and adoption.

The strongest authority boundary is human-controlled merge through the protected branch and review path. The writeenabled executor has broader filesystem authority than a production mutation sandbox should permit. Task, evolution, and lineage records are not tamper-evident, and protected-scope checks remain procedural rather than semantic guarantees. Provider protocols have been exercised with bundled adapters. In the evaluated snapshot, lineage discovery and cross-agent skill lookup still assume forge-hosted repositories and OurArk naming conventions. Pinned dependency resolution and descendant validation are tested. Shared libraries remain replaceable through the agent-owned adapter and dependency manifest.

Our claims are therefore limited to architecture, implemented mechanisms, and regression evidence.

