// Renders the caption overlay to transparent PNG frames with headless Chromium.
// Usage:
//   node render-overlay.mjs <outDir> [fps]            -> full trimmed range, frame N = TRIM.start + N/fps
//   node render-overlay.mjs <outDir> --at 5.9,22.7    -> single test frames (named by time)
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)("playwright"); // global install works via require
import { mkdirSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(process.argv[2] || "frames");
mkdirSync(outDir, { recursive: true });
const atIdx = process.argv.indexOf("--at");
const fps = atIdx < 0 ? Number(process.argv[3] || 30) : 30;
const WORKERS = 4;

const browser = await chromium.launch();
const url = pathToFileURL(path.join(here, "overlay.html")).href;

async function newPage() {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);
  return page;
}

if (atIdx >= 0) {
  const page = await newPage();
  for (const t of process.argv[atIdx + 1].split(",").map(Number)) {
    await page.evaluate((t) => renderAt(t), t);
    await page.screenshot({ path: path.join(outDir, `t${t.toFixed(2)}.png`), omitBackground: true });
  }
} else {
  const trim = await (await newPage()).evaluate(() => window.TRIM);
  const total = Math.round((trim.end - trim.start) * fps);
  let next = 0;
  const started = Date.now();
  await Promise.all(
    Array.from({ length: WORKERS }, async () => {
      const page = await newPage();
      while (next < total) {
        const n = next++;
        await page.evaluate((t) => renderAt(t), trim.start + n / fps);
        await page.screenshot({ path: path.join(outDir, `f${String(n).padStart(5, "0")}.png`), omitBackground: true });
        if (n % 150 === 0) console.log(`frame ${n}/${total}  ${((Date.now() - started) / 1000).toFixed(0)}s`);
      }
    })
  );
  console.log(`done: ${total} frames`);
}
await browser.close();
