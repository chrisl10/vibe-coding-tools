import test from "node:test";
import assert from "node:assert/strict";
import { composite, contrastRatio, assessContrast } from "../lib/contrast.mjs";

test("WCAG sRGB black/white ratio and alpha composition", () => {
  assert.equal(contrastRatio([0, 0, 0], [255, 255, 255]), 21);
  assert.equal(contrastRatio([255, 255, 255], [255, 255, 255]), 1);
  assert.deepEqual(composite([0, 0, 0, 0.5], [255, 255, 255, 1]), [127.5, 127.5, 127.5, 1]);
  assert.deepEqual(composite([0, 0, 0, 0], [0, 0, 0, 0]), [0, 0, 0, 0]);
});

test("normal text threshold uses the unrounded ratio", () => {
  const base = { kind: "text", background: [255, 255, 255, 1], fontSize: 16, fontWeight: 400 };
  assert.equal(assessContrast({ ...base, foreground: [119, 119, 119, 1] }).status, "fail");
  assert.equal(assessContrast({ ...base, foreground: [118, 118, 118, 1] }).status, "pass");
});

test("large text and UI use three, uncertain paint is unmeasured", () => {
  const base = { kind: "text", foreground: [119, 119, 119, 1], background: [255, 255, 255, 1], fontSize: 24, fontWeight: 400 };
  assert.equal(assessContrast(base).threshold, 3);
  assert.equal(assessContrast({ ...base, fontSize: 19, fontWeight: 700 }).threshold, 3);
  assert.equal(assessContrast({ ...base, kind: "ui" }).threshold, 3);
  assert.equal(assessContrast({ ...base, unknown: ["background image"] }).status, "unmeasured");
  assert.equal(assessContrast({ ...base, background: [0, 0, 0, 0] }).status, "unmeasured");
});
