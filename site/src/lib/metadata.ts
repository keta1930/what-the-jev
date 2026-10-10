import type { Metadata } from "next";
import { getDocument, entries, labels, urlFor, type Locale } from "./content";
import { siteUrl } from "./rss";
export function pageMetadata(slug: string[] = [], locale: Locale): Metadata {
  const id = slug.join("/");
  const doc = getDocument(id, locale);
  const name = labels[locale][id as keyof typeof labels.en];
  const title =
    doc?.title ||
    (slug[0] === "resources" && slug.length === 2
      ? entries("resources", locale).find((entry) => entry.category === slug[1])
          ?.group
      : undefined) ||
    name ||
    (id ? id.split("/").at(-1) : labels[locale].intro);
  return {
    title: `${title} · what-the-jev?!`,
    description: doc?.description || labels[locale].description,
    metadataBase: new URL(siteUrl),
    alternates: {
      canonical: urlFor(id, locale),
      languages: { en: urlFor(id, "en"), "zh-CN": urlFor(id, "zh") },
    },
    openGraph: {
      title,
      description: doc?.description || labels[locale].description,
      locale: locale === "zh" ? "zh_CN" : "en_US",
      type: "website",
    },
  };
}
