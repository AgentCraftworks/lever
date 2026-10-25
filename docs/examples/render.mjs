// Renders each <article class="ex"> in examples.html to <id>.png next to this file.
// Needs playwright and @fontsource/{mona-sans,monaspace-neon}; point NODE_PATH at a node_modules that has them.
//   NODE_PATH=/path/to/node_modules node docs/examples/render.mjs
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const require = createRequire(join(process.env.NODE_PATH ?? here, 'noop.js'));
const { chromium } = require('playwright');

const font = (pkg, file) => readFileSync(join(dirname(require.resolve(`${pkg}/package.json`)), 'files', file)).toString('base64');
const faces = [
  ['Mona Sans', '@fontsource/mona-sans', 400], ['Mona Sans', '@fontsource/mona-sans', 500], ['Mona Sans', '@fontsource/mona-sans', 700],
  ['Monaspace Neon', '@fontsource/monaspace-neon', 400],
].map(([family, pkg, w]) => {
  const slug = pkg.split('/')[1];
  return `@font-face{font-family:'${family}';font-weight:${w};src:url(data:font/woff2;base64,${font(pkg, `${slug}-latin-${w}-normal.woff2`)}) format('woff2')}`;
}).join('\n');

const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 1320, height: 900 } });
await page.goto(pathToFileURL(join(here, 'examples.html')).href);
await page.addStyleTag({ content: faces });
await page.evaluate(() => document.fonts.ready);
const ids = await page.$$eval('article.ex', (els) => els.map((e) => e.id));
for (const id of ids) {
  await page.locator(`#${id}`).screenshot({ path: join(here, `${id}.png`) });
  console.log(`${id}.png`);
}
await browser.close();
