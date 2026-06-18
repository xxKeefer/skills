async function prompt_date(tp: Tp, prompt = "Enter any date"): Promise<moment.Moment> {
  const now = tp.date.now("YYYY-MM-DD");
  const msg = `${prompt} (e.g., ${now})`;
  const date = await tp.system.prompt(msg, now);
  return moment(date!);
}

export = prompt_date;
