# MoCa — Methods

## Material and rights boundary

The pinned release has 144 causal and 62 moral stories. Original stories/questions, individual votes and textual requests are not distributed. preparation/code/prepare_data.py --source-dir accepts user-supplied local sources, checks hashes, 25 votes/item and answer_dist, then generates Git-ignored data/dataset.json. It does not download data. Public artifacts retain aggregate statistics and model Yes/No results.

## Adaptation and criteria

Each item uses one structured Yes/No judgment, without the paper's few-shot/persona or multi-model conditions. Jev P(Yes)>0.6 maps to Yes, <0.4 to No, otherwise Ambiguous. Human probabilities come from 25 votes and use the same boundaries. Both 0.4 and 0.6 are Ambiguous. Structured choice probabilities are not human response shares.

Three-class agreement, unambiguous-item AUROC, probability differences and story-bootstrap intervals are calculated offline. Factors overlap; group-mean contrasts are not the paper's AMCE or isolated causal effects. Analysis does not generate story-containing cases files. Public summaries can be read without the sources; full recomputation requires locally supplied data.

## Integration and reproduction

Historical runs used independent scripts and budget controls. Integration only imports completed results. config.yaml is a standard upstream-compatible entry, not a claim that the shared runner produced the historical responses. response objects remain unchanged; analysis paths are adjusted to this repository. README contains reproduction commands. No new paid calls, prompt changes or sampling occurred.
