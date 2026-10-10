export type Locale = "en" | "zh";
export const urlFor = (id: string, locale: Locale) =>
  `${locale === "zh" ? "/zh" : ""}${id ? `/${id}` : "/"}`.replace(/\/$/, "") ||
  "/";
export const labels = {
  en: {
    examples: "Examples",
    experiments: "Experiments",
    overview: "Overview",
    resources: "Resources",
    about: "About",
    updated: "Updated",
    source: "Source",
    contents: "On this page",
    all: "All",
    read: "Read article",
    intro: "A field guide to a decision model",
    description:
      "Reproducible examples, experiments, and resources exploring what Jev can do — and where its capabilities end.",
    browse: "Explore the field notes",
    back: "Back to",
    copy: "Copy Markdown",
    copied: "Copied",
    copyFailed: "Copy failed. Open the source to copy manually.",
  },
  zh: {
    examples: "示例",
    experiments: "实验",
    overview: "概览",
    resources: "资源",
    about: "关于",
    updated: "更新于",
    source: "源文件",
    contents: "本页目录",
    all: "全部",
    read: "阅读文章",
    intro: "决策模型观察录",
    description:
      "通过可复现的示例、实验与资源，探索 Jev 能做什么，以及它的能力边界。",
    browse: "开始探索",
    back: "返回",
    copy: "复制 Markdown",
    copied: "已复制",
    copyFailed: "复制失败，请打开源文件手动复制。",
  },
};
export const sections = [
  "examples",
  "experiments",
  "resources",
] as const;
export const descriptions = {
  en: {
    examples: "Small experiments. Concrete questions. Reproducible answers.",
    experiments:
      "Benchmarks and investigations, with data, results, and analysis.",
    resources: "Decision models and the ecosystem taking shape around them.",
  },
  zh: {
    examples: "从具体问题出发，用小规模示例观察决策模型。",
    experiments: "可复现的基准测试与探索，包含数据、结果与分析。",
    resources: "决策模型，以及围绕它们生长的工具与应用。",
  },
};
