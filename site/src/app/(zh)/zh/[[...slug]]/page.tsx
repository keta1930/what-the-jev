import { pageMetadata } from "@/lib/metadata";
import { SitePage, pageParams } from "@/components/page";
export const generateStaticParams = () => pageParams("zh");
export default async function Page({
  params,
}: {
  params: Promise<{ slug?: string[] }>;
}) {
  return <SitePage locale="zh" {...await params} />;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug?: string[] }>;
}) {
  return pageMetadata((await params).slug, "zh");
}
