"use strict";
function journal_weekly_name(m) {
    const year = m.isoWeekYear();
    const week = String(m.isoWeek()).padStart(2, "0");
    return `${year}-wk${week}-week`;
}
module.exports = journal_weekly_name;
