import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const script = path.join(path.dirname(fileURLToPath(import.meta.url)), "check_mermaid.mjs");

const report = (runs) => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "check-mermaid-"));
  const file = path.join(dir, "visualise_x.html");
  const json = JSON.stringify({ title: "t", path: file, skill: "", runs }).replaceAll("</", "<\\/");
  fs.writeFileSync(file, `<html><script type="application/json" id="runs">${json}</script></html>`);
  return file;
};

const run = (file) => {
  try {
    return { code: 0, out: execFileSync("node", [script, file], { encoding: "utf8" }) };
  } catch (error) {
    return { code: error.status, out: String(error.stdout) };
  }
};

const good = "flowchart LR\n  nA[a] --> nB[b]";
const reserved = "flowchart LR\n  create --> call\n  call --> done";

test("passes a report whose diagrams all parse", () => {
  const file = report([{ visuals: [{ question: "Top?", mermaid: good }], rows: [{ visuals: [{ question: "Row?", mermaid: good }] }] }]);
  const result = run(file);
  assert.equal(result.code, 0, result.out);
  assert.match(result.out, /ok/);
});

test("names each diagram that fails, in run and row visuals", () => {
  const file = report([
    { visuals: [{ question: "Top?", mermaid: reserved }], rows: [{ id: "r1.1", visuals: [{ question: "Row?", mermaid: reserved }] }] },
  ]);
  const result = run(file);
  assert.equal(result.code, 1);
  assert.match(result.out, /run visual "Top\?"/);
  assert.match(result.out, /row r1\.1 visual "Row\?"/);
});
