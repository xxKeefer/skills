const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const config = require("./journal_config.ts");

describe("journal_config", () => {
  it("returns journalDir", () => {
    assert.equal(config().journalDir, "01-journal");
  });

  it("returns types for all four levels", () => {
    const c = config();
    assert.equal(c.types.daily, "journal/daily");
    assert.equal(c.types.weekly, "journal/weekly");
    assert.equal(c.types.monthly, "journal/monthly");
    assert.equal(c.types.yearly, "journal/yearly");
  });

  it("returns tags for all four levels", () => {
    const c = config();
    assert.deepEqual(c.tags.daily, ["journal", "journal/daily"]);
    assert.deepEqual(c.tags.weekly, ["journal", "journal/weekly"]);
    assert.deepEqual(c.tags.monthly, ["journal", "journal/monthly"]);
    assert.deepEqual(c.tags.yearly, ["journal", "journal/yearly"]);
  });

  it("uses isoWeek for week start", () => {
    assert.equal(config().weekStart, "isoWeek");
  });

  it("lists days mon through sun", () => {
    const c = config();
    assert.equal(c.days.length, 7);
    assert.equal(c.days[0], "mon");
    assert.equal(c.days[6], "sun");
  });
});
