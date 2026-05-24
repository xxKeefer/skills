declare namespace moment {
  interface Moment {
    format(fmt: string): string;
    isoWeek(): number;
    isoWeekday(): number;
    isoWeekYear(): number;
    year(): number;
    month(): number;
    date(): number;
    day(): number;
    clone(): Moment;
    add(n: number, unit: string): Moment;
    subtract(n: number, unit: string): Moment;
    startOf(unit: string): Moment;
    endOf(unit: string): Moment;
    isBefore(other: Moment): boolean;
    isSameOrBefore(other: Moment): boolean;
  }
}

declare function moment(input?: string | Date): moment.Moment;

interface TpUser {
  journal_config(): JournalConfig;
  journal_daily_name(m: moment.Moment): string;
  journal_weekly_name(m: moment.Moment): string;
  journal_monthly_name(m: moment.Moment): string;
  journal_yearly_name(m: moment.Moment): string;
  journal_prev_next(tp: Tp, m: moment.Moment, level: string): { prev: string; next: string };
  journal_up_link(tp: Tp, m: moment.Moment, level: string): string;
  journal_occasions(tp: Tp, m: moment.Moment): { chores: { sym: string; name: string }[]; events: { sym: string; name: string }[] };
  vault_occasions(): { sym: string; name: string; type: "event" | "reminder"; test: (m: moment.Moment) => boolean }[];
  prompt_date(tp: Tp, prompt?: string): Promise<moment.Moment>;
  prompt_boolean(tp: Tp, prompt: string, defaultResponse?: string): Promise<boolean>;
  [key: string]: (...args: any[]) => any;
}

interface TpDate {
  now(fmt: string): string;
}

interface TpSystem {
  prompt(msg: string, defaultValue?: string): Promise<string | null>;
  suggester(labels: string[], values: string[]): Promise<string | null>;
}

interface Tp {
  user: TpUser;
  date: TpDate;
  system: TpSystem;
  file: {
    move(path: string): Promise<void>;
    title: string;
  };
}

interface JournalConfig {
  journalDir: string;
  types: Record<string, string>;
  tags: Record<string, string[]>;
  weekStart: string;
  days: string[];
}
