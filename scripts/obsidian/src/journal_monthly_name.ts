function journal_monthly_name(m: moment.Moment): string {
  const year = m.format("YYYY");
  const month = m.format("MM");
  const mon = m.format("MMM").toLowerCase();
  return `${year}-${month}-${mon}`;
}

export = journal_monthly_name;
