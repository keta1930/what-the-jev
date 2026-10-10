import test from "node:test";
import assert from "node:assert/strict";

for (const basePath of ["", "/what-the-jev"]) {
  test(`URL contract for ${basePath || "local development"}`, async () => {
    const saved = { ...process.env };
    const rootUrl = basePath
      ? "https://keta1930.github.io/what-the-jev"
      : "http://localhost:20242";
    process.env.NEXT_PUBLIC_BASE_PATH = basePath;
    process.env.SITE_URL = rootUrl + "/";
    try {
      const { withBasePath, pagePath, siteUrl, absoluteUrl } = await import(
        `../src/lib/paths.mjs?base=${basePath}`
      );
      assert.equal(withBasePath("/search/zh.json"), basePath + "/search/zh.json");
      assert.equal(withBasePath("/icon.svg"), basePath + "/icon.svg");
      assert.equal(withBasePath("/zh/rss.xml"), basePath + "/zh/rss.xml");
      assert.equal(withBasePath(withBasePath("/examples/")), basePath + "/examples/");
      for (const href of ["#heading", "?q=1", "https://example.com/image.png", "//cdn.example.com/icon.svg"])
        assert.equal(withBasePath(href), href);
      assert.equal(pagePath("/zh/examples/ticket-triage?q=1#答案"), "/zh/examples/ticket-triage/?q=1#答案");
      assert.equal(pagePath("/examples/"), "/examples/");
      assert.equal(pagePath("/"), "/");
      assert.equal(siteUrl, rootUrl);
      assert.equal(absoluteUrl(pagePath("/zh/examples")), rootUrl + "/zh/examples/");
      assert.equal(absoluteUrl("/rss.xml"), rootUrl + "/rss.xml");
    } finally {
      process.env = saved;
    }
  });
}
