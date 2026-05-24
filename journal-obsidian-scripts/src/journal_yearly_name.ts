function journal_yearly_name(m: moment.Moment): string {
  return m.format("YYYY");
}

export = journal_yearly_name;
