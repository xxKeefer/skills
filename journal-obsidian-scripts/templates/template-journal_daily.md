<%*
const m = await tp.user.prompt_date(tp);
const config = tp.user.journal_config();

const name = tp.user.journal_daily_name(m);
const { prev, next } = tp.user.journal_prev_next(tp, m, "daily");
const up = tp.user.journal_up_link(tp, m, "daily");
const { chores, events } = tp.user.journal_occasions(tp, m);

const newPath = `${config.journalDir}/${name}`;
await tp.file.move(newPath);

tR += `---\n`;
tR += `type: ${config.types.daily}\n`;
tR += `date: ${m.format("YYYY-MM-DD")}\n`;
tR += `tags: [${config.tags.daily.join(", ")}]\n`;
tR += `up: '[[${up}]]'\n`;
tR += `prev: '[[${prev}]]'\n`;
tR += `next: '[[${next}]]'\n`;
tR += `---\n\n`;

tR += `# ${m.format("dddd")} -- wk${String(m.isoWeek()).padStart(2, "0")}\n\n`;

tR += `> At a glance\n\n`;

tR += `## 📋 Today\n\n`;

tR += `### 🔄 Chores\n`;
for (const c of chores) {
  tR += `- [ ] ${c.sym} ${c.name}\n`;
}
tR += `\n`;

if (events.length > 0) {
  tR += `### 📆 Events\n`;
  for (const e of events) {
    tR += `- ${e.sym} ${e.name}\n`;
  }
  tR += `\n`;
}

const isWeekday = m.isoWeekday() <= 5;
if (isWeekday) {
  tR += `### 🧑‍💻 Work\n`;
  tR += `- [ ] \n\n`;
}

tR += `### 🎯 Tasks\n`;
tR += `- [ ] \n\n`;

tR += `## 💭 Thoughts and Ideas\n\n`;

tR += `## 🤔 Reflect\n\n`;
tR += `### 🧠 What I learned\n\n`;
tR += `### ✅ What went well\n\n`;
tR += `### ➡️ What is next\n\n`;
tR += `### ⚠️ What caused friction\n`;
%>
