"use client";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import {
  SearchDialog,
  SearchDialogContent,
  SearchDialogHeader,
  SearchDialogInput,
  SearchDialogList,
  SearchDialogOverlay,
  SearchDialogClose,
  type SharedProps,
} from "fumadocs-ui/components/dialog/search";
type Entry = { title: string; description: string; text: string; url: string };
export default function Search(props: SharedProps) {
  const pathname = usePathname();
  const locale =
    pathname === "/zh" || pathname.startsWith("/zh/") ? "zh" : "en";
  const [query, setQuery] = useState("");
  const [index, setIndex] = useState<Entry[]>([]);
  const [error, setError] = useState(false);
  useEffect(() => {
    if (!props.open) return;
    const controller = new AbortController();
    setError(false);
    fetch(`/search/${locale}.json`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error("Search index unavailable");
        return response.json();
      })
      .then(setIndex)
      .catch((error) => {
        if (error.name !== "AbortError") setError(true);
      });
    return () => controller.abort();
  }, [locale, props.open]);
  const terms = query.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  const results = terms.length
    ? index
        .filter((item) =>
          terms.every((term) =>
            `${item.title} ${item.description} ${item.text}`
              .toLocaleLowerCase()
              .includes(term),
          ),
        )
        .sort(
          (a, b) =>
            Number(b.title.toLocaleLowerCase().includes(terms.join(" "))) -
            Number(a.title.toLocaleLowerCase().includes(terms.join(" "))),
        )
        .slice(0, 24)
    : [];
  return (
    <SearchDialog {...props} search={query} onSearchChange={setQuery}>
      <SearchDialogOverlay />
      <SearchDialogContent>
        <SearchDialogHeader>
          <SearchDialogInput
            aria-label={locale === "zh" ? "搜索文档" : "Search documents"}
            placeholder={
              locale === "zh"
                ? "搜索示例、实验与资源…"
                : "Search examples, experiments, resources…"
            }
          />
          <SearchDialogClose />
        </SearchDialogHeader>
        <SearchDialogList
          items={results.map((item) => ({
            id: item.url,
            type: "page" as const,
            content: item.title,
            url: item.url,
          }))}
          Empty={() => (
            <p className="search-message">
              {error
                ? locale === "zh"
                  ? "搜索加载失败，请重新打开。"
                  : "Search failed to load. Please reopen."
                : terms.length
                  ? locale === "zh"
                    ? "未找到结果"
                    : "No results found"
                  : locale === "zh"
                    ? "输入关键词，搜索当前语言的全部文档。"
                    : "Type to search all documents in this language."}
            </p>
          )}
        />
      </SearchDialogContent>
    </SearchDialog>
  );
}
