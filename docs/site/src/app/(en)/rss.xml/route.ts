import { rss } from "@/lib/rss";
export const dynamic = "force-static";
export const GET = () => rss("en");
