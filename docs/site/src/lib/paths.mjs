export const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";

export function withBasePath(url) {
  if (!url.startsWith("/") || url.startsWith("//")) return url;
  if (basePath && (url === basePath || url.startsWith(`${basePath}/`)))
    return url;
  return basePath + url;
}

export function pagePath(url) {
  const [, pathname, suffix = ""] = url.match(/^([^?#]*)(.*)$/);
  return (pathname.endsWith("/") ? pathname : `${pathname}/`) + suffix;
}

export const siteUrl = (process.env.SITE_URL || "http://localhost:20242")
  .replace(/\/$/, "");

export const absoluteUrl = (url) => siteUrl + url;
