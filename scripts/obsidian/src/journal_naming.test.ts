const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const dailyName = require("./journal_daily_name.ts");
const weeklyName = require("./journal_weekly_name.ts");
const monthlyName = require("./journal_monthly_name.ts");
const yearlyName = require("./journal_yearly_name.ts");

function fakeMoment(overrides: Record<string, any>) {
  const { format: fmtMap, ...rest } = overrides;
  return {
    format: (fmt: string) => fmtMap?.[fmt] ?? "",
    isoWeek: () => 1,
    isoWeekYear: () => 2026,
    year: () => 2026,
    ...rest,
  } as any;
}

describe("journal_daily_name", () => {
  it("formats 2026-05-24 (Saturday, wk21)", () => {
    const m = fakeMoment({
      format: { "YYYY": "2026", "ddd": "Sat" },
      isoWeek: () => 21,
      isoWeekYear: () => 2026,
    });
    assert.equal(dailyName(m), "2026-wk21-sat");
  });

  it("pads week number", () => {
    const m = fakeMoment({
      format: { "YYYY": "2026", "ddd": "Mon" },
      isoWeek: () => 3,
      isoWeekYear: () => 2026,
    });
    assert.equal(dailyName(m), "2026-wk03-mon");
  });

  it("uses isoWeekYear for year-boundary dates", () => {
    const m = fakeMoment({
      format: { "YYYY": "2026", "ddd": "Thu" },
      isoWeek: () => 1,
      isoWeekYear: () => 2026,
    });
    assert.equal(dailyName(m), "2026-wk01-thu");
  });

  it("handles Dec 31 in next year's ISO week", () => {
    const m = fakeMoment({
      format: { "YYYY": "2025", "ddd": "Wed" },
      isoWeek: () => 1,
      isoWeekYear: () => 2026,
    });
    assert.equal(dailyName(m), "2026-wk01-wed");
  });
});

describe("journal_weekly_name", () => {
  it("formats week 21 of 2026", () => {
    const m = fakeMoment({
      isoWeek: () => 21,
      isoWeekYear: () => 2026,
    });
    assert.equal(weeklyName(m), "2026-wk21-week");
  });

  it("pads single-digit weeks", () => {
    const m = fakeMoment({
      isoWeek: () => 5,
      isoWeekYear: () => 2026,
    });
    assert.equal(weeklyName(m), "2026-wk05-week");
  });
});

describe("journal_monthly_name", () => {
  it("formats May 2026", () => {
    const m = fakeMoment({
      format: { "YYYY": "2026", "MM": "05", "MMM": "May" },
    });
    assert.equal(monthlyName(m), "2026-05-may");
  });

  it("formats December", () => {
    const m = fakeMoment({
      format: { "YYYY": "2026", "MM": "12", "MMM": "Dec" },
    });
    assert.equal(monthlyName(m), "2026-12-dec");
  });
});

describe("journal_yearly_name", () => {
  it("returns the year", () => {
    const m = fakeMoment({
      format: { "YYYY": "2026" },
    });
    assert.equal(yearlyName(m), "2026");
  });
});
