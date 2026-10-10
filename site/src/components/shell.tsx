import type { ReactNode } from "react";
import Link from "next/link";
import { Provider } from "./provider";
import { Header } from "./header";
import { Brand } from "./brand";
import { labels, urlFor, type Locale } from "@/lib/ui";
import "../app/global.css";
export function Shell({
  children,
  locale,
}: {
  children: ReactNode;
  locale: Locale;
}) {
  return (
    <html lang={locale === "zh" ? "zh-CN" : "en"} suppressHydrationWarning>
      <head>
        <link rel="icon" type="image/svg+xml" href="/icon.svg" />
        <link
          rel="preload"
          href="/fonts/cormorant-garamond-latin-wght-normal.woff2"
          as="font"
          type="font/woff2"
          crossOrigin="anonymous"
        />
        <link
          rel="preload"
          href="/fonts/inter-latin-wght-normal.woff2"
          as="font"
          type="font/woff2"
          crossOrigin="anonymous"
        />
        <link
          rel="alternate"
          type="application/rss+xml"
          title={`what-the-jev · ${locale}`}
          href={urlFor("rss.xml", locale)}
        />
      </head>
      <body>
        <Provider locale={locale}>
          <div className="site-shell">
            <a className="skip" href="#main">
              {locale === "zh" ? "跳到正文" : "Skip to content"}
            </a>
            <Header locale={locale} />
            {children}
            <footer className="site-footer">
              <div className="footer-identity">
                <span className="brand"><Brand /></span>
                <span>
                  {locale === "zh"
                    ? "开放探索，知其边界。"
                    : "Explore openly. Know the limits."}
                </span>
              </div>
              <div>
                <Link href={urlFor("about", locale)}>
                  {labels[locale].about}
                </Link>
                <a href={urlFor("rss.xml", locale)}>RSS</a>
                <a href="https://github.com/keta1930/what-the-jev">GitHub ↗</a>
                <span className="shortcut-hint">D · L · H</span>
              </div>
            </footer>
          </div>
        </Provider>
      </body>
    </html>
  );
}
