const config = {
  output: "export",
  basePath: process.env.NEXT_PUBLIC_BASE_PATH || "",
  trailingSlash: true,
  reactStrictMode: true,
  devIndicators: false,
  turbopack: { root: import.meta.dirname },
};
export default config;
