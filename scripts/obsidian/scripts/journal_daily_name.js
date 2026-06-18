"use strict";
function journal_daily_name(m) {
    const year = m.isoWeekYear();
    const week = String(m.isoWeek()).padStart(2, "0");
    const day = m.format("ddd").toLowerCase();
    return `${year}-wk${week}-${day}`;
}
module.exports = journal_daily_name;
