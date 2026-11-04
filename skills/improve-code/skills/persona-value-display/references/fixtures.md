# Fixtures: awkward display values, timezones, and locales

Test data for this lane's catalogue. Cite a value from here as the failing input in a finding, or type it into the running app. Strings in the tables and code blocks are byte-exact: some hold invisible characters (NBSP, ZWSP, BOM, ZWJ, RTL override). Copy them, don't retype them.

## Awkward display values

```ts
export const nasty = {
  longUnbroken: 'a'.repeat(120),
  longEmail: 'averyveryverylongemailaddress.with.subdomains@customer-enterprise-networks.example.com',
  uuidLike: ['a3f9c2e1-77b0-4c1d-9e8f-000000000001', 'a3f9c2e1-77b0-4c1d-9e8f-000000000002'],
  german: 'Verbindungsbandbreitenänderungsanforderung',
  emoji: '👨‍👩‍👧‍👦 Family Co 🇦🇺',
  combining: 'Zoë',
  rtl: 'שלום (Sydney) 123',
  html: '<img src=x onerror=alert(1)>',
  entity: 'AT&T &amp; Co',
  whitespace: '  leading\nline two\n\n  indented  ',
  zeroWidth: '​',
  empty: ['', ' ', null, undefined],
  numbers: [0, -0, -0.001, 0.1 + 0.2, 1.005, 999, 1000, 1500, 10000, 1e21, 2 ** 53 + 1, NaN],
  dates: ['2026-10-13', '2026-10-13T00:00:00Z', null, 0, 1760313600, '13/10/2026', '2026-04-05T02:30:00'],
  speedsMbps: [1, 50, 500, 999, 1000, 1500, 10000, 100000],
};
```


## Timezones and locales

Run the date and number checks under `TZ=UTC`, `TZ=America/Los_Angeles`, `TZ=Pacific/Kiritimati` (UTC+14), `TZ=Pacific/Auckland`, and `TZ=Australia/Sydney`, and at least once across a DST change. Locales: `en-AU`, `en-US`, `de-DE` (decimal comma, about 30% longer strings), `fr-FR` (narrow no-break space as thousands separator), `ja-JP` (IME input), and a pseudo-locale.
