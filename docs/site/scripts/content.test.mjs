import { groupEntries } from "../src/lib/group-order.mjs";
import test from "node:test";
import assert from "node:assert/strict";
import {
  mkdtempSync,
  mkdirSync,
  writeFileSync,
  rmSync,
  readFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { discover, identify, readDocument, resolveRepoLink } from "./lib/content.mjs";
import { withBasePath } from "../src/lib/paths.mjs";
import { formatCost } from "../src/lib/cost.mjs";
import { renderMarkdown } from "./lib/render.mjs";
import {
  indexRevisionDates,
  fingerprint,
  revisionDate,
} from "./lib/revision.mjs";

test("publishes only reader-facing sources, pairing both naming conventions", () => {
  assert.equal(identify("experiments/test/preparation/raw/paper.md"), null);
  assert.equal(identify("game/TODO.md"), null);
  assert.equal(identify("AGENTS.md"), null);
  assert.equal(identify("docs/jev/en/AGENTS.md"), null);
  assert.equal(identify("docs/jev/zh/TODO.md"), null);
  assert.equal(
    identify("example/paper-qa/README.zh.md").url,
    "/zh/examples/paper-qa",
  );
  for (const file of [
    "docs/jev/en/what-is-jev.md",
    "docs/jev/zh/using-jev.md",
    "docs/jev/README.md",
    "docs/jev/en/nested/guide.md",
  ]) assert.equal(identify(file), null);
});

test("frontmatter supplies sample counts and precise dollar costs without inventing absent fields", () => {
  const root = path.resolve(import.meta.dirname, "../../..");
  const english = readDocument(root, "example/ticket-triage/README.md");
  const chinese = readDocument(root, "example/ticket-triage/README.zh.md");
  const experiment = readDocument(root, "experiments/bbq/report/REPORT.md");
  assert.equal(english.samples, 1);
  assert.equal(english.cost, 0.000025872);
  assert.equal(chinese.cost, 0.000028728);
  assert.equal(experiment.samples, 58492);
  assert.equal(experiment.cost, 0.921154332);
  assert.equal(formatCost(english.cost), "$0.000025872");
  assert.equal(formatCost(0.000000000001), "$0.000000000001");
  assert.equal(formatCost(experiment.cost), "$0.921154332");
  const resource = readDocument(root, "resource/benchmarks/jevals.md");
  assert.ok(!Object.hasOwn(resource, "samples"));
  assert.ok(!Object.hasOwn(resource, "cost"));
});

test("Markdown preserves currency, braces, angle placeholders, code and GFM tables", async () => {
  const markdown =
    '# Title\n\n∫₀^{π/2} <option content> costs $0.0167, versus $0.0237.\n\n| A | B |\n| - | - |\n| 1 | 2 |\n\n```json\n{"x": "$\\\\log_3 81$"}\n```\n\n## 读取答案\n\n## 读取答案';
  const result = await renderMarkdown(markdown, (url) => url);
  assert.ok(/(?:&lt;|&#x3C;)option content(?:&gt;|>)/.test(result.html));
  assert.ok(result.html.includes("$0.0167, versus $0.0237"));
  assert.ok(result.html.includes("∫₀^{π/2}"));
  assert.ok(result.html.includes("<table>"));
  assert.ok(result.html.includes("language-json"));
  assert.ok(!result.html.includes("<h1"));
  assert.deepEqual(
    result.headings.map((h) => h.id),
    ["title", "读取答案", "读取答案-1"],
  );
});

test("link resolver preserves locale, suffixes and assets; rejects broken links and traversal", () => {
  const root = mkdtempSync(path.join(tmpdir(), "jev-links-"));
  try {
    mkdirSync(`${root}/docs`, { recursive: true });
    for (const file of ["a.md", "b.zh.md", "image.png"])
      writeFileSync(`${root}/docs/${file}`, "fixture");
    const doc = { sourcePath: "docs/a.md", locale: "en" };
    const map = new Map([["docs/b.zh.md", { url: "/zh/docs/b" }]]);
    assert.equal(
      resolveRepoLink(root, doc, "b.zh.md?q=1#读取答案", map, "abc").url,
      withBasePath("/zh/docs/b/?q=1#读取答案"),
    );
    assert.equal(
      resolveRepoLink(root, doc, "image.png", map, "abc").asset,
      "docs/image.png",
    );
    assert.equal(
      resolveRepoLink(root, doc, "image.png?q=1#preview", map, "abc").url,
      withBasePath("/repo-assets/docs/image.png?q=1#preview"),
    );
    assert.throws(
      () => resolveRepoLink(root, doc, "../../secret", map, "abc"),
      /outside repository/,
    );
    assert.throws(
      () => resolveRepoLink(root, doc, "missing.md", map, "abc"),
      /missing link/,
    );
    assert.throws(
      () => resolveRepoLink(root, doc, "javascript:alert(1)", map, "abc"),
      /unsafe link/,
    );
  } finally {
    rmSync(root, { recursive: true });
  }
});

test("revision identity detects same-day text and image changes, stays stable across builds", () => {
  const first = fingerprint(
    "body",
    [["fig.png", Buffer.from("image")]],
    "summary",
  );
  assert.equal(
    first,
    fingerprint("body", [["fig.png", Buffer.from("image")]], "summary"),
  );
  assert.notEqual(
    first,
    fingerprint("body changed", [["fig.png", Buffer.from("image")]], "summary"),
  );
  assert.notEqual(
    first,
    fingerprint("body", [["fig.png", Buffer.from("new image")]], "summary"),
  );
  assert.notEqual(
    first,
    fingerprint("body", [["fig.png", Buffer.from("image")]], "new summary"),
  );
  assert.equal(fingerprint("a\r\nb"), fingerprint("a\nb"));
  assert.equal(
    revisionDate({
      contentHash: first,
      previous: { contentHash: first, updatedAt: "2026-10-01" },
      modified: "2026-10-09",
    }),
    "2026-10-09T00:00:00.000Z",
  );
  assert.equal(
    revisionDate({
      modified: ["2026-10-09T09:00:00+08:00", "2026-10-09T02:00:00.000Z"],
    }),
    "2026-10-09T02:00:00.000Z",
  );
  assert.equal(
    revisionDate({
      modified: ["2026-10-01T00:00:00Z", "2026-10-09T00:00:00Z"],
    }),
    "2026-10-09T00:00:00.000Z",
  );
});

test("generated manifest covers every source and paired routes without duplicates", () => {
  const docs = JSON.parse(
    readFileSync(new URL("../.generated/content.json", import.meta.url)),
  );
  const root = path.resolve(import.meta.dirname, "../../..");
  assert.equal(docs.length, discover(root).length);
  assert.equal(new Set(docs.map((doc) => doc.url)).size, docs.length);
  for (const doc of docs) {
    assert.ok(
      docs.some(
        (other) =>
          other.url === doc.translationUrl &&
          other.id === doc.id &&
          other.locale !== doc.locale,
      ),
    );
    assert.ok(Number.isFinite(Date.parse(doc.updatedAt)));
  }
  assert.ok(docs.some((doc) => doc.kind === "resources" && doc.category));
  assert.ok(docs.every((doc) => !doc.sourcePath.startsWith("docs/jev/")));
  assert.ok(docs.every((doc) => !/^\/(zh\/)?docs(?:\/|$)/.test(doc.url)));
});

test("excluded Jev knowledge links retain their GitHub source and fragment", () => {
  const root = path.resolve(import.meta.dirname, "../../..");
  const doc = { sourcePath: "README.md", locale: "en" };
  for (const file of ["docs/jev/README.md", "docs/jev/en/using-jev.md", "docs/jev/zh/using-jev.md"]) {
    assert.equal(
      resolveRepoLink(root, doc, `${file}#reference`, new Map(), "abc").url,
      `https://github.com/keta1930/what-the-jev/blob/abc/${file}#reference`,
    );
  }
});

test("site development documentation remains a GitHub source link", () => {
  const root = path.resolve(import.meta.dirname, "../../..");
  assert.equal(
    resolveRepoLink(root, { sourcePath: "README.md" }, "docs/site/README.md", new Map(), "abc").url,
    "https://github.com/keta1930/what-the-jev/blob/abc/docs/site/README.md",
  );
});

test("a single updated article stays inside its original group", () => {
  const entries = [
    { id: "tools/one", group: "Tools", updatedAt: "2026-10-01", order: 0 },
    {
      id: "benchmarks/one",
      group: "Benchmarks",
      updatedAt: "2026-10-09",
      order: 2,
    },
    { id: "tools/two", group: "Tools", updatedAt: "2026-10-02", order: 1 },
    {
      id: "benchmarks/two",
      group: "Benchmarks",
      updatedAt: "2026-10-01",
      order: 3,
    },
  ];
  assert.deepEqual(
    groupEntries(entries, ["Tools", "Benchmarks"]).map((entry) => entry.id),
    ["tools/two", "tools/one", "benchmarks/one", "benchmarks/two"],
  );
});

test("one changed index summary updates only that entry, independent of cache", () => {
  const original = [
    { sourcePath: "a.md", description: "A", group: "Tools" },
    { sourcePath: "b.md", description: "B", group: "Tools" },
  ];
  const changed = [{ ...original[0], description: "New A" }, original[1]];
  const history = [{ date: "2026-10-01T08:00:00+08:00", entries: original }];
  const dates = indexRevisionDates(changed, "2026-10-09T02:00:00Z", history);
  assert.equal(dates.get("a.md"), "2026-10-09T02:00:00.000Z");
  assert.equal(dates.get("b.md"), "2026-10-01T00:00:00.000Z");
  assert.deepEqual(
    dates,
    indexRevisionDates(changed, "2026-10-09T02:00:00Z", history),
  );
  const committed = [
    { date: "2026-10-09T02:00:00Z", entries: changed },
    ...history,
  ];
  assert.deepEqual(
    dates,
    indexRevisionDates(changed, "2026-10-10T00:00:00Z", committed),
  );
});
