import data from "../../.generated/content.json";
import { sections } from "./ui";

export type Locale = "en" | "zh";
export type Heading = { id: string; title: string; depth: number };
export type Document = {
  id: string;
  locale: string;
  kind: string;
  category: string;
  url: string;
  sourcePath: string;
  title: string;
  description: string;
  group: string;
  order: number;
  raw: string;
  markdown: string;
  html: string;
  headings: Heading[];
  titleId: string;
  publishedAt: string;
  updatedAt: string;
  contentHash: string;
  sourceUrl: string;
  translationUrl: string | null;
  samples?: number;
  cost?: number;
};
export const documents: Document[] = data;
export { labels, sections, descriptions, urlFor } from "./ui";
export function getDocument(id: string, locale: Locale) {
  return documents.find((doc) => doc.id === id && doc.locale === locale);
}
export function entries(kind: string, locale: Locale) {
  return documents
    .filter(
      (doc) => doc.locale === locale && doc.kind === kind && doc.id !== kind,
    )
    .sort(
      (a, b) =>
        Date.parse(b.updatedAt) - Date.parse(a.updatedAt) ||
        a.order - b.order ||
        a.id.localeCompare(b.id),
    );
}
export function pageIds(locale: Locale) {
  return [...new Set([
    "",
    ...sections,
    ...documents.filter((doc) => doc.locale === locale).map((doc) => doc.id),
    ...entries("resources", locale).map((doc) => `resources/${doc.category}`),
  ])];
}
export function formatDate(date: string, locale: Locale) {
  return new Intl.DateTimeFormat(locale === "zh" ? "zh-CN" : "en", {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  }).format(new Date(date));
}
