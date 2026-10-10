import {
  readFileSync,
  writeFileSync,
  mkdirSync,
  rmSync,
  copyFileSync,
  existsSync,
  renameSync,
} from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import {
  discover,
  readDocument,
  extractIndex,
  resolveRepoLink,
  localUrl,
} from "./lib/content.mjs";
import { fingerprint, fileDates, revisionDate } from "./lib/revision.mjs";
import { indexDates } from "./lib/index-dates.mjs";
import { renderMarkdown } from "./lib/render.mjs";
import { basePath } from "../src/lib/paths.mjs";

export const site = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
export const root = path.resolve(site, "../..");
export async function sync() {
  const out = path.join(site, ".generated");
  mkdirSync(out, { recursive: true });
  const commit = execFileSync("git", ["rev-parse", "HEAD"], {
    cwd: root,
    encoding: "utf8",
  }).trim();
  const docs = discover(root).map((file) => readDocument(root, file));
  const bySource = new Map(docs.map((doc) => [doc.sourcePath, doc]));
  const byUrl = new Map(docs.map((doc) => [doc.url, doc]));
  if (byUrl.size !== docs.length) throw new Error("Duplicate document URL");
  for (const doc of docs.filter((doc) =>
    ["examples", "experiments", "resources"].includes(doc.id),
  )) {
    const entries = extractIndex(doc);
    const entryDates = indexDates(root, doc, entries);
    entries.forEach((entry, order) => {
      const target = bySource.get(entry.sourcePath);
      if (!target)
        throw new Error(
          `${doc.sourcePath}: index entry missing ${entry.sourcePath}`,
        );
      target.group = entry.group;
      target.indexDescription = entry.description;
      target.indexSource = doc.sourcePath;
      target.indexUpdatedAt = entryDates.get(entry.sourcePath);
      target.order = order;
      if (target.kind === "resources") target.description = entry.description;
    });
  }
  const assets = new Set();
  const dates = new Map();
  const getDates = (file) => {
    if (!dates.has(file)) dates.set(file, fileDates(root, file));
    return dates.get(file);
  };
  for (const doc of docs) {
    if (
      ["examples", "experiments", "resources"].includes(doc.kind) &&
      doc.id.includes("/") &&
      !doc.group
    )
      throw new Error(`Unindexed document: ${doc.sourcePath}`);
    const translated = byUrl.get(
      localUrl(doc.id, doc.locale === "zh" ? "en" : "zh"),
    );
    doc.translationUrl = translated?.url || null;
    const rendered = await renderMarkdown(doc.markdown, (href) => {
      const resolved = resolveRepoLink(root, doc, href, bySource, commit);
      if (resolved.asset) {
        assets.add(resolved.asset);
        doc.dependencies.push(resolved.asset);
      }
      return resolved.url;
    });
    Object.assign(doc, rendered);
    doc.contentHash = fingerprint(
      doc.raw,
      doc.dependencies.map((file) => [
        file,
        readFileSync(path.join(root, file)),
      ]),
      JSON.stringify([doc.indexDescription || "", doc.group]),
    );
    const date = getDates(doc.sourcePath);
    const declared = doc.declaredDate
      ? new Date(doc.declaredDate).toISOString()
      : date.published;
    doc.publishedAt = declared;
    const modified = [
      date.modified,
      ...doc.dependencies.map((file) => getDates(file).modified),
    ];
    if (doc.indexUpdatedAt) modified.push(doc.indexUpdatedAt);
    if (doc.declaredUpdated)
      modified.push(new Date(doc.declaredUpdated).toISOString());
    doc.updatedAt = revisionDate({ modified });
    doc.sourceUrl = `https://github.com/keta1930/what-the-jev/blob/${commit}/${doc.sourcePath}`;
    delete doc.tree;
    delete doc.declaredDate;
    delete doc.declaredUpdated;
  }
  for (const doc of docs) {
    for (const href of doc.links) {
      if (!href.startsWith("/") && !href.startsWith("#")) continue;
      const localHref = href.startsWith("/") ? href.slice(basePath.length) : href;
      const [targetUrl, fragment] = localHref.split("#");
      if (!fragment || targetUrl.startsWith("/repo-assets/")) continue;
      const target = targetUrl
        ? byUrl.get(targetUrl.split("?")[0].replace(/\/$/, ""))
        : doc;
      if (
        target &&
        !target.headings.some(
          (heading) => heading.id === decodeURIComponent(fragment),
        )
      )
        throw new Error(`${doc.sourcePath}: missing anchor ${href}`);
    }
  }
  const assetDir = `${site}/public/repo-assets`;
  rmSync(assetDir, { recursive: true, force: true });
  for (const asset of assets) {
    mkdirSync(path.dirname(`${assetDir}/${asset}`), { recursive: true });
    copyFileSync(`${root}/${asset}`, `${assetDir}/${asset}`);
  }
  const serialized = JSON.stringify(docs, null, 2) + "\n";
  if (
    !existsSync(`${out}/content.json`) ||
    readFileSync(`${out}/content.json`, "utf8") !== serialized
  ) {
    writeFileSync(`${out}/content.json.tmp`, serialized);
    renameSync(`${out}/content.json.tmp`, `${out}/content.json`);
  }
  const searchDir = `${site}/public/search`;
  mkdirSync(searchDir, { recursive: true });
  for (const locale of ["en", "zh"]) {
    const index = docs
      .filter((doc) => doc.locale === locale)
      .map(({ title, description, markdown, url, kind }) => ({
        title,
        description,
        text: markdown,
        url,
        kind,
      }));
    writeFileSync(`${searchDir}/${locale}.json`, JSON.stringify(index));
  }
  console.log(
    `Synced ${docs.length} documents / ${docs.filter((doc) => doc.locale === "en").length} bilingual pairs and ${assets.size} images.`,
  );
  return docs;
}
if (process.argv[1] === fileURLToPath(import.meta.url)) await sync();
