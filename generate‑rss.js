const fs=require("fs");


let posts=
JSON.parse(
fs.readFileSync(
"posts.json",
"utf8"
)
);



let items="";


posts.forEach(post=>{


items+=`

<item>

<title>
${post.title}
</title>


<link>
${post.url}
</link>


<description>
${post.description}
</description>


<pubDate>
${post.date}
</pubDate>


</item>

`;

});



let rss=`

<?xml version="1.0" encoding="UTF-8"?>

<rss version="2.0">

<channel>


<title>
Wesley Blog
</title>


<link>
https://wesleykq3.github.io
</link>


<description>
个人知识库
</description>


${items}


</channel>

</rss>

`;



fs.writeFileSync(
"feed.xml",
rss
);
