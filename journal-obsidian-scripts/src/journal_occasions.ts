interface OccasionResult {
  sym: string;
  name: string;
}

interface OccasionsOutput {
  chores: OccasionResult[];
  events: OccasionResult[];
}

function journal_occasions(tp: Tp, m: moment.Moment): OccasionsOutput {
  const occasions = tp.user.vault_occasions();
  const chores: OccasionResult[] = [];
  const events: OccasionResult[] = [];

  for (const occ of occasions) {
    if (!occ.test(m)) continue;
    const item = { sym: occ.sym, name: occ.name };
    if (occ.type === "reminder") {
      chores.push(item);
    } else {
      events.push(item);
    }
  }

  return { chores, events };
}

export = journal_occasions;
