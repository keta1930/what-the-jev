# what-the-jev?!

![cover](docs/cover.png)

*English | [简体中文](README.zh.md)*

## Introduction

**what-the-jev** showcases what Jev (TypeSafe AI's "System One" decision model) can do across a wide range of tasks. It is a growing collection of reproducible benchmarks and experiments: every task ships with its dataset, run configuration, raw model responses, and analysis reports. Whether you are new to Jev or want to explore it in depth, this project is a good place to start.

## Repository Structure

```text
what-the-jev/
├── example/                   lightweight examples
│   ├── us-election/           [History] Tests whether Jev can recall the winners of the eight US presidential elections from 1996 to 2024.
│   ├── math-word-problem/     [Arithmetic] Tests Jev on grade-school arithmetic word problems.
│   ├── university-math/       [Arithmetic] Tests Jev on calculus, linear algebra, and probability problems.
│   ├── pixel-recognition/     [Vision] Tests whether Jev can identify image content from raw pixel values alone.
│   ├── ethics-dilemmas/       [Ethics] Tests Jev's acceptability judgments in classic ethical dilemmas.
│   ├── injection-guard/       [Security] Tests whether Jev can detect prompt-injection attacks hidden in tool-call results.
│   ├── paper-qa/              [Paper Reading] Tests whether Jev can answer questions about a research paper from only part of its text.
│   └── ticket-triage/         [Business] Tests Jev's classification of customer-support tickets, refund claims, and urgency.
├── experiments/               professional-grade experiments
│   ├── gpqa-diamond/          [Benchmark] Explore JEV's performance on GPQA Diamond graduate-level science questions.
│   ├── gsm8k/                 [Benchmark] Explore JEV's performance on GSM8K grade-school math word problems.
│   ├── mmlu-pro/              [Benchmark] Explore JEV's performance on MMLU-Pro college-level questions across 14 disciplines.
│   ├── bbq/                   [Benchmark] Explore JEV's performance on BBQ's bias-sensitive questions, and whether it leans toward stereotypes.
│   ├── socialiqa/             [Benchmark] Explore JEV's performance on SocialIQA social commonsense questions, and whether confidence marks trustworthy answers.
│   ├── paper-classification/  [Paper Classification] Explore JEV's performance on paper library management: deciding, based on a research preference, whether an arXiv paper belongs in a paper library, and which topic it falls under.
│   ├── paper-qa/              [Paper QA] Explore JEV's performance on paper QA: answering questions from a paper's own text.
│   ├── prompt-routing/        [Prompt Routing] Explore JEV's performance on prompt routing.
│   ├── skill-routing/         [Skill Routing] Explore JEV's performance on skill routing.
│   ├── boston-housing/        [Numeric Regression] Explore JEV's performance on Boston suburb housing price prediction and relative comparison.
│   ├── titanic/               [Classification Prediction] Explore JEV's performance on Titanic passenger survival prediction, and how structured fields and prose text compare as input.
│   ├── dpo-jev-judge/         [LLM Training] Explore JEV's performance on preference annotation for DPO training data.
│   └── grpo-jev-judge/        [LLM Training] Explore JEV's performance on GRPO trajectory reward assignment.
├── resource/                  catalog of Jev-related projects and models
│   ├── closed-source-models/  [Closed-Source Models] Jev and its proprietary competitors
│   ├── open-source-models/    [Open-Source Models] open-weight decision models and replicas
│   ├── use-cases/             [Use Cases] applications built with Jev
│   ├── integrations/          [Integrations] gateways, frameworks, and platforms serving Jev
│   ├── tools/                 [Tools] SDKs, MCP servers, CLIs, and libraries
│   └── benchmarks/            [Benchmarks] independent and official evaluations
├── docs/jev/                  [AGENT] Jev knowledge base
├── src/decision_models/       the framework that runs an experiment
├── schema/                    dataset and result schemas
├── tests/                     tests for the framework
├── run.py                     CLI entry point
├── AGENTS.md                  [AGENT] project execution instructions
└── .claude/rules/             [AGENT] project execution standard
```

See [example/INDEX.md](example/INDEX.md) for the full index of lightweight examples.

See [experiments/INDEX.md](experiments/INDEX.md) for the full index of experiments.

See [resource/README.md](resource/README.md) for the full index of the resource catalog.

## Contributing

Our goal is a decision-model community built entirely in the open-source spirit, exploring what decision models can be used for and where their capabilities end.

Any contribution is welcome: code, corrections, experiments or examples, resource entries, and more.

We look forward to your pull request.

## Citation

If you use this repository, please cite it:

```bibtex
@software{what_the_jev,
  author = {{what-the-jev contributors}},
  title = {what-the-jev: Decision-model use cases and capability boundaries},
  url = {https://github.com/keta1930/what-the-jev},
  license = {MIT}
}
```

## Contact

📧 Email: yandeheng1@gmail.com

## License

[MIT](LICENSE)
