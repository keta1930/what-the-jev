import { documents, type Locale } from "./content";
export const siteUrl = (
  process.env.SITE_URL || "http://localhost:20242"
).replace(/\/$/, "");
const escape = (value: string) =>
  value.replace(
    /[<>&"']/g,
    (character) =>
      ({
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
      })[character]!,
  );
export function rss(locale: Locale) {
  const docs = documents
    .filter((doc) => doc.locale === locale)
    .toSorted(
      (a, b) =>
        Date.parse(b.updatedAt) - Date.parse(a.updatedAt) ||
        a.id.localeCompare(b.id),
    );
  const prefix = locale === "zh" ? "/zh" : "";
  const items = docs
    .map(
      (doc) =>
        `<item><title>${escape(doc.title)}</title><link>${escape(siteUrl + doc.url)}</link><guid isPermaLink="false">${escape(`urn:what-the-jev:${locale}:${doc.id}:${doc.contentHash}`)}</guid><pubDate>${new Date(doc.updatedAt).toUTCString()}</pubDate><description>${escape(doc.description)}</description></item>`,
    )
    .join("\n");
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>what-the-jev · ${locale}</title><link>${escape(siteUrl + prefix + "/")}</link><description>${locale === "zh" ? "示例、实验与资源的新增和修改。" : "New and updated examples, experiments, and resources."}</description><language>${locale === "zh" ? "zh-CN" : "en"}</language><atom:link href="${escape(siteUrl + prefix + "/rss.xml")}" rel="self" type="application/rss+xml"/><lastBuildDate>${new Date(docs[0].updatedAt).toUTCString()}</lastBuildDate>${items}</channel></rss>`;
  return new Response(xml, {
    headers: {
      "Content-Type": "application/rss+xml; charset=utf-8",
      "Cache-Control": "public, max-age=0, must-revalidate",
    },
  });
}
