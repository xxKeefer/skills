"use strict";
function journal_monthly_name(m) {
    const year = m.format("YYYY");
    const month = m.format("MM");
    const mon = m.format("MMM").toLowerCase();
    return `${year}-${month}-${mon}`;
}
module.exports = journal_monthly_name;
