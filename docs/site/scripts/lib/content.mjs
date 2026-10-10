import { readdirSync, readFileSync, statSync, existsSync } from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import { toString } from "mdast-util-to-string";
import { visit } from "unist-util-visit";
import { withBasePath, pagePath } from "../../src/lib/paths.mjs";

export const parser = unified().use(remarkParse).use(remarkGfm);
export const hashText = (text) => text.replace(/\r\n/g, "\n");
export const localUrl = (id, locale) => `${locale === "zh" ? "/zh" : ""}/${id}`;

export function identify(file) {
  if (/^(AGENTS|CLAUDE|TODO)(?:\.zh)?\.md$/i.test(path.posix.basename(file)))
    return null;
  const locale = /\.zh\.md$/.test(file) ? "zh" : "en";
  const plain = file.replace(/\.zh\.md$/, ".md");
  let id;
  if (/^README\.md$/.test(plain)) id = "about";
  else if (plain === "example/INDEX.md") id = "examples";
  else if (plain === "experiments/INDEX.md") id = "experiments";
  else if (plain === "resource/README.md") id = "resources";
  else if (/^example\/[^/]+\/README\.md$/.test(plain))
    id = `examples/${plain.split("/")[1]}`;
  else if (/^experiments\/[^/]+\/report\/REPORT\.md$/.test(plain))
    id = `experiments/${plain.split("/")[1]}`;
  else if (/^resource\/[^/]+\/[^/]+\.md$/.test(plain))
    id = plain.replace(/^resource\//, "resources/").replace(/\.md$/, "");
  if (!id) return null;
  return {
    id,
    locale,
    kind: id.split("/")[0],
    category: id.startsWith("resources/") ? id.split("/")[1] : "",
    url: localUrl(id, locale),
  };
}

export function discover(root) {
  const found = ["README.md", "README.zh.md"];
  function walk(dir) {
    for (const entry of readdirSync(path.join(root, dir), {
      withFileTypes: true,
    })) {
      const file = `${dir}/${entry.name}`;
      if (
        entry.isDirectory() &&
        !["preparation", "data", "result", "scripts", "code", "fig"].includes(
          entry.name,
        )
      )
        walk(file);
      else if (entry.isFile() && identify(file)) found.push(file);
    }
  }
  for (const dir of ["example", "experiments", "resource"])
    walk(dir);
  return found.sort();
}

export function readDocument(root, sourcePath) {
  const raw = readFileSync(path.join(root, sourcePath), "utf8");
  const { data, content } = matter(raw);
  const tree = parser.parse(content);
  const heading = tree.children.find(
    (node) => node.type === "heading" && node.depth === 1,
  );
  const paragraph = tree.children.find(
    (node) =>
      node.type === "paragraph" &&
      !/English\s*\||简体中文\s*\|/.test(toString(node)) &&
      toString(node).length > 20,
  );
  const identity = identify(sourcePath);
  return {
    ...identity,
    sourcePath,
    title: String(data.title || (heading && toString(heading)) || identity.id),
    description: String(
      data.summary || (paragraph && toString(paragraph)) || "",
    ).slice(0, 320),
    declaredDate: data.date,
    declaredUpdated: data.updated,
    ...(data.samples !== undefined ? { samples: data.samples } : {}),
    ...(data.cost !== undefined ? { cost: data.cost } : {}),
    raw,
    markdown: content,
    tree,
    dependencies: [],
    order: 0,
    group: "",
  };
}

export function extractIndex(doc) {
  let group = "";
  const entries = [];
  for (const node of doc.tree.children) {
    if (node.type === "heading" && node.depth === 2) group = toString(node);
    if (!["list", "table"].includes(node.type)) continue;
    const rows = node.type === "list" ? node.children : node.children.slice(1);
    for (const row of rows) {
      let link;
      visit(row, "link", (node) => {
        if (!link && /\.md(?:#.*)?$/.test(node.url)) link = node;
      });
      if (!link) continue;
      const description =
        node.type === "table"
          ? toString(row.children.at(-1))
          : toString(row)
              .replace(toString(link), "")
              .replace(/^\s*[—–-]\s*/, "");
      entries.push({
        sourcePath: path.posix.normalize(
          path.posix.join(path.posix.dirname(doc.sourcePath), link.url),
        ),
        group,
        description,
      });
    }
  }
  return entries;
}

export function resolveRepoLink(root, doc, href, bySource, commit) {
  if (/^(https?:|mailto:)/i.test(href) || href.startsWith("//"))
    return { url: href };
  if (/^[a-z][a-z\d+.-]*:/i.test(href))
    throw new Error(`${doc.sourcePath}: unsafe link ${href}`);
  if (href.startsWith("#") || href.startsWith("?")) return { url: href };
  const [, pathname, suffix = ""] = href.match(/^([^?#]*)(.*)$/);
  const target = path.posix.normalize(
    path.posix.join(
      path.posix.dirname(doc.sourcePath),
      decodeURIComponent(pathname),
    ),
  );
  if (target.startsWith("../") || path.isAbsolute(target))
    throw new Error(`${doc.sourcePath}: link outside repository ${href}`);
  if (!existsSync(path.join(root, target)))
    throw new Error(`${doc.sourcePath}: missing link ${href} (${target})`);
  if (bySource.has(target))
    return { url: withBasePath(pagePath(bySource.get(target).url + suffix)) };
  if (/\.(png|jpe?g|gif|webp|svg|avif)$/i.test(target))
    return { url: withBasePath(`/repo-assets/${target}${suffix}`), asset: target };
  const type = statSync(path.join(root, target)).isDirectory()
    ? "tree"
    : "blob";
  return {
    url: `https://github.com/keta1930/what-the-jev/${type}/${commit}/${target}${suffix}`,
  };
}
