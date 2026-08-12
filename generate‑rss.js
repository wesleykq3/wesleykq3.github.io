const fs = require("fs");

// ================================
// 读取 posts.json
// ================================

const posts = JSON.parse(
    fs.readFileSync("posts.json", "utf8")
);


// ================================
// XML特殊字符转义
// 防止标题、描述中出现 &, <, > 等导致XML错误
// ================================

function escapeXml(value) {
    if (value === undefined || value === null) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&apos;");
}


// ================================
// 生成 RSS items
// ================================

let items = "";

posts.forEach(post => {

    items += `
    <item>
        <title>${escapeXml(post.title)}</title>

        <link>${escapeXml(post.url)}</link>

        <guid isPermaLink="true">
            ${escapeXml(post.url)}
        </guid>

        <description>
            ${escapeXml(post.description)}
        </description>

        <pubDate>${escapeXml(post.date)}</pubDate>
    </item>
    `;
});


// ================================
// RSS主体
// ================================

const rss = `<?xml version="1.0" encoding="UTF-8"?>

<rss version="2.0">

    <channel>

        <title>Wesley Blog</title>

        <link>https://wesleykq3.github.io/</link>

        <description>个人知识库</description>

        <language>zh-CN</language>

        <generator>GitHub Actions RSS Generator</generator>

        ${items}

    </channel>

</rss>
`;


// ================================
// 写入 feed.xml
// ================================

fs.writeFileSync(
    "feed.xml",
    rss.trim(),
    "utf8"
);

console.log("RSS generated successfully.");
console.log("Output: feed.xml");
