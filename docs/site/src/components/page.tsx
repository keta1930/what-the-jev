import Link from "next/link";
import { groupEntries } from "@/lib/group-order.mjs";
import { CopyButton } from "./copy-button";
import { DocumentMeta } from "./document-meta";
import { TableOfContents } from "./toc";
import { notFound } from "next/navigation";
import { DocsBody } from "fumadocs-ui/layouts/docs/page";
import {
  documents,
  entries,
  getDocument,
  labels,
  descriptions,
  sections,
  urlFor,
  formatDate,
  type Locale,
} from "@/lib/content";
export function SitePage({
  slug = [],
  locale,
}: {
  slug?: string[];
  locale: Locale;
}) {
  const id = slug.join("/");
  const t = labels[locale];
  if (!id)
    return (
      <main id="main" className="home">
        <div className="hero">
          <p className="eyebrow">{t.intro}</p>
          <h1>
            {locale === "en" ? (
              <>What can <em>jev</em><br />actually do?</>
            ) : (
              <>Jev 到底<br /><em>能做什么？</em></>
            )}
          </h1>
          <p className="hero-description">{t.description}</p>
          <p className="hero-formula">
            <em>p</em>(answer <span className="pipe">|</span> state, questions)
          </p>
          <nav className="hero-nav" aria-label={t.browse}>
            {sections.map((section) => (
              <Link
                key={section}
                href={urlFor(section, locale)}
                className={section === "examples" ? "primary" : undefined}
              >
                {t[section]}
                <span aria-hidden>↗</span>
              </Link>
            ))}
          </nav>
        </div>
      </main>
    );
  const section = sections.find((section) => section === id);
  const category =
    slug[0] === "resources" && slug.length === 2 ? slug[1] : null;
  if (section || category) {
    const kind = section || "resources";
    const indexDoc = getDocument(kind, locale);
    const groupOrder =
      indexDoc?.headings
        .filter((heading) => heading.depth === 2)
        .map((heading) => heading.title) || [];
    const all = groupEntries(entries(kind, locale), groupOrder);
    const categories = [
      ...new Map(all.map((doc) => [doc.category, doc.group])).entries(),
    ];
    const selected = category
      ? all.filter((doc) => doc.category === category)
      : all;
    if (category && !selected.length) notFound();
    return (
      <main id="main" className="listing">
        <p className="eyebrow">WHAT-THE-JEV / {kind.toUpperCase()}</p>
        <h1 id={indexDoc?.titleId}>
          {category
            ? categories.find(([key]) => key === category)?.[1]
            : t[kind]}
        </h1>
        <p className="lead">{descriptions[locale][kind]}</p>
        {kind === "resources" && (
          <nav
            className="filters"
            id={
              indexDoc?.headings.find(
                (heading) =>
                  heading.depth === 2 &&
                  !all.some((doc) => doc.group === heading.title),
              )?.id
            }
          >
            <Link
              aria-current={!category ? "page" : undefined}
              href={urlFor("resources", locale)}
            >
              {t.all} <small>{all.length}</small>
            </Link>
            {categories.map(([key, title]) => (
              <Link
                key={key}
                aria-current={key === category ? "page" : undefined}
                href={urlFor(`resources/${key}`, locale)}
              >
                {title}
              </Link>
            ))}
          </nav>
        )}
        <div className="entry-list">
          {selected.map((doc, index) => (
            <div key={doc.id}>
              {selected.findIndex((item) => item.group === doc.group) ===
                index &&
                doc.group && (
                  <h2
                    className="group-heading"
                    id={
                      indexDoc?.headings.find(
                        (heading) => heading.title === doc.group,
                      )?.id
                    }
                  >
                    {doc.group}
                  </h2>
                )}
              <Link className="entry" key={doc.id} href={doc.url}>
                <span className="entry-number">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <div>
                  <h2>{doc.title}</h2>
                  <p className="entry-summary">{doc.description}</p>
                  <DocumentMeta doc={doc} locale={locale} />
                </div>
                <time dateTime={doc.updatedAt}>
                  {formatDate(doc.updatedAt, locale)}
                </time>
                <span className="entry-arrow">↗</span>
              </Link>
            </div>
          ))}
        </div>
      </main>
    );
  }
  const doc = getDocument(id, locale);
  if (!doc) notFound();
  const parent = doc.kind === "about" ? "" : doc.kind;
  return (
    <main
      id="main"
      className="article-page"
      data-translation={doc.translationUrl || ""}
      data-translation-anchors={JSON.stringify(
        getDocument(doc.id, locale === "zh" ? "en" : "zh")?.headings.map(
          (heading) => heading.id,
        ) || [],
      )}
    >
      <Link className="breadcrumb" href={urlFor(parent, locale)}>
        ← {parent ? t[parent as keyof typeof t] : "what-the-jev"}
      </Link>
      <header className="article-header">
        <p className="eyebrow">{doc.group || doc.kind}</p>
        <h1 id={doc.titleId}>{doc.title}</h1>
        <div className="article-meta">
          <span>
            {t.updated}{" "}
            <time dateTime={doc.updatedAt}>
              {formatDate(doc.updatedAt, locale)}
            </time>
          </span>
          <DocumentMeta doc={doc} locale={locale} />
          <a href={doc.sourceUrl}>{t.source} ↗</a>
          <CopyButton markdown={doc.raw} locale={locale} />
        </div>
      </header>
      <div className="reading-grid">
        <DocsBody className="article-body">
          <div dangerouslySetInnerHTML={{ __html: doc.html }} />
        </DocsBody>
        <TableOfContents headings={doc.headings} title={t.contents} />
      </div>
    </main>
  );
}
export function pageParams(locale: Locale) {
  const paths = new Set([
    "",
    ...sections,
    ...documents.filter((doc) => doc.locale === locale).map((doc) => doc.id),
    ...entries("resources", locale).map((doc) => `resources/${doc.category}`),
  ]);
  return [...paths].map((path) => ({ slug: path ? path.split("/") : [] }));
}
