interface Occasion {
  sym: string;
  name: string;
  type: "event" | "reminder";
  section: "chores" | "work" | "tasks";
  test: (m: moment.Moment) => boolean;
}

const OCCASIONS: Occasion[] = [
  // --- EXAMPLE BIRTHDAYS ---
  { sym: "🎂", name: "Example Person A", type: "event", section: "chores", test: (m) => m.format("DDMM") === "0101" },
  { sym: "🎂", name: "Example Person B", type: "event", section: "chores", test: (m) => m.format("DDMM") === "1507" },

  // --- EXAMPLE FIXED HOLIDAYS ---
  {
    sym: "🥂",
    name: "New Year's Day",
    type: "event",
    section: "chores",
    test: (m) =>
      (m.month() === 0 && m.date() === 1) ||
      (m.month() === 0 && m.date() === 2 && m.day() === 1) ||
      (m.month() === 0 && m.date() === 3 && m.day() === 1),
  },
  {
    sym: "🎅",
    name: "Christmas Day",
    type: "event",
    section: "chores",
    test: (m) =>
      (m.month() === 11 && m.date() === 25) ||
      (m.month() === 11 && (m.date() === 26 || m.date() === 27) && m.day() === 1),
  },

  // --- EXAMPLE FLOATING HOLIDAYS ---
  {
    sym: "👷",
    name: "Example Labour Day (1st Mon May)",
    type: "event",
    section: "chores",
    test: (m) => m.month() === 4 && m.day() === 1 && m.date() <= 7,
  },

  // --- EXAMPLE REMINDERS ---
  {
    sym: "🟡",
    name: "Example Bins (even weeks)",
    type: "reminder",
    section: "chores",
    test: (m) => m.day() === 3 && m.isoWeek() % 2 === 0,
  },
  {
    sym: "🔴",
    name: "Example Bins (odd weeks)",
    type: "reminder",
    section: "chores",
    test: (m) => m.day() === 3 && m.isoWeek() % 2 !== 0,
  },
];

function vault_occasions(): Occasion[] {
  return OCCASIONS;
}

export = vault_occasions;
