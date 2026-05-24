type Level = "daily" | "weekly" | "monthly" | "yearly";

const PARENT_MAP: Partial<Record<Level, keyof TpUser>> = {
  daily: "journal_weekly_name",
  weekly: "journal_monthly_name",
  monthly: "journal_yearly_name",
};

function journal_up_link(tp: Tp, m: moment.Moment, level: Level): string | undefined {
  const nameFn = PARENT_MAP[level];
  if (!nameFn) return undefined;
  return tp.user[nameFn](m);
}

export = journal_up_link;
