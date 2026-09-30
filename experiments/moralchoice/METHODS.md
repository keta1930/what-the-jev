# MoralChoice — Methods

## Material and adaptation

The pinned CSVs contain 687 low- and 680 high-ambiguity scenarios, totaling 1,367. A 1,767 statement in the source card conflicts with the files; the files determine coverage. Original contexts/actions/order are retained. Each request contains six questions: ab/repeat/compare in both orders. repeat is structured action selection rather than the paper's verbatim repetition, so these are not same-protocol paper comparisons.

## Scoring and stability

Low-ambiguity action1 is the reference; high ambiguity has no universal answer. reference.option_to_action maps every response to its underlying action. Reverse/compare keys must not be compared directly. Analysis reports six-variant agreement, order agreement, changes in P(action1), and first-position share. The scenario is the statistical unit; its six judgments are dependent.

Auxiliary contrasts use one explicitly Yes and one No violation label. Rules overlap and denominators must not be added. action1 share is not position preference. Reference alignment and auxiliary-rule alignment are distinct, so some low-ambiguity auxiliary rates can be below 100%. Raw judgment-level Wilson intervals in machine summaries are descriptive, not independent-sample inference; the main report uses scenario-level outcomes.

## Source anomalies

G_530 has identical actions and remains in the complete primary analysis. Excluding it gives 616/679 (90.72%) high-ambiguity six-variant agreement as sensitivity context. Spelling variants such as Do cause pain and Do not break promise remain unchanged. The paper PDF is not included.

## Integration and reproduction

Historical runs used independent scripts and budget controls. Integration only imports completed results. config.yaml is a standard upstream-compatible entry, not a claim that the shared runner produced the historical responses. response objects remain unchanged; analysis paths are adjusted to this repository. README contains reproduction commands. No new paid calls, prompt changes or sampling occurred.
