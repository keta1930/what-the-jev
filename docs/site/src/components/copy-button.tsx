"use client";
import { useState } from "react";
import { labels, type Locale } from "@/lib/ui";
export function CopyButton({
  markdown,
  locale,
}: {
  markdown: string;
  locale: Locale;
}) {
  const [status, setStatus] = useState("");
  return (
    <>
      <button
        className="copy-button"
        data-copy-markdown
        onClick={async () => {
          try {
            await navigator.clipboard.writeText(markdown);
            setStatus(labels[locale].copied);
          } catch {
            setStatus(labels[locale].copyFailed);
          }
        }}
      >
        {labels[locale].copy} <kbd>M</kbd>
      </button>
      <span role="status">{status}</span>
    </>
  );
}
