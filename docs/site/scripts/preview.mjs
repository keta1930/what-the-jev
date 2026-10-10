import { createServer } from "node:http";
import { createReadStream, existsSync, statSync } from "node:fs";
import path from "node:path";
import { basePath } from "../src/lib/paths.mjs";

const root = path.resolve(import.meta.dirname, "../out");
if (!existsSync(`${root}/index.html`))
  throw new Error("Static export missing: run npm run build first");
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".xml": "application/rss+xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".woff2": "font/woff2",
};
createServer((request, response) => {
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
  } catch {
    response.writeHead(400).end();
    return;
  }
  if (basePath && !pathname.startsWith(`${basePath}/`) && pathname !== basePath) {
    response.writeHead(404).end();
    return;
  }
  let file = path.resolve(root, `.${pathname.slice(basePath.length) || "/"}`);
  if (file !== root && !file.startsWith(root + path.sep)) {
    response.writeHead(404).end();
    return;
  }
  if (existsSync(file) && statSync(file).isDirectory()) {
    if (!pathname.endsWith("/")) {
      const query = new URL(request.url, "http://localhost").search;
      response.writeHead(308, { Location: pathname + "/" + query }).end();
      return;
    }
    file = path.join(file, "index.html");
  }
  const found = existsSync(file) && statSync(file).isFile();
  if (!found) file = `${root}/404.html`;
  response.writeHead(found ? 200 : 404, {
    "Content-Type": types[path.extname(file)] || "application/octet-stream",
  });
  if (request.method === "HEAD") response.end();
  else createReadStream(file).pipe(response);
}).listen(Number(process.env.PORT || 20242), "0.0.0.0", () => {
  console.log(`Static export: http://localhost:${process.env.PORT || 20242}${basePath}/`);
});
