type Level = "daily" | "weekly" | "monthly" | "yearly";

const LEVEL_CONFIG: Record<Level, { unit: string; nameFn: keyof TpUser }> = {
  daily: { unit: "days", nameFn: "journal_daily_name" },
  weekly: { unit: "weeks", nameFn: "journal_weekly_name" },
  monthly: { unit: "months", nameFn: "journal_monthly_name" },
  yearly: { unit: "years", nameFn: "journal_yearly_name" },
};

function journal_prev_next(tp: Tp, m: moment.Moment, level: Level): { prev: string; next: string } {
  const { unit, nameFn } = LEVEL_CONFIG[level];
  const prev = tp.user[nameFn](m.clone().subtract(1, unit));
  const next = tp.user[nameFn](m.clone().add(1, unit));
  return { prev, next };
}

export = journal_prev_next;
