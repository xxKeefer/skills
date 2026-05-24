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
