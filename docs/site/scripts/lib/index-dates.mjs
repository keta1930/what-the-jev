import { execFileSync } from "node:child_process";
import matter from "gray-matter";
import { parser, extractIndex } from "./content.mjs";
import { fileDates, indexRevisionDates } from "./revision.mjs";

export function indexDates(root, doc, entries) {
  const log = execFileSync(
    "git",
    ["log", "--format=%H %cI", "--", doc.sourcePath],
    { cwd: root, encoding: "utf8" },
  ).trim();
  const history = log
    ? log.split("\n").map((line) => {
        const [commit, date] = line.split(" ");
        const raw = execFileSync(
          "git",
          ["show", `${commit}:${doc.sourcePath}`],
          { cwd: root, encoding: "utf8" },
        );
        return {
          date,
          entries: extractIndex({
            sourcePath: doc.sourcePath,
            tree: parser.parse(matter(raw).content),
          }),
        };
      })
    : [];
  return indexRevisionDates(
    entries,
    fileDates(root, doc.sourcePath).modified,
    history,
  );
}
