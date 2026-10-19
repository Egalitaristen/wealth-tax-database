// defuddle_extract.mjs: turn saved HTML into clean markdown plus title, author and publication date.
// Usage: node skill/scripts/defuddle_extract.mjs PAGE.html [URL]   (prints one JSON object)
// Setup (once):  cd skill/scripts && npm install defuddle jsdom
import { JSDOM } from 'jsdom';
import { Defuddle } from 'defuddle/node';
import fs from 'fs';
const [, , file, url = 'https://example.com/'] = process.argv;
const dom = new JSDOM(fs.readFileSync(file, 'utf8'), { url });
const r = await Defuddle(dom.window.document, url, { markdown: true });
console.log(JSON.stringify({ title: r.title, author: r.author, published: r.published, site: r.site, words: r.wordCount, content: r.content }));
