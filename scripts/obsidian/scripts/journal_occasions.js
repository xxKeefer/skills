"use strict";
function journal_occasions(tp, m) {
    const occasions = tp.user.vault_occasions();
    const chores = [];
    const work = [];
    const tasks = [];
    for (const occ of occasions) {
        if (!occ.test(m))
            continue;
        const item = { sym: occ.sym, name: occ.name };
        const section = occ.section || "chores";
        if (section === "work")
            work.push(item);
        else if (section === "tasks")
            tasks.push(item);
        else
            chores.push(item);
    }
    return { chores, work, tasks };
}
module.exports = journal_occasions;
