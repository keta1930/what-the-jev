"use client";
import { useEffect, useRef } from "react";
import type { Heading } from "@/lib/content";
export function TableOfContents({
  headings,
  title,
}: {
  headings: Heading[];
  title: string;
}) {
  const details = useRef<HTMLDetailsElement>(null);
  useEffect(() => {
    if (details.current)
      details.current.open = window.matchMedia("(min-width: 901px)").matches;
  }, []);
  return (
    <aside className="toc">
      <details ref={details}>
        <summary>{title}</summary>
        <nav>
          {headings
            .filter((heading) => heading.depth > 1 && heading.depth < 4)
            .map((heading) => (
              <a
                key={heading.id}
                href={`#${heading.id}`}
                className={heading.depth === 3 ? "sub" : ""}
              >
                {heading.title}
              </a>
            ))}
        </nav>
      </details>
    </aside>
  );
}
