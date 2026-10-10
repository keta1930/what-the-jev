import type { Metadata } from "next";
import { getDocument, entries, labels, urlFor, type Locale } from "./content";
import { siteUrl, absoluteUrl, pagePath } from "./paths.mjs";
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
      canonical: absoluteUrl(pagePath(urlFor(id, locale))),
      languages: {
        en: absoluteUrl(pagePath(urlFor(id, "en"))),
        "zh-CN": absoluteUrl(pagePath(urlFor(id, "zh"))),
      },
    },
    openGraph: {
      title,
      description: doc?.description || labels[locale].description,
      locale: locale === "zh" ? "zh_CN" : "en_US",
      type: "website",
      url: absoluteUrl(pagePath(urlFor(id, locale))),
    },
  };
}
