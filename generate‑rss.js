const fs = require("fs");

const siteTitle = "我的个人站点";
const siteDescription = "个人笔记与随笔";
const DOMAIN = process.env.SITE_DOMAIN;

if (!DOMAIN) {
  throw new Error("环境变量 SITE_DOMAIN 未配置，请在仓库 Settings → Variables 添加");
}

const raw = fs.readFileSync("./posts.json", "utf‑8");
const posts = JSON.parse(raw);

// 按发布日期倒序，最新文章放在RSS最前面
posts.sort((a, b) => {
  return new Date(b.date).getTime() - new Date(a.date).getTime();
});

let itemBlocks = "";
for (const post of posts) {
  const pubDate = new Date(post.date).toUTCString();
  const fullUrl = DOMAIN + post.url;
  itemBlocks += `
<item>
  <title>${escapeXml(post.title)}</title>
  <link>${escapeXml(fullUrl)}</link>
  <pubDate>${pubDate}</pubDate>
  <description>${escapeXml(post.desc)}</description>
</item>
`;
}

const rssContent = `<?xml version="1.0" encoding="UTF‑8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>${escapeXml(siteTitle)}</title>
  <link>${escapeXml(DOMAIN)}</link>
  <description>${escapeXml(siteDescription)}</description>
  <atom:link href="${escapeXml(DOMAIN + "/rss.xml")}" rel="self" type="application/rss+xml" />
${itemBlocks}
</channel>
</rss>
`;

fs.writeFileSync("./rss.xml", rssContent, "utf‑8");

function escapeXml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}
