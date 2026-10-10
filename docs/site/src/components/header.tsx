"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useTheme } from "next-themes";
import { useEffect, useRef, useState } from "react";
import { useSearchContext } from "fumadocs-ui/contexts/search";
import { labels, sections, urlFor, type Locale } from "@/lib/ui";
import { Brand } from "./brand";
export function Header({ locale }: { locale: Locale }) {
  const pathname = usePathname();
  const router = useRouter();
  const { resolvedTheme, setTheme } = useTheme();
  const { open, setOpenSearch } = useSearchContext();
  const help = useRef<HTMLDialogElement>(null);
  const [shortcuts, setShortcuts] = useState(false);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    setShortcuts(localStorage.getItem("jev-shortcuts") !== "off");
    setReady(true);
  }, []);
  const toggleTheme = () =>
    setTheme(resolvedTheme === "dark" ? "light" : "dark");
  const toggleLanguage = () => {
    const article = document.querySelector<HTMLElement>("[data-translation]");
    if (article && !article.dataset.translation) return;
    const next =
      article?.dataset.translation ||
      (locale === "zh"
        ? pathname.slice(3) || "/"
        : `/zh${pathname === "/" ? "" : pathname}`);
    // 只在对应译文仍有相同标题时保留片段。
    const anchors = JSON.parse(
      article?.dataset.translationAnchors || "[]",
    ) as string[];
    const hash = window.location.hash;
    const fragment =
      hash && anchors.includes(decodeURIComponent(hash.slice(1))) ? hash : "";
    router.push(next + window.location.search + fragment);
  };
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (
        !shortcuts ||
        open ||
        help.current?.open ||
        event.metaKey ||
        event.ctrlKey ||
        event.altKey ||
        event.repeat ||
        event.isComposing
      )
        return;
      if (
        event.target instanceof HTMLElement &&
        (event.target.isContentEditable ||
          event.target.closest("input,textarea,select,[role=dialog]"))
      )
        return;
      const key = event.key.toLowerCase();
      if (key === "d") {
        event.preventDefault();
        toggleTheme();
      }
      if (key === "l") {
        event.preventDefault();
        toggleLanguage();
      }
      if (key === "h") {
        event.preventDefault();
        router.push(urlFor("", locale));
      }
      if (key === "m") {
        event.preventDefault();
        document
          .querySelector<HTMLButtonElement>("[data-copy-markdown]")
          ?.click();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });
  return (
    <>
      <header className="site-header" data-ready={ready}>
        <Link className="brand" href={urlFor("", locale)}>
          <Brand />
        </Link>
        <nav aria-label={locale === "zh" ? "主导航" : "Main navigation"}>
          <Link
            href={urlFor("", locale)}
            aria-current={pathname === urlFor("", locale) ? "page" : undefined}
          >
            {labels[locale].overview}
          </Link>
          {sections.map((section) => (
            <Link
              key={section}
              href={urlFor(section, locale)}
              aria-current={
                pathname.startsWith(urlFor(section, locale))
                  ? "page"
                  : undefined
              }
            >
              {labels[locale][section]}
            </Link>
          ))}
        </nav>
        <div className="controls">
          <button
            className="search-trigger"
            onClick={() => setOpenSearch(true)}
            aria-label={locale === "zh" ? "搜索文档" : "Search documents"}
            title="⌘ / Ctrl K"
          >
            ⌕ <kbd>⌘K</kbd>
          </button>
          <button
            onClick={toggleTheme}
            aria-label={locale === "zh" ? "切换明暗模式" : "Toggle theme"}
            title="D"
          >
            <span className="sun">☼</span>
            <span className="moon">☾</span>
          </button>
          <button
            onClick={toggleLanguage}
            title="L"
            aria-label={locale === "zh" ? "Switch to English" : "切换到中文"}
          >
            {locale === "zh" ? "EN" : "中"}
          </button>
          <button
            onClick={() => help.current?.showModal()}
            aria-label={locale === "zh" ? "快捷键帮助" : "Keyboard shortcuts"}
          >
            ?
          </button>
        </div>
        <a className="github-button" href="https://github.com/keta1930/what-the-jev">
          GitHub ↗
        </a>
      </header>
      <dialog
        ref={help}
        className="help-dialog"
        onClick={(event) => {
          if (event.target === event.currentTarget) help.current?.close();
        }}
      >
        <div>
          <button
            className="dialog-close"
            onClick={() => help.current?.close()}
            aria-label={locale === "zh" ? "关闭" : "Close"}
          >
            ×
          </button>
          <h2>{locale === "zh" ? "快捷键" : "Keyboard shortcuts"}</h2>
          <dl>
            {[
              ["⌘ / Ctrl K", locale === "zh" ? "搜索文档" : "Search documents"],
              ["D", locale === "zh" ? "切换明暗模式" : "Toggle theme"],
              ["L", locale === "zh" ? "切换语言" : "Switch language"],
              ["H", locale === "zh" ? "返回首页" : "Go home"],
              [
                "M",
                locale === "zh" ? "复制文章 Markdown" : "Copy article Markdown",
              ],
              ["Esc", locale === "zh" ? "关闭弹窗" : "Close dialog"],
            ].map(([key, text]) => (
              <div key={key}>
                <dt>
                  <kbd>{key}</kbd>
                </dt>
                <dd>{text}</dd>
              </div>
            ))}
          </dl>
          <label>
            <input
              type="checkbox"
              checked={shortcuts}
              onChange={(event) => {
                setShortcuts(event.target.checked);
                localStorage.setItem(
                  "jev-shortcuts",
                  event.target.checked ? "on" : "off",
                );
              }}
            />
            {locale === "zh"
              ? "启用单字母快捷键"
              : "Enable single-letter shortcuts"}
          </label>
        </div>
      </dialog>
    </>
  );
}
