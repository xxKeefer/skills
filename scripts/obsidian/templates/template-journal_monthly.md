<%*
const m = await tp.user.prompt_date(tp, "Enter any date in the target month");
const config = tp.user.journal_config();

const monthStart = m.clone().startOf("month");
const name = tp.user.journal_monthly_name(m);
const { prev, next } = tp.user.journal_prev_next(tp, m, "monthly");
const up = tp.user.journal_up_link(tp, m, "monthly");

const newPath = `${config.journalDir}/${name}`;
await tp.file.move(newPath);

const seenWeeks = new Set();
const weeks = [];
const cursor = monthStart.clone();
while (cursor.month() === monthStart.month()) {
  const weekKey = `${cursor.isoWeekYear()}-wk${String(cursor.isoWeek()).padStart(2, "0")}`;
  if (!seenWeeks.has(weekKey)) {
    seenWeeks.add(weekKey);
    weeks.push(tp.user.journal_weekly_name(cursor));
  }
  cursor.add(1, "days");
}

tR += `---\n`;
tR += `type: ${config.types.monthly}\n`;
tR += `date: ${monthStart.format("YYYY-MM-DD")}\n`;
tR += `tags: [${config.tags.monthly.join(", ")}]\n`;
tR += `up: '[[${up}]]'\n`;
tR += `prev: '[[${prev}]]'\n`;
tR += `next: '[[${next}]]'\n`;
tR += `---\n\n`;

tR += `# 📅 ${m.format("MMMM YYYY")} -- Monthly Planner\n\n`;

tR += `> At a glance\n\n`;

tR += `## 🎯 Goals\n\n`;
tR += `- [ ] \n\n`;

tR += `## 📆 Events\n\n`;
tR += `- \n\n`;

tR += `## 📝 Overview\n\n`;
tR += `| Plan | Notes |\n`;
tR += `| ---- | ----- |\n`;
for (const w of weeks) {
  tR += `| [[${w}]] | |\n`;
}
tR += `\n`;

tR += `## 💡 Insights\n\n`;

tR += `## 🤔 Reflect\n\n`;
tR += `### ✅ What went well\n\n`;
tR += `### ⚠️ What caused friction\n\n`;
tR += `### ➡️ What is next\n`;
%>
