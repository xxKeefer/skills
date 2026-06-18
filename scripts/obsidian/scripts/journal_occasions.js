"use strict";
function journal_occasions(tp, m) {
    const occasions = tp.user.vault_occasions();
    const chores = [];
    const events = [];
    for (const occ of occasions) {
        if (!occ.test(m))
            continue;
        const item = { sym: occ.sym, name: occ.name };
        if (occ.type === "reminder") {
            chores.push(item);
        }
        else {
            events.push(item);
        }
    }
    return { chores, events };
}
module.exports = journal_occasions;
