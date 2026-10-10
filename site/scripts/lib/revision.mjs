import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync, statSync } from "node:fs";
import { hashText } from "./content.mjs";

export function fingerprint(raw, assets = [], description = "") {
  const hash = createHash("sha256")
    .update(hashText(raw))
    .update("\0" + description);
  for (const [name, bytes] of assets.toSorted(([a], [b]) => a.localeCompare(b)))
    hash.update("\0" + name + "\0").update(bytes);
  return hash.digest("hex");
}

export function fileDates(root, file) {
  const log = execFileSync("git", ["log", "--format=%cI", "--", file], {
    cwd: root,
    encoding: "utf8",
  })
    .trim()
    .split("\n")
    .filter(Boolean)
    .map((date) => new Date(date).toISOString());
  const bytes = readFileSync(`${root}/${file}`);
  let clean = false;
  try {
    clean = bytes.equals(
      execFileSync("git", ["show", `HEAD:${file}`], {
        cwd: root,
        stdio: ["ignore", "pipe", "ignore"],
        maxBuffer: 20 * 1024 * 1024,
      }),
    );
  } catch {
    /* 未跟踪文件使用文件自身时间。 */
  }
  const modified =
    clean && log.length
      ? log[0]
      : statSync(`${root}/${file}`).mtime.toISOString();
  return { published: log.at(-1) || modified, modified };
}

export function revisionDate({ modified }) {
  const dates = Array.isArray(modified) ? modified : [modified];
  return new Date(
    Math.max(...dates.map((date) => new Date(date).getTime())),
  ).toISOString();
}

export function indexRevisionDates(entries, modified, history) {
  const dates = new Map();
  for (const entry of entries) {
    let date = modified;
    for (const snapshot of history) {
      const older = snapshot.entries.find(
        (item) => item.sourcePath === entry.sourcePath,
      );
      if (
        !older ||
        older.description !== entry.description ||
        older.group !== entry.group
      )
        break;
      date = snapshot.date;
    }
    dates.set(entry.sourcePath, new Date(date).toISOString());
  }
  return dates;
}
