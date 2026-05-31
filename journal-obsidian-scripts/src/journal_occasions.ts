interface OccasionResult {
  sym: string;
  name: string;
}

interface OccasionsOutput {
  chores: OccasionResult[];
  work: OccasionResult[];
  tasks: OccasionResult[];
}

function journal_occasions(tp: Tp, m: moment.Moment): OccasionsOutput {
  const occasions = tp.user.vault_occasions();
  const chores: OccasionResult[] = [];
  const work: OccasionResult[] = [];
  const tasks: OccasionResult[] = [];

  for (const occ of occasions) {
    if (!occ.test(m)) continue;
    const item = { sym: occ.sym, name: occ.name };
    const section = occ.section ?? "chores";
    if (section === "work") work.push(item);
    else if (section === "tasks") tasks.push(item);
    else chores.push(item);
  }

  return { chores, work, tasks };
}

export = journal_occasions;
