"use strict";
const PARENT_MAP = {
    daily: "journal_weekly_name",
    weekly: "journal_monthly_name",
    monthly: "journal_yearly_name",
};
function journal_up_link(tp, m, level) {
    const nameFn = PARENT_MAP[level];
    if (!nameFn)
        return undefined;
    return tp.user[nameFn](m);
}
module.exports = journal_up_link;
