import { spawn } from "node:child_process";
import chokidar from "chokidar";
import { sync, root, site } from "./sync.mjs";
await sync();
const server = spawn(
  process.execPath,
  [
    "node_modules/next/dist/bin/next",
    "dev",
    "--hostname",
    "0.0.0.0",
    "--port",
    process.env.PORT || "20242",
  ],
  { cwd: site, stdio: "inherit" },
);
let timer;
let pending = Promise.resolve();
const watcher = chokidar.watch(
  [
    "README.md",
    "README.zh.md",
    "example",
    "experiments",
    "resource",
    "docs/cover.png",
  ].map((file) => `${root}/${file}`),
  {
    ignoreInitial: true,
    ignored: (file) =>
      /\/(preparation|data|result|\.git|node_modules)(\/|$)/.test(file),
  },
);
watcher.on("all", () => {
  clearTimeout(timer);
  timer = setTimeout(() => {
    pending = pending
      .then(sync)
      .catch((error) => console.error("[content sync]", error));
  }, 250);
});
for (const signal of ["SIGINT", "SIGTERM"])
  process.on(signal, () => {
    watcher.close();
    server.kill(signal);
  });
server.on("exit", (code) => {
  watcher.close();
  process.exit(code || 0);
});
