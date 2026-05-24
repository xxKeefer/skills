function journal_weekly_name(m: moment.Moment): string {
  const year = m.isoWeekYear();
  const week = String(m.isoWeek()).padStart(2, "0");
  return `${year}-wk${week}-week`;
}

export = journal_weekly_name;
