const fs = require("fs");
const path = require("path");
const { Client } = require("@notionhq/client");
const csv = require("csv-parser");
require("dotenv").config();

// 🔐 Load Notion Token + DB ID
const NOTION_TOKEN = process.env.NOTION_TOKEN;
//const DATABASE_ID = process.env.NOTION_DATABASE_ID;
const DATABASE_ID = "25d2cf81cbcb80f2af21000c0cd9ef2e";
console.log("📄 DB ID loaded:", DATABASE_ID);


if (!NOTION_TOKEN) {
    console.error("❌ NOTION_TOKEN not loaded. Check .env file format and location.");
    process.exit(1);
}

console.log("🔐 Token loaded:", NOTION_TOKEN.slice(0, 10) + "...");

const notion = new Client({ auth: NOTION_TOKEN });

async function addRowToNotion(row) {
    try {
        const response = await notion.pages.create({
            parent: { database_id: DATABASE_ID },
            properties: {
                title: {
                    title: [{ text: { content: row.title || "Untitled" } }],
                },
                score: {
                    number: parseFloat(row.score),
                },
                date: {
                    date: { start: row.date || new Date().toISOString() },
                },
                url: {
                    url: row.url,
                },
                pros: {
                    rich_text: [{ text: { content: row.pros || "" } }],
                },
                cons: {
                    rich_text: [{ text: { content: row.cons || "" } }],
                },
                notes: {
                    rich_text: [{ text: { content: row.notes || "" } }],
                },
            },
        });

        console.log(`✅ Added: ${row.title}`);
    } catch (error) {
        console.error(`❌ Error adding ${row.title || "undefined"}:`, error.body || error);
    }
}

async function main() {
    const target = process.argv[2] || "lofi"; // default
    const csvPath = path.join(__dirname, `${target}_articles.csv`);

    console.log(`📥 Syncing from: ${csvPath}`);


    if (!fs.existsSync(csvPath)) {
        console.error("❌ CSV file not found:", csvPath);
        process.exit(1);
    }

    console.log("📥 Reading from:", csvPath);

    fs.createReadStream(csvPath)
        .pipe(csv())
        .on("data", (row) => addRowToNotion(row))
        .on("end", () => {
            console.log("✅ All rows processed.");
        });
}

main();
