<%*
const m = await tp.user.prompt_date(tp, "Enter any date in the target week");
const config = tp.user.journal_config();

const weekStart = m.clone().startOf("isoWeek");
const name = tp.user.journal_weekly_name(m);
const { prev, next } = tp.user.journal_prev_next(tp, m, "weekly");
const up = tp.user.journal_up_link(tp, m, "weekly");

const newPath = `${config.journalDir}/${name}`;
await tp.file.move(newPath);

const weekEvents = [];
for (let i = 0; i < 7; i++) {
  const day = weekStart.clone().add(i, "days");
  const { events } = tp.user.journal_occasions(tp, day);
  for (const e of events) {
    weekEvents.push(`- ${e.sym} ${e.name} (${day.format("ddd")})`);
  }
}

const weekNum = String(m.isoWeek()).padStart(2, "0");

tR += `---\n`;
tR += `type: ${config.types.weekly}\n`;
tR += `date: ${weekStart.format("YYYY-MM-DD")}\n`;
tR += `tags: [${config.tags.weekly.join(", ")}]\n`;
tR += `up: '[[${up}]]'\n`;
tR += `prev: '[[${prev}]]'\n`;
tR += `next: '[[${next}]]'\n`;
tR += `---\n\n`;

tR += `# 📅 Week ${weekNum} -- ${m.isoWeekYear()}\n\n`;

tR += `> At a glance\n\n`;

tR += `## 🎯 Goals\n\n`;
tR += `- [ ] \n\n`;

tR += `## 📆 Events\n\n`;
if (weekEvents.length > 0) {
  for (const e of weekEvents) {
    tR += `${e}\n`;
  }
} else {
  tR += `- (none this week)\n`;
}
tR += `\n`;

tR += `## 📝 Days\n\n`;
tR += `| Day | Link | Notes |\n`;
tR += `| --- | ---- | ----- |\n`;
for (let i = 0; i < 7; i++) {
  const day = weekStart.clone().add(i, "days");
  const dayName = config.days[i].charAt(0).toUpperCase() + config.days[i].slice(1);
  const dayLink = tp.user.journal_daily_name(day);
  tR += `| ${dayName} | [[${dayLink}]] | |\n`;
}
tR += `\n`;

tR += `## 🤔 Reflect\n\n`;
tR += `### ✅ What went well\n\n`;
tR += `### ⚠️ What caused friction\n\n`;
tR += `### ➡️ What is next\n`;
%>
