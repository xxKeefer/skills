#!/usr/bin/env node
/** Parses every Mermaid diagram in a report's runs block, and names each one that fails. Usage: check_mermaid.mjs <report path> */
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const cache = path.join(process.env.XDG_CACHE_HOME || path.join(os.homedir(), ".cache"), "visualise-pr");
const modules = path.join(cache, "node_modules");
if (!fs.existsSync(path.join(modules, "mermaid")) || !fs.existsSync(path.join(modules, "jsdom"))) {
  fs.mkdirSync(cache, { recursive: true });
  execFileSync("npm", ["install", "--silent", "--prefix", cache, "mermaid@11", "jsdom"], { stdio: "inherit" });
}

const { JSDOM } = await import(pathToFileURL(path.join(modules, "jsdom", "lib", "api.js")).href);
const dom = new JSDOM("<!doctype html><body></body>");
globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.DOMParser = dom.window.DOMParser;
const { default: mermaid } = await import(pathToFileURL(path.join(modules, "mermaid", "dist", "mermaid.core.mjs")).href);
mermaid.initialize({ startOnLoad: false, securityLevel: "loose" });

const html = fs.readFileSync(process.argv[2], "utf8");
const block = html.match(/<script type="application\/json" id="runs">([\s\S]*?)<\/script>/);
const data = JSON.parse(block[1].replaceAll("<\\/", "</"));

const diagrams = [];
for (const run of data.runs) {
  for (const v of run.visuals || []) if (v.mermaid) diagrams.push([`run visual "${v.question}"`, v.mermaid]);
  for (const row of run.rows || []) {
    for (const v of row.visuals || []) if (v.mermaid) diagrams.push([`row ${row.id} visual "${v.question}"`, v.mermaid]);
  }
}

let failed = 0;
for (const [label, text] of diagrams) {
  try {
    await mermaid.parse(text);
  } catch (error) {
    failed += 1;
    const message = String(error.message || error).split("\n").slice(0, 3).join(" | ");
    console.log(`${label}: ${message}`);
  }
}
if (failed) {
  console.log(`${failed} of ${diagrams.length} diagrams fail. Fix: correct each one, write the report again, and run this check again.`);
  process.exit(1);
}
console.log(`ok: ${diagrams.length} diagrams parse`);
