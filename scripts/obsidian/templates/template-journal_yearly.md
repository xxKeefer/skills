<%*
const m = await tp.user.prompt_date(tp, "Enter any date in the target year");
const config = tp.user.journal_config();

const name = tp.user.journal_yearly_name(m);
const { prev, next } = tp.user.journal_prev_next(tp, m, "yearly");

const newPath = `${config.journalDir}/${name}`;
await tp.file.move(newPath);

tR += `---\n`;
tR += `type: ${config.types.yearly}\n`;
tR += `date: ${m.format("YYYY")}-01-01\n`;
tR += `tags: [${config.tags.yearly.join(", ")}]\n`;
tR += `prev: '[[${prev}]]'\n`;
tR += `next: '[[${next}]]'\n`;
tR += `---\n\n`;

tR += `# 📅 Yearly Planner -- ${m.format("YYYY")}\n\n`;

tR += `> At a glance\n\n`;

tR += `## 🎯 Goals\n\n`;
tR += `- [ ] \n\n`;

tR += `## 📆 Events\n\n`;
tR += `- \n\n`;

tR += `## 📝 Monthly Plans\n\n`;
tR += `| Plan | Notes |\n`;
tR += `| ---- | ----- |\n`;
const months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
for (let i = 0; i < 12; i++) {
  const monthMoment = m.clone().month(i).date(1);
  const monthLink = tp.user.journal_monthly_name(monthMoment);
  tR += `| [[${monthLink}]] | |\n`;
}
tR += `\n`;

tR += `## 🤔 Reflect\n\n`;
tR += `### ✅ What went well\n\n`;
tR += `### ⚠️ What caused friction\n\n`;
tR += `### ➡️ What is next\n`;
%>
