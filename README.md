# what-the-jev?!

![cover](docs/cover.png)

*English | [简体中文](README.zh.md)*

## Introduction

**what-the-jev** showcases what Jev (TypeSafe AI's "System One" model) can do across a wide range of tasks. Whether you are new to Jev or want to explore it in depth, this project is a good place to start.

## Repository Structure

```text
what-the-jev/
├── example/                lightweight examples
│   ├── us-election/        [History] Tests whether Jev can recall the winners of the eight US presidential elections from 1996 to 2024.
│   ├── math-word-problem/  [Arithmetic] Tests Jev on grade-school arithmetic word problems.
│   ├── university-math/    [Arithmetic] Tests Jev on calculus, linear algebra, and probability problems.
│   ├── pixel-recognition/  [Vision] Tests whether Jev can identify image content from raw pixel values alone.
│   ├── ethics-dilemmas/    [Ethics] Tests Jev's acceptability judgments in classic ethical dilemmas.
│   ├── injection-guard/    [Security] Tests whether Jev can detect prompt-injection attacks hidden in tool-call results.
│   └── ticket-triage/      [Business] Tests Jev's classification of customer-support tickets, refund claims, and urgency.
├── experiments/            professional-grade experiments
└── docs/jev/               【AGENT】Jev knowledge base
```

See [example/INDEX.md](example/INDEX.md) for the full index of lightweight examples.

## Contributing

New interesting and valuable experiments are welcome.

## Citation

If you use this repository, please cite it:

```bibtex
@software{what_the_jev,
  author = {Yan, Yixin and Cao, Rong},
  title = {what-the-jev: A showcase of Jev decision-model capabilities across tasks},
  url = {https://github.com/keta1930/what-the-jev},
  license = {MIT}
}
```

## Contact

📧 Email: yandeheng1@gmail.com

## License

[MIT](LICENSE)
