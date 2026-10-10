import type { MetadataRoute } from "next";
import { entries, getDocument, pageIds, sections, urlFor } from "@/lib/content";
import { pageLanguages } from "@/lib/metadata";
import { absoluteUrl, pagePath } from "@/lib/paths.mjs";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  return (["en", "zh"] as const).flatMap((locale) =>
    pageIds(locale).map((id) => {
      const doc = getDocument(id, locale);
      const dates = doc ? [doc.updatedAt] : [];
      if (sections.some((section) => section === id))
        dates.push(...entries(id, locale).map((entry) => entry.updatedAt));
      const lastModified = dates.length
        ? new Date(Math.max(...dates.map((date) => Date.parse(date)))).toISOString()
        : undefined;
      return {
        url: absoluteUrl(pagePath(urlFor(id, locale))),
        ...(lastModified ? { lastModified } : {}),
        alternates: { languages: pageLanguages(id) },
      };
    }),
  );
}
