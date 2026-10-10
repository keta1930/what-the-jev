"use client";
import { RootProvider } from "fumadocs-ui/provider/next";
import type { ReactNode } from "react";
import type { Locale } from "@/lib/ui";
import Search from "./search";
export function Provider({
  children,
  locale,
}: {
  children: ReactNode;
  locale: Locale;
}) {
  return (
    <RootProvider
      search={{ SearchDialog: Search, preload: false }}
      theme={{ defaultTheme: "system", enableSystem: true }}
      i18n={{
        locale,
        translations:
          locale === "zh"
            ? {
                "Search(search dialog)": "搜索",
                "Close Search(search dialog)(aria-label)": "关闭搜索",
                "No results found(search dialog)": "未找到结果",
              }
            : {},
      }}
    >
      {children}
    </RootProvider>
  );
}
