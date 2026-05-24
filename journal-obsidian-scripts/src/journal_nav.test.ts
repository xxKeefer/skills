const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const prevNext = require("./journal_prev_next.ts");
const upLink = require("./journal_up_link.ts");

function fakeMoment(overrides: Record<string, any> = {}) {
  const { format: fmtMap, ...rest } = overrides;
  const self: any = {
    format: (fmt: string) => fmtMap?.[fmt] ?? "",
    isoWeek: () => 21,
    isoWeekYear: () => 2026,
    year: () => 2026,
    month: () => 4,
    date: () => 24,
    day: () => 6,
    clone: () => fakeMoment(overrides),
    add: (n: number, _unit: string) => {
      if (_unit === "days") return fakeMoment({ ...overrides, _dayOffset: (overrides._dayOffset ?? 0) + n });
      if (_unit === "weeks") return fakeMoment({ ...overrides, _weekOffset: (overrides._weekOffset ?? 0) + n });
      if (_unit === "months") return fakeMoment({ ...overrides, _monthOffset: (overrides._monthOffset ?? 0) + n });
      if (_unit === "years") return fakeMoment({ ...overrides, _yearOffset: (overrides._yearOffset ?? 0) + n });
      return self;
    },
    subtract: (n: number, unit: string) => self.add(-n, unit),
    startOf: () => self,
    ...rest,
  };
  return self;
}

function fakeTp(nameResults: Record<string, Record<string, string>>) {
  return {
    user: {
      journal_daily_name: (m: any) => nameResults.daily?.[JSON.stringify(m)] ?? "daily-result",
      journal_weekly_name: (m: any) => nameResults.weekly?.[JSON.stringify(m)] ?? "weekly-result",
      journal_monthly_name: (m: any) => nameResults.monthly?.[JSON.stringify(m)] ?? "monthly-result",
      journal_yearly_name: (m: any) => nameResults.yearly?.[JSON.stringify(m)] ?? "yearly-result",
    },
  } as any;
}

describe("journal_prev_next", () => {
  it("returns prev and next daily names by delegating to tp.user", () => {
    const calls: { fn: string; arg: any }[] = [];
    const tp = {
      user: {
        journal_daily_name: (m: any) => { calls.push({ fn: "daily", arg: m }); return `daily-${calls.length}`; },
        journal_weekly_name: (m: any) => { calls.push({ fn: "weekly", arg: m }); return `weekly-${calls.length}`; },
        journal_monthly_name: (m: any) => { calls.push({ fn: "monthly", arg: m }); return `monthly-${calls.length}`; },
        journal_yearly_name: (m: any) => { calls.push({ fn: "yearly", arg: m }); return `yearly-${calls.length}`; },
      },
    } as any;
    const m = fakeMoment();
    const result = prevNext(tp, m, "daily");
    assert.equal(result.prev, "daily-1");
    assert.equal(result.next, "daily-2");
    assert.equal(calls.length, 2);
    assert.equal(calls[0].fn, "daily");
    assert.equal(calls[1].fn, "daily");
  });

  it("returns prev and next weekly names", () => {
    const calls: string[] = [];
    const tp = {
      user: {
        journal_weekly_name: (m: any) => { calls.push("weekly"); return `wk-${calls.length}`; },
      },
    } as any;
    const m = fakeMoment();
    const result = prevNext(tp, m, "weekly");
    assert.equal(result.prev, "wk-1");
    assert.equal(result.next, "wk-2");
  });

  it("returns prev and next monthly names", () => {
    const calls: string[] = [];
    const tp = {
      user: {
        journal_monthly_name: (m: any) => { calls.push("monthly"); return `mon-${calls.length}`; },
      },
    } as any;
    const m = fakeMoment();
    const result = prevNext(tp, m, "monthly");
    assert.equal(result.prev, "mon-1");
    assert.equal(result.next, "mon-2");
  });

  it("returns prev and next yearly names", () => {
    const calls: string[] = [];
    const tp = {
      user: {
        journal_yearly_name: (m: any) => { calls.push("yearly"); return `yr-${calls.length}`; },
      },
    } as any;
    const m = fakeMoment();
    const result = prevNext(tp, m, "yearly");
    assert.equal(result.prev, "yr-1");
    assert.equal(result.next, "yr-2");
  });
});

describe("journal_up_link", () => {
  it("daily links up to weekly", () => {
    const tp = {
      user: {
        journal_weekly_name: () => "2026-wk21-week",
      },
    } as any;
    const m = fakeMoment();
    assert.equal(upLink(tp, m, "daily"), "2026-wk21-week");
  });

  it("weekly links up to monthly", () => {
    const tp = {
      user: {
        journal_monthly_name: () => "2026-05-may",
      },
    } as any;
    const m = fakeMoment();
    assert.equal(upLink(tp, m, "weekly"), "2026-05-may");
  });

  it("monthly links up to yearly", () => {
    const tp = {
      user: {
        journal_yearly_name: () => "2026",
      },
    } as any;
    const m = fakeMoment();
    assert.equal(upLink(tp, m, "monthly"), "2026");
  });

  it("yearly returns undefined (no parent)", () => {
    const tp = { user: {} } as any;
    const m = fakeMoment();
    assert.equal(upLink(tp, m, "yearly"), undefined);
  });
});
