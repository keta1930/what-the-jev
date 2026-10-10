import { pageMetadata } from "@/lib/metadata";
import { SitePage, pageParams } from "@/components/page";
export const generateStaticParams = () => pageParams("en");
export const dynamicParams = false;
export default async function Page({
  params,
}: {
  params: Promise<{ slug?: string[] }>;
}) {
  return <SitePage locale="en" {...await params} />;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug?: string[] }>;
}) {
  return pageMetadata((await params).slug, "en");
}
