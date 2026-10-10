import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkRehype from "remark-rehype";
import rehypeSlug from "rehype-slug";
import rehypeHighlight from "rehype-highlight";
import rehypeStringify from "rehype-stringify";
import { visit } from "unist-util-visit";
import { toString } from "mdast-util-to-string";

export async function renderMarkdown(markdown, resolve) {
  const headings = [];
  const links = [];
  let titleId = "";
  const result = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(() => (tree) => {
      visit(tree, (node) => {
        // 仓库中的尖括号占位符按 Markdown 文本显示，不执行 HTML/JSX。
        if (node.type === "html") node.type = "text";
        if (["link", "image", "definition"].includes(node.type)) {
          node.url = resolve(node.url);
          links.push(node.url);
        }
      });
    })
    .use(remarkRehype)
    .use(rehypeSlug)
    .use(() => (tree) => {
      visit(tree, "element", (node, index, parent) => {
        if (/^h[1-6]$/.test(node.tagName)) {
          const item = {
            id: String(node.properties.id),
            title: toString(node),
            depth: Number(node.tagName[1]),
          };
          headings.push(item);
          if (node.tagName === "h1" && !titleId) {
            titleId = item.id;
            parent.children.splice(index, 1);
            return index;
          }
        }
        if (node.tagName === "img") node.properties.loading = "lazy";
      });
    })
    .use(rehypeHighlight, { detect: false, ignoreMissing: true })
    .use(rehypeStringify)
    .process(markdown);
  return { html: String(result), headings, titleId, links };
}
