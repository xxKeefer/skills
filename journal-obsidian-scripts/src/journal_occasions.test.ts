const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const promptDate = require("./prompt_date.ts");
const promptBoolean = require("./prompt_boolean.ts");
const vaultOccasions = require("./vault_occasions.ts");
const journalOccasions = require("./journal_occasions.ts");

function fakeMoment(overrides: Record<string, any>) {
  const { format: fmtMap, ...rest } = overrides;
  return {
    format: (fmt: string) => fmtMap?.[fmt] ?? "",
    isoWeek: () => 1,
    isoWeekYear: () => 2026,
    year: () => 2026,
    month: () => 0,
    date: () => 1,
    day: () => 1,
    ...rest,
  } as any;
}

function fakeTp(overrides: Record<string, any> = {}) {
  return {
    date: { now: (fmt: string) => "2026-05-24" },
    system: {
      prompt: async (msg: string, def?: string) => def ?? null,
      ...overrides.system,
    },
    user: {
      vault_occasions: () => vaultOccasions(),
      ...overrides.user,
    },
  } as any;
}

// --- prompt_date ---

describe("prompt_date", () => {
  it("returns a moment from user input", async () => {
    let capturedArg = "";
    const tp = fakeTp({
      system: {
        prompt: async (_msg: string, _def?: string) => "2026-06-15",
      },
    });
    // prompt_date calls global moment() -- we need to stub it
    const originalMoment = globalThis.moment;
    const fakeParsed = { isMoment: true, value: "2026-06-15" };
    (globalThis as any).moment = (input?: string) => ({ ...fakeParsed, input });
    try {
      const result = await promptDate(tp);
      assert.equal(result.input, "2026-06-15");
    } finally {
      (globalThis as any).moment = originalMoment;
    }
  });

  it("uses custom prompt text", async () => {
    let capturedMsg = "";
    const tp = fakeTp({
      system: {
        prompt: async (msg: string, def?: string) => {
          capturedMsg = msg;
          return "2026-01-01";
        },
      },
    });
    (globalThis as any).moment = (input?: string) => ({ input });
    try {
      await promptDate(tp, "Pick a date");
      assert.ok(capturedMsg.includes("Pick a date"));
    } finally {
      delete (globalThis as any).moment;
    }
  });
});

// --- prompt_boolean ---

describe("prompt_boolean", () => {
  it("returns true for 'yes'", async () => {
    const tp = fakeTp({
      system: { prompt: async () => "yes" },
    });
    assert.equal(await promptBoolean(tp, "Continue?"), true);
  });

  it("returns true for 'Y'", async () => {
    const tp = fakeTp({
      system: { prompt: async () => "Y" },
    });
    assert.equal(await promptBoolean(tp, "Continue?"), true);
  });

  it("returns true for 'true'", async () => {
    const tp = fakeTp({
      system: { prompt: async () => "true" },
    });
    assert.equal(await promptBoolean(tp, "Continue?"), true);
  });

  it("returns true for '1'", async () => {
    const tp = fakeTp({
      system: { prompt: async () => "1" },
    });
    assert.equal(await promptBoolean(tp, "Continue?"), true);
  });

  it("returns false for 'no'", async () => {
    const tp = fakeTp({
      system: { prompt: async () => "no" },
    });
    assert.equal(await promptBoolean(tp, "Continue?"), false);
  });

  it("returns false for null (cancelled)", async () => {
    const tp = fakeTp({
      system: { prompt: async () => null },
    });
    assert.equal(await promptBoolean(tp, "Continue?"), false);
  });
});

// --- vault_occasions ---

describe("vault_occasions", () => {
  it("returns an array of occasions", () => {
    const result = vaultOccasions();
    assert.ok(Array.isArray(result));
    assert.ok(result.length > 0);
  });

  it("each occasion has sym, name, type, and test", () => {
    const result = vaultOccasions();
    for (const occ of result) {
      assert.equal(typeof occ.sym, "string");
      assert.equal(typeof occ.name, "string");
      assert.ok(occ.type === "event" || occ.type === "reminder");
      assert.equal(typeof occ.test, "function");
    }
  });

  it("contains no real personal data", () => {
    const result = vaultOccasions();
    const names = result.map((o: any) => o.name);
    assert.ok(names.some((n: string) => n.includes("Example")));
  });
});

// --- journal_occasions ---

describe("journal_occasions", () => {
  it("returns chores and events arrays", () => {
    const tp = fakeTp();
    const m = fakeMoment({});
    const result = journalOccasions(tp, m);
    assert.ok(Array.isArray(result.chores));
    assert.ok(Array.isArray(result.events));
  });

  it("separates reminders into chores and events into events", () => {
    const tp = fakeTp({
      user: {
        vault_occasions: () => [
          { sym: "A", name: "Chore1", type: "reminder", test: () => true },
          { sym: "B", name: "Event1", type: "event", test: () => true },
          { sym: "C", name: "Chore2", type: "reminder", test: () => false },
        ],
      },
    });
    const m = fakeMoment({});
    const result = journalOccasions(tp, m);
    assert.equal(result.chores.length, 1);
    assert.equal(result.chores[0].name, "Chore1");
    assert.equal(result.events.length, 1);
    assert.equal(result.events[0].name, "Event1");
  });

  it("filters occasions by date using the test function", () => {
    const tp = fakeTp({
      user: {
        vault_occasions: () => [
          { sym: "X", name: "Match", type: "event", test: (m: any) => m.date() === 15 },
          { sym: "Y", name: "NoMatch", type: "event", test: (m: any) => m.date() === 20 },
        ],
      },
    });
    const m = fakeMoment({ date: () => 15 });
    const result = journalOccasions(tp, m);
    assert.equal(result.events.length, 1);
    assert.equal(result.events[0].name, "Match");
  });

  it("returns empty arrays when no occasions match", () => {
    const tp = fakeTp({
      user: {
        vault_occasions: () => [
          { sym: "X", name: "Nope", type: "event", test: () => false },
        ],
      },
    });
    const m = fakeMoment({});
    const result = journalOccasions(tp, m);
    assert.equal(result.chores.length, 0);
    assert.equal(result.events.length, 0);
  });
});
