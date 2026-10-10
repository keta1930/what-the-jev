import type { ReactNode } from "react";
import Link from "next/link";
import localFont from "next/font/local";
import { Provider } from "./provider";
import { Header } from "./header";
import { Brand } from "./brand";
import { labels, urlFor, type Locale } from "@/lib/ui";
import { withBasePath } from "@/lib/paths.mjs";
import "../app/global.css";

const serif = localFont({
  src: [
    { path: "../../public/fonts/cormorant-garamond-latin-wght-normal.woff2", weight: "300 700", style: "normal" },
    { path: "../../public/fonts/cormorant-garamond-latin-wght-italic.woff2", weight: "300 700", style: "italic" },
  ],
  variable: "--cormorant-font",
  display: "swap",
  adjustFontFallback: false,
});
const sans = localFont({
  src: [
    { path: "../../public/fonts/inter-latin-wght-normal.woff2", weight: "100 900", style: "normal" },
    { path: "../../public/fonts/inter-latin-wght-italic.woff2", weight: "100 900", style: "italic" },
  ],
  variable: "--inter-font",
  display: "swap",
  adjustFontFallback: false,
});
const mono = localFont({
  src: "../../public/fonts/jetbrains-mono-latin-wght-normal.woff2",
  weight: "100 800",
  variable: "--jetbrains-font",
  display: "swap",
  adjustFontFallback: false,
});
export function Shell({
  children,
  locale,
}: {
  children: ReactNode;
  locale: Locale;
}) {
  return (
    <html
      lang={locale === "zh" ? "zh-CN" : "en"}
      className={`${serif.variable} ${sans.variable} ${mono.variable}`}
      suppressHydrationWarning
    >
      <head>
        <link rel="icon" type="image/svg+xml" href={withBasePath("/icon.svg")} />
        <link
          rel="alternate"
          type="application/rss+xml"
          title={`what-the-jev · ${locale}`}
          href={withBasePath(urlFor("rss.xml", locale))}
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
                <a href={withBasePath(urlFor("rss.xml", locale))}>RSS</a>
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
