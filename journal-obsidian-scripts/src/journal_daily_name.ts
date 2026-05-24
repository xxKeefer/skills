function journal_daily_name(m: moment.Moment): string {
  const year = m.isoWeekYear();
  const week = String(m.isoWeek()).padStart(2, "0");
  const day = m.format("ddd").toLowerCase();
  return `${year}-wk${week}-${day}`;
}

export = journal_daily_name;
