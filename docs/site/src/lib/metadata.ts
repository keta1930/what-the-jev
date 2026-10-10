import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getDocument, entries, labels, pageIds, sections, urlFor, type Locale } from "./content";
import { siteUrl, absoluteUrl, pagePath } from "./paths.mjs";

const siteName = "what-the-jev?!";
const home = {
  en: {
    title: "Reproducible Jev decision model experiments",
    description: "Explore Jev decision models through reproducible examples, benchmarks, experiment reports, and community resources. Open-source code, data, and raw responses.",
  },
  zh: {
    title: "可复现的 Jev 决策模型实验",
    description: "通过可复现的示例、基准测试、实验报告与社区资源探索 Jev 决策模型。公开代码、数据与原始响应，记录模型表现及能力边界。",
  },
};
const cover = {
  url: absoluteUrl("/repo-assets/docs/cover.png"),
  width: 1672,
  height: 385,
  alt: siteName,
};

export function pageLanguages(id: string) {
  const languages: Record<string, string> = {};
  for (const locale of ["en", "zh"] as const) {
    if (pageIds(locale).includes(id))
      languages[locale === "zh" ? "zh-CN" : "en"] = absoluteUrl(pagePath(urlFor(id, locale)));
  }
  if (languages.en) languages["x-default"] = languages.en;
  return languages;
}

function pageInfo(slug: string[], locale: Locale) {
  const id = slug.join("/");
  if (!pageIds(locale).includes(id)) notFound();
  const doc = getDocument(id, locale);
  const category = slug[0] === "resources" && slug.length === 2;
  const selected = category
    ? entries("resources", locale).filter((entry) => entry.category === slug[1])
    : [];
  const title = !id
    ? home[locale].title
    : id === "about"
      ? labels[locale].about
      : selected[0]?.group || doc!.title;
  const description = !id
    ? home[locale].description
    : category
      ? locale === "zh"
        ? `${title}：${selected.length} 项 Jev 相关资源，包含项目简介与源链接。`
        : `${title}: ${selected.length} Jev-related resources with project summaries and source links.`
      : doc!.description;
  const article = Boolean(doc && id !== "about" && !sections.some((section) => section === id));
  return {
    id, doc, title: `${title} · ${siteName}`, description, article,
    canonical: absoluteUrl(pagePath(urlFor(id, locale))),
  };
}

export function pageMetadata(slug: string[] = [], locale: Locale): Metadata {
  const page = pageInfo(slug, locale);
  return {
    title: page.title,
    description: page.description,
    metadataBase: new URL(siteUrl),
    ...(!page.id ? {
      verification: { google: "Tc7-HGdw7xp0c7T4932yG1N4bq3_m0XiGoccTL1itjo" },
    } : {}),
    alternates: {
      canonical: page.canonical,
      languages: pageLanguages(page.id),
    },
    robots: { index: true, follow: true, "max-image-preview": "large" },
    openGraph: {
      title: page.title,
      description: page.description,
      siteName,
      locale: locale === "zh" ? "zh_CN" : "en_US",
      alternateLocale: locale === "zh" ? "en_US" : "zh_CN",
      type: page.article ? "article" : "website",
      ...(page.article ? { modifiedTime: page.doc!.updatedAt } : {}),
      url: page.canonical,
      images: [cover],
    },
    twitter: {
      card: "summary_large_image",
      title: page.title,
      description: page.description,
      images: [cover],
    },
  };
}

export function pageStructuredData(slug: string[] = [], locale: Locale) {
  const page = pageInfo(slug, locale);
  const website = {
    "@type": "WebSite",
    "@id": absoluteUrl("/#website"),
    url: absoluteUrl("/"),
    name: siteName,
    inLanguage: ["en", "zh-CN"],
  };
  const type = page.article ? "TechArticle" : page.id === "about" ? "AboutPage" : page.id ? "CollectionPage" : "WebPage";
  return {
    "@context": "https://schema.org",
    "@graph": [website, {
      "@type": type,
      "@id": `${page.canonical}#page`,
      url: page.canonical,
      name: page.title,
      description: page.description,
      inLanguage: locale === "zh" ? "zh-CN" : "en",
      isPartOf: { "@id": website["@id"] },
      ...(page.article ? {
        headline: page.doc!.title,
        mainEntityOfPage: page.canonical,
        dateModified: page.doc!.updatedAt,
        isBasedOn: page.doc!.sourceUrl,
      } : {}),
      ...(!page.id ? {
        mainEntity: {
          "@type": "CreativeWork",
          name: siteName,
          description: labels[locale].description,
          url: "https://github.com/keta1930/what-the-jev",
        },
      } : {}),
    }],
  };
}
