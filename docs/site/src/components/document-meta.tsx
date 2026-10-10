import { formatCost } from "@/lib/cost.mjs";
import type { Document, Locale } from "@/lib/content";

export function DocumentMeta({
  doc,
  locale,
}: {
  doc: Document;
  locale: Locale;
}) {
  if (doc.samples === undefined && doc.cost === undefined) return null;
  return (
    <span className="document-meta">
      {doc.samples !== undefined && (
        <span>
          {doc.samples.toLocaleString(locale === "zh" ? "zh-CN" : "en-US")}
          {locale === "zh" ? " 个样本" : doc.samples === 1 ? " sample" : " samples"}
        </span>
      )}
      {doc.cost !== undefined && (
        <span>{locale === "zh" ? "费用" : "Cost"} {formatCost(doc.cost)}</span>
      )}
    </span>
  );
}
