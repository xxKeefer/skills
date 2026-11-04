# Wrapper changes (the project's analytics lib)

### D. Wrapper changes (the project's analytics lib)

16. **Weakened gate (Change Requested).** Any change that sends under denied consent, sends identity or page views under unknown consent, queues while disabled, shrinks the redaction denylist, removes a second redaction pass or the URL strip, enables PostHog autocapture/session recording/vendor persistence/vendor flags, or moves a base-event field from "reserved" to stamped without saying why (the high-entropy block fingerprints a device). Each is a privacy regression that no call-site review will catch afterwards.
17. **Stamped-field or lib-event change (Change Requested).** Renaming or retyping a base-event field, or a field of the wrapper's click, page-view or milestone event, or a milestone status or trigger value. Every dashboard filters on these.
